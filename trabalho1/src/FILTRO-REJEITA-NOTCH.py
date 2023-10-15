import numpy as np
import cv2
from matplotlib import pyplot as plt
import sys

def notchRejectFilter(shape, D0, uk, vk):
    P, Q = shape

    H = np.zeros((P,Q))

    for u in range(P):
        for v in range(Q):
            d1 = np.sqrt((u - P / 2 + uk)**2 + (v - Q/2 + vk) ** 2)
            d2 = np.sqrt((u - P / 2 - uk)**2 + (v - Q/2 - vk) ** 2)
            
            if d1 <= D0 or d2 <= D0:
                H[u,v] = 0.0
            else:
                H[u,v] = 1.0

    return H

if(len(sys.argv) < 2):
    print("Executar programa com nome do arquivo de imagem.")
    exit(1)

image = cv2.imread(sys.argv[1], cv2.IMREAD_GRAYSCALE)

f = np.fft.fft2(image)
fshift = np.fft.fftshift(f)
magnitudeSpectrum = 20*np.log(np.abs(fshift))

H1 = notchRejectFilter(image.shape, 10, 39, 30 )
H2 = notchRejectFilter(image.shape, 10, -39, 30 )
H3 = notchRejectFilter(image.shape, 5, 78, 30 )
H4 = notchRejectFilter(image.shape, 5, -78, 30 )

NotchFilter = H1*H2*H3*H4
imageFiltered = fshift * NotchFilter
imageFiltered_ishift = np.fft.ifftshift(imageFiltered)
imageFiltered_inversef = np.fft.ifft2(imageFiltered_ishift)

finalImage = np.abs(imageFiltered_inversef)

plt.figure()
plt.imshow(image, cmap='gray')
plt.title('Original')
plt.savefig("../assets/questao3/questao3-1/original.jpg")

plt.figure()
plt.imshow(magnitudeSpectrum, cmap='gray')
plt.title('Magnitude Spectrum')
plt.savefig("../assets/questao3/questao3-2/magnitude_spectrum.jpg")

plt.figure()
plt.imshow(magnitudeSpectrum*NotchFilter, "gray") 
plt.title("Notch Reject Filter")
plt.savefig("../assets/questao3/questao3-2/filter.jpg")

plt.figure()
plt.imshow(finalImage, "gray") 
plt.title("Result")
plt.savefig("../assets/questao3/questao3-2/result.jpg")

