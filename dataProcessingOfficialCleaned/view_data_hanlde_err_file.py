"""
BACKUP code 
# print(tsv_read_df.shape[0])
#[tsv_read_df.iloc[:,5].isna().sum()] )
["23352816.conll", "23352769.conll", "23352702.conll", "23357329.conll", "23352733.conll", "24492634.txt"]

"""



path = "23352901.conll/CURATION_USER (1).tsv"
# f = open(path, "r")
# print(f.read())
import pandas as pd
import csv
# tsv_read_df = pd.read_fwf(path)

import os
from pprint import pprint
from os.path import isfile, join, isdir
from os import listdir
# import openpyxl 
import shutil


# wb_obj = openpyxl.load_workbook(path) 
# sheet_obj = wb_obj.active 


# MAX = 10000
# LIMIT_LEN_A_LINE = 100 
# end_line = 0
# for i in range(10,MAX,1):
#     cell_obj = sheet_obj.cell(row = i, column = 1)
#     if cell_obj.value is None:
#         end_line = i-1
#         break
    # print(i, cell_obj.value)
    # print(f"end line {i}")
    # print(cell_obj.value)
# print("end line", end_line)
# cell_obj = sheet_obj.cell(row = end_line, column = 3)
# print( len((cell_obj.value)) )


# # /Users/n2t2k/Documents/Studying/Master/Thesis/InProgress/DataVLSP2020/VLSP2020_RE_test
mypath = '../../DataVLSP2020/VLSP2020_RE_test'
# mypath = ''
# onlydir = [ d for d in listdir(mypath) if isdir(join(mypath, d))]

# print(len(onlydir))
# print(">"*20)
# # print(listdir(mypath)
# listdirls = listdir(mypath)
# print(len(listdirls))


# folder = listdirls[50]
# print(folder)
# path_to_file = join(mypath, folder)
# path_to_file = "/Users/n2t2k/Documents/Studying/Master/Thesis/InProgress/SmallCode/dataProcessing/23351164.dev"
# # file_name = "CURATION_USER.tsv"
# file_name = "CURATION_USER copy.tsv"
# file_name = "CURATION_USER_26.tsv"


# full_path_to_file = join(path_to_file,file_name)
# full_path_to_file = "/Users/n2t2k/Documents/Studying/Master/Thesis/InProgress/SmallCode/dataProcessing/dev/23352592.conll/CURATION_USER copy.tsv"
# print(isfile(full_path_to_file))


def get_sentence_line_number(full_path_to_file, sent_line_number=True):
    N = 10
    with open(full_path_to_file, "r") as file:  # the a opens it in append mode
        for i in range(N):
            line = next(file).strip()
            # print(i,line[:6])
            if line[:6] ==  "#Text=":
                if sent_line_number:
                    return i
                else:
                    return line

def has_relation(tsv_read_df):
    rel_col_null_count = [tsv_read_df.iloc[:,5].isnull().sum()][0]

    if len(tsv_read_df.index) == rel_col_null_count:
        # print("empty relation >>> ", rel_col_null_count) 
        # print(tsv_read_df.iloc[:,5])

        return False
    return True


def create_folder_for_dev_processed_files(parent_dir):
    exclude_folder = ['no_relation', "error_files", "worked_files_excell", "skip_review_later"]
    for fl in exclude_folder:
        path = os.path.join(parent_dir, fl)
        if not isdir(path):
            os.mkdir(path)


def write_append_data_to_txt_file(full_path_to_file, lines):
    with open(full_path_to_file,'a') as out:
        for l in lines:
            out.write(f'{l},')
            

# sentence_line_number = get_sentence_line_number(full_path_to_file, True)
# print("sentence_line_number >>>" , sentence_line_number \
#         if str(sentence_line_number).isnumeric() else sentence_line_number[:50])


# tsv_read_df = pd.read_csv(full_path_to_file, sep='\t', encoding = 'utf-8',  skiprows=sentence_line_number+1, header=None)
# tsv_read_df = pd.read_csv(full_path_to_file, sep="\t", encoding = 'utf-8',  skiprows=10, header=None, quoting =3).replace('"','', regex=True)


