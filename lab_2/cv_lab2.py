from PIL import Image, ImageDraw
import numpy as np
from scipy import fftpack
import imageio

def display_np(x):
	"""
	Display a numpy array as an image
	"""
	result = Image.fromarray(x.astype('uint8'))
	result.show()

def read_image(x):
	x = Image.open(x).convert("L")
	x = np.array(x)
	return x

def filter_im(im, high = False, radius = 70):
	eX, eY = radius, radius
	x, y = im.shape[1], im.shape[0]
	bbox = (x/2 - eX/2, y/2 - eY/2, x/2 + eX/2, y/2 + eY/2)

	color = 255 if not high else 0
	fill  = 0 if not high else 255
	fpass = Image.new("L", (im.shape[1], im.shape[0]), color=color) 
	draw = ImageDraw.Draw(fpass)
	draw.ellipse(bbox, fill=fill)
	return np.array(fpass)

def join_im(f1, f2, im1, im2):
	assert im1.shape == im2.shape

	canvas = np.full(im1.shape, 255, dtype = complex)
	for i in range(im1.shape[0]):
	    for j in range(im1.shape[1]):
	        if f1[i,j] == 0: canvas[i,j] = im1[i,j]
	        else: canvas[i,j] = im2[i,j]
	return canvas

plane = read_image('plane2.png')
pilot = read_image("pilot.jpg")

r,c = 100,425
plane = plane[r:r + 470, c: c + 299]

assert plane.shape == pilot.shape

pilot_fft = fftpack.fftshift(fftpack.fft2(pilot))
plane_fft = fftpack.fftshift(fftpack.fft2(plane))

imageio.imsave('pilot_fft.png', (np.log(abs(pilot_fft))* 255 /np.amax(np.log(abs(pilot_fft)))).astype(np.uint8))
imageio.imsave('plane_fft.png', (np.log(abs(plane_fft))* 255 /np.amax(np.log(abs(plane_fft)))).astype(np.uint8))

pilot_im = read_image('pilot_fft.png')
plane_im = read_image('plane_fft.png')

pilot_low = filter_im(pilot_im)
pilot_high = filter_im(pilot_im, True)

plane_low = filter_im(plane_im)
plane_high = filter_im(plane_im, True)

pp1 = join_im(pilot_low, plane_high, pilot_fft, plane_fft)
pp2 = join_im(pilot_high, plane_low, pilot_fft, plane_fft)


ifft1 = abs(fftpack.ifft2(fftpack.ifftshift(pp1)))
ifft2 = abs(fftpack.ifft2(fftpack.ifftshift(pp2)))

imageio.imsave('plane_and_pilot.png', ifft1.astype(np.uint8))
imageio.imsave('pilot_and_plane.png', ifft2.astype(np.uint8))