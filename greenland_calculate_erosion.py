#greenland_calc_erosion.py
import netCDF4 as nc
import matplotlib.pyplot as plt
import numpy as np
import matlab
import matlab.engine as mlab

fn='/Users/keislingldeo/Documents/lamont21-22/greenland_erosion/data/greenland_800kyr_min_exposure.nc'
ds=nc.Dataset(fn)

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



#print('erosion is',np.sum(erosion[1:1600,65,65]))


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

for ii in range(1,135):  #135
	print(ii)	
	
	np.savetxt("besum_.txt", besum, delimiter="\t", fmt="%1.4e")
	np.savetxt("alsum_.txt", alsum, delimiter="\t", fmt="%1.4e")
	np.savetxt("csum_.txt",csum, delimiter="\t", fmt="%1.4e")
	np.savetxt("bedepthsum_.txt", bedepthsum, delimiter="\t", fmt="%1.4e")
	np.savetxt("aldepthsum_.txt", aldepthsum, delimiter="\t", fmt="%1.4e")
	np.savetxt("cdepthsum_.txt", cdepthsum, delimiter="\t", fmt="%1.4e")


	for jj in range(1,165): #165

#		print(ii)
#		print(jj)

#		print(lat[ii])
#		print(lon[jj])

		mlat=matlab.double([lat[ii]])
		mlon=matlab.double([lon[jj]])


#		mlat=matlab.double([70])
#		mlon=matlab.double([-10])
		elv=matlab.double([100])
#		elv=matlab.double(0:1601,ii,jj)



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

			print(be)
 		
eng.quit()


np.savetxt("besum_final_1.45_1.5.txt", besum, delimiter="\t", fmt="%1.4e")
np.savetxt("alsum_final_1.45_1.5.txt", alsum, delimiter="\t", fmt="%1.4e")
np.savetxt("csum_final_1.45_1.5.txt",csum, delimiter="\t", fmt="%1.4e")
np.savetxt("bedepthsum_final_1.45_1.5.txt", bedepthsum, delimiter="\t", fmt="%1.4e")
np.savetxt("aldepthsum_final_1.45_1.5.txt", aldepthsum, delimiter="\t", fmt="%1.4e")
np.savetxt("cdepthsum_final_1.45_1.5.txt", cdepthsum, delimiter="\t", fmt="%1.4e")


plt.imshow(besum, origin='lower')
plt.colorbar()
plt.show()

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






