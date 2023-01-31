"""
script to connect filterbank files

headers are automatically generated mock information, alter if necessary
"""
import your
import numpy as np
import os
__author__ = "Harry Qiu"
from your.formats.filwriter import make_sigproc_object

# filelist=np.loadtxt("filelist",dtype='str')

def _main():
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    parser = ArgumentParser(description='Script description', formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', help='Be verbose')
    parser.add_argument('-o', '--output',type=str, default="test",help='Output File Name')
    parser.add_argument('-N','--segments',type=int, default=20,help='how many files per filterbank segment')
    # parser.add_argument('--nsamp',type=int, default=20,help='how many files per filterbank segment')

    parser.add_argument(dest='files', nargs='+')
    parser.set_defaults(verbose=False)
    values = parser.parse_args()
    seg=values.segments
    filname=values.output
    fillength=len(values.files)
    inject_iter=fillength//seg+1
    # print(values.files,fillength,inject_iter)
    for i in range(inject_iter):
        print(f"reading files {values.files[i*seg:(i+1)*seg]}, writing to {filname}_{i}.fil")
        write_filterbanks(files=values.files[i*seg:(i+1)*seg],filname=f"{filname}_{i}.fil")




def write_filterbanks(files,filname,total_length=65536):
    from your.formats.filwriter import make_sigproc_object
    for i,filename in enumerate(files):
        fbank= your.Your(filename)
        if i ==0:
            print()
            newdata=make_sigproc_object(rawdatafile=filname,
                                        source_name = fbank.source_name.decode(),
                                        nchans = fbank.nchans,
                                        foff = fbank.foff,
                                        fch1 = fbank.fch1,
                                        tsamp =fbank.tsamp,
                                        tstart = fbank.tstart,
                                        nbits=8,
                                        src_raj=123456.78, # HHMMSS.SS
                                        src_dej=-123456.78, # DDMMSS.SS
                                        machine_id=0,
                                        nbeams=1,
                                        ibeam=0,
                                        nifs=1,
                                        barycentric=0,
                                        pulsarcentric=0,
                                        data_type=0,
                                        az_start=-1,
                                        za_start=-1
                                        )
            newdata.write_header(filname)

        print(filename)
        totaldata=fbank.get_data(nstart=0,nsamp=total_length) ### TOTAL FAST DATA IS 1024 * 64 SUBINTS
        ### reads out stokes I data
        ### this step reads all subints to merge into one datachunk, can't stop printing subint readouts
        newdata.append_spectra(totaldata.astype(np.int8),filname)

if __name__ == '__main__':
    _main()
