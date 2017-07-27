import math

from PIL import Image

############################################################################


#Function that takes the elements of a list and adds them on a string.

def _placeElementsToString(inList):

    outString = ""
    count = 0

    for i in inList:

        if i == 0:

            outString += "0"
            count += 1

            if count == 8: break

        else:

             outString += "1"
             count = 0

    return outString



#Function that converts a string to ascii and stores the result in a list.

def _toAscii(strText):

    resultList = []

    for i in range(0, len(strText)):

        resultList.append(ord(strText[i]))

    return resultList



#Function that converts ascii to binary and stores the result as a list.

def _toBinary(numberList):

    expList = [128,64,32,16,8,4,2,1]

    resultList = []

    for n in numberList:

        for exp in expList:

            if n < exp:

                resultList.append(0)

            else:

                resultList.append(1)
                n = n - exp

    #Appending ending sequence      

    for i in range(0,8): resultList.append(0)

    #Bit stuffing

    if len(resultList) % 3 == 1:

        resultList.append(0)
        resultList.append(0)

    if len(resultList) % 3 == 2:

        resultList.append(0)


    return resultList



#Function that converts a binary number to decimal number.

def _binaryToDecimal(binaryList):

    number = 0

    for i in range(0,len(binaryList)):

        if binaryList[i] == 1: number = number * 2 + 1

        else: number = number * 2

    return number
    


#Function that creates triple bit pairs in order to make the insertion process easier.

def _createTripleBitPairs(binaryList):

    tempList = []
    newList = []

    for i in range (0,len(binaryList),3):

        if i <= len(binaryList)-1: tempList.append(binaryList[i])
        if i <= len(binaryList)-2: tempList.append(binaryList[i+1])
        if i <= len(binaryList)-3: tempList.append(binaryList[i+2])

        newList.append(list(tempList))
        tempList.clear()

    return newList


###########################################################################


#Function that returns all pixels of an image in a list.

def _getImagePixels(image):

    return list(image.getdata())



#Function that converts a pixel from RGB to binary.

def _rgbToBinary(pixel):

    binaryPixel = []

    exp = 7

    for i in range(0,exp+1):

        if math.pow(2,exp-i) > pixel:

            binaryPixel.append(0)

        else:

            binaryPixel.append(1)
            pixel = pixel - math.pow(2,exp-i)

    return binaryPixel




#Function that inserts the LSB in a binary pixel list and returns a new list.

def _insertBit(binaryPixelList, bit):

    if not binaryPixelList[len(binaryPixelList)-1] == bit:

        binaryPixelList[len(binaryPixelList)-1] = bit

    return binaryPixelList




#Function that inserts all bits of input text in image's pixels and returns a list with the new pixels.

def _insertBitsToPixels(binaryList, pixelList):


    for i in range(0,len(binaryList)):

        bin = list(binaryList[i])
        currentPixel = list(pixelList[i])

        currentPixel[0] = _rgbToBinary(currentPixel[0])
        currentPixel[1] = _rgbToBinary(currentPixel[1])
        currentPixel[2] = _rgbToBinary(currentPixel[2])

        _insertBit(currentPixel[0], bin[0])
        _insertBit(currentPixel[1], bin[1])
        _insertBit(currentPixel[2], bin[2])

        currentPixel[0] = int(_binaryToDecimal(currentPixel[0]))
        currentPixel[1] = int(_binaryToDecimal(currentPixel[1]))
        currentPixel[2] = int(_binaryToDecimal(currentPixel[2]))

        pixelList[i] = currentPixel



#Creates a pixel tuple in order to be compatible for saving the new image.

def _createPixelTuple(pixelList):

    newPixelList = []

    for p in pixelList:

        newPixelList.append(tuple(p))

    return tuple(newPixelList)


######################################################################################

#Function that gets the LSB from every R,G and B value of every pixel and creates a new list.

def _getLsbFromPixels(pixelList):

    lsbList = []
    currentPixel = []

    count = 0


    for i in range(0,len(pixelList)):


        currentPixel = list(pixelList[i])

        for j in range(0,3):

            currentPixel[j] = _rgbToBinary(currentPixel[j])

        for j in range(0,3):

            if currentPixel[j][7] == 0: count += 1

            else: count = 0

            lsbList.append(currentPixel[j][7])

        if count == 8: break
        

    return lsbList



#Function that splits a string every 8 characters and returns a list of strings.

def _splitString(inputString):

    tempList = []
    
    tempString = ""

    for i in range(0,len(inputString),8):

        tempString = inputString[i:i+8]

        if tempString == "00000000": break

        else: tempList.append(inputString[i:i+8])


    return tempList



#Function that gets a message from a binary string list and returns a string.

def _getStringMessage(stringList):

    number = 0;

    message = ""

    for s in stringList:

        if len(s) == 8:

            number = int(s,2)
            message += str(chr(number))

    return message



#Function that checks if the message can be embedded in the image.

def _canEmbed(message, image):

    numOfMessageBits = len(message) * 3
    numOfImageLSB = image.size[0] * image.size[1] * 3

    if numOfMessageBits >= numOfImageLSB - 2:

        return False

    else: return True



#Function that checks if a file is JPEG or PNG.

def _isValidImageFile(imageNameString):

    tempString = imageNameString[-3:]

    if tempString == "jpg" or tempString == "png":
        return True

    else: return False



 #Function that embeds a message in a JPG or a PNG image and return a new PNG image with the embedded message.


def embedMessage(imagePathName, stegoPathName, message):

    aList = []
    bList = []
    cList = []

    pixels = []
    pixelTuple = ()

    if not _isValidImageFile(imagePathName):

        print("Invalid image file format. Try using JPG or PNG instead.")
        return None

    try:

        image = Image.open(imagePathName)
        print("Loaded image")

    except IOError:

        print("There was an error occured in opening image %s. Check if path name is correct." % (imagePathName))
        return None

    if not _canEmbed(message, image):

        print("Message length too big for storing. Try using a larger image.")
        return None 

    aList = _toAscii(message)
    bList = _toBinary(aList)
    cList = _createTripleBitPairs(bList)

    pixels = _getImagePixels(image)

    _insertBitsToPixels(cList, pixels)

    pixelTuple = _createPixelTuple(pixels)
    
    try:

        stegoImage = Image.new("RGB", image.size)
        print("New image created.")

    except IOError:

        print("There was an error occured creating image %s." % (stegoImage))
        return None

    if not _isValidImageFile(stegoPathName):

        print("Invalid image file format. Try using JPG or PNG instead.")
        return None

    stegoImage.putdata(pixelTuple)
    print("Stored pixels to new image.")
    stegoImage.save(stegoPathName)
    print("Image saved.")

    return stegoImage



#Function that extracts the message from a PNG image and returns the message.

def extractMessage(imagePathName):

    imagePixels = []
    lsbList = []
    newLsbList = []
    newList = []

    lsbString = ""
    message = ""

    if not _isValidImageFile(imagePathName):

        print("Invalid image file extension. Try using JPG or PNG instead.")
        return ""

    try:
        image = Image.open(imagePathName)
        print("Loaded image.") 

    except IOError:
        print("There was an error occured in opening image %s. Check if path name is correct." % (imagePathName))


    imagePixels = _getImagePixels(image)

    print("Extracting LSB from pixels...")

    lsbList = _getLsbFromPixels(imagePixels)

    lsbString = _placeElementsToString(lsbList)

    newList = _splitString(lsbString)

    message = _getStringMessage(newList)

    return message

######################################################################################
