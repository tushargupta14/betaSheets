## Utility Codes


import json 

path_to_data = "allBeta_data/"

## Returns a json dict of the desired file
def open_json_file(pdb_name,chain,folder_name,path_to_data = "allBeta_data/"):


	data = json.load(open(path_to_data+folder_name+pdb_name+"_"+chain+".json","rb+"))

	return data