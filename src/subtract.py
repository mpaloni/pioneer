import torch, torchvision
import os
import argparse
from PIL import Image
import PIL.ImageOps
#from utils import normalize

def normalize(x, dim=1):
    '''
    Projects points to a sphere.
    '''
    zn = x.norm(2, dim=dim)
    zn = zn.unsqueeze(1)
    return x.div(zn).expand_as(x)    

def main():
	#define parameters
	parser = argparse.ArgumentParser(description='PIONEER Zeta')
	parser.add_argument('--first', type=str, help='Subject on the left side of the operator')
	parser.add_argument('--second', type=str, help='Subject on the right side of the operator')
	parser.add_argument('--third', type=str, default=None, help='Subject to apply the difference')
	parser.add_argument('--operator', type=str, help='Operator: minus or plus or both or avg')
	parser.add_argument('--source', type=str, default=None, help='Source directory')
	parser.add_argument('--target', type=str, default=None, help='Target directory')
	parser.add_argument('--intensify', type=int, default=None, help='Intensify the effect')
	parser.add_argument('--avg_keyword', type=str, default=None, help='Keyword to count the avg with. All and only files of interest should have this word in their name')

	args=parser.parse_args()
	
	assert(args.operator)
	if args.operator == "avg" or args.operator == "minus" or args.operator == "plus" or args.operator == "both":
		assert(args.source)
	
	if args.operator != "avg" and args.operator != "norm" and args.operator != "flip":
		assert(args.first)
		assert(args.second)

		#get args
		par1=args.first
		par2=args.second
	
	#decide save and load folders
	if args.operator != "scattered_subtraction":
		load_folder=os.path.expanduser(args.source)
		
	if (args.target):
		save_folder=os.path.expanduser(args.target)
	else:
		save_folder=os.path.expanduser(args.source)
		
		
	#load latent presentations
	if args.operator != "avg" and args.operator != "scattered_subtraction" and args.operator != "norm" and args.operator != "flip":
		f1=torch.load(os.path.join(load_folder,par1))
		f2=torch.load(os.path.join(load_folder,par2))

	#decide operation
	if args.operator == "minus":
		f3=torch.sub(f1,f2)
		f3_name = str(par1)+"_minus_"+str(par2)
		torch.save(f3, os.path.join(save_folder,f3_name))

		# f_normalized=normalize(f3)
		# fn_name = str(par1)+" minus "+str(par2)+" normalized_late"
		# torch.save(f_normalized, os.path.join(save_folder,fn_name))

	elif args.operator == "plus":
		f3=torch.add(f1,f2)
		# f3_name = str(par1)+"_plus_"+str(par2)
		f3_name = str(par1).replace("_late","")+"_result_late"
		torch.save(f3, os.path.join(save_folder,f3_name))

		# f_normalized=normalize(f3)
		# fn_name = str(par1)+" plus "+str(par2)+" normalized_late"
		# torch.save(f_normalized, os.path.join(save_folder,fn_name))

	elif args.operator == "both": #this will output latent presentation applied to the selected file
		assert(args.third)
		par3=args.third
		ft=torch.load(os.path.join(load_folder,par3))
		f3_name = str(par3)+ " plus " + str(par1)+ " minus "+str(par2)
		f3=torch.sub(f1,f2)
		if args.intensify:
			for i in range(args.intensify):
				f3=torch.add(f3,ft)
				torch.save(f3, os.path.join(save_folder,f3_name))
			return
		else:
			f3=torch.add(f3,ft)
			torch.save(f3, os.path.join(save_folder,f3_name))
	elif args.operator == "avg": #count average for files which have --args.avg_keyword in their name
		count=0
		sum = torch.Tensor()
		for file in os.listdir(load_folder):
			if args.avg_keyword in file and "png" not in file and "jpg" not in file: #ignore image files
				print("Adding "+str(file)+" to average")
				count=count+1
				if count == 1:
					sum = torch.load(os.path.join(load_folder,file))
				else:
					sum = sum + torch.load(os.path.join(load_folder,file))
					
		sum = sum / count
		torch.save(sum, os.path.join(save_folder,"avg"+str(args.avg_keyword)))
		sum = normalize(sum)
		torch.save(sum, os.path.join(save_folder,"avg normalized "+str(args.avg_keyword)))
		
	elif args.operator == "scattered_subtraction": #take files from two different sources and always subtract file from second location from file from first location
		assert(args.first)
		assert(args.second)
		
		left_list=sorted(os.listdir(os.path.expanduser(args.first)))
		right_list=sorted(os.listdir(os.path.expanduser(args.second)))
		
		left_path=os.path.expanduser(args.first)
		right_path=os.path.expanduser(args.second)
		
		left_list=[l for l in left_list if (l.endswith(".png")==0 and l!="log")]
		right_list=[r for r in right_list if (r.endswith(".png")==0 and r!="log")]
		
		sum = torch.Tensor()
		count=0
		for left_name,right_name in zip(left_list,right_list):
			left_file=torch.load(os.path.join(left_path,left_name))
			right_file=torch.load(os.path.join(right_path,right_name))
			print("Subtracting "+right_name+" from "+left_name)
			result=torch.sub(left_file,right_file)
			if count != 0:
				sum = sum + result
			else:
				sum = result
			count=count+1
			
		print("Saving result in to "+save_folder+" with name scattered_subtraction_late.")
		sum = sum / count
		torch.save(sum, os.path.join(save_folder,"scattered_subtraction_late"))
		# sum = normalize(sum)
		# torch.save(sum, os.path.join(save_folder,"scattered_subtraction_normalized_late"))
		
	elif args.operator == "norm":
		#Normalize the given latent presentation
		par1=args.first
		f1=torch.load(os.path.join(load_folder,par1))
		f3=normalize(f1)
		f3_name = str(par1).replace("late","")+"normalized_late"
		torch.save(f3, os.path.join(save_folder,f3_name))
		
	elif args.operator == "flip":
		#Flip all images in given folder
		for file in os.listdir(load_folder):
			with Image.open(os.path.join(load_folder,file)) as f1:
				#f1=torch.load(os.path.join(load_folder,file))
				#f3 = PIL.ImageOps.invert(f1)
				f3=torchvision.transforms.functional.hflip(f1)
				#f3_name = str(file).replace(".png","")+"_flipped.png"
				f3_name = str(file).replace(".jpg","")+"_flipped.jpg"
				f3.save(os.path.join(save_folder,f3_name))
		
	elif args.operator == "flip_all_ways":
		#Flip first latent presentation with delta in range -1...0...1
		par1=args.first
		f1=torch.load(os.path.join(load_folder,par1))
		par2=args.second
		f2=torch.load(os.path.join(load_folder,par2))
		
		for i in range(-10,21,1):
			#multiply f2 with scalar i
			ii=float(i/10)
			
			a=torch.FloatTensor([ii])
			m=f2*a.cuda().expand_as(f2)
			f3=torch.add(f1,m)
			n=str(i+10)
			f3_name = str(par1).replace("_late","")+"_flipped_"+n.zfill(2)+"_late"
			print(f3_name)
			torch.save(f3, os.path.join(save_folder,f3_name))
		
	else:
		print("Operator erroneously defined")
		raise

	# torch.save(f3, os.path.join(save_folder,f3_name))

main()