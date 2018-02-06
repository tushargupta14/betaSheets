## Exdtracts the curvature values for each direction
## Random information
from calculate_curvature import *
from get_residue_dict import *
from collections import defaultdict
def curvature_values_along(pdb_name,chain,sheet_dict,residue_dict):

	curvature_dict = defaultdict(list)
	for sheet,residue_list in sheet_dict.iteritems():

		#print sheet,residue_list
		curv_3 = calculate_data_points(residue_list,residue_dict,npoints = 3,slide_value = 1)

		curv_5 = calculate_data_points(residue_list,residue_dict,npoints = 5,slide_value = 1)
		#print curv_3,curv_5
		curvature_dict[sheet] = [curv_3,curv_5]
		

	return curvature_dict

def curvature_values_across(pdb_name,chain,sheet_dict,residue_dict):

	curvature_dict = defaultdict(list)
	for sheet,residue_list in sheet_dict.iteritems():

		#print sheet,residue_list

		if len(residue_list)==0 :
			continue
		start_residues = residue_list[0]
		last_residues = residue_list[1]

		curv_1 = calculate_data_points(start_residues,residue_dict,npoints = 3,slide_value = 1)

		curv_2 = calculate_data_points(last_residues,residue_dict,npoints = 3,slide_value = 1)

		curvature_dict[sheet] = [curv_1,curv_2]
		
		#print curv_1,curv_2
	
	return curvature_dict

def recurse_pdbs() :


	path_to_pdb_list = "all_beta_sheets"
	path_to_backbone_info = "allBeta_data/backbone_info/"
	#path_to_pdbs = "/home/twistgroup/pdb/"

	path_to_json_files = "allBeta_data/sheets/"

	path_to_output = "allBeta_data/curvature/"

	file = open(path_to_pdb_list,"rb+")

	#unique_pdb_set = set()
	error =0
	count =0

	error_file = open("allBeta_curvature_error.txt","wb+")
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

			residue_dict = get_residue_dict(path_to_backbone_info,pdb_name)

			## residues along the strand
			sheet_dict = json.load(open(path_to_json_files+"along/"+pdb_name+"_"+chain+".json","rb+"))
			along_curv_dict = curvature_values_along(pdb_name,chain,sheet_dict,residue_dict)

			with open(path_to_output+"along/"+pdb_name+"_"+chain+".json","wb+") as f :

				json.dump(along_curv_dict,f)
			## residues across the strand
			sheet_dict = json.load(open(path_to_json_files+"across/"+pdb_name+"_"+chain+".json","rb+"))
		
			across_curv_dict = curvature_values_across(pdb_name,chain,sheet_dict,residue_dict)
			with open(path_to_output+"across/"+pdb_name+"_"+chain+".json","wb+") as f :

				json.dump(across_curv_dict,f)



		except Exception as e :
			print e
			error+=1
			error_file.write(str(e)+"\t"+pdb_name+"\t"+chain+"\n")
			continue


		count+=1
		


	print error,count

if __name__ == "__main__" :

	##path_to_backbone_info = "allBeta_data/backbone_info/"
	#path_to_json_files = "allBeta_data/sheets/"
	#pdb_name = "2ich"
	#chain = "A"
	#residue_dict = get_residue_dict(path_to_backbone_info,pdb_name)

			## residues along the strand
	#sheet_dict = json.load(open(path_to_json_files+"along/"+pdb_name+"_"+chain+".json","rb+"))
	#along_curv_dict = curvature_values_across(pdb_name,chain,sheet_dict,residue_dict)


	recurse_pdbs()
