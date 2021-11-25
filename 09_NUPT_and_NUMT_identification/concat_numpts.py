#!/usr/bin/env python

#from R02.4 concatenate tandem numpts
#sort blast first by contig and start

import sys

f = open(sys.argv[1],'r') #input blast
g = open(sys.argv[2],'w') #out blast

overlap = int(sys.argv[3])

contigpos=int(sys.argv[4])
startpos=int(sys.argv[5])
endpos=int(sys.argv[6])


contigs={}
concats={}

print("Reading blast")
for i in f: 
	
	k=i.rstrip("\n").split("\t")
	
	id1=k[-1]
	contig=k[contigpos]
	x=int(k[startpos])
	y=int(k[endpos])
	if x<y:
		start=x
		end=y
	else:
		start=y
		end=x
		
	pid=float(k[2])
	
	if contig not in contigs.keys():
		
		k3=i.rstrip("\n").split("\t")
		k3[startpos]=start
		k3[endpos]=end
		newi="\t".join(str(p) for p in k3)+"\n"
		
		contigs[contig]=[(start,end,pid,newi)]
		
	else:
		#check if identical
		if start==contigs[contig][-1][0] and end==contigs[contig][-1][1]:
			newpid=(contigs[contig][-1][2]+pid)/2

			k2=contigs[contig][-1][3].split("\t")
		
			k2[2]=newpid
			k2[-1]=k2[-1].rstrip("\n")+";"+id1+"_identical"
			
			newi="\t".join(str(p) for p in k2)+"\n"
			
			contigs[contig][-1]=(start,end,newpid,newi)
		#not identical
		else:
			if start< contigs[contig][-1][1]+overlap:#catenate
				
				newstart=contigs[contig][-1][0] #file sorted by start so cannot be less than current start
				
				if end>contigs[contig][-1][1]: #if internal numpt, use existing end
					newend=end
				else:
					newend=contigs[contig][-1][1]
				
				#weight pid by lengths
				len1=float((contigs[contig][-1][1])-(contigs[contig][-1][0]))
				len2=float(end-start)
				
				newpid=((contigs[contig][-1][2]*len1)+(pid*len2))/(len1 + len2)
				
				#print(contigs[contig][-1][1],contigs[contig][-1][0],start,end,contigs[contig][-1][2],len1,pid,len2)
				
				k2=contigs[contig][-1][3].split("\t")
					
				k2[startpos]=newstart
				k2[endpos]=newend
				
				k2[3]=len1 + len2
				k2[2]=newpid
				k2[-1]=k2[-1].rstrip("\n")+";"+id1
				
				newi="\t".join(str(p) for p in k2)+"\n"
				
				contigs[contig][-1]=(newstart,newend,newpid,newi)
			else:#don't catenate
				contigs[contig].append((start,end,pid,i))
			
for x in contigs.keys():

	for y in contigs[x]:
	
		g.write(y[3])
		


f.close()
g.close()

print("done")	
		
		
		
		