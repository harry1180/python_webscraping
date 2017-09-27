import os,glob,time
from bs4 import BeautifulSoup
currentDirABSPath=os.path.split(os.path.abspath(__file__))[0]
startTime=time.time();
def extractQueries(sourceFolder="SourceXMLs",targetFolder="TargetTXTs2",targetFileExt=".txt"):
    sourceFolderABSPath=os.path.join(currentDirABSPath,sourceFolder);
    targetFolderABSPath=os.path.join(currentDirABSPath,targetFolder);
    try:
        os.mkdir(targetFolderABSPath)
    except:
        pass
    stringtoGetXMLs=os.path.join(sourceFolder,"*.xml")
    filesList=glob.glob(stringtoGetXMLs);
    #print("ABS1",sourceFolderABSPath);
    #print("ABS2",targetFolderABSPath);
    for inputFile in filesList:
        print("Filename:",os.path.split(inputFile)[1]);
        soup=BeautifulSoup(open(inputFile),"lxml")
        outputFile=inputFile.split(os.sep)[-1];
        outputFilePath=os.path.join(targetFolderABSPath,outputFile[:-4])+targetFileExt;
        code=open(outputFilePath,"w")

        tgtLoadOrders=soup.find_all("targetloadorder")
        tgtLoadOrdersList=[None]*len(tgtLoadOrders)
        for eachTag in tgtLoadOrders:
            tgtLoadOrdersList[int(eachTag['order'])-1]=eachTag['targetinstance']
        #print("tgtLoadOrdersList : ",tgtLoadOrdersList)

        
        tgtLoadOrdersDict={}.fromkeys(range(0,len(tgtLoadOrders)),[])
        #print("tgtLoadOrdersDict : ",tgtLoadOrdersDict)
        for eachTag in tgtLoadOrders:
            tempList=[]
            tempList.append(eachTag['targetinstance'])
            tgtLoadOrdersDict[int(eachTag['order'])-1]=tgtLoadOrdersDict[int(eachTag['order'])-1]+tempList
        #print("tgtLoadOrdersDict : ",tgtLoadOrdersDict)
        
        
        SQnExpMappingDict={}
        SQnExpConnections=soup.find_all("connector",attrs={"frominstancetype":["Source Qualifier"],"toinstancetype":["Expression"]})
        for eachTag in SQnExpConnections:
            if eachTag['toinstance'] not in SQnExpMappingDict.keys():
                SQnExpMappingDict[eachTag['toinstance']]=eachTag['frominstance']
        #print("SQnExpMappingDict : ",SQnExpMappingDict)

        ExpnTgtMappingDict={}
        ExpnTgtConnections=soup.find_all("connector",attrs={"frominstancetype":["Expression"],"toinstancetype":["Target Definition"]})
        for eachTag in ExpnTgtConnections:
            if eachTag['toinstance'] not in ExpnTgtMappingDict.keys():
                #ExpnTgtMappingDict[eachTag['toinstance']]=eachTag['frominstance']
                ExpnTgtMappingDict[eachTag['toinstance']]=SQnExpMappingDict[eachTag['frominstance']] #to map Source Qualifiers with their respective target definitions 
        #print("ExpnTgtMappingDict : ",ExpnTgtMappingDict)

        Tgt2SrcMappingDict={}
        Tgt2SrcMappingDict.update(ExpnTgtMappingDict)
        SQnTgtConnections=soup.find_all("connector",attrs={"frominstancetype":["Source Qualifier"],"toinstancetype":["Target Definition"]})
        for eachTag in SQnTgtConnections:
            if eachTag['toinstance'] not in Tgt2SrcMappingDict.keys():
                Tgt2SrcMappingDict[eachTag['toinstance']]=eachTag['frominstance']
        #print("Tgt2SrcMappingDict : ",Tgt2SrcMappingDict)
                



        
        sourceContents=soup.find_all("transformation",attrs={"type":["Source Qualifier"]})
        sList=[]
        sourcesDict={}

        for instance in sourceContents:
            tempSrcName=instance['name']
            sList.append(tempSrcName)
            sourcesDict[tempSrcName]={}.fromkeys(["Sql Query","Pre SQL","Post SQL"],"")
            instanceContents=instance.find_all("tableattribute",attrs={"name" : ["Sql Query","Pre SQL","Post SQL"]})
            for eachTag in instanceContents:
                if (eachTag['name']== "Sql Query"):
                    sourcesDict[tempSrcName]["Sql Query"]=eachTag['value'];
                elif (eachTag['name']== "Pre SQL"):
                    sourcesDict[tempSrcName]["Pre SQL"]=eachTag['value'];
                elif (eachTag['name']== "Post SQL"):
                    sourcesDict[tempSrcName]["Post SQL"]=eachTag['value'];


        sourceContents2=soup.find_all("sesstransformationinst",attrs={"transformationtype":["Source Qualifier"]})        
        for instance in sourceContents2:
            tempSrcName=instance['sinstancename']
            if tempSrcName not in sList:
                sList.append(tempSrcName)
                sourcesDict[tempSrcName]={}.fromkeys(["Sql Query","Pre SQL","Post SQL"],"")
            instanceContents=instance.find_all("attribute",attrs={"name" : ["Sql Query","Pre SQL","Post SQL"]})
            for eachTag in instanceContents:
                if (eachTag['name']== "Sql Query"):
                    if len(eachTag['value'])>0:
                        sourcesDict[tempSrcName]["Sql Query"]=eachTag['value'];
                elif (eachTag['name']== "Pre SQL"):
                    if len(eachTag['value'])>0:
                        sourcesDict[tempSrcName]["Pre SQL"]=eachTag['value'];
                elif (eachTag['name']== "Post SQL"):
                    if len(eachTag['value'])>0:
                        sourcesDict[tempSrcName]["Post SQL"]=eachTag['value'];

       


        
        """print ("Sources List : ",sList);
        sList.sort()
        print ("Sorted Targets List : ",sList);
        temp=0
        for key in sList:
            temp+=1;
            print("Source%d Name : "%temp,key);
            code.write("\n\n\nSource Name : "+key);
            #print("SQL Query : \n",sourcesDict[key]["Sql Query"]);
            code.write("\n\n\nSQL Query : \n"+sourcesDict[key]["Sql Query"]);
            #print("Pre SQL : \n",sourcesDict[key]["Pre SQL"]);
            code.write("\n\n\nPre SQL : \n"+sourcesDict[key]["Pre SQL"]);
            #print("Post SQL : \n",(sourcesDict[key]["Post SQL"].rjust(50)))
            code.write("\n\n\nPost SQL : \n"+sourcesDict[key]["Post SQL"]);"""

        targetContents=soup.find_all("instance",attrs={"transformation_type":["Target Definition"]})
        tList=[]
        targetsDict={}
        for instance in targetContents:
            tempTgtName=instance['transformation_name']
            tList.append(tempTgtName)
            targetsDict[tempTgtName]={}.fromkeys(["Pre SQL","Post SQL"],"")
            instanceContents=instance.find_all("tableattribute",attrs={"name" : ["Pre SQL","Post SQL"]})
            for eachTag in instanceContents:
                if (eachTag['name']== "Pre SQL"):
                    targetsDict[tempTgtName]["Pre SQL"]=eachTag['value'];
                elif (eachTag['name']== "Post SQL"):
                    targetsDict[tempTgtName]["Post SQL"]=eachTag['value'];


        targetContents2=soup.find_all("sesstransformationinst",attrs={"transformationtype":["Target Definition"]})

        for instance in targetContents2:
            tempTgtName=instance['sinstancename']
            if tempTgtName not in tList:
                tList.append(tempTgtName)
                targetsDict[tempTgtName]={}.fromkeys(["Pre SQL","Post SQL"],"")
            instanceContents=instance.find_all("attribute",attrs={"name" : ["Pre SQL","Post SQL"]})
            for eachTag in instanceContents:
                if (eachTag['name']== "Pre SQL"):
                    if len(eachTag['value'])>0:
                        targetsDict[tempTgtName]["Pre SQL"]=eachTag['value'];
                elif (eachTag['name']== "Post SQL"):
                    if len(eachTag['value'])>0:
                        targetsDict[tempTgtName]["Post SQL"]=eachTag['value'];


                    
        """print ("Targets List : ",tList);
        tList.sort()
        print ("Sorted Targets List : ",tList);
        temp=0
        for key in tList:
            temp+=1;
            print("Target%d Name : "%temp,key);
            code.write("\n\n\nTarget%d Name : "%temp+key);
            #print("Pre SQL : \n",targetsDict[key]["Pre SQL"]);
            code.write("\n\n\nPre SQL : \n"+targetsDict[key]["Pre SQL"]);
            #print("Post SQL : \n",(targetsDict[key]["Post SQL"].rjust(50)))
            code.write("\n\n\nPost SQL : \n"+targetsDict[key]["Post SQL"]);

        tgtLoadOrders=soup.find_all("targetloadorder")
        tgtLoadOrdersList=[None]*len(tgtLoadOrders)
        for eachTag in tgtLoadOrders:
            tgtLoadOrdersList[int(eachTag['order'])-1]=eachTag['targetinstance']
        print("tgtLoadOrdersList : ",tgtLoadOrdersList)

        SQnTgtConnections=soup.find_all("connector",attrs={"frominstancetype":["Source Qualifier"],"toinstancetype":["Target Definition"]})
        Tgt2SrcMappingDict={}
        for eachTag in SQnTgtConnections:
            if eachTag['toinstance'] not in Tgt2SrcMappingDict.keys():
                Tgt2SrcMappingDict[eachTag['toinstance']]=eachTag['frominstance']
        print("Tgt2SrcMappingDict : ",Tgt2SrcMappingDict)"""
        
        print ("Sources List : ",sList);
        print("Targets List : ",tList);
        print("tgtLoadOrdersList : ",tgtLoadOrdersList)
        print("tgtLoadOrdersDict : ",tgtLoadOrdersDict)

        print("SQnExpMappingDict : ",SQnExpMappingDict)
        print("ExpnTgtMappingDict : ",ExpnTgtMappingDict)
        print("Tgt2SrcMappingDict : ",Tgt2SrcMappingDict)
       
        
        temp=0
        for num in tgtLoadOrdersDict.keys():
            temp+=1;
            temp2=0
            for tgtKey in tgtLoadOrdersDict[num]:
                temp2+=1;
                srcKey=Tgt2SrcMappingDict[tgtKey]
                if temp2==1:
                    print("Source%d Name : "%temp,srcKey);
                    code.write("\n\n\nSource%d Name : "%temp+srcKey);
                    #print("Pre SQL : \n",sourcesDict[srcKey]["Pre SQL"]);
                    code.write("\n\n\nPre SQL : \n"+sourcesDict[srcKey]["Pre SQL"].replace("\r",""));
                    #print("SQL Query : \n",sourcesDict[srcKey]["Sql Query"));
                    code.write("\n\n\nSQL Query : \n"+sourcesDict[srcKey]["Sql Query"].replace("\r",""));
                    #print("Post SQL : \n",(sourcesDict[srcKey]["Post SQL"].rjust(50)))
                    code.write("\n\n\nPost SQL : \n"+sourcesDict[srcKey]["Post SQL"].replace("\r",""));

                    print("Target%d Name : "%temp,tgtKey);
                    code.write("\n\n\nTarget%d Name : "%temp+tgtKey);
                    #print("Pre SQL : \n",targetsDict[tgtKey]["Pre SQL"]);
                    code.write("\n\n\nPre SQL : \n"+targetsDict[tgtKey]["Pre SQL"].replace("\r",""));
                    #print("Post SQL : \n",(targetsDict[tgtKey]["Post SQL"].rjust(50)))
                    code.write("\n\n\nPost SQL : \n"+targetsDict[tgtKey]["Post SQL"].replace("\r",""));
                if temp2>1:
                    print("Target%d-%d Name : "%(temp,temp2),tgtKey);
                    #print("Target%d Name : "%temp,tgtKey);
                    code.write("\n\n\nTarget%d-%d Name : "%(temp,temp2)+tgtKey);
                    #print("Pre SQL : \n",targetsDict[tgtKey]["Pre SQL"]);
                    code.write("\n\n\nPre SQL : \n"+targetsDict[tgtKey]["Pre SQL"].replace("\r",""));
                    #print("Post SQL : \n",(targetsDict[tgtKey]["Post SQL"].rjust(50)))
                    code.write("\n\n\nPost SQL : \n"+targetsDict[tgtKey]["Post SQL"].replace("\r",""));
                
            

        code.close();
        """code=open(outputFilePath,"r+")
        content=code.read()
        #print(repr(content))
        #content.replace("\\r","")
        code.write(content)
        code.close()"""
        print ("###############################\n");
    print ("Log : \n\tNo.of Processed Files : %d "%len(filesList));
    


print("""\t\t\t\tWelcome
            This version is tested on Python 3.6
""");
extractQueries()
endTime=time.time()
execTime=endTime-startTime
print("\tExecution Time : %f secs"%execTime);

