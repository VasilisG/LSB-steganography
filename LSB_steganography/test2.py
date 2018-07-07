import LsbFileSteg

filename = "test.txt"
imageName = "E:\\My images\\Random images\\stars_background.png"
newFilename = "E:\\My images\\Random images\\stego_stars_background.png"
decodedFilename = "decodedFile"

print("Encoding...")
img = LsbFileSteg.encodeLSB(filename, imageName, newFilename)
print("Encoding finished.")

print("Decoding...")
LsbFileSteg.decodeLSB(newFilename, decodedFilename)
print("Decoding finished.")