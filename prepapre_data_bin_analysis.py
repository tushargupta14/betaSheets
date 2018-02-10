## Script to prepared data to analyse for binning


from utilities import *


def handle_across_values(across_dict,across_first,across_last) :


	if len(across_dict)==0 :
		return

	for sheet in across_dict.iterkeys() :

		first_points = across_dict[sheet][0]
		last_points = across_dict[sheet][1]

		#print first_points
		#print last_points
		if len(first_points)!=0:
			for point in first_points :
				if point >= 0 and type(point) == float: 
					across_first.write(str(point)+"\n")

		if len(last_points)!=0 :
			for point in last_points :
				if point >= 0 and type(point) == float: 
					across_last.write(str(point)+"\n")
	return

def handle_along_values(along_dict,along_3,along_5):

	if len(along_dict)==0 :
		return

	for sheet in along_dict.iterkeys() :

		curv_3 = along_dict[sheet][0]
		curv_5 = along_dict[sheet][1]

		#print curv_3
		#print curv_5
		
		for point in curv_3 :
			if point >= 0 and type(point) == float: 
				along_3.write(str(point)+"\n")

		
		for point in curv_5 :
			if point >=0 and type(point) == float:
				along_5.write(str(point)+"\n")


	return

def recurse_pdbs():


	path_to_pdb_list = "final_pdb_list"

	file = open(path_to_pdb_list,"rb+")
	error = 0
	count = 0
	across_first = open("across_first.txt","wb+")

	across_last = open("across_last.txt","wb+")
	along_3 = open("along_3.txt","wb+")

	along_5 = open("along_5.txt","wb+")

	for line in file :

		vals = line.rstrip("\n")
		#print vals

		pdb_name = vals[:4]
		pdb_name = pdb_name.lower()
		chain =  vals[-1]
		print pdb_name,"-",chain

		try :

			across_dict = open_json_file(pdb_name,chain,"curvature/across/")

			along_dict = open_json_file(pdb_name,chain,"curvature/along/")

			handle_across_values(across_dict,across_first,across_last)

			handle_along_values(along_dict,along_3,along_5)

		except Exception as e :

			print e
			error+=1

		count+=1

	print "error:",error,"pdbs:",count
    #print "error:",error,"pdbs",count

	
if __name__ == "__main__" :
	
	#enter_single_pdb()
	recurse_pdbs()
