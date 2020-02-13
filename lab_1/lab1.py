from PIL import Image
from PIL import ImageFilter
import numpy as np
from matplotlib import pyplot as plt

im = Image.open('sample.jpg')

a = np.zeros((3,3))
a[1,1] = 1

b = np.ones((3,3))

c = np.zeros((3,3))
c[1,0], c[1,2] = -1, 1

d = np.array([[0.003,0.013,0.022,0.013,0.003],
             [0.013,0.059,0.097,0.059,0.013],
             [0.022,0.097,0.159,0.097,0.022],
             [0.013,0.059,0.097,0.059,0.013],
             [0.003,0.013,0.022,0.013,0.003]])

e = np.zeros((5,5))
e[1:4,1:4] = a
alpha = 0.9 + 1
e = e * alpha - d

f = np.zeros((5,5))
f[1:4,1:4] = c
f = f * d

def check_range(x): return (np.min(x), np.max(x))

def convolve(image, kernel, kernel_name, div = 1):
    
    # get the pixel values
    pixels = np.array(image)
#     print(check_range(pixels))

    # this assumes the kernel is square
    to_remove = 4 if kernel.shape[0] == 5 else 2
    
    # how much subset of the image to take at a time eg 3*3
    size = kernel.shape[0]
    
    # initialize a canvas for the output with 0s. We will fill values in this
    output = np.zeros((pixels.shape[0] - to_remove, pixels.shape[1] - to_remove, pixels.shape[2]))
    for ch in range(pixels.shape[2]):
        for j in range(pixels.shape[1] - to_remove):
            for i in range(pixels.shape[0] - to_remove):
                output[i][j][ch] = np.sum(kernel * pixels[i:i+size, j:j+size, ch]) / div
#     print(check_range(output))
    if check_range(output)[0] < 0:
        np.clip(output, 0, 255, out=output)
    result = Image.fromarray(output.astype('uint8'))
    result.save(kernel_name + ".jpg")
#     image.show()
#     result.show()

convolve(im, a, "Identity")
convolve(im, b, "Box blur", 9)
convolve(im, c, "Horizontal derivative")
convolve(im, d, "Gaussian")
convolve(im, e, "Sharpening")
convolve(im, f, "Derivative of Gaussian")