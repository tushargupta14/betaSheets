import json

import re 
def clean_residue(residue) :


	clean_residue  = re.findall('^\d+',residue)

	#print clean_residue,residue
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