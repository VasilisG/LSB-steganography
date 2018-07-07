from PIL import Image
import os

filename = "test.txt"
imageExtension = "png"
bitsPerChar = 8
bitsForSize = 32
bitsPerPixel = 3

def canEncode(filename, imageName):
    fileSize = 0
    imageSize = 0
    extensionSize = len("".join(filename[filename.find("."):]))
    sizeInfo = int(bitsForSize / bitsPerChar)

    try:
        fileSize = os.path.getsize(filename)
    except os.error:
        print("Could not find file %s." % filename)
        return False

    try:
        imageSize = os.path.getsize(imageName)
    except os.error:
        print("Could not find file %s." % imageName)
        return False

    totalSize = extensionSize + sizeInfo + fileSize
    return totalSize <= imageSize

def getFileData(filename):
    inFile = None

    try:
        inFile = open(filename, "rb")
    except IOError:
        print("Could not open file %s." % filename)

    bytes = [l for line in inFile for l in line]
    binaries = [bin(b)[2:].rjust(bitsPerChar,'0') for b in bytes]
    binaries = "".join(binaries)

    extension = filename[filename.find('.')+1:]
    extension = [bin(ord(b))[2:].rjust(bitsPerChar,'0') for b in extension]
    extension = "".join(extension) + '0' * bitsPerChar

    size = int(len(binaries) / bitsPerChar)
    size = [bin(size)[2:].rjust(bitsForSize,'0')]
    size = "".join(size) + '0' * bitsPerChar

    bitStuffing = (len(extension) + len(size) + len(binaries)) % bitsPerPixel

    data = "".join([extension, size, binaries, '0' * bitStuffing])
    data = [data[i * bitsPerPixel : i * bitsPerPixel + bitsPerPixel] for i in range(0,int(len(data)/bitsPerPixel))]

    return data

def createNewPixels(imageFilename, data):
    img = Image.open(imageFilename)
    imgSize = img.size

    pixels = list(img.getdata())

    binaryPixels = [list(bin(p)[2:].rjust(bitsPerChar,'0') for p in pixel) for pixel in pixels]

    for i in range(len(data)):
        for j in range(len(data[i])):
            binaryPixels[i][j] = list(binaryPixels[i][j])
            binaryPixels[i][j][-1] = data[i][j]
            binaryPixels[i][j] = "".join(binaryPixels[i][j]) 

    newPixels = [tuple(int(p,2) for p in pixel) for pixel in binaryPixels]
    return newPixels

def encodeLSB(filename, imageFilename, newFilename):
    if canEncode(filename, imageFilename):
        data = getFileData(filename)
        newPixels = createNewPixels(imageFilename, data)

        stegoImageFilename = ".".join([newFilename, imageExtension])

        newImg = Image.new("RGB", imgSize)
        newImg.putdata(newPixels)
        newImg.save(stegoImageFilename)

        return newImg

################## Decoding functions #######################################

def getLSBs(binaryPixels):
    return [p[-1] for pixel in binaryPixels for p in pixel]

def getExtensionInfo(lsbPixels):
    extension = []
    currentIndex = 0
    for p in range(0,len(lsbPixels),bitsPerChar):
        letter = lsbPixels[p:p+bitsPerChar]
        letter = "".join(letter)
        if letter == "00000000":
            currentIndex = currentIndex + bitsPerChar
            break
        extension.append("".join(letter))
        currentIndex = currentIndex + bitsPerChar

    extension = "".join([chr(int(e,2)) for e in extension])
    return (extension, currentIndex)


def getSizeInfo(lsbPixels, index):
    totalZeros = 0
    currentIndex = 0
    size = []
    for p in lsbPixels[index:]:
        if currentIndex == bitsForSize:
            break
        size.append(p)
        currentIndex = currentIndex + 1
    size = int("".join(size), 2)
    return (size, index + currentIndex)

def getData(lsbPixels, index, size):
    currentIndex = 0
    data = []
    for p in range(index,len(lsbPixels[index:]),bitsPerChar):
        if currentIndex == size * bitsPerChar:
            break
        data.append("".join(lsbPixels[p:p+bitsPerChar]))
        currentIndex = currentIndex + bitsPerChar

    return (data[1:], currentIndex)

def decodeLSB(stegoFilename, finalFilename):
    img = None
    newFile = None

    try:
        img = Image.open(stegoFilename)
    except:
        print("Could not open file %s." % stegoFilename)
        return None

    pixels = list(img.getdata())
    binaryPixels = [(bin(p)[2:].rjust(bitsPerChar,'0') for p in pixel) for pixel in pixels]
    lsbPixels = getLSBs(binaryPixels)

    extension, currentIndex = getExtensionInfo(lsbPixels)
    size, currentIndex = getSizeInfo(lsbPixels, currentIndex)
    data, currentIndex = getData(lsbPixels, currentIndex, size)

    finalFilename = '.'.join([finalFilename, extension])

    try:
        newFile = open(finalFilename, "wb")
    except IOError:
        print("Could not open file %s." % finalFilename)

    for d in data:
        newFile.write(bytes([int(d,2)]))