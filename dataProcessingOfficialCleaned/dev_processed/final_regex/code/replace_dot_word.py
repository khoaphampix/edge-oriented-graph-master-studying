from os import listdir
import os
from os.path import isfile, join, isdir
import json
import letter
import number
import dot_ent
def write_append_data_to_txt_file(full_path_to_file, txt):
    with open(full_path_to_file,'a') as out:
        # out.write(f'{txt}\n')
        out.write(f'{txt}')



def read_json(data_json):
    with open(data_json) as json_file:
        return json.load(json_file)


def check_replace_word(line, word, letter_j, number_j):
    for k , v in letter_j:
        if k in word :
            if len(k) == 2:
                if k== word:
                    return True, word.replace(k,v)
            else:
                return True, word.replace(k,v)

    for k , v in number_j:
        if k in word :
            if len(k) in [3,4,5] and ("," not in word):
                if k == word:
                    return True, word.replace(k,v)
            else:
                return True, word.replace(k,v)
    return None, word


def hard_list_replace(filename, special_letter, special_number):
    special_ls = special_letter+special_number
    with open(filename, "r") as file:
        row_list = []
        org_row_list = []


        for line in file:
            sent = line[8:11] in ("|a|","|t|")
            line_new = f"{line}"
            ls = line_new.split("...")   
            if (not sent) and  ls:
                line_new = line_new.replace("...","   ") # ... in entity
            # print(len(ls), sent)
            if sent and len(ls) > 1:
                i = 0
                for j in ls:
                    if i > 0:
                        print(i, len(j), "...")
                        if(ls[i].strip()) == "":
                            line_new = line_new.replace("...","   ",1) # ... ...
                        elif(ls[i].strip())[0].isupper():
                            line_new = line_new.replace("...","  .",1) # ... Cha
                        else:
                            line_new = line_new.replace("...","   ",1) # ... cont
                    i+=1
            
            line_new = line_new.replace(".."," .") # .. Cha
            line_new = line_new.replace("…"," ") # .. Cha'
            for txt in special_ls:
                line_new = line_new.replace(txt[0], txt[1]) # .. Cha'


            org_row_list.append(line)
            row_list.append(line_new)

    return row_list, org_row_list

def replace_again(row_list, final_debug_ls, dot_ent):
    row_list_new = []
    for row in row_list:
        for final_lt in final_debug_ls:
            row = row.replace(final_lt[0], final_lt[1])

        if len(row.strip()):
            doc_id = dot_ent.get(row[:8], None)
            if doc_id:
                for w in doc_id:
                    row = row.replace(w[0],w[1])

        row_list_new.append(row)
    return row_list_new

def create_json_number_fn_split(filename, out_put, letter_j, number_j, dict_arg={}):
    
    # with open(out_put,'w') as out:
    #     out.write("")

    dot_ent = dict_arg["dot_ent"]


    letter_j, special_letter, final_debug_letter = letter_j
    number_j, special_number, final_debug_num = number_j

    final_debug_ls = final_debug_letter+final_debug_num

    row_list = []
    file, org_file = hard_list_replace(filename, special_letter, special_number)
    for line, org_line in zip(file, org_file):
        line_new = f"{line}"
        word_line_split = line.split(" ")
        replace_set = set()
        for word in word_line_split:                
            if "." in word and len(word.strip()) > 1:
                replace_set.add(word)
        replace_set_list = list(replace_set)
        replace_set_list.sort(key=lambda s: len(s), reverse=True)
        for w in replace_set_list:
            check, new_word = check_replace_word(line_new, w, letter_j, number_j)
            if check:
                print(f" old: {w}, new_word {new_word}") 
                line_new = line_new.replace(w,new_word)
        row_list.append(line_new)

    row_list = replace_again(row_list, final_debug_ls, dot_ent)

    return row_list




folder = \
    "/Users/n2t2k/Documents/Studying/Master/Thesis/InProgress/Coding/ORIGIN_RUN_ALL_edge-oriented-graph-master-studying/dataProcessingOfficialCleaned/dev_processed/final_regex/single_doc_files"

processed_txt = f"{folder}/processed_txt"
remove_dot_docs = f"{folder}/remove_dot_docs"
split_sentence_for_segmentation = f"{folder}/split_sentence_for_segmentation"



letter_j = letter.LETER_VAR, letter.SPECIAL_NUMBER_VAR, letter.FINAL_AFTER_DEBUG_LETER
number_j = number.NUMBER_VAR, number.SPECIAL_NUMBER_VAR, number.FINAL_AFTER_DEBUG_NUM
dot_ent = dot_ent.DOT_ENT

onlyfiles = [f for f in listdir(processed_txt) if isfile(join(processed_txt, f))]

file_merge_all = join(folder, "file_merge_all.txt")
file_only_sentence_merge_all = join(folder, "file_only_sentence_merge_all.txt")
with open(file_merge_all,'w') as out:
    out.write("")

with open(file_only_sentence_merge_all,'w') as out:
    out.write("")

for file in onlyfiles:
    file_in = join(processed_txt, file)
    file_out = join(remove_dot_docs, file)
    for_segmentation_file_out = join(split_sentence_for_segmentation, file)

    print(f"working ... {file}")
    row_list =  create_json_number_fn_split(
                    file_in, 
                    file_out, 
                    letter_j, 
                    number_j,
                    {"dot_ent":dot_ent}
                )   

    with open(for_segmentation_file_out,'w') as out:
        out.write("")

    with open(file_out,'w') as out:
        out.write("")

    # break
    for r in row_list:
        write_append_data_to_txt_file(file_out, r)
        write_append_data_to_txt_file(file_merge_all, r)
        if r[8:11] == "|a|":
            write_append_data_to_txt_file(file_only_sentence_merge_all, r)
            
            split_sentence = r[11:].split(".")
            for split_row in split_sentence:
                # write_append_data_to_txt_file(for_segmentation_file_out, split_row)
                with open(for_segmentation_file_out,'a') as out:
                    out.write(split_row+'\n')

    with open(file_merge_all,'a') as out:
        out.write('\n'*2)