# try:
# tsv_read_df = pd.read_csv(full_path_to_file, sep='\t', encoding = 'utf-8',  skiprows=5, nrows=1, header=None)
# tsv_read_df = pd.read_csv(full_path_to_file, sep='\t', encoding = 'utf-8',  skiprows=4, nrows=1, header=None)
# tsv_read_df = pd.read_csv(full_path_to_file, nrows=10)





# cols = ["index_org", "start_end", "text", "ent_no", "ent_type", "rel", "rel_pair", "last"]
# tsv_read_df.columns = cols

# save sentence to excell for reading

# sentence = pd.read_csv(full_path_to_file, sep='\t', encoding = 'utf-8', skiprows=4,  nrows=1,  header=None)
# full_path_to_file_excell_view = join(path_to_file,'data_new_excell_sentence.xlsx')
# tsv_read_df.to_excel(full_path_to_file_excell_view, encoding='utf-8', index=False)

dev_test_folder = \
        "/Users/n2t2k/Documents/Studying/Master/Thesis/InProgress/Coding/ORIGIN_RUN_ALL_edge-oriented-graph-master-studying/dataProcessingOfficialCleaned"

def save_excell_for_view(mypath, data_set="dev"):
    if data_set=="dev":
        mypath_data = f"{mypath}/VLSP2020_RE_dev"
        dev_processed = f"{mypath}/dev_processed"
    else:
        mypath_data = f"{mypath}/VLSP2020_RE_train"
        dev_processed = f"{mypath}/train_processed"
    create_folder_for_dev_processed_files(dev_processed)

    # print("data_set ", data_set)
    # return

    no_relation_file = join(dev_processed,f"no_relation.txt")
    double_quote_err_file = join(dev_processed,f"double_quote_err.txt")
    data_errors_files = join(dev_processed,f"data_errors_files.txt")

    with open(no_relation_file, 'w') as f:
        f.write('')
    with open(double_quote_err_file, 'w') as f:
        f.write('')
    with open(data_errors_files, 'w') as f:
        f.write('')

    # if isfile(double_quote_err_file):
    #     os.remove(double_quote_err_file)

    exclude_folder = ['no_relation', "error_files", "worked_files_excell", "skip_review_later"]
    sub_folder_ls = [ d for d in listdir(mypath_data) if ( isdir(join(mypath_data, d)) and d not in exclude_folder)]
    print("onlydir ", sub_folder_ls)
    
    total, double_quote, no_relation,skip_review_later, worked_files, data_errors_ = 0,0,0,0,0,0
    for fd in sub_folder_ls:
        print(f"{total}.___")
        total+=1
        if fd in ["23352000.conll"]:
        # if fd in ["23352816.conll", "23352600.conll", "23352014.conll","23352620.conll","23352605.conll"]: # dev 9 cols/ 91.1
            tsv_read_df.to_excel(join(dev_processed,f"skip_review_later/{fd}.xlsx"), encoding='utf-8', index=False)
            skip_review_later+=1
            write_append_data_to_txt_file(join(dev_processed,f"no_relation.txt"), [fd])                    
            continue
        print(f"working on ------------ {fd}")
        full_path_to_file = join(f"{mypath_data}/{fd}","CURATION_USER.tsv")
        if not isfile(full_path_to_file):
            full_path_to_file = join(f"{mypath_data}/{fd}","CURATION_USER (1).tsv")

        # print(fd)
        try:
            sentence_line_number = get_sentence_line_number(full_path_to_file, True)
            tsv_read_df = pd.read_csv(full_path_to_file, sep='\t', encoding = 'utf-8', skiprows=sentence_line_number+1, header=None)

            try:
                if data_set=="dev":
                    data_errors_files_ls =  ["23352517.conll", "23352491.conll", "23352491.conll", 
                    "23352654.conll", "23352410.conll", "23352457.conll", "23352014.conll",
                    "23352620.conll", "23352337.conll", "23352090.conll", "23352393.conll", "23352110.conll", "23352110.conll" ] #23352110 ent with *
                elif data_set=="train":
                    data_errors_files_ls = ["23352802.conll","23353967.conll","23352730.conll","23352753.conll","23357329.conll",
                                "23354982.conll","23352696.conll","23351970.conll","23352690.conll","23357095.conll",
                                "23353864.conll","23356245.conll","23354400.conll","23351841.conll","23355817.conll",
                                "23352857.conll","23351556.conll","23351489.conll","23352814.conll", "23351516.conll",
                                "23355290.conll","23352738.conll","23353874.conll","23351672.conll","23354619.conll", "23352695.conll"] #23352695 ent with *
                else:
                    data_errors_files_ls =  ["23352517.conll", "23352491.conll", "23352491.conll", 
                    "23352654.conll", "23352410.conll", "23352457.conll", "23352014.conll",
                    "23352620.conll", "23352337.conll", "23352090.conll", "23352393.conll"]

                if fd in data_errors_files_ls:
                    data_errors_+=1
                    tsv_read_df.to_excel(join(dev_processed,f"data_errors_files_excell/{fd}.xlsx"), encoding='utf-8', index=False)
                    write_append_data_to_txt_file(join(dev_processed,f"data_errors_files.txt"), [fd]) 
                    continue
    
                tsv_read_df_org_idx = tsv_read_df.iloc[:,0]
                for name, values in tsv_read_df_org_idx.iteritems():
                    int(values.split("-")[1])
            except:
                data_errors_+=1
                tsv_read_df.to_excel(join(dev_processed,f"data_errors_files_excell/{fd}.xlsx"), encoding='utf-8', index=False)
                write_append_data_to_txt_file(join(dev_processed,f"data_errors_files.txt"), [fd]) 
                continue



            # print(len(tsv_read_df.columns))
            if len(tsv_read_df.columns) < 7:
                print("no relation? >>>", fd)
                if not has_relation(tsv_read_df):
                    print("no relation ")
                    print("\t confirm relation >>>", fd)
                    tsv_read_df.to_excel(join(dev_processed,f"no_relation/{fd}.xlsx"), encoding='utf-8', index=False)
                    no_relation+=1                    
                    write_append_data_to_txt_file(join(dev_processed,f"no_relation.txt"), [fd])                    
                    continue
        except:
            print(f"file with double quote???: {fd}")
            shutil.copy(full_path_to_file, join(dev_processed,f"error_files/{fd}.tsv"))
            double_quote+=1
            write_append_data_to_txt_file(join(dev_processed,f"double_quote_err.txt"), [fd])
            continue




