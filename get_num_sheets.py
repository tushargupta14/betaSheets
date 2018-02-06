## Checking the number of sheets from the curvature data 

import json
def recurse_pdbs() :



    path_to_pdb_list = "final_pdb_list"
    #path_to_pdbs = "/home/twistgroup/pdb/"

    path_to_json_files = "allBeta_data/curvature/along/"
    #path_to_output = "allBeta_data/sheets/across/"

    file = open(path_to_pdb_list,"rb+")

    #chain_break_file = open("allBeta_chain_break_across_pdbs.txt","wb+")

    #chain_break_file.write("PDB"+"\t"+"CHAIN"+"\t"+"SHEET"+"\t"+"RESIDUE"+"\n")

    error = 0
    count = 0

    #error_file = open("allBata_final_sheet_errors_across.txt","wb+")
    num_sheets = 0 
    for line in file :

    	vals = line.rstrip("\n")
        #print vals
        pdb_name = vals[:4]
        pdb_name = pdb_name.lower()
        chain =  vals[-1]
        
        print pdb_name,"-",chain
        try :
        	sheet_dict = json.load(open(path_to_json_files+pdb_name+"_"+chain+".json","rb+"))

    		if len(sheet_dict)==0 :
    			continue
	    	for sheet in sheet_dict.iterkeys():
	    		if len(sheet_dict[sheet])>0:
	    			num_sheets+=1
        except Exception as e :

        	print e
        	error+=1
        	#error_file.write(str(e)+"\t"+pdb_name+"\t"+chain+"\n")
    
        count+=1
        #break

    print "number of sheets extracted :",num_sheets
    print "error:",error,"pdbs",count
if __name__  == "__main__" :

	recurse_pdbs()
