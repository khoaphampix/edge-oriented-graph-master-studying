"""
INPUT: 
    - all docs, 1 paragraph - 1 line (filter (no-relation) raw data without any processing like: remove dot, quote ...)
    - All_sentence.PubTator.txt
    
OUTPUT: 
    - all docs, 1 paragraph - with splited sentences with struct: <code><$$##$$$$##$$><sent><$$##$$$$##$$><sent>
    - saved to <split_sentence_from_paragraph.txt>
    
# HOW 
split to sentence smartly by underthesea (recognize 20.10, TP.HCM ...)
replace \xa0 (bug by text after processed by underthesea)

"""


import json

from underthesea import sent_tokenize, word_tokenize


def write_append_data_to_txt_file(full_path_to_file, txt):
    with open(full_path_to_file,'a') as out:
        out.write(f'{txt}\n')
        # out.write(f'{txt}')s
        
def clear_file(full_path_to_file):
    with open(full_path_to_file,'w') as out:
        out.write(f'')

folder = \
    "/Users/n2t2k/Documents/Studying/Master/Thesis/InProgress/Coding/ORIGIN_RUN_ALL_edge-oriented-graph-master-studying/dataProcessingOfficialCleaned/dev_processed"


filename = f"{folder}/All_sentence.PubTator.txt"
folder = \
    "/Users/n2t2k/Documents/Studying/Master/Thesis/InProgress/Coding/ORIGIN_RUN_ALL_edge-oriented-graph-master-studying/dataProcessingOfficialCleaned/dev_processed/split_sentence_underthesea/docs"

split_sentence_from_paragraph_file = f"{folder}/split_sentence_from_paragraph.txt"
split_sentence_with_token_from_paragraph_file = f"{folder}/split_sentence_with_token_from_paragraph.txt"


def sentence_with_word_tokenize(sentence_org):
    sentence = word_tokenize(sentence_org, format="text")
    # tokens = sentence.split(" ")
    print(sentence)
    print(sentence_org)
    if len(sentence) != len(sentence_org):
        sentence_org_replace = sentence_org
        lw = sentence.split(" ")
        lw = set(w for w in lw if "_" in w)
        # print(lw)
        for w in lw:
            w_ = f"{w}"
            w = w.replace("_", " ")
            # print(w_, w)
            sentence_org_replace = sentence_org_replace.replace(w, w_)
        if len(sentence_org_replace) == len(sentence_org):
            sentence = sentence_org_replace
        else:
            sentence = ""
    print(sentence)
    return sentence


def split_sentence_from_paragraph(filename, out_put, out_put_with_token):

    stop_line = 9999
    current_line = 0
    clear_file(out_put)
    clear_file(out_put_with_token)
    
    with open(filename, "r") as file:
        count = 0
        full_set = set()
        for line in file:
            current_line+=1
            if current_line > stop_line:
                break
            
            # print(line)
            code_ = line[0:8]
            # print(code_)
            line = line[11:]
            sentence_list = sent_tokenize(line)
            # print(sentence_list)
            # print("\n"*2)
            # for sent in sentence_list:
            #     print(sent)
            para_sents = ""
            para_sents_tk = ""
            for s in sentence_list:
                s = s.replace("\xc2\xa0", " ").replace("\xa0", " ").replace("    ", " ").replace("   ", " ").replace("  ", " ")

                if s[-1] == ".":
                    s = s[:-1]
                
                # para_sents = "$$##$$$$##$$".join(map(str,[s.replace("\xa0", " ") for s in sentence_list]))
                count=+1
                
                para_sents+=("$$##$$$$##$$"+s)
                para_sents_tk+=("$$##$$$$##$$"+sentence_with_word_tokenize(s))
            write_append_data_to_txt_file(out_put, code_+para_sents)                 
            write_append_data_to_txt_file(out_put_with_token, code_+para_sents_tk)
                
    print("total: ", count)
               
split_sentence_from_paragraph(filename, split_sentence_from_paragraph_file, split_sentence_with_token_from_paragraph_file)

# sentence_org = "Bị xe tải cuốn vào gầm, cháu bé thoát chết thần kỳ Khoảng 17h chiều ngày 21-9, tại ngã tư Phan Đình Phùng và Lê Lợi , thuộc phường Nghĩa Chánh , TP Quảng Ngãi xảy ra vụ tai nạn giao thông giữa xe ô tô tải và xe đạp"
# s = sentence_with_word_tokenize(sentence_org)
