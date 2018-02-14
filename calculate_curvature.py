#!/usr/bin/python2.7
### Script to calculate the curvature values

import json
import numpy as np 
import re
import math
from get_residue_dict import *

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
	
	return (1/R)

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


"""def calculate_curvature(pdb_name,chain,sheet_dict) :

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
"""