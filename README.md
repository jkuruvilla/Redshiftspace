# Redshiftspace-
Creating redshift space simulation datacubes from the Gadget simulation. File format used is HDF5

Instructions:

Compile the cython code first. Can be done using the following two commands:

1. cython -a redshifthdf5.pyx
2. gcc -shared -pthread -fPIC -fwrapv -O2 -Wall -fno-strict-aliasing -I/usr/include/python2.7 -o redshifthdf5.so redshifthdf5.c
