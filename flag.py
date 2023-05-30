"""
script to flag channels with a constant value.

"""
import your
import numpy as np
import os
from your.formats.filwriter import make_sigproc_object
__author__ = "Harry Qiu <hao.qiu@skao.int>"



def _main():
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    parser = ArgumentParser(description='Script description', formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', help='Be verbose')
    parser.add_argument('-o', '--output',type=str, default="flagged.fil",help='Output File Name, no suffix')
    parser.add_argument('-i', '--input',type=str, default="test.fil",help='Input File Name, no suffix')

    parser.add_argument('-f', '--flag',type=str, default="rfi.flags",help='list of channels to flag')
    parser.add_argument('-s','--samples',type=int, default=6553600,help='file sample length')
    parser.add_argument('-S','--seglen',type=int, default=5000,help='read in segment sample length factor, read in length is tbin*seglen')




    ## your has not implemented this feature yet

    # parser.add_argument(dest='files', nargs='+')
    parser.set_defaults(verbose=False)
    values = parser.parse_args()
    filname=values.output
    fb= your.Your(values.file)
    newdata=make_sigproc_object(rawdatafile  = filname,
                                source_name = fb.source_name.decode(),
                                nchans  = fb.nchans,
                                foff = fb.foff, #MHz
                                fch1 = fb.fch1, # MHz
                                tsamp = fb.tsamp, # seconds
                                tstart = fb.tstart, #MJD
                                src_raj=123456.78, # HHMMSS.SS
                                src_dej=-123456.78, # DDMMSS.SS
                                machine_id=0,
                                nbeams=1,
                                ibeam=0,
                                nbits=8,
                                nifs=1,
                                barycentric=0,
                                pulsarcentric=0,
                                data_type=0,
                                az_start=-1,
                                za_start=-1,
                                )
    newdata.write_header(filname)
    seglen=values.seglen
    looprange=values.samples//(seglen)+1
    for round in range(looprange):
        print(f'reading segement {round}/{looprange}, length is {seglen}',end = "\r")
        reduced_data=cutflag(fb,flags,tstart=round*seglen,total_length=seglen)
        newdata.append_spectra(reduced_data.astype(np.int8),filname)
    print(f'Finished total length {fb.native_nspectra}, flagged {}channels')


def cutflag(fb,flags,tstart=0,total_length=65536):
     ### LONGER THAN SINGLE FAST OBS FILE TO ENSURE THE WHOLE DATA SET IS COLLECTED.
    totaldata=fb.get_data(nstart=tstart,nsamp=total_length)
    flagged=totaldata*flags
    return flagged

if __name__ == '__main__':
    _main()
