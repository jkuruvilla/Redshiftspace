__license__   = "GNU GPLv3 <https://www.gnu.org/licenses/gpl.txt>"
__copyright__ = "2015, Joseph Kuruvilla"
__author__    = "Joseph Kuruvilla <joseph.k@uni-bonn.de>"
__version__   = "1.0"

'''
Program to create redshift space simulation cube from GADGET simulation.
File format: hdf5

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

# ------------------
# Importing Modules
# ------------------

import h5py
import numpy as np
import sys
import redshifthdf5 as rhdf5

# ----------------------------
# Global variable declaration
#-----------------------------

ax = int(sys.argv[1]) #0-xaxis, 1-yaxis, 2-zaxis

# --------------------
#   Program  start
# --------------------    

if __name__ == "__main__":

  input_file = " " #Enter your input file here
  snap = h5py.File(input_file ,'r')
  
  head = snap["Header"] #reading header header

  omegam = head.attrs.get('Omega0')
  omegal = head.attrs.get('OmegaLambda')
  a      = head.attrs.get('Time')
  H      = (100*head.attrs.get('HubbleParam'))*np.sqrt((omegam/(a**3))+(omegal))  #H_0 = 100*h

  xxmax, xxmin = int(head.attrs.get('BoxSize')), 0

  if ax == 0:
    axis = 'xaxis'
  elif ax == 1:
    axis = 'yaxis'
  elif ax == 2:
    axis = 'zaxis'

  output_file = " "#Enter the name of your output file
  fsnap       = h5py.File(output_file, 'w')

  g = fsnap.create_group('/Header') #creating header in the output file

  g.attrs['NumPart_ThisFile']    = head.attrs.get('NumPart_ThisFile')
  g.attrs['NumPart_Total']       = head.attrs.get('NumPart_Total')
  g.attrs['MassTable']           = head.attrs.get('MassTable')
  g.attrs['Time']                = head.attrs.get('Time')
  g.attrs['Redshift']            = head.attrs.get('Redshift')
  g.attrs['BoxSize']             = head.attrs.get('BoxSize')
  g.attrs['NumFilesPerSnapshot'] = head.attrs.get('NumFilesPerSnapshot')
  g.attrs['Omega0']              = head.attrs.get('Omega0')
  g.attrs['OmegaLambda']         = head.attrs.get('OmegaLambda')
  g.attrs['HubbleParam']         = head.attrs.get('HubbleParam')
  g.attrs['Flag_Sfr']            = head.attrs.get('Flag_Sfr')
  g.attrs['Flag_Cooling']        = head.attrs.get('Flag_Cooling')
  g.attrs['Flag_StellarAge']     = head.attrs.get('Flag_StellarAge')
  g.attrs['Flag_Metals']         = head.attrs.get('Flag_Metals')
  g.attrs['Flag_Feedback']       = head.attrs.get('Flag_Feedback')

  vel = snap["/PartType1/Velocities"][:]
  pos = snap["/PartType1/Coordinates"][:]
  ids = snap["/PartType1/ParticleIDs"][:]

  print("starting") #optional

  pos = rhdf5.iteration(pos, vel, np.sqrt(a), H, xxmin, xxmax, ax) #calling the cythonized function for faster computation
           
  g1 = fsnap.create_group('PartType1') #creating a group in the output file
  g1['Coordinates'] = pos[:]
  g1['ParticleIDs'] = ids[:]
  g1['Velocities']  = vel[:]
  
  fsnap.close()
