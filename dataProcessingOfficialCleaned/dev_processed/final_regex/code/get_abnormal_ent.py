from os import listdir
import os
from os.path import isfile, join, isdir
import json
import letter
import number

def write_append_data_to_txt_file(full_path_to_file, txt):
    with open(full_path_to_file,'a') as out:
        out.write(f'{txt}\n')



def read_json(data_json):
    with open(data_json) as json_file:
        return json.load(json_file)


folder = \
    "/Users/n2t2k/Documents/Studying/Master/Thesis/InProgress/Coding/ORIGIN_RUN_ALL_edge-oriented-graph-master-studying/dataProcessingOfficialCleaned/dev_processed/final_regex/single_doc_files"

split_sentence_for_segmentation = f"{folder}/split_sentence_for_segmentation"

abnormal_ents_path = join(f"{folder}/debug_after_merge", "abnormal_ents.txt")
file_merge_all = join(folder, "file_merge_all.txt")

abnormal_chars = ["(",")", "'","’", '"', "/", ",", "‘"]

with open(abnormal_ents_path,'w') as out:
    out.write(f'')


s1 = u'ÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚÝàáâãèéêìíòóôõùúýĂăĐđĨĩŨũƠơƯưẠạẢảẤấẦầẨẩẪẫẬậẮắẰằẲẳẴẵẶặẸẹẺẻẼẽẾếỀềỂểỄễỆệỈỉỊịỌọỎỏỐốỒồỔổỖỗỘộỚớỜờỞởỠỡỢợỤụỦủỨứỪừỬửỮữỰựỲỳỴỵỶỷỸỹ'
s0 = u'AAAAEEEIIOOOOUUYaaaaeeeiioooouuyAaDdIiUuOoUuAaAaAaAaAaAaAaAaAaAaAaAaEeEeEeEeEeEeEeEeIiIiOoOoOoOoOoOoOoOoOoOoOoOoUuUuUuUuUuUuUuYyYyYyYy '
se = u"0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
vn_s = s1+s0+se
ent_type= [
    "PERSON",
    "ORGANIZATION",
    "LOCATION"
]

with open(file_merge_all,'r') as merge_all:
    id = None
    idx = 1
    for sent in merge_all:
        if len(sent.split()) and sent[8:11] not in  ("|a|","|t|"): 
            sent = sent.split("\t")
            if len(sent)>4:
                ent = sent[3]
                # if any(e in ent for e in abnormal_chars):
                flag = False
                if any(e not in vn_s for e in ent):   
                    flag = True  
                elif ent.strip() != ent:
                    flag = True  

                if flag:
                    if id != sent[0]:
                        write_append_data_to_txt_file(
                            abnormal_ents_path,
                            f"\n{idx}."
                        )
                        idx+=1
                    id = sent[0]

                    write_append_data_to_txt_file(
                        abnormal_ents_path,
                        f"{id}\t<{ent}>"
                    )
        

            
