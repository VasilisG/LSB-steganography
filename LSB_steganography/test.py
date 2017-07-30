import os
import lsbSteg

message = "This is a test message to be embedded in an image."
imageName = "stars_background.jpg"
stegoImageName = "stego_stars_background.png"

imageWorkingDirectory = os.getcwd()
imageWorkingDirectory = workingDirectory + "\\" + imageName

stegoImageWorkingDirectory = os.getcwd()
stegoImageWorkingDirectory = stegoImageWorkingDirectory + "\\" + stegoImageName

lsbSteg.embedMessage(imageWorkingDirectory, stegoImageWorkingDirectory, message)

stegoMessage = lsbSteg.extractMessage(stegoImageWorkingDirectory)

print(stegoMessage)
