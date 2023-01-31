"""
script to cut pulsar data into subbands,and convert to filterbank or fits format
filterbank files using astropy/your


"""
import your
import numpy as np
import os
__author__ = "Harry Qiu <hao.qiu@skao.int>"


def _main():
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    parser = ArgumentParser(description='Script description', formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', help='Be verbose')
    parser.add_argument('-o', '--output',type=str, default="subband",help='Output File Name, no suffix')
    parser.add_argument('-f', '--file',type=str, default="test.fil",help='Input File Name')
    parser.add_argument('--ch1',type=int, default=0,help='starting channel')
    parser.add_argument('--cmax',type=int, default=8192,help='total channels')
    parser.add_argument('--nstart',type=int, default=0,help='start sample')
    parser.add_argument('--nsamp',type=int, default=-1,help='length of data to write, -1 for end of file')

    ## your has not implemented this feature yet
    # parser.add_argument('-b','--tbin',type=int, default=1,help='tscrunch samples per bin')
    # parser.add_argument('--fbin',type=int, default=1,help='fscrunch samples per bin')
    # parser.add_argument(dest='files', nargs='+')
    parser.set_defaults(verbose=False)
    values = parser.parse_args()
    cutoutfil(values.file,values.output,values.ch1,values.cmax,values.nstart,values.nsamp)


def cutoutfil(filename,output,ch1,cmax,nstart,nsamp):
    your_object=your.Your(filename)
    if nsamp == -1:
        writer_object = your.Writer(
        your_object,
        nstart=nstart,
        c_min=ch1,
        c_max=cmax,
        outdir="./",
        outname=output,
        time_decimation_factor=1,
        frequency_decimation_factor=1)
    else:
        writer_object = your.Writer(
        your_object,
        nstart=nstart,
        nsamp=nsamp,
        c_min=ch1,
        c_max=cmax,
        outdir="./",
        outname=output,
        time_decimation_factor=1,
        frequency_decimation_factor=1)
    writer_object.to_fil()




if __name__ == '__main__':
    _main()
