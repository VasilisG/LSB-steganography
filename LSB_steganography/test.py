import LsbSteg

message = "This is a hidden text in an image"

imageFilename = "stars_background.jpg"
newImageFilename = "stego_stars_background"

newImg = LsbSteg.encodeLSB(message, imageFilename, newImageFilename)
if not newImg is None:
        print("Stego image created.")

print("Decoding...")
message = LsbSteg.decodeLSB("stego_stars_background.png")
print("Final message: ", message)
