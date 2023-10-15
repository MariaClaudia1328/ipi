import numpy as np
import cv2
import sys

def sharpening(image, filterType):

    if(filterType == "-8"):
        laplacianKernel = np.array([[1,1,1],
                                    [1,-8,1],
                                    [1,1,1]])
    elif(filterType == "8"):
        laplacianKernel = np.array([[-1,-1,-1],
                                    [-1,8,-1],
                                    [-1,-1,-1]])
    elif(filterType == "-4"):
        laplacianKernel = np.array([[0,1,0],
                                    [1,-4,1],
                                    [0,1,0]])
    elif(filterType == "4"):
        laplacianKernel = np.array([[0,-1,0],
                                    [-1,4,-1],
                                    [0,-1,0]])
    else:
        print("O tipo de filtro laplaciano pode ser +/-8 ou +/-4")
        exit(1)

    image = cv2.imread(image,cv2.IMREAD_GRAYSCALE)
    laplacianOutput = cv2.filter2D(image, cv2.CV_64F, laplacianKernel)
    
    laplacianOutput = cv2.convertScaleAbs(laplacianOutput)
    laplacianOutput = cv2.add(laplacianOutput, 128)

    if(filterType != "4" and filterType != "-4"):
        cv2.imwrite("../assets/questao2/questao2-1/originalImage.jpg", image)
        cv2.imwrite(f'../assets/questao2/questao2-1/laplacianFilteredImage_{filterType}.jpg', laplacianOutput)
    
    blur = cv2.GaussianBlur(image, (3,3), 0.5)
    laplacianOutput = cv2.filter2D(blur, cv2.CV_64F, laplacianKernel)
    
    laplacianOutput = cv2.convertScaleAbs(laplacianOutput)
    laplacianOutput = cv2.add(laplacianOutput, 128)

    cv2.imwrite(f"../assets/questao2/questao2-2/gaussianBlurAndLaplacian_{filterType}.jpg", laplacianOutput)

    blur = cv2.GaussianBlur(image, (3,3), 1)
    laplacianOutput = cv2.filter2D(blur, cv2.CV_64F, laplacianKernel)
    
    laplacianOutput = cv2.convertScaleAbs(laplacianOutput)
    laplacianOutput = cv2.add(laplacianOutput, 128)

    cv2.imwrite(f"../assets/questao2/questao2-3/gaussianBlurAndLaplacian_{filterType}.jpg", laplacianOutput)

    return

if(len(sys.argv) < 3):
    print("Executar programa com nome do arquivo e qual o tipo do filtro Laplaciano.")
    exit(1)

# Coleta de resultados
sharpening(sys.argv[1], sys.argv[2])