
#! /usr/bin/env python
import os
import sys
import re
import webbrowser
html = '<html> ...  "Harry just helped you in retriving columns taken from XAH :)" ...</html>'
path = os.path.abspath('Hail_Harry.html')
url = 'file://' + path
err_occur=[]
original=sys.stdout
count=0
#with open(path, 'w') as f:
file=open(path,'w')
print ("enter the alias of headers table")
#h=input()
file.write("Harry just helped you in retriving columns taken from XAH :)" +'<br><br>')
f =open('Hail_Harry.txt', 'w')
#file.write("Harry just helped you in retriving columns taken from XAH :)"+'\n')
pattern=re.compile(r"\b*Pushdown Optimization*Full\w*.\b",re.IGNORECASE)
with open ('sample.txt',"rt") as in_file:
    for line in in_file:
        if pattern.search(line)!=None:
            start=line.find('Pushdown Optimization.') +1
            end=line.find(' ',start)
            print (line[start:end])
            file.write(line[start:end]+'<br>')
            f.write(line[start:end]+'\n')
            count=count+1
            i=count
            print (count)
webbrowser.open(url)           
file.close()
f.close()

#html = '<html> ...  "Harry just helped you in retriving columns taken from XAH :)" ...</html>'
#path = os.path.abspath('Hail_Harry1.html')
#url = 'file://' + path
#c=0
#f1=open(path,'w')
#print ("enter lines table alias name:")

