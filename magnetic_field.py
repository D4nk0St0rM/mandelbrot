
### Import required packages  ###
import numpy as np
import matplotlib.pyplot as plt
import sys
import time
from math import *
import matplotlib.pyplot as plt
from scipy import interpolate
from scipy.interpolate import interp1d

######################

### Set globals, lists. variables, constants used in program ###

distance = np.array ([-60,-50,-40,-30,-20,-10,0,10,20,30,40,50,60])
magfield = np.array ([2.161,2.807,3.778,4.776,5.768,6.553,6.854,6.554,5.768,4.776,3.778,2.807,2.161])

# graph and plot the values
def plot_points():
  #global x_array, y_array
  x = distance
  y = magfield
  plt.figure(figsize=(20,15))
  plt.title(r'$\mathrm{Magnetic\ Field\ of \ Single\ Coil\ with\ radius\ 55.0\ cm\ ,12\ loops\ ,&\ 0.5\ Ampere}$', fontsize=14)
  plt.xlabel(r'distance - $\mathrm{(\ d)\ /\ cm}$', fontsize=12)
  plt.ylabel(r'Magnetic Field Strength  - $\mathrm{(\ B)\ \ /\mu\ T}$', fontsize=12)
  f = interp1d(x, y)
  f2 = interp1d(x, y, kind='cubic')
  xnew = np.linspace(-60, 60, num=600, endpoint=True)
  plt.plot(x, y)
  plt.plot(x, y, '-w', xnew, f2(xnew), '-g')
  plt.xticks(np.arange(min(x), max(x)+1, 5.0))
  plt.yticks(np.arange(0, max(y)+1, 0.25))
  plt.minorticks_on()
  plt.grid(which='major',linestyle='dotted')
  plt.grid(which='minor',linestyle='dotted')
  plt.ylim(bottom=0)
  plt.xlim(left=-60,right=60)
  plt.show()
# Turn on the minor TICKS, which are required for the minor GRID
# colNames={'X-Data','Y-Data'};
# T = plt.table(distance,magfield);
# t=uitable(f,'Data',data,'Position',[300,100,200,300],'ColumnName',colNames);
plt.show()
plot_points()
