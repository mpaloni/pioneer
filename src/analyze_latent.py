import torch, torchvision
import os
import argparse

def main():
	parser = argparse.ArgumentParser(description='PIONEER Zeta')
	parser.add_argument('--first', type=str, help='Subject on the left side of the operator')
	
	args=parser.parse_args()
	
	f1=torch.load(os.path.expanduser(args.first))
	#First is the file to be analyzed
	
	#calculate sum
	sum=torch.sum(f1)
	#avg
	avg=torch.mean(f1)
	#min
	min=torch.min(f1)
	#max
	max=torch.max(f1)
	
	print("Sum: ", sum)
	print("Avg: ", avg)
	print("Min: ", min)
	print("Max: ", max)
	
main()
