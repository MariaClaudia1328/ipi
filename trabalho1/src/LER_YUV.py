import numpy as np

def LER_YUV(filePath, width, height, frameNumber):
    
    frameSize = int(width * height * 1.5)

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


