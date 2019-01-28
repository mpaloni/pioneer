import sys, os
from PIL import Image

def combined(dir_path, specifier=""):
	images=[]
	for img_name in sorted(os.listdir(dir_path),reverse=True):
		if (img_name.endswith(specifier+".png") or img_name.endswith(specifier+".jpg")):
			img_path=os.path.join(dir_path, img_name)
			images.append(Image.open(img_path))

	widths, heights = zip(*(i.size for i in images))

	total_width = sum(widths)
	max_height = max(heights)

	new_im = Image.new('RGB', (total_width, max_height))

	x_offset = 0
	for im in images:
		new_im.paste(im, (x_offset,0))
		print(im)
		x_offset += im.size[0]

	new_im.save(dir_path+specifier+'combined.png')
	print("Saved to "+dir_path+specifier+'combined.png')
	
def stacked(dir_path):
	#Add X images on top of eachother, assume same size
	images=[]
	# print(sorted(os.listdir(dir_path),reverse=False))
	for img_name in sorted(os.listdir(dir_path),reverse=False):
		if "combined" in img_name:
			img_path=os.path.join(dir_path, img_name)
			images.append(Image.open(img_path))
			
	widths, heights = zip(*(i.size for i in images))

	total_width = max(widths)
	max_height = sum(heights)

	new_im = Image.new('RGB', (total_width, max_height))

	y_offset = 0
	for im in images:
		new_im.paste(im, (0,y_offset))
		print(im)
		y_offset += im.size[1]

	new_im.save(dir_path+'stacked.png')
	print("Saved to "+dir_path+'stacked.png')

import imageio
def makeGIF(dir_path):
	images = []
	for filename in sorted(os.listdir(dir_path),reverse=False):
		if filename.endswith(".png"):
			images.append(imageio.imread(os.path.join(dir_path,filename)))
	gif_path=os.path.join(dir_path, "combined.gif")
	imageio.mimsave(gif_path, images)
	print(gif_path)
	
def makeMP4(dir_path):
	images = []
	for filename in sorted(os.listdir(dir_path),reverse=False):
		if filename.endswith(".png"):
			images.append(imageio.imread(os.path.join(dir_path,filename)))
	gif_path=os.path.join(dir_path, "combined.mp4")
	imageio.mimsave(gif_path, images)
	print(gif_path)
	
dir_path=sys.argv[1]
print("Params "+str(len(sys.argv)))
if len(sys.argv)==3:
	if(sys.argv[2]=='stacked'):
		print("Stacking images")
		stacked(dir_path)
	elif(sys.argv[2]=='gif'):
		print("GIF")
		makeGIF(dir_path)
	elif(sys.argv[2]=='mp4'):
		print("MP4")
		makeMP4(dir_path)
	else:
		specifier=sys.argv[2]
		print("Specifier is ",specifier)
		combined(dir_path,specifier)
else:
	print("Else combine")
	combined(dir_path)
# stacked(dir_path)
