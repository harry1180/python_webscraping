import xlrd
import csv
import json
def csv_from_excel():
    wb = xlrd.open_workbook('ISO10383_MIC.xls')
    sh = wb.sheet_by_name('MICs List by CC')
    your_csv_file = open('your_csv_file.csv', 'w')
    wr = csv.writer(your_csv_file, quoting=csv.QUOTE_ALL)

    for rownum in range(sh.nrows):
        wr.writerow(sh.row_values(rownum))

    your_csv_file.close()
with open('your_csv_file.csv') as f:
    
    a = [{k: str(v) for k, v in row.items()}
         for row in csv.DictReader(f, skipinitialspace=True)]
    with open ('output.json','w') as o:
        
        for item in a:
            json.dump(item, o, indent=4, sort_keys=True)
            o.write('\n,')

def s3_file_upload(local_file, s3_bucket, s3_path, s3_file_nm='default', aws_profile=AWS_PROFILE):

    if s3_file_nm == 'default':
        s3_file_nm = os.path.basename(local_file)


    conn = S3Connection(profile_name=aws_profile)
    bucket = conn.get_bucket(s3_bucket)
    key_name = s3_file_nm
    full_key_name = os.path.join(s3_path, key_name)
    k = bucket.new_key(full_key_name)
    k.set_contents_from_filename(local_file)

print('end')
