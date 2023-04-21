import gzip
import shutil
    
def unzip(zipped_file_name):    
    unzipped_file = 'enwiki-latest-abstract.xml'
    with gzip.open(filename=zipped_file_name, mode='rb') as f_in:
        with open(unzipped_file, mode='wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

    return unzipped_file

def trunc(unzipped):
    with open(unzipped, mode='r') as in_f:
        full_str = ""
        for i in range(12000):
            full_str += in_f.readline()
    with open(f"truncated_{unzipped}", mode='w')as out_f:
        out_f.write(full_str)
        


file_name = "/home/drews/LLMHumanModeling/data/wiki/enwiki-latest-abstract.xml.gz"
new_f = unzip(zipped_file_name=file_name)
trunc(new_f)
