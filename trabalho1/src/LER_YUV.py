import numpy as np

def LER_YUV(filePath, width, height, frameNumber):
    
    # frame_size = (width * height) + (width // 2) * (height // 2) * 2
    frameSize = int(width * height * 3 / 2)

    # Read the .yuv file into a NumPy array
    with open(filePath, 'rb') as file:

        # Jump to the location given from the beginning of the file
        bytesToSkip = frameNumber * width * height
        file.seek(bytesToSkip, 0 )

        yuvData = file.read(frameSize)

        ySize = width * height
        uvSize = ySize // 4

        Y = yuvData[:ySize]
        U = yuvData[ySize:ySize+uvSize]
        V = yuvData[ySize + uvSize:]

        Y = np.frombuffer(Y, dtype=np.uint8).reshape(height, width)
        U = np.frombuffer(U, dtype=np.uint8).reshape(height//2, width//2)
        V = np.frombuffer(V, dtype=np.uint8).reshape(height//2, width//2)

    return [Y,U,V]

[Y,U,V] = LER_YUV("foreman.yuv", 358, 288, 10)


def resize2hw (image):
    newImageHeight = image.height*2
    newImageWidth = image.width*2

    newImage = np.zeros((newImageWidth, newImageHeight))

    # copia a primeira coluna pra newImage 
        # pula pra coluna de newImage + 2
    
    # copia a primeira linha pra newImage
        # pula pra linha de newImage + 2


def fillWithImmediates (image):
    # percorre todo newImage e subtitui os pixels pretos (valor = 0)
    return

def fillWithAvarage (image):
    return



