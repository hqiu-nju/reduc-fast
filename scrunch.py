"""
script to manipulate filterbank files and tscrunch/fscrunch them.

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
    parser.add_argument('-o', '--output',type=str, default="subband",help='Output File Name, no suffix')
    parser.add_argument('-f', '--file',type=str, default="test.fil",help='Input File Name')
    parser.add_argument('-t','--tbin',type=int, default=1,help='tscrunch samples per bin')
    parser.add_argument('-c','--fbin',type=int, default=1,help='fscrunch channels per bin')
    parser.add_argument('-s','--samples',type=int, default=6553600,help='file sample length')
    parser.add_argument('-S','--seglen',type=int, default=1000,help='read in segment sample length factor, read in length is tbin*seglen')
    parser.add_argument('-r', '--ra', dest = 'ra', default = 123456.78, type=float, help = "Source RAJ (HHMMSS.sss)")
    parser.add_argument('-d', '--dec', dest = 'dec', default = -123456.78, type=float, help = "Source RAJ (DDMMSS.sss")
    parser.add_argument('-n', '--src', dest = 'src', default = "", type=str, help = "Source Name")


    ## your has not implemented this feature yet

    # parser.add_argument(dest='files', nargs='+')
    parser.set_defaults(verbose=False)
    values = parser.parse_args()
    filname=values.output
    fb= your.Your(values.file)
    newdata=make_sigproc_object(rawdatafile  = filname,
                                telescope_id = 21, # FAST according to PRESTO
                                source_name = values.src or (fbank.source_name.decode() if isinstance(fbank.source_name, bytes) else fbank.source_name),
                                nchans  = fb.nchans//values.fbin,
                                foff = fb.foff*values.fbin, #MHz
                                fch1 = fb.fch1, # MHz
                                tsamp = fb.native_tsamp*values.tbin, # seconds
                                tstart = fb.tstart, #MJD
                                src_raj=raj, # HHMMSS.SS
                                src_dej=decj, # DDMMSS.SS
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
    looprange=values.samples//(values.tbin*seglen)+1
    for round in range(looprange):
        print(f'reading segement {round}/{looprange}, length is {values.tbin*seglen}',end = "\r")
        reduced_data=cutscrunch(fb,values.tbin,values.fbin,tstart=round*values.tbin*seglen,total_length=values.tbin*seglen)
        newdata.append_spectra(reduced_data.astype(np.int8),filname)
    print(f'Finished total length {fb.native_nspectra}, tscrunched by {values.tbin}, fscrunched by {values.fbin}')

def scrunch(fb,tbin,fbin,total_length=65536):
     ### LONGER THAN SINGLE FAST OBS FILE TO ENSURE THE WHOLE DATA SET IS COLLECTED.
    totaldata=fb.get_data(nstart=0,nsamp=total_length)
    tscrunch=totaldata.reshape(-1,tbin,fb.nchans).mean(1)
    fscrunch=tscrunch.reshape(-1,fb.nchans//fbin,fbin).mean(2) 
    return fscrunch

def cutscrunch(fb,tbin,fbin,tstart=0,total_length=65536):
     ### LONGER THAN SINGLE FAST OBS FILE TO ENSURE THE WHOLE DATA SET IS COLLECTED.
    totaldata=fb.get_data(nstart=tstart,nsamp=total_length)
    tscrunch=totaldata.reshape(-1,tbin,fb.nchans).mean(1)
    fscrunch=tscrunch.reshape(-1,fb.nchans//fbin,fbin).mean(2) 
    return fscrunch

if __name__ == '__main__':
    _main()
