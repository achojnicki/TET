from random import randint
from PIL import Image
import numpy as np


def generate_noise_array(x,y):
	data=[]
	for _x in range(0, x):
		data.append([])
		for _y in range(0, y):
			r=randint(0,255)
			data[_x].append([r,r,r])

	data=np.array(data, dtype=np.uint8)
	data.reshape(x,y,3)
	return data



base_image = Image.fromarray(generate_noise_array(200,200)).convert('RGB')
frames=[]
for frame in range(5):
	frames.append(Image.fromarray(generate_noise_array(200,200)).convert('RGB'))

base_image.save("noise.gif", save_all=True, append_images=frames, duration=10, loop=0)

