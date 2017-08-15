import os
import LsbSteg

message = "This is a test message to be embedded in an image."
imageName = "stars_background.jpg"
stegoImageName = "stego_stars_background.png"

imageWorkingDirectory = os.getcwd() + "\\" + imageName
stegoImageWorkingDirectory = os.getcwd() + "\\" + stegoImageName

LsbSteg.embedMessage(imageWorkingDirectory, stegoImageWorkingDirectory, message)

stegoMessage = LsbSteg.extractMessage(stegoImageWorkingDirectory)

print(stegoMessage)
