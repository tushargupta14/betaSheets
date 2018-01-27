## Script to find the intersection between pdb_list and pdb files 

import os

import shutil 


def copy_pdbs() :


	path_to_pdb_list = "all_beta_sheets"

	path_to_pdbs = "/home/twistgroup/pdb/"

	file = open(path_to_pdb_list,"rb+")

	dst = "allBeta_pdb_final/"
	src = path_to_pdbs

	error = 0 
	count = 0 
	for line in file :
		vals = line.split(" ")

		if "IDs" in vals[0] :
			continue

		print vals[0]

		pdb_name = vals[0][:4]
		pdb_name = pdb_name.lower()
		
		res =  os.path.isfile(path_to_pdbs+"pdb"+pdb_name+".ent")

		if res :
			shutil.copyfile(src+"pdb"+pdb_name+".ent",dst+pdb_name)
			count+=1
		else :
			print "File does not exist"
			error+=1

	print error,count



def check_files() :


	path_to_pdb_list = "all_beta_sheets"
	path_to_pdbs = "/home/twistgroup/pdb/"
	file = open(path_to_pdb_list,"rb+")
	error =0
	count  = 0	
	outfile = open("missing_pdbs.txt","wb+")

	for line in file :

		vals = line.split(" ")

		if "IDs" in vals[0] :
			continue

		print vals[0]

		pdb_name = vals[0][:4]
		pdb_name = pdb_name.lower()
		chain =  vals[0][-1]

		#print pdb_name,"-",chain

		res =  os.path.isfile(path_to_pdbs+"pdb"+pdb_name+".ent")
		if res :
			count+=1
		else :
			error+=1
			print pdb_name
			outfile.write(pdb_name+'\n')
	print error,count,error+count

	outfile.close()

if __name__ == "__main__" :

	#check_files()
	copy_pdbs()
