#!/usr/bin/env python3

#from R02.4 filter blast results to remove nested hits

import sys

f = open(sys.argv[1],'r') #input blast

g = open(sys.argv[2],'w') #output blast

contig_col = int(sys.argv[3])
start_col = int(sys.argv[4])
end_col = int(sys.argv[5])


filename=sys.argv[1].split("/")[-1].split(".")[0]


#read blast into dict
blast={}
f.readline() #skip header 
for i in f:

	k=i.split("\t")
	
	contig = k[contig_col]
	x= int(k[start_col])
	y= int(k[end_col])
	
	if y<x:
		start=y
		end=x
	else:
		start=x
		end=y
	if contig not in blast.keys():
		blast[contig]=[(start,end,i)]
	else:
		blast[contig].append((start,end,i))
	print(contig,start,end)
	
for i in blast.keys(): #contigs
	n=-1
	nests=[]
	for j in blast[i]:
		n=n+1
		for p in blast[i]:
			if j[2]!=p[2]:
				if j[0]>=p[0] and j[1]<=p[1]:
					nests.append(n)
	print(nests)
	c=-1
	for v in blast[i]:
		c=c+1
		if c not in nests:
		
			g.write(v[2]) #if not nested write to output
		

	
	
		
		
		
		
		
		
		