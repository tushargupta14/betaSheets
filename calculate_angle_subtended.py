## Calculates the angle subtended at the center using the curvature values

import numpy as np


def get_center(points,distances):

	A = points["A"]
	B = points["B"] 
	C = points["C"] 

	a = distances["a"] 
	b = distances["b"] 
	c = distances["c"]


	b1 = a*a * (b*b + c*c - a*a)
	b2 = b*b * (a*a + c*c - b*b)
	b3 = c*c * (a*a + b*b - c*c)

	P = np.column_stack((A, B, C)).dot(np.hstack((b1, b2, b3)))

	P /= b1 + b2 + b3

	return P



def get_angle(center,A,C):


	v1 = -(A - center)
	v2 = -(C - center)

	cosine_angle =  np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
	angle = np.arccos(cosine_angle)

	#print np.degrees(angle)
	return np.degrees(angle)



def compute_angle_subtended(residue_dict,residue_list,npoints):

	
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

	points = {}
	distances = {}

	points["A"] = A
	points["B"]  = B
	points["C"] = C

	distances["a"] = a
	distances["b"] = b
	distances["c"] = c

	s = (a+b+c)/2

	R = a*b*c / 4 / np.sqrt(s*(s-a)*(s-b)*(s-c))
	
	P = get_center(points,distances) ## center of the circle 

	#print A,B,C,P

	angle_subtended = get_angle(P,A,C)

	return angle_subtended

def calculate_data_points(residue_list,residue_dict,npoints,slide_value) :

	## Only input odd values
	## Call this to compute curvature points of a residue list

	if(len(residue_list)<npoints) :
		return ([],[])
	i = 0
	
	#print residue_list
	angle_list = []
	#eviations_list = []

	while(i<len(residue_list)):

		angle_list.append(compute_angle_subtended(residue_dict,residue_list[i:i+npoints],npoints))
		#deviations_list.append(compute_deviations(residue_dict,residue_list[i:i+npoints],npoints))

		i += slide_value


	#print npoints,residue_list,curvature_list,deviations_list

	return angle_list



