from PIL import Image

bitsPerChar = 8
bitsPerPixel = 3
maxBitStuffing = 2
extension = "png"

def canEncode(message, image):
       width, height = image.size
       imageCapacity = width * height * bitsPerPixel
       messageCapacity = (len(message) * bitsPerChar) - (bitsPerChar + maxBitStuffing)
       return imageCapacity >= messageCapacity

def createBinaryTriplePairs(message):
       binaries = list("".join([bin(ord(i))[2:].rjust(bitsPerChar,'0') for i in message]) + "".join(['0'] * bitsPerChar))
       binaries = binaries + ['0'] * (len(binaries) % bitsPerPixel)
       binaries = [binaries[i*bitsPerPixel:i*bitsPerPixel+bitsPerPixel] for i in range(0,int(len(binaries) / bitsPerPixel))]
       return binaries

def embedBitsToPixels(binaryTriplePairs, pixels):
       binaryPixels = [list(bin(p)[2:].rjust(bitsPerChar,'0') for p in pixel) for pixel in pixels]
       for i in range(len(binaryTriplePairs)):
              for j in range(len(binaryTriplePairs[i])):
                     binaryPixels[i][j] = list(binaryPixels[i][j])
                     binaryPixels[i][j][-1] = binaryTriplePairs[i][j]
                     binaryPixels[i][j] = "".join(binaryPixels[i][j])

       newPixels = [tuple(int(p,2) for p in pixel) for pixel in binaryPixels]
       return newPixels

def encodeLSB(message, imageFilename, newImageFilename):
       img = Image.open(imageFilename)
       size = img.size

       if not canEncode(message, img):
              return None

       binaryTriplePairs = createBinaryTriplePairs(message)

       pixels = list(img.getdata())
       newPixels = embedBitsToPixels(binaryTriplePairs, pixels)

       newImg = Image.new("RGB", size)
       newImg.putdata(newPixels)

       finalFilename = ".".join([newImageFilename,extension])
       newImg.save(finalFilename)

       return newImg

def getLSBsFromPixels(binaryPixels):
       totalZeros = 0
       binList = []
       for binaryPixel in binaryPixels:
              for p in binaryPixel:
                     if p[-1] == '0':
                            totalZeros = totalZeros + 1
                     else:
                            totalZeros = 0
                     binList.append(p[-1])
                     if totalZeros == bitsPerChar:
                            return  binList

def decodeLSB(imageFilename):
       img = Image.open(imageFilename)
       pixels = list(img.getdata())
       binaryPixels = [list(bin(p)[2:].rjust(bitsPerChar,'0') for p in pixel) for pixel in pixels]
       binList = getLSBsFromPixels(binaryPixels)
       message = "".join([chr(int("".join(binList[i:i+bitsPerChar]),2)) for i in range(0,len(binList)-bitsPerChar,bitsPerChar)])
       return message