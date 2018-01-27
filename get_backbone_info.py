### Creating the new atom info file in dependency outuput
### Retrieving backbone Information


import os
def create_new_atom_info(pdb_name,path_to_output,path_to_input):


	print path_to_input+pdb_name
	pdb_file = open(path_to_input+pdb_name,"rb+")
	
	output_file = open(path_to_output+pdb_name+"_backbone.txt","wb+")

	for line in pdb_file :


		if("ATOM" in line) :

			vals = [el for el in line.rstrip("\n").split(" ") if el is not ""]
			#print vals
				
			if vals[2] == "CA" :
				#print vals
				
				if len(vals[4])==5:
					residue_number = vals[4][1:]
					chain = vals[4][0]
					output_file.write(residue_number+"\t"+vals[2]+"\t"+vals[3]+"\t"+chain+"\t"+vals[1]+"\t"+vals[5]+"\t"+vals[6]+"\t"+vals[7]+"\n")
				else :
					residue_number = vals[5]
					chain = vals[4]
					output_file.write(residue_number+"\t"+vals[2]+"\t"+vals[3]+"\t"+chain+"\t"+vals[1]+"\t"+vals[6]+"\t"+vals[7]+"\t"+vals[8]+"\n")



def run_on_pdbs(path_to_pdbs  = "/home/twistgroup/betaSheets/allBeta_pdb_final/") :

	path_to_output = "allBeta_data/backbone_info/"

	for file in os.listdir(path_to_pdbs) :

		try :
			pdb_name = file

			print pdb_name

			create_new_atom_info(pdb_name,path_to_output,path_to_pdbs)
			
		except Exception as e :

			print e


def run_on_single() :

	path_to_pdbs  = "/home/twistgroup/betaSheets/pdb_final/"
	path_to_output = "data/backbone_info/"

	create_new_atom_info("4bfr",path_to_output,path_to_pdbs)



if __name__ == "__main__" :

	#run_on_single()
	run_on_pdbs()

	## path to pdb 

	#path_to_input = "pdb_files_temp/"
	
	#create_new_atom_info("1bcm",path_to_output,path_to_input)
