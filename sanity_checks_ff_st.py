import os,glob,time
from bs4 import BeautifulSoup
currentDirABSPath=os.path.split(os.path.abspath(__file__))[0]
startTime=time.time();
def extractQueries(sourceFolder="SourceXMLs",targetFolder="Sanity_checks_op",targetFileExt=".txt"):
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
        print("------------------File Name------------------------")
        print("\n\nFilename:",os.path.split(inputFile)[1]);
        soup=BeautifulSoup(open(inputFile),"lxml")

        
        outputFile=inputFile.split(os.sep)[-1];
        outputFilePath=os.path.join(targetFolderABSPath,outputFile[:-4])+targetFileExt;


        code=open(outputFilePath,"w")
 

        
          

        task_type = soup.find_all("taskinstance", attrs = {"tasktype":"Session"})
        for each in task_type:
        
            if each["fail_parent_if_instance_fails"]!= 'YES':
                code.write("fail_parent_if_instance_fails should be yes")
                code.write("\n")
            else:
                code.write("fail_parent_if_instance_fails is ticked")
                code.write("\n")
            if each["fail_parent_if_instance_did_not_run"]!='YES':
                code.write("FAIL_PARENT_IF_INSTANCE_DID_NOT_RUN should be yes")
                code.write("\n")
            else:
                code.write("FAIL_PARENT_IF_INSTANCE_DID_NOT_RUN is ticked")
                code.write("\n")
            if each["reusable"]!='NO':
                code.write("reusable should be no")
                code.write("\n")
            else:
                code.write("reusable is not ticked")
                code.write("\n")
            if each["treat_inputlink_as_and"]!="YES":
                code.write("treat_inputlink_as_and should be yes")
                code.write("\n")
            else:
                code.write("treat_inputlink_as_and is ticked")
                code.write("\n")


        code.write("\n")
       
        configContents=soup.find_all("config",attrs={"name":["default_session_config"]})
        cList=[]
        configDict={}

        for instance in configContents:
            tempSrcName=instance['name']
            cList.append(tempSrcName)
            configDict[tempSrcName]={}.fromkeys(["Stop on errors","Save session log for these runs","Pre 85 Timestamp Compatibility","Override tracing"],"")
            instanceContents=instance.find_all("attribute",attrs={"name" : ["Stop on errors"]})
            for eachTag in instanceContents:
                if (eachTag['name']== "Stop on errors" and eachTag['value']!="1"):
                  code.write("Stop on errors should be 1")
                  code.write("\n")
                else:
                  code.write("Stop on errors is ticked")
                  code.write("\n")
                if (eachTag['name']== "Save session log for these runs" and eachTag['value']!="5"):
                  code.write("Save session log for these runs should be 5")
                  code.write("\n")
                else:
                  code.write("Save session log for these runs is ticked")
                  code.write("\n")
                if (eachTag['name']== "Pre 85 Timestamp Compatibility" and eachTag['value']!="YES"):
                  code.write("Pre 85 Timestamp Compatibility should be yes")
                  code.write("\n")
                else:
                  code.write("Pre 85 Timestamp Compatibility is ticked")
                  code.write("\n")
                  
                if (eachTag['name']== "Override tracing" and eachTag['value']!="Normal"):
                  code.write("Override tracing should be normal")
                  code.write("\n")
                else:
                  code.write("Override tracing is ticked")
                  code.write("\n")
            code.write("\n")


    
        sourceContents1=soup.find_all("transformation",attrs={"type":["Source Qualifier"]})
        sList1=[]
        sourcesDict1={}

        for instance in sourceContents1:
            tempSrcName=instance['name']
            sList1.append(tempSrcName)
            sourcesDict1[tempSrcName]={}.fromkeys(["Tracing Level"],"")
            instanceContents1=instance.find_all("tableattribute",attrs={"name" : ["Tracing Level"]})

            for eachTag in instanceContents1:
                if (eachTag['name']=="Tracing Level" and eachTag['value']!="Normal" ):
                 code.write("Tracing Level should be normal :"+instance['name'])
                 code.write("\n")




                    
        sessionwContents=soup.find_all("sessionextension",attrs={"name":["Relational Writer"]})
        sList=[]
        sessionDict={}

        for instance in sessionwContents:     
            tempSrcName=instance['name']
            sList.append(tempSrcName)
            instanceContents=instance.find_all("attribute",attrs={"name":["Target load type","Reject file directory" ,"Reject filename" ]})
            code.write(instance['sinstancename'])
            code.write("\n")
            for eachTag in instanceContents:

                if (eachTag['name']== "Target load type"):
                  code.write("Target load Type  :   "+eachTag['value'])
                  code.write("\n")
                  
                if (eachTag['name']== "Reject file directory" ):
                  code.write("Reject file directory:   "+eachTag['value'])
                  code.write("\n")
                 
                  
                if (eachTag['name']== "Reject filename" ):
             
                  code.write("Reject Filename is:   "+eachTag['value'])
                  code.write("\n\n")
                  
              



   
        sessionContents=soup.find_all("sessionextension",attrs={"name":["Relational Writer"]})
        sList=[]
        sessionDict={}

        for instance in sessionContents:     
            tempSrcName=instance['name']
            sList.append(tempSrcName)
            instanceContents=instance.find_all("attribute",attrs={"name":["Target load type"]})
            for eachTag in instanceContents:

                if (eachTag['name']== "Insert" and eachTag[value]!="YES"):
                 code.write(instance['sinstancename'])
                 code.write("   :insert should be yes")
                 code.write("\n")
                else:
                 code.write(instance['sinstancename'])
                 code.write("   :insert is ticked")
                 code.write("\n")
                 
                 if (eachTag['name']== "Update as Update" and eachTag[value]!="NO"):
                    code.write(instance['sinstancename'])
                    code.write("   :Update as Update should be no")
                    code.write("\n")
                 else:
                  code.write(instance['sinstancename'])
                  code.write("   :Update as Update is  not ticked")
                  code.write("\n")

                 if (eachTag['name']== "Update as Insert" and eachTag[value]!="NO"):
                   code.write(instance['sinstancename'])
                   code.write("   :Update as Insert should be no")
                   code.write("\n")
                 else:
                  code.write(instance['sinstancename'])
                  code.write("   :Update as Insert is  not ticked")
                  code.write("\n")
                 
                 if (eachTag['name']== "Update else Insert" and eachTag[value]!="NO"):
                    code.write(instance['sinstancename'])
                    code.write("   :Update else Insert should be no")
                    code.write("\n")
                 else:
                  code.write(instance['sinstancename'])
                  code.write("   :Update else Insert is  not ticked")
                  code.write("\n")
            
            code.write("\n\n")
        sessionProps = soup.find_all("sesstransformationinst",attrs={"transformationtype":["Target Definition"]})
        dict_props = {}.fromkeys(["Table Name Prefix"],"")
        for eachTag in sessionProps:
            each = eachTag.find_all("attribute", attrs = {"name":["Table Name Prefix"]})
            for i in each:
                dict_props[i["name"]] = i["value"]
                code.write(eachTag['sinstancename'])
                code.write("   :Table Prefix name:   "+dict_props[i["name"]])
                code.write("\n")


        code.write("\n\n")
        session_Config = soup.find_all("attribute", attrs = {"name":["Pushdown Optimization","Session Log File Name","Session Log File directory","Parameter Filename"]})
        for each in session_Config:
            if (each['name'] == "DTM buffer size"):
              code.write("DTM buffer size:   "+each['value'])
              code.write("\n")
          
            if (each['name'] == "Pushdown Optimization"):
              code.write("Pushdown Optimization :    "+each['value'])
              code.write("\n")

            if (each['name'] == "Session Log File Name"):
             code.write("Session Log File Name:   "+each['value'])
             code.write("\n")

            if (each['name'] == "Session Log File directory"):
                 code.write("Session Log File directory:   "+each['value'])
                 code.write("\n")
            if (each['name'] == "Parameter Filename" and each['value']!= ""):
                    code.write("\nParameter File Name:   "+each['value'])
                    code.write("\n")


       

        code.close();

extractQueries()
endTime=time.time()
execTime=endTime-startTime
print("\tExecution Time : %f secs"%execTime);

