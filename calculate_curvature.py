#!/usr/bin/python2.7
### Script to calculate the curvature values

import json
import numpy as np 
import re
import math
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
	

def compute_curvature(residue_dict,residue_list,npoints) :

	### Only a helper function 
	### Call calculate_curvature

	if(len(residue_list)%2==0 or len(residue_list) < npoints) :

		return -10000

	r1 = residue_dict[residue_list[0]]
	r2 = residue_dict[residue_list[len(residue_list)/2]]
	r3 = residue_dict[residue_list[-1]]

	A = np.array(r1)
	B = np.array(r2)
	C = np.array(r3)

	a = np.linalg.norm(C-A)
	b = np.linalg.norm(C-B)
	c = np.linalg.norm(B-A)

	s = (a+b+c)/2

	R = a*b*c / 4 / np.sqrt(s*(s-a)*(s-b)*(s-c))

	return (1/R)*180/math.pi

def calculate_data_points(residue_list,residue_dict,npoints,slide_value) :

	## Only input odd values
	## Call this to compute curvature points of a residue list

	if(len(residue_list)<npoints) :
		return ([],[])
	i = 0
	
	#print residue_list
	curvature_list = []
	#eviations_list = []

	while(i<len(residue_list)):

		curvature_list.append(compute_curvature(residue_dict,residue_list[i:i+npoints],npoints))
		#deviations_list.append(compute_deviations(residue_dict,residue_list[i:i+npoints],npoints))

		i += slide_value


	#print npoints,residue_list,curvature_list,deviations_list

	return curvature_list


def calculate_curvature(pdb_name,chain,sheet_dict) :

	path_to_backbone_info = "data/backbone_info/"
	path_to_output = "data/curvature/"

	residue_dict = get_residue_dict(path_to_backbone_info,pdb_name)

	curvature_dict = {}
	for sheet,residue_list in sheet_dict.iteritems() :


		#print sheet,residue_list


		curv_3 = calculate_data_points(residue_list,residue_dict,npoints = 3,slide_value = 1)

		#if len(curv_3)==0  :
			#curv_3_top = []

		#print curv_3	

		curv_5 = calculate_data_points(residue_list,residue_dict,npoints = 5,slide_value = 1)

		#if len(curv_5)==0 or len(dev_5)==0 :
			#curv_5_top = []
		#else :
			#curv_5_top = [x for _,x in sorted(zip(dev_5,curv_5),key = lambda pair : pair[0],reverse = True)]
			#print curv_5,dev_5


		curv_7 = calculate_data_points(residue_list,residue_dict,npoints = 7,slide_value = 1)

		
		#if len(curv_7)==0 or len(dev_7)==0 :
			#curv_7_top = []
		#else :
		#curv_7_top = [x for _,x in sorted(zip(dev_7,curv_7),key = lambda pair : pair[0],reverse = True)]
		

	
		curvature_dict[sheet] = curv_3,curv_5,curv_7
		#print curv_3
		#print curv_5
		#print curv_7	
		
	with open(path_to_output+pdb_name+"_"+chain+".json","wb+") as f :
                        json.dump(curvature_dict,f)

def recurse_pdbs() :


	path_to_pdb_list = "30k_pdb_list"

	path_to_pdbs = "/home/twistgroup/pdb/"

	path_to_json_files = "data/sheet_info/"
	path_to_output = "data/curvature/"

	file = open(path_to_pdb_list,"rb+")

	#unique_pdb_set = set()
	error =0
	count =0

	error_file = open("curvature_error.txt","wb+")
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
		#sheet_dict = json.load(open(path_to_json_files+pdb_name+"_"+chain+".json","rb+"))	
		
		try :
			sheet_dict = json.load(open(path_to_json_files+pdb_name+"_"+chain+".json","rb+"))
			calculate_curvature(pdb_name,chain,sheet_dict)
		except Exception as e :
			print e
                        error+=1
                        error_file.write(str(e)+"\t"+pdb_name+"\t"+chain+"\n")
                        continue
		count+=1
	print error,count

if __name__ == "__main__" :



	recurse_pdbs()
