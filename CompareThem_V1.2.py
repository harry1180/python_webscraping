from bs4 import BeautifulSoup
soup=BeautifulSoup(open("wf_ST_XXTSL_XAAS_TRANSACTION.xml"),"lxml")
code=open("code.txt","w")











transformationContents=soup.find_all("tableattribute",attrs={"name" : ["Sql Query","Pre SQL","Post SQL"]})
temp=0;
sList=[]
print("length",len(transformationContents));
for i in transformationContents:
    if (i.parent['name'] not in sList):
        temp+=1;
        #print ("Source%d : "%temp+i.parent['name']+"\n");
        sList.append(i.parent['name'])
        code.write("\nSource%d : "%temp+i.parent['name']+"\n");
    #print (i['name']+" : \n"+i['value']+"\n");
    code.write("\n"+i['name']+" : \n"+i['value']+"\n");

sessionContents=soup.find_all("attribute",attrs={"name" : ["Pre SQL","Post SQL"]})
temp=0;
tList=[]
for i in sessionContents:
    if (i.parent['sinstancename'] not in tList):
        temp+=1;
        #print ("Target%d : "%temp+i.parent['sinstancename']+"\n");
        tList.append(i.parent['sinstancename'])
        code.write("\nTarget%d : "%temp+i.parent['sinstancename']+"\n");
    #print (i['name']+" : \n"+i['value']+"\n");
    code.write("\n"+i['name']+" : \n"+i['value']+"\n");

print(sList,"\n",tList)
code.close();
