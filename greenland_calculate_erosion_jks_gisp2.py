#greenland_calc_erosion.py
import netCDF4 as nc
import matplotlib.pyplot as plt
import numpy as np
import matlab
import matlab.engine as mlab
import os


directory='/Users/keislingldeo/Documents/lamont21-22/greenland_erosion/data/'

for file in os.listdir(directory):
	filename = os.fsdecode(file)
	if filename.endswith("_exposure.nc"):
	
		fn=os.path.join(directory, filename)
		print(fn)


#fn='/Users/keislingldeo/Documents/lamont21-22/greenland_erosion/data/rip33_gdgt_1.6_0.5_3.nc'


		ds=nc.Dataset(fn)

		## for GISP2 - ii is 66, jj is 97
		## for CR1 - ii is 55, jj is 65


		#see the variables inside ds: 

		thickness=ds['h'][:]
		time=ds['time'][:]
		ua=ds['ua'][:]
		va=ds['va'][:]
		elev=ds['hb'][:]
		lat=ds['lat'][:]
		lon=ds['lon'][:]

		uasq=np.square(ua)
		vasq=np.square(va)
		veltot=np.sqrt(uasq+vasq)

		print ('ua')
		print(uasq.shape)
		print(veltot.shape)

		#CALCULATE TOTAL EROSION for each timestep

		C=1.1721e-5
		b=0.6341

		#erosion=C*veltot.**b
		erosion=500*C*np.power(veltot,b)
		col1=time[0:1601]


		ii=55
		jj=65

		print('erosion at CR1 is',np.sum(erosion[1:1600,ii,jj]))


		thksum=np.empty([thickness.shape[1],thickness.shape[2]])
		print(thksum.shape)
		thksum=np.sum(thickness,axis=0)
		thksum[thksum>=1] = 1

		besum=np.zeros([thickness.shape[1],thickness.shape[2]])
		alsum=np.zeros([thickness.shape[1],thickness.shape[2]])
		csum=np.zeros([thickness.shape[1],thickness.shape[2]])

		bedepthsum=np.zeros([thickness.shape[1],thickness.shape[2]])
		aldepthsum=np.zeros([thickness.shape[1],thickness.shape[2]])
		cdepthsum=np.zeros([thickness.shape[1],thickness.shape[2]])


		eng=mlab.start_matlab()


		#print(ii)	
	
		np.savetxt("besum_.txt", besum, delimiter="\t", fmt="%1.4e")
		np.savetxt("alsum_.txt", alsum, delimiter="\t", fmt="%1.4e")
		np.savetxt("csum_.txt",csum, delimiter="\t", fmt="%1.4e")
		np.savetxt("bedepthsum_.txt", bedepthsum, delimiter="\t", fmt="%1.4e")
		np.savetxt("aldepthsum_.txt", aldepthsum, delimiter="\t", fmt="%1.4e")
		np.savetxt("cdepthsum_.txt", cdepthsum, delimiter="\t", fmt="%1.4e")


		mlat=matlab.double([lat[ii]])
		mlon=matlab.double([lon[jj]])

		print('latitute is', mlat, 'longitude is', mlon)


		elv=matlab.double([100])
		#elv=matlab.double(np.mean([elev[0:1601,ii,jj]]))



		col2=erosion[0:1601,ii,jj]
		col3=veltot[0:1601,ii,jj]
		col4=thickness[0:1601,ii,jj]
		output=np.stack((col1, col2, col3, col4), axis=1)
		np.savetxt("one-site-erosion.txt", output, delimiter="\t", fmt="%1.4e")

		if thksum[ii,jj]==1:

			(be,al,c,be_depth,al_depth,c_depth) = eng.CoreModel_totalerosion_pleisto_BeAlC(mlat,mlon,elv,'one-site-erosion.txt',nargout=6)
			besum[ii,jj]=be
			alsum[ii,jj]=al
			csum[ii,jj]=c
			bedepthsum[ii,jj]=be_depth
			aldepthsum[ii,jj]=al_depth
			cdepthsum[ii,jj]=c_depth

			print('the ending beryllium concentration at CR1 is', be)
	
		eng.quit()


		np.savetxt("besum_final.txt", besum, delimiter="\t", fmt="%1.4e")
		np.savetxt("alsum_final.txt", alsum, delimiter="\t", fmt="%1.4e")
		np.savetxt("csum_final.txt",csum, delimiter="\t", fmt="%1.4e")
		np.savetxt("bedepthsum_final.txt", bedepthsum, delimiter="\t", fmt="%1.4e")
		np.savetxt("aldepthsum_final.txt", aldepthsum, delimiter="\t", fmt="%1.4e")
		np.savetxt("cdepthsum_final.txt", cdepthsum, delimiter="\t", fmt="%1.4e")

	else:
		continue



		#plt.imshow(besum, origin='lower')
		#plt.colorbar()
		#plt.show()

		#CoreModel_totalerosion_pleisto_BeAlC.m. You'll see the 
		#inputs are lat, long, elevation, 
		#time, erosion rate, velocity, thickness 
		#(those last 4 inputs being the columns from your .txt file). 
		#
		#

		## CREATE A LOOP TO RUN ALLIE'S SCRIPT.
		# 

		#for ii in range(thickness.shape[1]):
		#	for jj in range(thickness.shape[2]):
		#		thksum[ii][jj]=np.sum(thickness[:][jj][ii],axis=0)
		#	print(ii)




		#mask out shelf


		# #plot the mask for ice/not ice






