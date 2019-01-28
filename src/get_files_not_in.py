
import os
import argparse
import csv
import shutil


def main():
	print("Started")
	#define parameters
	# parser = argparse.ArgumentParser(description='PIONEER Zeta')
	# parser.add_argument('--first', type=str, help='Subject on the left side of the operator')
	# parser.add_argument('--second', type=str, help='Subject on the right side of the operator')
	# parser.add_argument('--third', type=str, default=None, help='Subject to apply the difference')
	# parser.add_argument('--operator', type=str, help='Operator: minus or plus or both or avg')
	# parser.add_argument('--source', type=str, default=None, help='Source directory')
	# parser.add_argument('--target', type=str, default=None, help='Target directory')
	# parser.add_argument('--intensify', type=str, default=None, help='Intensify the effect')
	# parser.add_argument('--avg_keyword', type=str, default=None, help='Keyword to count the avg with. All and only files of interest should have this word in their name')

	# args=parser.parse_args()
	

	csv_path=os.path.expanduser("~/dippa/glasses.csv")
	source=os.path.expanduser("~/dippa/img_align_celeba")
	target=os.path.expanduser("~/dippa/celeba_noglasses/img")
	
	src_files = os.listdir(source)
	glasses=[]
	with open(csv_path, 'r') as csvfile:
		reader = csv.reader(csvfile, delimiter=',', quotechar='|')
		for row in reader:
			glasses.append(', '.join(row).replace('"', ''))
			
	src_files = os.listdir(source)
	for file_name in src_files:   
		full_file_name = os.path.join(source, file_name)
		if (file_name not in glasses):
			print("Shifting "+file_name+" to "+target)
			shutil.copy(full_file_name, target)

main()
