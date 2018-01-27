import json


def recurse_pdbs() :


        path_to_pdb_list = "30k_pdb_list"
        #path_to_pdbs = "/home/twistgroup/pdb/"

        path_to_json_files = "data/curvature/"

        file = open(path_to_pdb_list,"rb+")
	sheet_info_file = open("sheet_info.txt","wb+")

	sheet_info_file.write("PDB"+"\t"+"CHAIN"+"\t"+"SHEET"+"\n")
	error = 0
	count  =0

	error_file = open("max_min_errors.txt","wb+")

	total_sheets =0

	max_3 = -10000

	min_3 = 100000
        max_5 = -10000

	min_5 = 100000
	max_7 = -10000

	min_7 = 100000

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
                	curvature_dict = json.load(open(path_to_json_files+pdb_name+"_"+chain+".json","rb+"))
			
			total_sheets+=len(curvature_dict) 

			for sheet in curvature_dict.iterkeys() :

				curv_3 = curvature_dict[sheet][0]
				curv_5 = curvature_dict[sheet][1]
				curv_7 = curvature_dict[sheet][2]
                		
				if len(curv_3) > 3 :
	
					max_3 = max(max_3,max(curv_3))
				else :
					error_file.write("Length Insufficient"+"\t"+pdb_name+"\t"+sheet+"\n")
				if len(curv_5) >5 :
					max_5 = max(max_5,max(curv_5))
				else :
					error_file.write("Length Insufficient"+"\t"+pdb_name+"\t"+sheet+"\n")

				if len(curv_7)>7 :
					max_7 = max(max_7,max(curv_7))
				else :
					error_file.write("Length Insufficient"+"\t"+pdb_name+"\t"+sheet+"\n")
				
				if len(curv_3)>3 :		
					min_3 = min(min_3,min(curv_3[:-2]))
				else :
                                        error_file.write("Length Insufficient"+"\t"+pdb_name+"\t"+sheet+"\n")

				if len(curv_5) >5 :
					min_5 = min(min_5,min(curv_5[:-4]))
				else :
					error_file.write("Length Insufficient"+"\t"+pdb_name+"\t"+sheet+"\n")
				
				if len(curv_7) > 7:
					min_7 = min(min_7,min(curv_7[:-6]))
				else :

					error_file.write("Length Insufficient"+"\t"+pdb_name+"\t"+sheet+"\n")
				sheet_info_file.write(pdb_name+"\t"+chain+"\t"+sheet+"\n")
								
		except Exception as e :
			
			print e
			error+=1
			error_file.write(str(e)+"\t"+pdb_name+"\t"+chain+"\n")
			continue 
	
		count+=1
		
	print min_3,max_3
	print min_5,max_5
	print min_7,max_7

	print total_sheets



if __name__ == "__main__" :


	recurse_pdbs()
