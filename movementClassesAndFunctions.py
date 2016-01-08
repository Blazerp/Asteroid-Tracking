import pyfits

class Image(object):
    
    def __init__(self, fitsFile, imageNumber = 0, typeOfImage = 4):
        #Opens the file from a relative directory(It may work for absolute but
        #It has not worked for me)
        self.hduList = pyfits.open(fitsFile)
        #Starts at zero because of list indexing
        self.number = imageNumber
        #raw will be 3 flux will be 4 and flux error will be 5
        self.typeOfImage = typeOfImage
        #initializes the list of pixels in one image
        self.listOfPixels = self.listCreator()
        #finds the maximum pixel brightness inside the image
        self.max = findMax(self.listOfPixels) + 1
        #list of the pixels listed by coordinate and organized by brightness
        #ie. (1,2):341.223 would be an item in a dictionary
        #the list is organized from 0-9 with 9 being the brightest and 0 being
        #the dimmest
        self.caders = [{},{},{},{},{},{},{},{},{},{}]
        
    def returnPixelValue(self,x,y):
        #this function returns a pixel value at a certain coordinate
        return(self.listOfPixels[x][y])

    def listCreator(self):
        #This Function's purpose is to initialize the image from the fits file
        sciData = self.hduList[1].data
        xyList = sciData.field(self.typeOfImage)[self.number]
        return(xyList)
    
    def addRow(self,side = "bottom"):
        return(None)
    
    def changeListToBrightness(self):
        #This function organizes the pixels by how bright they are in relation to
        #the maximum
        i = 0 #horizontal coordinate
        j = 0 #vertical coordinate
        for row in self.listOfPixels: #iterates through the rows in the image
            for pixel in row: #iterates through the pixels in the row
                #this line is reasonablly complex, basicaly it takes a pixel value,
                #then it finds which spot in the list it should go in and lastly
                #it adds the pixel to a dictionary at a coordinate key
                self.caders[int(self.whichSpot(pixel))][(i + 1,j + 1)] = pixel
                #increments the number of vertical coordinates
                i += 1
            #increments the amount of horizontal coordinates
            j += 1
            #resets the number of vertical coordinates
            i = 0
        return(self.caders[9],self.caders[8])

    def whichSpot(self,pixel):
        #takes a pixel and finds out what area it falls in on a 0-9 scale of brightness
        return(((float(self.truncate((pixel/self.max),1)))*10))
        

    def truncate(self, f, n):
        #this function is to truncate a decimal to a certain place
        s = '{}'.format(f)
        if 'e' in s or 'E' in s:
            return '{0:.{1}f}'.format(f, n)
        i, p, d = s.partition('.')
        return('.'.join([i, (d+'0'*n)[:n]]))
        

def comparePixels(first, second):
##This function's purpose is to compare two pixel values...
##if the first pixel is larger, then it returns 1
##if the first is smaller, it returns -1
##if they are equal, then it returns 0
##all the paths return the difference between the
##first and second Always a positive difference
    if first < second:
        return(-1,(second - first))
    elif first > second:
        return(1,(first - second))
    else:
        return(0,0)
    
def clearAll():
    l = range(100000)
    del l 
 
def findMax(listMax):
    #this function finds the maximum value inside a list
    #first initialize a value inside of the list
    maxNum = listMax[0][0]
    #then iterate through the rows of the image
    for listmax in listMax:
        #then iterate through the individual pixels in that row
        for item in listmax:
            #if the item is larger than the maximum, set the maximum equal to the item
            if item > maxNum:
                maxNum = item
    return(maxNum)


    
clearAll()
imageList = []
i = 0
while i < 3000:
    imageOne = Image("ktwo200000854-c00_lpd-targ.fits.gz", imageNumber = i)
    imageTwo = Image("ktwo200000854-c00_lpd-targ.fits.gz", imageNumber = i + 1)
    if (imageTwo.listOfPixels[0][0] != 0) and (imageOne.listOfPixels[0][0] != 0):
        one9, one8 = imageOne.changeListToBrightness()
        two9, two8 = imageOne.changeListToBrightness()
        if (one9 == two9) and (one8 == two8):
            i +=2
        else:
            print("WRONG")
            i +=2
        print("PASSED" + " " + str(i))

    else:
        print("EMPTY")
        i += 2
    del(imageOne)
    del(imageTwo)
    clearAll()

