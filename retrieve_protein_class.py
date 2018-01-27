
import re

def extract_char(str) :
	word1 = " ".join(re.findall("[a-zA-Z@]+", str))
	return word1

def extract_int(str) : 
	word = " ".join(re.findall("[^a-zA-Z@]+",str))
	return word

class litera :

	def __init__(self,start,end):
		self.start = start
		self.end = end

		if extract_char(start) == '':
			self.start += '@'
		if extract_char(end) == '':
			self.end += '@'

	def __iter__(self):
		self.ele = self.start
		return self

	def next(self):
		next_lit = self.ele

		if (int(extract_int(next_lit)) > int(extract_int(self.end))) or (extract_int(next_lit) == extract_int(self.end) and ord(extract_char(next_lit))) > ord(extract_char(self.end)):
			raise StopIteration

		
		if extract_char(next_lit)!='Z':
			self.ele = extract_int(next_lit)+chr(ord(extract_char(next_lit))+1)
		else : 
			self.ele = str(int(extract_int(next_lit))+1)+'@'
		
		return next_lit.strip('@')