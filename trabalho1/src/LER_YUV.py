import numpy as np
import cv2

def LER_YUV(filePath, width, height, frameNumber):
    
    # frame_size = (width * height) + (width // 2) * (height // 2) * 2
    frameSize = int(width * height * 3 / 2)

    # Read the .yuv file into a NumPy array
    with open(filePath, 'rb') as file:

        # Jump to the location given from the beginning of the file
        bytesToSkip = frameNumber * width * height
        file.seek(bytesToSkip, 0 )

        yuvData = np.fromfile(file, dtype=np.uint8, count = frameSize)

        ySize = width * height
        uvSize = ySize // 4

        Y = yuvData[:ySize].reshape(height, width)
        U = yuvData[ySize:ySize+uvSize].reshape(height//2, width//2)
        V = yuvData[ySize + uvSize:].reshape(height//2, width//2)

    return [Y,U,V]


def resize2hw (image, newSize):

    imageHeight = image.shape[0]
    imageWidth = image.shape[1]

    newImageHeight = imageHeight*2*newSize
    newImageWidth = imageWidth*2*newSize

    newImage = np.zeros((newImageHeight, newImageWidth), dtype=np.uint8)

    l = 0
    m = 0
    for i in range(0,imageHeight):
        for j in range(0,imageWidth):
            newImage[l][m] = image[i][j]
            m += 2
        l += 2
        m = 0
        
    return newImage

def fillWithImmediates (imageIn):
    image = imageIn.copy()
    imageHeight = image.shape[0]
    imageWidth = image.shape[1]

    for i in range(0,imageHeight):
        for j in range(0,imageWidth):
            if(np.all(image[i][j] != 0)): continue
            
            if(i != 0): 
                image[i][j] = image[i-1][j]
            else:
                image[i][j] = image[i][j-1]
    return image

def fillWithAvarage (imageIn):
    image = imageIn.copy()
    imageHeight = image.shape[0]
    imageWidth = image.shape[1]

    
    for i in range(0,imageHeight):
        for j in range(0,imageWidth):
            if(np.all(image[i][j] != 0)): continue

            if(i%2 == 0):
                if(j+1 >= imageWidth):
                    image[i][j] = image[i][j-1]
                else:
                    image[i][j] = (np.uint16(image[i][j-1]) + np.uint16(image[i][j+1] )) / 2
            elif(j%2 == 0):
                if(i+1 >= imageHeight):
                    image[i][j] = image[i-1][j]
                else:
                    image[i][j] = (np.uint16(image[i-1][j]) + np.uint16(image[i+1][j] )) / 2
            else:
                if(i+1 >= imageHeight and j+1 >= imageWidth):
                    image[i][j] = image[i-1][j-1]
                elif(i+1 >= imageHeight):
                    image[i][j] = (np.uint16(image[i-1][j-1]) + np.uint16(image[i-1][j+1] )) / 2
                elif(j+1 >= imageWidth):
                    image[i][j] = (np.uint16(image[i-1][j-1]) + np.uint16(image[i+1][j-1] )) / 2
                else:
                    image[i][j] = (np.uint16(image[i-1][j-1]) + np.uint16(image[i+1][j+1]) + np.uint16(image[i-1][j+1]) + np.uint16(image[i+1][j-1])) / 4
    return image

[Y,U,V] = LER_YUV("foreman.yuv", 352, 288, 15)


originalY = Y
originalU = U
originalV = V

originalY = resize2hw(originalY, 1)
originalU = resize2hw(originalU, 1)
originalV = resize2hw(originalV, 1)

originalY = fillWithAvarage(originalY)
originalU = fillWithAvarage(originalU)
originalV = fillWithAvarage(originalV)

originalU = np.repeat(originalU, 2, axis=0)
originalU = np.repeat(originalU, 2, axis=1)
originalV = np.repeat(originalV, 2, axis=0)
originalV = np.repeat(originalV, 2, axis=1)

yuvOriginal = np.stack((originalY,originalV,originalU), axis = -1)
bgr_image = cv2.cvtColor(yuvOriginal, cv2.COLOR_YCR_CB2BGR)
cv2.imshow('YUV Original Image', bgr_image)

newU = resize2hw(U, 1)
newV = resize2hw(V, 1)

newU = fillWithAvarage(newU)
newV = fillWithAvarage(newV)

mergedYUV = cv2.merge([Y, newV, newU])
print(mergedYUV.shape)
bgr_image = cv2.cvtColor(mergedYUV, cv2.COLOR_YCrCb2BGR)

cv2.imshow('YUV Image', bgr_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

