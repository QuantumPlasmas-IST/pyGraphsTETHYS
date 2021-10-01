import glob
import matplotlib.pyplot as plt
import numpy as np
import time

from pydmd import HODMD


# Read file
for filename in glob.glob("electro_*.dat"):
	data = np.loadtxt(filename)
	label = filename.replace('preview_','').replace('.dat','')
	time = data[:, 0]
	netQ = data[:, 1]
	iDS   = data[:, 2]
	iHall = data[:, 3]
	VDS = data[:, 4]
	iD  = data[:, 5]
	iS  = data[:, 6]
	Pohm = data[:, 7]
	Pcap = data[:, 8]
	pX = data[:, 9]
	dpX= data[:, 10]
	ddpX= data[:, 11]
	pY= data[:, 12]
	dpY= data[:, 13]
	ddpY= data[:, 14]
	dt = time[1]-time[0]
	snapshots = iDS

	hodmd = HODMD(svd_rank=0, exact=True, opt=True, d=205).fit(snapshots)
	amplitudes = hodmd._compute_amplitudes(hodmd.modes, snapshots, hodmd.eigs, True)
	l = hodmd.eigs
	w = np.log(hodmd.eigs)/dt
	wr = np.imag(w) 
	wi = np.real(w)


	#Plotting
	plt.plot(dt*hodmd.original_timesteps, snapshots, '-', label=r'$I_{DS}$ input')
	plt.plot(dt*hodmd.dmd_timesteps, hodmd.reconstructed_data[0].real, '--', label='HODMD reconstruction')
	plt.legend()
	fig_name = 'HODMD_Reconstruction_' + label + '.png'
	plt.savefig(fig_name, quality=100)
	plt.close("all")

	plt.xlim(0,100)
	plt.ylabel(r'$a_m$')
	plt.xlabel(r'$\Re(\omega_m)$')
	plt.plot(wr/(2.0*np.pi),np.abs(amplitudes),'.')
	fig_name = 'HODMD_Modes_' + label + '.png'
	plt.savefig(fig_name, quality=100)
	plt.close("all")

	#Log savinf
	logname = 'HoDMD_' + label + '.dat'
	logfile = open(logname, 'w') 
	print >>logfile,'#' + label
	print >>logfile,'#amp\twr\twi\tRe(eigen)\tIm(eigen)'
	out_data=np.column_stack((np.abs(amplitudes),wr,wi,np.real(l),np.imag(l)))
	np.savetxt(logfile, sorted(out_data,key=lambda row:row[1]), delimiter='\t', newline='\n', header='', footer='', comments='# ', encoding=None,fmt='%.6f')
	logfile.close()



