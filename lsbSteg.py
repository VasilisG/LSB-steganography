import math

from PIL import Image

############################################################################


#Function that takes the elements of a list and adds them on a string (CORRECT)

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



#Function that converts a string to ascii and stores the result in a list. (CORRECT)

def _toAscii(strText):

    resultList = []

    for i in range(0, len(strText)):

        resultList.append(ord(strText[i]))

    return resultList



#Function that converts ascii to binary and stores the result as a list. (CORRECT)

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



#Function that converts a binary number to decimal number. (CORRECT)

def _binaryToDecimal(binaryList):

    number = 0

    for i in range(0,len(binaryList)):

        if binaryList[i] == 1: number = number * 2 + 1

        else: number = number * 2

    return number
    


#Function that creates triple bit pairs in order to make the insertion process easier. (CORRECT)

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


#Function that returns all pixels of an image in a list. (CORRECT)

def _getImagePixels(image):

    return list(image.getdata())



#Function that converts a pixel from RGB to binary. (CORRECT)

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




#Function that inserts the LSB in a binary pixel list and returns a new list. (CORRECT)

def _insertBit(binaryPixelList, bit):

    if not binaryPixelList[len(binaryPixelList)-1] == bit:

        binaryPixelList[len(binaryPixelList)-1] = bit

    return binaryPixelList




#Function that inserts all bits of input text in image's pixels and returns a list with the new pixels. (CORRECT)

def _insertBitsToPixels(binaryList, pixelList):


    for i in range(0,len(binaryList)):

        bin = list(binaryList[i])
        currentPixel = list(pixelList[i])

        #print("Bin: ", bin)
        #print("Current pixel: ", currentPixel)


        currentPixel[0] = _rgbToBinary(currentPixel[0])
        currentPixel[1] = _rgbToBinary(currentPixel[1])
        currentPixel[2] = _rgbToBinary(currentPixel[2])

        #print("Current pixel(binary): ", currentPixel)

        _insertBit(currentPixel[0], bin[0])
        _insertBit(currentPixel[1], bin[1])
        _insertBit(currentPixel[2], bin[2])

        currentPixel[0] = int(_binaryToDecimal(currentPixel[0]))
        currentPixel[1] = int(_binaryToDecimal(currentPixel[1]))
        currentPixel[2] = int(_binaryToDecimal(currentPixel[2]))

        #print("Current pixel: ", currentPixel)

        pixelList[i] = currentPixel



#Creates a pixel tuple in order to be compatible for saving the new image. (CORRECT)

def _createPixelTuple(pixelList):

    newPixelList = []

    for p in pixelList:

        newPixelList.append(tuple(p))

    return tuple(newPixelList)


######################################################################################

#Function that gets the LSB from every R,G and B value of every pixel and creates a new list. (CORRECT)

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



#Function that checks if we reached the end of reading bits. [NOT USED]

def _isEndingSequence(binaryOctet):

    for i in range(0,len(binaryOctet)):

        if binaryOctet[i] == 1: return False;

    return True



#Function that creates octets of the elements of the input list and returns a new list as output. [NOT USED]

def _createOctets(lsbList):

    count = 0
    tempList = []
    octetList = []

    for i in lsbList:

        tempList.append(i)

        count += 1

        if count % 8 == 0 and not count == 0:

            if _isEndingSequence(tempList): break;

            else:
                octetList.append(list(tempList))
                tempList.clear()

            count = 0

    return octetList



#Function that splits a string every 8 characters and returns a list of strings. (CORRECT)

def _splitString(inputString):

    tempList = []
    
    tempString = ""

    for i in range(0,len(inputString),8):

        tempString = inputString[i:i+8]

        if tempString == "00000000": break

        else: tempList.append(inputString[i:i+8])


    return tempList



#Function that gets the message from the binary list, converts it to ASCII and stores it to a string. [NOT USED]

def _getMessage(binaryList):

    tempList = []
    number = 0
    count = 0
    message = ""

    tempList = _createOctets(binaryList)

    for element in tempList:

        number = int(_binaryToDecimal(element))

        if number > 127: number = int(number / 2)

        message += str(chr(number))


    return message



#Function that gets a message from a binary string list and returns a string. (CORRECT)

def _getStringMessage(stringList):

    number = 0;

    message = ""

    for s in stringList:

        if len(s) == 8:

            number = int(s,2)
            message += str(chr(number))

    return message



#Function that checks if the message can be embedded in the image. (CORRECT)

def _canEmbed(message, image):

    numOfMessageBits = len(message) * 3
    numOfImageLSB = image.size[0] * image.size[1] * 3

    if numOfMessageBits >= numOfImageLSB - 2:

        print("Message is too big to fit in image. Try a bigger image to embed the message.")
        return False

    else: return True



#Function that checks if a file is JPEG or PNG. (CORRECT)

def _isValidImageFile(imageNameString):

    tempString = imageNameString[-3:]
    #print(tempString)

    if tempString == "jpg" or tempString == "png":
        return True

    else: return False



 #Function that embeds a message in a JPG or a PNG image and return a new PNG image with the embedded message. (CORRECT)


def embedMessage(imageNameString, stegoNameString, message):

    aList = []
    bList = []
    cList = []

    pixels = []
    pixelTuple = ()

    if not _isValidImageFile(imageNameString):

        print("Invalid image file format. Try using JPG or PNG instead.")
        return None

    try:
        image = Image.open(imageNameString)
        print("Loaded image")

    except IOError:
        print("There was an error occured in opening image %s. Check if path name is correct." % (imageNameString))

    aList = _toAscii(message)
    bList = _toBinary(aList)
    cList = _createTripleBitPairs(bList)

    pixels = list(image.getdata())

    _insertBitsToPixels(cList, pixels)

    pixelTuple = _createPixelTuple(pixels)

    stegoImage = Image.new("RGB", image.size)
    print("New image created.")
    stegoImage.putdata(pixelTuple)
    print("Storing LSBs...")
    stegoImage.save(stegoNameString)
    print("Image saved.")

    return stegoImage



#Function that extracts the message from a PNG image and returns the message. (CORRECT)

def extractMessage(imageNameString):

    imagePixels = []
    lsbList = []
    newLsbList = []
    lsbString = ""
    newList = []
    message = ""

    if not _isValidImageFile(imageNameString):

        print("Invalid image file extension. Try using JPG or PNG instead.")
        return ""

    try:
        image = Image.open(imageNameString)
        print("Loaded image.") 

    except IOError:
        print("There was an error occured in opening image %s. Check if path name is correct." % (imageNameString))


    imagePixels = list(image.getdata())

    print("Extracting LSB from pixels...")

    lsbList = _getLsbFromPixels(imagePixels)
    #newLsbList = _createTripleBitPairs(lsbList)

    lsbString = _placeElementsToString(lsbList)

    newList = _splitString(lsbString)

    message = _getStringMessage(newList)

    return message



######################################################################################