# ref_ent = int( ref_ent_org.split("-")[1] )

        tsv_read_df.columns = ["index_org", "start_end", "text", "ent_no", "ent_type", "rel", "rel_pair", "last"]
        # read sentence
        tsv_read_df.to_excel(join(dev_processed,f"worked_files_excell/{fd}.xlsx"), encoding='utf-8', index=False)
        worked_files+=1
        
    print("-"*150, '\n'*3)
    print("-"*50, data_set, "-"*50)
    print(f"total: {total}")
    print(f"double_quote: {double_quote}")
    print(f"no_relation: {no_relation}")
    print(f"skip_review_later: {skip_review_later}")
    print(f"data_errors_: {data_errors_}")
    print(f"worked_files: {worked_files}")

    # full_path_to_file = join(f"{mypath}/{fd}","CURATION_USER.tsv")
    # print(isfile(full_path_to_file), fd)
    # # print(fd)
    # tsv_read_df = pd.read_csv(full_path_to_file, sep='\t', encoding = 'utf-8',  skiprows=50, header=None)
    # # tsv_read_df.columns = ["index_org", "start_end", "text", "ent_no", "ent_type", "rel", "rel_pair", "last"]
    # # # read sentence
    # # tsv_read_df.to_excel(join(mypath,f"{fd}.xlsx"), encoding='utf-8', index=False)


save_excell_for_view(dev_test_folder,"dev")
# save_excell_for_view(dev_test_folder,"train")





#------------------------------------------------#------------------------------------------------

# for df in tsv_read_df:
#     print(df)

# print(tsv_read_df.columns)
print("- "*50)



# # print(tsv_read_df.iloc[-5:-1,])
# print(tsv_read_df.iloc[0,0])
# print(tsv_read_df.head(5))
# print(tsv_read_df.tail(5))
print("- "*50)

# tsv_read_df = tsv_read_df.iloc[3:]
# tsv_read_df = tsv_read_df.iloc[1:]
