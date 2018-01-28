### Extracting sheet info for along

from get_residue_dict import *
from collections import defaultdict

def sheet_info_along(pdb_name,chain,sheet_dict,chain_break_file) :


	path_to_backbone_info = "allBeta_data/backbone_info/"

	path_to_output = "allBeta_data/sheets/along/"


	residue_dict = get_residue_dict(path_to_backbone_info,pdb_name)

	final_sheet_dict = defaultdict(list)

	for sheet in sheet_dict.iterkeys() :

		residue_ranges = sheet_dict[sheet]["residue_range"]
		
		

		if len(residue_ranges) < 4 :
			#print sheet,residue_ranges
			continue


		for residue_range in residue_ranges :

			flag = 1
			residue_list = []
			for i in range(residue_range[0],residue_range[1]+1):
				
				if i not in residue_dict :

					#print "Chain break Exception","residue:",i
					chain_break_file.write(pdb_name+"\t"+chain+"\t"+sheet+"\t"+str(i)+"\n")
					flag = 0
					break
				
				residue_list.append(i)

			if flag :

				start = residue_range[0]
				middle = int((residue_range[1]+residue_range[0])/2)
				end = residue_range[1]


				final_sheet_dict[sheet].append(start)
				if middle != start and middle != end :
					final_sheet_dict[sheet].append(middle)
				final_sheet_dict[sheet].append(end)

			else :

				final_sheet_dict[sheet] = []


	#print final_sheet_dict

	return final_sheet_dict