## Exdtracts the curvature values for each direction

from calculate_angle_subtended import *
from get_residue_dict import *
from collections import defaultdict


def angle_values_along(pdb_name,chain,sheet_dict,residue_dict):

	angle_dict = defaultdict(list)
	for sheet,residue_list in sheet_dict.iteritems():

		#print sheet,residue_list
		A_3 = calculate_data_points(residue_list,residue_dict,npoints = 3,slide_value = 1)

		A_5 = calculate_data_points(residue_list,residue_dict,npoints = 5,slide_value = 1)
		#print curv_3,curv_5
		angle_dict[sheet] = [A_3,A_5]
		

	return angle_dict

def angle_values_across(pdb_name,chain,sheet_dict,residue_dict):

	angle_dict = defaultdict(list)
	for sheet,residue_list in sheet_dict.iteritems():

		#print sheet,residue_list

		if len(residue_list)==0 :
			continue
		start_residues = residue_list[0]
		last_residues = residue_list[1]

		A_1 = calculate_data_points(start_residues,residue_dict,npoints = 3,slide_value = 1)

		A_2 = calculate_data_points(last_residues,residue_dict,npoints = 3,slide_value = 1)

		angle_dict[sheet] = [A_1,A_2]
		
		#print curv_1,curv_2
	
	return angle_dict

def recurse_pdbs() :


	path_to_pdb_list = "final_pdb_list"
	path_to_backbone_info = "allBeta_data/backbone_info/"
	#path_to_pdbs = "/home/twistgroup/pdb/"

	path_to_json_files = "allBeta_data/sheets/"

	path_to_output = "allBeta_data/angle/"

	file = open(path_to_pdb_list,"rb+")

	#unique_pdb_set = set()
	error =0
	count =0

	error_file = open("allBeta_angle_error.txt","wb+")
	for line in file :

		vals = line.rstrip("\n")
		#print vals
		pdb_name = vals[:4]
		pdb_name = pdb_name.lower()
		chain =  vals[-1]
		
		print pdb_name,"-",chain	
		
		
		try :

			residue_dict = get_residue_dict(path_to_backbone_info,pdb_name)

			## residues along the strand
			sheet_dict = json.load(open(path_to_json_files+"along/"+pdb_name+"_"+chain+".json","rb+"))
			along_angle_dict = angle_values_along(pdb_name,chain,sheet_dict,residue_dict)

			with open(path_to_output+"along/"+pdb_name+"_"+chain+".json","wb+") as f :
				json.dump(along_angle_dict,f)
			## residues across the strand
			
			sheet_dict = json.load(open(path_to_json_files+"across/"+pdb_name+"_"+chain+".json","rb+"))
		
			across_angle_dict = angle_values_across(pdb_name,chain,sheet_dict,residue_dict)
			with open(path_to_output+"across/"+pdb_name+"_"+chain+".json","wb+") as f :

				json.dump(across_angle_dict,f)

			#break


		except Exception as e :
			print e
			error+=1
			error_file.write(str(e)+"\t"+pdb_name+"\t"+chain+"\n")
			continue


		count+=1
		


	print error,count

if __name__ == "__main__" :

	#path_to_backbone_info = "allBeta_data/backbone_info/"
	#path_to_json_files = "allBeta_data/sheets/"
	#pdb_name = "2ich"
	#chain = "A"
	#residue_dict = get_residue_dict(path_to_backbone_info,pdb_name)
	#print residue_dict
			## residues along the strand
	#sheet_dict = json.load(open(path_to_json_files+"across/"+pdb_name+"_"+chain+".json","rb+"))
	#across_curv_dict = angle_values_across(pdb_name,chain,sheet_dict,residue_dict)
	#print across_curv_dict

	recurse_pdbs()
