import xlrd


def Validation(filename):
    wb = xlrd.open_workbook(filename)
    
    n= wb.sheet_names()
    
    first_sheet = wb.sheet_by_index(0)
    cell = first_sheet.cell(0,0)
    dd1 = {}
    dd2={}
    for i in range(first_sheet.nrows):
        cell = first_sheet.cell(i,0)
        if 'Source Server Details' in str(cell):
            for j in range(5):
                k=i+j
                #print(first_sheet.cell(k+1,0),first_sheet.cell(k+1,1))
                dd1.update({str(first_sheet.cell(k+1,0)).replace('text:','').strip('\''):str(first_sheet.cell(k+1,1)).replace('text:','').strip('\'')}) 
        if 'Target Server Details' in str(cell):
            for j in range(5):
                k=i+j
                dd2.update({str(first_sheet.cell(k+1,0)).replace('text:','').strip('\''):str(first_sheet.cell(k+1,1)).replace('text:','').strip('\'')}) 
        if 'Source Disk Details' in str(cell):
            for j in range(5):
                k=i+j
                if len(str(first_sheet.cell(k+1,0)).replace('text:',''))>2:
                    #print(first_sheet.cell(k+1,0),first_sheet.cell(k+1,1))
                    dd1.update({str(first_sheet.cell(k+1,0)).replace('text:','').strip('\''):str(first_sheet.cell(k+1,1)).replace('text:','').strip('\'')})
                else:
                    break
        if 'Target Disk Details' in str(cell):
            for j in range(100):
                k=i+j
                if k<(first_sheet.nrows)-1 and len(str(first_sheet.cell(k+1,0)).replace('text:',''))>3: 
                    dd2.update({str(first_sheet.cell(k+1,0)).replace('text:','').strip('\''):str(first_sheet.cell(k+1,1)).replace('text:','').strip('\'')}) 
                else:
                    break
    
    
    
    for source,target in zip(dd1,dd2):
        if dd1[source]==dd2[target]:
            print('Test for {} is passed and the value is {}'.format(source,dd1[source]))
        else:
            print('Test for {} is failed and the value for source is {} and the value for target is {}'.format(source, dd1[source], dd2[target]))
import os,glob
#Validation('abc.xlsx')
currentDirABSPath=os.path.split(os.path.abspath(__file__))[0]
stringtoGetxlsx=os.path.join(currentDirABSPath,"*.xlsx")
filesList=glob.glob(stringtoGetxlsx)
print(stringtoGetxlsx)
for inputFile in filesList:
    print("Started Validation for Filename:{}".format(os.path.split(inputFile)[1]))
    filename = os.path.split(inputFile)[1]
    print('\n')
    try:
        Validation(filename)
    except Exception as e:
        print(e)
        continue
    finally:
        print('Validation is completed for {}'.format(filename))
