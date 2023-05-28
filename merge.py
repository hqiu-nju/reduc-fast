"""
script to connect filterbank files

headers are automatically generated mock information, alter if necessary
"""
import your
import logging
import numpy as np
import os
__author__ = "Harry Qiu"
from your.formats.filwriter import make_sigproc_object

# filelist=np.loadtxt("filelist",dtype='str')

def _main():
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    parser = ArgumentParser(description='Script description', formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', help='Be verbose')
    parser.add_argument('-o', '--output', type=str, default="test", help='Output File Name')
    parser.add_argument('-N', '--segments', type=int, default=20, help='how many files per filterbank segment')
    parser.add_argument('-s', '--samples-per-file', dest='samples', type=int, default=65536, help='Nubmer of time samples to read per input file, set to < 1 to read all data')
    parser.add_argument('-r', '--ra', dest = 'ra', default = 123456.78, type=float, help = "Source RAJ (HHMMSS.sss)")
    parser.add_argument('-d', '--dec', dest = 'dec', default = -123456.78, type=float, help = "Source RAJ (DDMMSS.sss")
    parser.add_argument('-n', '--src', dest = 'src', default = "", type=str, help = "Source Name")

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
        write_filterbanks(values.files[i*seg:(i+1)*seg],f"{filname}_{i}.fil",values.samples,values.ra,values.dec,values.src)




def write_filterbanks(files,filname,total_length=0, raj = 123456.78, decj = -123456.78, name = None):
    from your.formats.filwriter import make_sigproc_object
    cached_total_length = total_length
    for i,filename in enumerate(files):
        fbank= your.Your(filename)
        if i ==0:
            print()
            newdata=make_sigproc_object(rawdatafile=filname,
                                        telescope_id = 21, # FAST according to PRESTO
                                        source_name = name or (fbank.source_name.decode() if isinstance(fbank.source_name, bytes) else fbank.source_name),
                                        nchans = fbank.nchans,
                                        foff = fbank.foff,
                                        fch1 = fbank.fch1,
                                        tsamp =fbank.native_tsamp,
                                        tstart = fbank.tstart,
                                        nbits=8,
                                        src_raj=raj, # HHMMSS.SS
                                        src_dej=decj, # DDMMSS.SS
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
        if cached_total_length < 1:
                total_length = fbank.nspec
        print(filename)
        totaldata=fbank.get_data(nstart=0,nsamp=total_length) ### TOTAL FAST DATA IS 1024 * 64 SUBINTS
        ### reads out stokes I data
        ### this step reads all subints to merge into one datachunk, can't stop printing subint readouts
        newdata.append_spectra(totaldata.astype(np.int8),filname)

# Silence the Polarization is AABB..." spam
logger = logging.getLogger(your.formats.psrfits.__name__)
class NoPolWarningFilter(logging.Filter):
    parsed = False
    def filter(self, record):
        returnVal = record.getMessage().startswith('Polarization is ')
        if returnVal:
            if not self.parsed:
                self.parsed = True
            else:
                return False
        return True
logger.addFilter(NoPolWarningFilter())

if __name__ == '__main__':
    _main()
