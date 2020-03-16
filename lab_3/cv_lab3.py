from PIL import Image, ImageDraw
import numpy as np
import copy
import imageio

# the functions in this lab are taken from CV Assignment 1
def display_np(*imgs):
	for im in imgs:
	    result = Image.fromarray(im.astype('uint8'))
	    result.show()

def check_range(*x): 
	for x_ in x:
	    print(np.min(x_), np.max(x_))

def read_image(x, mode = None):
	x = Image.open(x).convert(mode)
	x = np.array(x)
	return x

def normalize(input_im): 
	base = input_im.min() 
	roof = input_im.max() 
	diff = roof - base 
	scale = diff /255

	input_im = input_im - base 
	output = input_im/scale
	return output

def conv1d(image, kernel, order = 'C', div = 1, norm = True):
	im = copy.deepcopy(image.flatten())
	k = copy.deepcopy(kernel.flatten(order = order))

	size = len(k)
	to_remove = len(k) - 1

	output = np.full((im.shape), 255)
	for i in range(len(im) - to_remove):
	    output[i] = np.sum(k * im[i:i+size]) / div
	output = output.reshape(image.shape)
	if norm: output = normalize(output)
	return output

def conv2d(image, kernel, div = 1, norm = True):
	# number of rows and columns of the kernel
	r = kernel.shape[0]
	c = kernel.shape[1]

	# initialize a canvas for the output with 255s. We will fill values in this
	output = np.full(image.shape, 255)
	for i in range(image.shape[0] - r - 1):
	    for j in range(image.shape[1] - c - 1):
	        output[i][j] = np.sum(kernel * image[i:i+r, j:j+c]) / div
	if norm: output = normalize(output)
	return output


im = read_image('trial_2.png', 'L')
# display_np(im)

dx = np.array([-1, 1])

Ix = conv1d(im, dx)
Iy = conv1d(im.T, dx).T

# display_np(Ix, Iy)

Ix2 = normalize(Ix * Ix)
Ixy = normalize(Ix * Iy)
Iy2 = normalize(Iy * Iy)

imageio.imsave('Ix.png',Ix)
imageio.imsave('Iy.png',Iy)
imageio.imsave('Ix2.png',Ix2)
imageio.imsave('Ixy.png',Ixy)
imageio.imsave('Iy2.png',Iy2)

# display_np(Ix2, Ixy, Iy2)

b = np.ones((3,3))

Aw = conv2d(Ix2, b)
Bw = conv2d(Ixy, b)
Cw = conv2d(Iy2, b)

T = 5.3
op_img = Image.open('trial_2.png')
draw = ImageDraw.Draw(op_img)
for i in range(im.shape[0]):
    for j in range(im.shape[1]):
        eigv, eigvec = np.linalg.eig(np.array([[Aw[i,j], Bw[i,j]],
                                               [Bw[i,j], Cw[i,j]]]))
        m = min(eigv)
        if m > T:
            draw.line(((j-5,i) ,(j+5,i)), fill =(255,0,0))
            draw.line(((j,i-5),(j,i+5)), fill=(255,0,0))
op_img.show()
op_img.save('output.png')