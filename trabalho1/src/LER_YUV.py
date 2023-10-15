import numpy as np
import cv2
import sys

def LER_YUV(filePath, width, height, frameNumber):
    
    # frameSize = (width * height) + (width // 2) * (height // 2) * 2
    frameSize = int(width * height * 3 / 2)

    # Lê o arquivo e processa Y, U e V
    with open(filePath, 'rb') as file:

        # Salta para posição dada a partir do começo do arquivo
        bytesToSkip = frameNumber * width * height
        file.seek(bytesToSkip, 0)
        yuvData = np.fromfile(file, dtype=np.uint8, count = frameSize)

        # Calcula tamanho de Y, U e V
        ySize = width * height
        uvSize = ySize // 4

        # Separa Y, U e V
        Y = yuvData[:ySize].reshape(height, width)
        U = yuvData[ySize:ySize+uvSize].reshape(height//2, width//2)
        V = yuvData[ySize + uvSize:].reshape(height//2, width//2)

    return [Y,U,V]

# Redimensiona altura e largura da imagem em múltiplo de 2
def resize2hw (image, newSize):

    # Calcula tamanhos da imagem a ser redimensionada
    imageHeight = image.shape[0]
    imageWidth = image.shape[1]

    # Cria nova imagem com o tamanho escolhido, com todos os pixels pretos
    newImageHeight = imageHeight*2*newSize
    newImageWidth = imageWidth*2*newSize
    newImage = np.zeros((newImageHeight, newImageWidth), dtype=np.uint8)

    # Preenche nova imagem pixel a pixel, saltando uma coluna e uma linha
    l = 0
    m = 0
    for i in range(0,imageHeight):
        for j in range(0,imageWidth):
            newImage[l][m] = image[i][j]
            m += 2
        l += 2
        m = 0
        
    return newImage

# Preenche pixels pretos com pixels imediatos à esquerda ou superiores
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

# Preenche pixels pretos com a média dos pixels que não são pretos
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

# Uso das funções criadas acima

#RESULTADOS

#QUESTAO 1.1
# Extrai Y,U e V de arquivo de video

if(len(sys.argv) < 5):
    print("Executar programa com nome do arquivo, largura, altura e numero do quadro.")
    exit(1)

[Y,U,V] = LER_YUV(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))

originalY = Y
originalU = U
originalV = V

cv2.imwrite("../assets/questao1/questao1-1/originalY.jpg", originalY)
cv2.imwrite("../assets/questao1/questao1-1/originalU.jpg", originalU)
cv2.imwrite("../assets/questao1/questao1-1/originalV.jpg", originalV)

originalU = np.repeat(originalU, 2, axis=0)
originalU = np.repeat(originalU, 2, axis=1)
originalV = np.repeat(originalV, 2, axis=0)
originalV = np.repeat(originalV, 2, axis=1)

yuvOriginal = np.stack((originalY,originalV,originalU), axis = -1)
bgrImage = cv2.cvtColor(yuvOriginal, cv2.COLOR_YCR_CB2BGR)
cv2.imwrite("../assets/questao1/questao1-1/YUV_Original_Image.jpg", bgrImage)

# Transforma U e V para mesmo tamanho de Y
newU = resize2hw(U, 1)
newV = resize2hw(V, 1)

#QUESTAO 1.2
cv2.imwrite("../assets/questao1/questao1-2/Resized_U.jpg", newU)
cv2.imwrite("../assets/questao1/questao1-2/Resized_V.jpg", newV)

# Preenche pixels de U e V com média
newU_avg = fillWithAvarage(newU)
newV_avg = fillWithAvarage(newV)

# Preenche pixels de U e V com imediatos
newU_imm = fillWithImmediates(newU)
newV_imm = fillWithImmediates(newV)

#QUESTAO 1.3 e 1.4
# Utiliza preenchimento dos pixels pretos com a média para criar nova imagem
mergedYUV_avg = cv2.merge([Y, newV_avg, newU_avg])
bgrImage_avg = cv2.cvtColor(mergedYUV_avg, cv2.COLOR_YCrCb2BGR)
cv2.imwrite("../assets/questao1/questao1-3/newU_Image_(U_and_V_resized)_[Avarage].jpg", newU_avg)
cv2.imwrite("../assets/questao1/questao1-3/newV_Image_(U_and_V_resized)_[Avarage].jpg", newV_avg)
cv2.imwrite("../assets/questao1/questao1-3/YUV_Image_(U_and_V_resized)_[Avarage].jpg", bgrImage_avg)
cv2.imwrite("../assets/questao1/questao1-4/YUV_Image_(U_and_V_resized)_[Avarage].jpg", bgrImage_avg)

# Utiliza preenchimento dos pixels pretos com imediatos para criar nova imagem
mergedYUV_imm = cv2.merge([Y, newV_imm, newU_imm])
bgrImage_imm = cv2.cvtColor(mergedYUV_imm, cv2.COLOR_YCrCb2BGR)
cv2.imwrite("../assets/questao1/questao1-2/newU_Image_(U_and_V_resized)_[Immediate].jpg", newU_imm)
cv2.imwrite("../assets/questao1/questao1-2/newV_Image_(U_and_V_resized)_[Immediate].jpg", newV_imm)
cv2.imwrite("../assets/questao1/questao1-2/YUV_Image_(U_and_V_resized)_[Immediate].jpg", bgrImage_imm)
cv2.imwrite("../assets/questao1/questao1-4/YUV_Image_(U_and_V_resized)_[Immediate].jpg", bgrImage_imm)

originalY = Y
originalU = U
originalV = V

#QUESTAO 1.5
# Duplica o tamanho de Y, U e V 
originalY_2x = resize2hw(originalY, 1)
originalU_2x = resize2hw(originalU, 1)
originalV_2x = resize2hw(originalV, 1)

# Preenche os pixels pretos com os imediatos 
originalY_2x_imm = fillWithImmediates(originalY_2x)
originalU_2x_imm = fillWithImmediates(originalU_2x)
originalV_2x_imm = fillWithImmediates(originalV_2x)

# Faz um 'upsampling' de U e V para que fiquem no mesmo
# formato que Y e assim, podemos converter a imagem YUV
# para RGB
originalU_2x_imm = np.repeat(originalU_2x_imm, 2, axis=0)
originalU_2x_imm = np.repeat(originalU_2x_imm, 2, axis=1)
originalV_2x_imm = np.repeat(originalV_2x_imm, 2, axis=0)
originalV_2x_imm = np.repeat(originalV_2x_imm, 2, axis=1)

# Mostra imagem YUV com o dobro do tamanho no formato 4:2:0

# Utiliza preenchimento dos pixels pretos com imediatos para criar nova imagem
yuv2x_imm = np.stack((originalY_2x_imm, originalV_2x_imm, originalU_2x_imm), axis = -1)
bgr2x_imm = cv2.cvtColor(yuv2x_imm, cv2.COLOR_YCR_CB2BGR)
cv2.imwrite("../assets/questao1/questao1-5/Y_Resized_by_2_[Immediate].jpg", originalY_2x_imm)
cv2.imwrite("../assets/questao1/questao1-5/U_Resized_by_2_[Immediate].jpg", originalU_2x_imm)
cv2.imwrite("../assets/questao1/questao1-5/V_Resized_by_2_[Immediate].jpg", originalV_2x_imm)
cv2.imwrite("../assets/questao1/questao1-5/YUV_Resized_by_2_[Immediate].jpg", bgr2x_imm)

# Preenche os pixels pretos com a média 
originalY_2x_avg = fillWithAvarage(originalY_2x)
originalU_2x_avg = fillWithAvarage(originalU_2x)
originalV_2x_avg = fillWithAvarage(originalV_2x)

originalU_2x_avg = np.repeat(originalU_2x_avg, 2, axis=0)
originalU_2x_avg = np.repeat(originalU_2x_avg, 2, axis=1)
originalV_2x_avg = np.repeat(originalV_2x_avg, 2, axis=0)
originalV_2x_avg = np.repeat(originalV_2x_avg, 2, axis=1)

# Utiliza preenchimento dos pixels pretos com media para criar nova imagem
yuv2x_avg = np.stack((originalY_2x_avg, originalV_2x_avg, originalU_2x_avg), axis = -1)
bgr2x_avg = cv2.cvtColor(yuv2x_avg, cv2.COLOR_YCR_CB2BGR)
cv2.imwrite("../assets/questao1/questao1-5/Y_Resized_by_2_[Avarage].jpg", originalY_2x_avg)
cv2.imwrite("../assets/questao1/questao1-5/U_Resized_by_2_[Avarage].jpg", originalU_2x_avg)
cv2.imwrite("../assets/questao1/questao1-5/V_Resized_by_2_[Avarage].jpg", originalV_2x_avg)
cv2.imwrite("../assets/questao1/questao1-5/YUV_Resized_by_2_[Avarage].jpg", bgr2x_avg)



