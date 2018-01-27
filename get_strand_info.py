### Script to prepare the strand info for each pdb along with chain
### runs after backbone info 
### Extracts the residue information for each sheet
import retrieve_protein_class as rpc 
from collections import defaultdict
import re
import json


def clean_residue(residue) :


	clean_residue  = re.findall('^\d+',residue)

	if len(clean_residue)==0:
                return int(residue)
        else :
                return int(clean_residue[0])



def get_residue_dict(path_to_backbone_info,pdb_name) :


	backbone_file = open(path_to_backbone_info+pdb_name+"_backbone.txt")

	residue_dict = {}


	for line in backbone_file :

		vals = line.rstrip("\n").split("\t")
		
		x = vals[5]
		y = vals[6]
		z = vals[7]
		
		residue = clean_residue(vals[0])
		#print x,y,z
		#residue_dict[vals[0]] = [float(vals[5]),float(vals[6]),float(vals[7])]
		
		## Checking if a valid float
		try :
			x = float(x)
		except :

			if x.count('-') == 2 or x.count('-')==1 :
				a = float(x.rsplit('-',1)[0])
				b = float('-'+x.rsplit('-',1)[1])
				c = float(y)
				#print x,y,z
				#print a,b,c
				residue_dict[residue] = [a,b,c]
				continue		

		try :
			y = float(y)
		except :

			if y.count('-') == 2 or y.count('-')==1:
				a = x
				b = float(y.rsplit('-',1)[0])
 				c = float('-'+y.rsplit('-',1)[1])
				residue_dict[residue] = [a,b,c]
				#print x,y,z
                                #print a,b,c
				continue

		residue_dict[residue] = [float(vals[5]),float(vals[6]),float(vals[7])]

		#residue_dict[vals[0]] = [float(vals[5]),float(vals[6]),float(vals[7])]
	
	backbone_file.close()
	return residue_dict

def extract_strand_info(pdb_name,chain):


	path_to_dataset_pdbs = "allBeta_pdb_final/"
	path_to_backbone_info = "allBeta_data/backbone_info/"
	path_to_output = "allBeta_data/strand_info/"
	pdb_file = open(path_to_dataset_pdbs+pdb_name,"rb+")

	lines  = pdb_file.readlines()

	pdb_file.close()
	

	sheet_lines = [el for el in lines if el.split(" ")[0] == "SHEET"]

	#residue_dict = get_residue_dict(path_to_backbone_info,pdb_name)
	sheet_dict = defaultdict(lambda : defaultdict(list))

	prev_sheet = ''

	residue_list = []

	for i in range(len(sheet_lines)) :


		sheet_lines[i] = [x for x in sheet_lines[i].rstrip("\n").split(" ") if x is not '']

		#print sheet_lines[i]

		## when the number of strands 2 digit 
		if len(sheet_lines[i][2]) == 4 :

			curr_chain  = sheet_lines[i][7]
			if curr_chain != chain :
				continue

			num_strands = sheet_lines[i][2][2:]

			if num_strands < 4 :
				continue


			curr_sheet = sheet_lines[i][2][:2]
			residue_range = (sheet_lines[i][5],sheet_lines[i][8])
			
			sense = sheet_lines[i][9]	

		else :

			curr_chain  = sheet_lines[i][8]
			if curr_chain != chain :
				continue

			num_strands = sheet_lines[i][3]

			if num_strands < 4 :
				continue
			curr_sheet = sheet_lines[i][2]
			residue_range = (sheet_lines[i][6],sheet_lines[i][9])
			sense = sheet_lines[i][10]
			
		if prev_sheet!= curr_sheet :

			#residue_list = []
			min_residue = 100000
			max_residue = -100000

		min_residue = min(min_residue,clean_residue(residue_range[0]))
		max_residue = max(max_residue,clean_residue(residue_range[1]))
			
		#for i in rpc.litera(residue_range[0],residue_range[1]):
			#if i in residue_dict :
				#residue_list.append(i)
		#print sense
		sheet_dict[curr_sheet]["residue_range"] = [min_residue,max_residue]
		sheet_dict[curr_sheet]["chain"] = chain
		sheet_dict[curr_sheet]["direction"] = sense
		
		prev_sheet = curr_sheet	
	
	#print sheet_dict 
	return sheet_dict


def recurse_pdbs() :


	path_to_pdb_list = "all_beta_sheets"

	#path_to_pdbs = "pdb/"
	path_to_output = "allBeta_data/strand_info/"
	file = open(path_to_pdb_list,"rb+")

	#unique_pdb_set = set()
	error_file = open("allBeta_strand_error_pdbs.txt","wb+")
	error =0
	count =0
	for line in file :

		vals = line.split(" ")

		if "IDs" in vals[0] :
			continue

		#print vals[0]

		pdb_name = vals[0][:4]
		chain =  vals[0][-1]
		pdb_name = pdb_name.lower()

		print pdb_name,"-",chain
		
		
		try :
			pdb_sheet_dict = extract_strand_info(pdb_name,chain)
		
		except Exception as e :

			print e
			error+=1
			error_file.write(str(e)+"\t"+pdb_name+"\t"+chain+"\n")
			continue
		with open(path_to_output+pdb_name+"_"+chain+".json","wb+") as f :
			json.dump(pdb_sheet_dict,f)
		#break
		count+=1
		#unique_pdb_set.add(pdb_name)

	print "error:",error,"count:",count

def enter_single_pdb():
	
	pdb_name = "4bfr"
	chain = "A"
	pdb_sheet_dict = extract_strand_info(pdb_name,chain)

	
	
if __name__ == "__main__" :
	
	#enter_single_pdb()
	recurse_pdbs()
