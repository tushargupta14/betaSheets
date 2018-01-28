### Script to get valid sheets 
### Taking care of chain break
import json

import re 

from get_residue_dict import *
from get_sheet_info_along import *

	


def extract_sheet_info(pdb_name,chain,sheet_dict,chain_break_file):

	path_to_backbone_info = "allBeta_data/backbone_info/"

	path_to_output = "allBeta_data/sheet_info/"

	#chain_break_file = open("chain_break_pdbs.txt","wb+")

	residue_dict = get_residue_dict(path_to_backbone_info,pdb_name)

	final_sheet_dict = {}
	
	for sheet in sheet_dict.iterkeys() :

		residue_range = sheet_dict[sheet]["residue_range"]
		residue_list = []
		for i in range(residue_range[0],residue_range[1]+1):
			
			if i not in residue_dict :

				print "Chain break Exception","residue:",i
				chain_break_file.write(pdb_name+"\t"+chain+"\t"+sheet+"\t"+str(i)+"\n")
				residue_list = []
				break
			else :
				residue_list.append(i)
		
		if len(residue_list):	
			final_sheet_dict[sheet] = residue_list
	
	
	#print final_sheet_dict 

	return final_sheet_dict
	
def recurse_pdbs() :


    path_to_pdb_list = "all_beta_sheets"
    #path_to_pdbs = "/home/twistgroup/pdb/"

    path_to_json_files = "allBeta_data/strand_wise_info/"
    path_to_output = "allBeta_data/sheets/along/"

    file = open(path_to_pdb_list,"rb+")

    chain_break_file = open("allBeta_chain_break_pdbs.txt","wb+")

    chain_break_file.write("PDB"+"\t"+"CHAIN"+"\t"+"SHEET"+"\t"+"RESIDUE"+"\n")

    error = 0
    count = 0

    error_file = open("allBata_final_sheet_errors.txt","wb+")
    num_sheets = 0 
    for line in file :

    	vals = line.split(" ")
    	if "IDs" in vals[0] :
    		continue
        #print vals[0]
        pdb_name = vals[0][:4]

        chain =  vals[0][-1]

        pdb_name = pdb_name.lower()

        print pdb_name,"-",chain
        ## retrieving strand data
        try :
        	sheet_dict = json.load(open(path_to_json_files+pdb_name+"_"+chain+".json","rb+"))

        	pdb_sheet_dict = sheet_info_along(pdb_name,chain,sheet_dict,chain_break_file)

        except Exception as e :

        	print e
        	error+=1
        	error_file.write(str(e)+"\t"+pdb_name+"\t"+chain+"\n")
        	continue

        num_sheets+= len(pdb_sheet_dict)
        print len(pdb_sheet_dict)

        with open(path_to_output+pdb_name+"_"+chain+".json","wb+") as f :
			json.dump(pdb_sheet_dict,f)
        count+=1


    print error,count
    print "number of sheets extracted :",num_sheets
if __name__  == "__main__" :

	recurse_pdbs()
