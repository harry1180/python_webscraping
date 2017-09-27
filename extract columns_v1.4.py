import re
import sys
err_occur=[]
original=sys.stdout
count=0
file =open('output.txt', 'w')
pattern=re.compile(r"\bXAH\w*.\b",re.IGNORECASE)
with open ('sample.txt',"rt") as in_file:
    for line in in_file:
        if pattern.search(line)!=None:
            start=line.find('XAH.') +4
            end=line.find(' ',start)
            print (line[start:end])
            file.write(line[start:end]+'\n')
            
            count=count+1
            i=count
           
file.close()



            

            
        
        
        #if pattern.search(line)!=None:
            #print(line,end='')
            #m=re.search('XAH.(.+?) ', line)
            #found=m.group(1)
                
            

     
            
            
            
