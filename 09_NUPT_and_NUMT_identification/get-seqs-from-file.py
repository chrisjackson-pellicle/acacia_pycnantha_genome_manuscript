#!/usr/bin/env python3

#from Bio import SeqIO
import sys

print("n.b. '>' is not included in the name list to search")

listfile1 = open(sys.argv[1],'r') 

inputfile = open(sys.argv[2],'r') 

g = open(sys.argv[3],'w') 

delim=sys.argv[4]

print('reading file')
#x = SeqIO.to_dict(SeqIO.parse(inputfile,'fasta'))

x = {}

for i in inputfile:
	
	if i[0]!="#":
		if i[0]==">":
			
			id1=i.split(">")[1].rstrip("\n")
			x[id1]=""
		else:
			x[id1]=x[id1]+i.rstrip("\n")


data={}

print('parsing file')
for i in x.keys():
	#print x[i].description.split(",")[0]
	if delim!="":
		data[i.split(delim)[0]]=x[i]
	else:
		data[i]=x[i]
	
print(len(data.keys()),'sequences')

c=0

print('fetching sequences')
for k in listfile1:
	name=k.rstrip("\n")#.split(delim)[0]
	#print name, str(data[name])
	try:
		c=c+1
		g.write(">"+str(name)+"\n"+str(data[name])+"\n")
	except:
		c=c-1
		#print name,'not found'


print("%s got %s sequences" %(str(sys.argv[2]),str(c)))

g.close()
