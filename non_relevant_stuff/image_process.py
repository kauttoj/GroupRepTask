# process images generated by https://this-person-does-not-exist.com/en

from PIL import Image, ImageChops, ImageOps,ImageDraw
import glob

from PIL import ImageFont


ROOT = r'C:\Code\GroupRepTask\non_relevant_stuff'"\\"
newsize_agent = (150,200)
newsize_task = (240,360) # width,height

def process_image(f_in,f_out,newsize,text=(None,'G')):
	im = Image.open(f_in)
	target_aspect = newsize[0]/newsize[1]
	width, height = im.size[0], im.size[1]
	current_aspect = width/height
	if current_aspect>target_aspect:
		width_cut =  width - target_aspect*height
		left = round(width_cut/2)
		top = height
		right = round(width-width_cut/2)
		bottom = 0
		# Cropped image of above dimension
		# (It will not change original image)
		im1 = im.crop((left, bottom, right, top)) # (left, upper, right, lower)
	else:
		height_cut = (-width+target_aspect*height)/target_aspect
		top = round(height_cut / 2)
		left = 0
		right = width
		bottom = round(height - height_cut / 2)
		# Cropped image of above dimension
		# (It will not change original image)
		im1 = im.crop((left, top, right,bottom))  # (left, upper, right, lower)

	im1 = im1.resize(newsize)

	if text[0] is not None:
		myFont = ImageFont.truetype("arial.ttf",300)
		w, h = myFont.getsize(text[0])
		I1 = ImageDraw.Draw(im1)
		if text[1]=='G':
			I1.text((im1.size[0]/2 -w/2,im1.size[1]/2-h/2),text[0],font=myFont,fill=(0,255, 0))
		else:
			I1.text((im1.size[0]/2 -w/2,im1.size[1]/2-h/2), text[0],font=myFont,fill=(255, 0, 0))

	im1.save(f_out)

for gender in ['female','male']:
	res = glob.glob(ROOT + r'\random_%s\*.jpg' % gender)
	for k,im in enumerate(res):
		new_file = ROOT + r'random_%s\resized\%sface%i.jpg' % (gender,gender,k+1)
		process_image(
			im,
			new_file,newsize_agent)

for k,typ in enumerate(['xes','oes']):
	res = glob.glob(ROOT + r'\tasks\*.jpg') +glob.glob(ROOT + r'\tasks\*.png')
	res*=2
	for k,im in enumerate(res):
		new_file = ROOT + r'tasks\%s\filename%i.jpg' % (typ,k+1)
		process_image(
			im,
			new_file,newsize_task,
			text=('X','R') if typ=='xes' else ('o','G')
		)


print('done!')
	