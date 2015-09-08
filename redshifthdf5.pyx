'''
__license__   = "GNU GPLv3 <https://www.gnu.org/licenses/gpl.txt>"
__copyright__ = "2015, Joseph Kuruvilla"
__author__    = "Joseph Kuruvilla <joseph.k@uni-bonn.de>"
__version__   = "1.0"

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

from __future__ import division
import numpy as np
cimport numpy as np

DTYPEf = np.float32
ctypedef np.float32_t DTYPEf_t

cimport cython

@cython.boundscheck(False)
@cython.wraparound(False)

def iteration(np.ndarray[DTYPEf_t, ndim=2] data, np.ndarray[DTYPEf_t, ndim=2] data1, float sq_scale_factor, float hubble, int xmin, int xmax, int axis):
  """
  Function to go through each particle and distort the simulation cube to emulate redshift space configuration. 
  Distortion is done by following equation s = z + v_z/(a*H)  |  considering the line of sight to be z axis.
  data is the position array
  data1 is the line of sight velocity array
  sq_scale_factor is the square root of the scale factor. Square root is used due to the GADGET normalisation scheme
  axid: 0 for x-axis, 1 for y-axis, 2 for z-axis
  """
  cdef int i
  
  for i in range(1024**3):
    data[i,axis]+=(data1[i,axis]/(sq_scale_factor*hubble))
    if data[i,axis] > xmax:
        data[i,axis] =  data[i,axis] - xmax
    elif data[i,axis] < xmin:
        data[i,axis] = xmax + data[i,axis]
        
  return data
  
  