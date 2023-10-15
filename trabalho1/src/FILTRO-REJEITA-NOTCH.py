import numpy as np
import cv2
from matplotlib import pyplot as plt
import sys

def getFshift (img):
    
    f = np.fft.fft2(img)
    fshift = np.fft.fftshift(f)
    phase_spectrumR = np.angle(fshift)
    magnitudeSpectrum = 20 * np.log(np.abs(fshift))

    return fshift, magnitudeSpectrum, phase_spectrumR


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
    print("Executar programa com nome do arquivo.")
    exit(1)

img = cv2.imread(sys.argv[1], cv2.IMREAD_GRAYSCALE)

f = np.fft.fft2(img)
fshift = np.fft.fftshift(f)
phase_spectrum = np.angle(fshift)
magnitude_spectrum = 20*np.log(np.abs(fshift))

H1 = notchRejectFilter(img.shape, 10, 39, 30 )
H2 = notchRejectFilter(img.shape, 10, -39, 30 )
H3 = notchRejectFilter(img.shape, 5, 78, 30 )
H4 = notchRejectFilter(img.shape, 5, -78, 30 )

NotchFilter = H1*H2*H3*H4
NotchRejectCenter = fshift * NotchFilter
NotchReject = np.fft.ifftshift(NotchRejectCenter)
inverse_NotchReject = np.fft.ifft2(NotchReject)

Result = np.abs(inverse_NotchReject)

plt.figure()
plt.imshow(img, cmap='gray')
plt.title('Original')
plt.savefig("../assets/questao3/questao3-1/original.jpg")

plt.figure()
plt.imshow(magnitude_spectrum, cmap='gray')
plt.title('Magnitude Spectrum')
plt.savefig("../assets/questao3/questao3-2/magnitude_spectrum.jpg")

plt.figure()
plt.imshow(magnitude_spectrum*NotchFilter, "gray") 
plt.title("Notch Reject Filter")
plt.savefig("../assets/questao3/questao3-2/filter.jpg")

plt.figure()
plt.imshow(Result, "gray") 
plt.title("Result")
plt.savefig("../assets/questao3/questao3-2/result.jpg")

