from mpl_toolkits.mplot3d import Axes3D
import h5py as h5
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import os
import glob
import fnmatch
from matplotlib.ticker import MultipleLocator
from matplotlib import cm
import matplotlib.gridspec as gridspec

plt.style.use(['science','std-colors'])



#filename='hdf5_2D_S=20.00vF=10.00vis=0.00l=0.00wc=5.00.h5'
filename='hdf5_2D_S=30.00vF=6.00vis=0.100odd=0.000l=0.000wc=0.00therm=0.00.h5'
#filename='hdf5_2D_S=30.00vF=5.00vis=0.070odd=0.000l=0.000wc=0.00therm=0.00.h5'

f = h5.File(filename, "r")
density_group = f['Data/Density']
velocity_group = f['Data/VelocityX']

#key='snapshot_00600'
#key='snapshot_00239'
key='snapshot_00008'
n = density_group[key]
u = velocity_group[key]
N = np.array(n)
U = np.array(u)
X = np.linspace(0, 1.0, 151)
Y = np.linspace(0, 1.0, 151)
#Y = np.linspace(0, 1.0, 301)
#Y = np.linspace(0, 1.0, 376)


#fig = plt.figure(figsize=(13.5,8))  # PRL default width
fig = plt.figure(figsize=(4.5,3.5))
#fig = plt.figure()

ax1 = plt.axes(projection='3d')


ax1.set_xlabel(r'$x/L$',labelpad=-5)
ax1.set_ylabel(r'$y/W$',labelpad=-5)
ax1.set_zlabel(r'$n/n_0$',labelpad=-2)
#ax1.view_init(elev=20, azim=135)
ax1.view_init(elev=15, azim=120)
ax1.grid(False)
ax1.xaxis.pane.set_edgecolor('k')
ax1.yaxis.pane.set_edgecolor('k')
ax1.zaxis.pane.set_edgecolor('k')
ax1.xaxis.pane.fill = False
ax1.yaxis.pane.fill = False
ax1.zaxis.pane.fill = False
#ax1.xaxis.pane.fill = True
#ax1.yaxis.pane.fill = True
#ax1.zaxis.pane.fill = True


ax1.xaxis.set_rotate_label(False)
ax1.yaxis.set_rotate_label(False)
#ax1.zaxis.set_rotate_label(False)

X, Y = np.meshgrid(X, Y)
#surf = ax1.plot_surface(X,Y,N)#,cstride=1,rstride=1,color="white",shade=False)
surf = ax1.plot_wireframe(X,Y,N,cstride=5,rstride=15,linewidth=0.5,color='k')#,cstride=1,rstride=1,color="white",shade=False)


#cset = ax1.contourf(X, Y, U, zdir='z', offset=0.94, cmap=cm.ocean)
cset = ax1.contourf(X, Y, U,100, zdir='z', offset=.94, cmap=cm.Spectral)
cset.set_clim(0, 1.2)

ax1.set_xlim(1 ,0)  
ax1.set_ylim(0, 1)
#ax1.set_zlim(1, 2)  
ax1.set_zlim(.94, 1.)  

ax1.set_yticks(np.arange(0, 1.1, 0.2))
ax1.set_xticks(np.arange(0, 1.1, 0.2))
#ax1.set_zticks(np.arange(1, 2.1, 0.2))
#ax1.set_zticks(np.arange(.95, 1.01, 0.025))
ax1.set_zticks(np.arange(.94, 1.01, 0.02))

ax1.xaxis._axinfo['tick']['inward_factor'] = 0
ax1.xaxis._axinfo['tick']['outward_factor'] = 0.4
ax1.yaxis._axinfo['tick']['inward_factor'] = 0
ax1.yaxis._axinfo['tick']['outward_factor'] = 0.4
ax1.zaxis._axinfo['tick']['inward_factor'] = 0
ax1.zaxis._axinfo['tick']['outward_factor'] = 0.4
ax1.zaxis._axinfo['tick']['outward_factor'] = 0.4

ax1.xaxis.set_minor_locator(MultipleLocator(0.1))
ax1.yaxis.set_minor_locator(MultipleLocator(0.1))
ax1.zaxis.set_minor_locator(MultipleLocator(0.01))

ax1.tick_params(axis='x', which='major', pad=-3,labelsize='x-small')
ax1.tick_params(axis='y', which='major', pad=-3,labelsize='x-small')
ax1.tick_params(axis='z', which='major', pad=0,labelsize='x-small')

cmap = mpl.cm.Spectral
norm = mpl.colors.Normalize(vmin=0, vmax=1.2)
cbar=fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap),ax=ax1, orientation='horizontal',aspect=25,shrink=0.75,pad=-0.07)

#cbar=fig.colorbar(cset,ax=ax1,ticks=[ 0,0.2,0.4,0.6,0.8, 1,1.2],orientation = 'horizontal',shrink=0.6,aspect=25,pad=-0.07)  
cset.set_clim(0, 1.2)
cbar.solids.set_edgecolor("face")
cbar.set_label(r'$v_x/v_0$', labelpad=-20,x=1.1)

print(np.amax(U))

#tick_list = [ 0,0.2,0.4,0.6,0.8, 1,1.2]
#cbar.set_ticklabels(list(map(str, tick_list)))
cset.set_clim(0, 1.2)



fig.tight_layout(pad=0)
fig.savefig("shockfront.pdf", bbox_inches='tight',pad_inches = 0)
#fig.savefig("shockfront.png", bbox_inches='tight',pad_inches = 0)

