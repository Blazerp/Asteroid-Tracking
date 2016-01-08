import pyfits


    
hduList = pyfits.open("ktwo200000854-c00_lpd-targ.fits.gz")
sciData = hduList[1].data
#print(sciData.field(3)[0])
#for item in sciData.field(3)[0][0]:
#   print(item)
##listOfNums = range(0,5)
##for item in listOfNums:
##    print(sciData.field(4)[item][0][0
for item in sciData.field(3)[0]:
    print(item);
    
hduList.close()
