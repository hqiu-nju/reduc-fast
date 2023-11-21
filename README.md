# reduc-fast
data reduction tools for fast transient search observation data 

Was developed for dealing with FAST observations, but works generically for psrfits and filterbank files
## dependencies
your (https://thepetabyteproject.github.io/your/0.6.6/).

## getting started
subband.py is the easiest way to spit out a chunk of the data into a filterbank format, you can also use it to convert a whole file.

merge.py and scrunch.py are a little bit more hardcoded to work on data length. I plan to merge the functions in these scripts eventually...
