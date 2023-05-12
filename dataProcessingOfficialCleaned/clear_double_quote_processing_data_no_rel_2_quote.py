import os
from os import listdir
from os.path import isfile, join, isdir

import pandas as pd
from pprint import pprint


mask_ent_name = {
    "PERSON" : "per",
    "LOCATION" : "loc",
    "ORGANIZATION" : "org",
    "PERSON_single": "per_single",
    "LOCATION_single": "loc_single",
    "ORGANIZATION_single": "org_single",
}

def replace2symbol(string):
    string =  string.replace('”', '"')\
                    .replace('“', "'")\
                    .replace(' ', ' ')\
                    .replace('’', "'")\
                    .replace('–', '-')\
                    .replace('‘', "'")\
                    .replace('‑', '-')\
                    .replace('»', '"')\
                    .replace('—', '-')\
                    .replace('¾', '')\
                    .replace('²', '')\
                    .replace('…', '')\
                    .replace('½', '')\
                    .replace('\u200b', ' ')\
                    .replace("\ufeff", '')\
                    .replace("\xc2\xa0", " ")\
                    .replace("\xa0", " ")\
                    .replace("   ", " ")\
                    .replace("  ", " ")

    return string

class Doc():
    def __init__(self):
        self.key = "123"
        self.title = ""
        self.sents = ""
        self.per=[]
        self.loc=[]
        self.org=[]
        self.per_single=[]
        self.loc_single=[]
        self.org_single=[]
        self.rels =[]


class Entity():
    def __init__(self):
        self.start = 0
        self.end = 0
        self.text = ""
        self.type = ""
        self.ent_code = ""
        self.single_index_org = ""
        self.index_org = ""
        

class Relation():
    def __init__(self):
        self.type = ""
        self.ent_right_index_org= None
        self.ent_left_index_org = None
        self.ent_right_code = None
        self.ent_left_code = None

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
                    return line[6:]
                    
def create_ent(ent_obj, e_type, new_doc_obj, idx, start_end, t):
    ent_obj.type = e_type
    ent_obj.ent_code = new_doc_obj.key+pars_ent_number_code(idx)
    ent_obj.start = start_end.split("-")[0]
    ent_obj.end = start_end.split("-")[-1]
    ent_obj.text = t
    return ent_obj

def pars_ent_number_code(number):
    digit = 5-len(str(number))
    if digit:
        return ("0"*digit)+str(number)
    return number


def break_title_and_sent(sent):
    i=0
    for c in sent:
        if c == ".":
            return sent[:i+1], sent[i+1:], 
        i+=1


def read_ignore_file(path1, path2=None, path3=None):
    l1 = ""
    with open(path1, "r") as file:  # the a opens it in append mode
        l1 = next(file).strip()
    l2 = ""
    if path2:
        with open(path2, "r") as file:  # the a opens it in append mode
            l2 = next(file).strip()
    l3 = ""
    if path3:
        with open(path3, "r") as file:  # the a opens it in append mode
            l3 = next(file).strip()
    l = l1+l2+l3
    return l[:-1].split(",")

def par_ent(doc_obj,df, mask_ent_name):

    doc_obj_key = doc_obj.key
    single_ents = {}
    distinct_map_text_code = {
        "PERSON":{
                "single":{},
                "multiple":{}
        },
        "LOCATION":{
            "single":{},
            "multiple":{}
        }, 
        "ORGANIZATION":{
            "single":{},
            "multiple":{}
        }
    }

    three_ent_dict = {
        "PERSON":[], 
        "LOCATION":[], 
        "ORGANIZATION":[],
        "PERSON_single":{}, 
        "LOCATION_single":{}, 
        "ORGANIZATION_single":{}
    }
    idx =0
    for index, row in df.iterrows():
        ent_type = index.split("[")
        idx+=1
        if ent_type[0] in ["PERSON", "LOCATION", "ORGANIZATION"]:
            if len(ent_type) > 1:
                ent_obj = Entity()
                ent_obj.type = ent_type[0]
                ent_obj.start = row["start_end"][0].split("-")[0]
                ent_obj.end = row["start_end"][-1].split("-")[-1]
                text = " ".join(row["text"])
                ent_obj.text = text
                ent_obj.index_org = row["index_org"][0]

                exist_code = distinct_map_text_code[ent_type[0]]["multiple"].get(text, None)
                if exist_code is not None:
                    ent_code = exist_code[0]
                    distinct_map_text_code[ent_type[0]]["multiple"][text][1] = exist_code[1]+1
                else:
                    ent_code = doc_obj_key+pars_ent_number_code( row["index_org"][0].split("-")[-1])
                    distinct_map_text_code[ent_type[0]]["multiple"][text] = [ent_code, 1]

                ent_obj.ent_code = ent_code
                three_ent_dict[ent_type[0]].append(ent_obj)
            else:
                for single_text, single_start_end, single_index_org in zip(row["text"], row["start_end"], row["index_org"]):
                    ent_obj = Entity()
                    ent_obj.type = ent_type[0]
                    ent_obj.start = single_start_end.split("-")[0]
                    ent_obj.end = single_start_end.split("-")[-1]
                    ent_obj.text = single_text                    
                    ent_obj.index_org = single_index_org
                    exist_code = distinct_map_text_code[ent_type[0]]["single"].get(single_text, None)
                    if exist_code:
                        ent_code = exist_code
                    else:
                        ent_code = doc_obj_key+pars_ent_number_code( single_index_org.split("-")[-1] )
                    distinct_map_text_code[ent_type[0]]["single"][single_text] = ent_code

                    ent_obj.ent_code = ent_code
                    if three_ent_dict[ent_type[0]+"_single"].get(single_text, None) is None:
                        three_ent_dict[ent_type[0]+"_single"][single_text] = [ent_obj]
                    else:
                        three_ent_dict[ent_type[0]+"_single"][single_text].append(ent_obj)


    for k, v in three_ent_dict.items():
        setattr(doc_obj,mask_ent_name[k], v)
    return doc_obj, distinct_map_text_code



def complete_docs(new_doc_obj, distinct_map_text_code):
    for k, v in new_doc_obj.per_single.items():
        multiple_text_dict = distinct_map_text_code[v[0].type]["multiple"]

        code_ls =[]
        for km, vm in multiple_text_dict.items():
            if k in km.split(" "):
                if len(code_ls) == 0:
                    code_ls = vm
                else:
                    if vm[1] > code_ls[1]:
                        code_ls = vm
        for vi in v:
            if len(code_ls) > 0:
                vi.ent_code = code_ls[0]
            new_doc_obj.per.append(vi)
    new_doc_obj.per_single = None

    for k, v in new_doc_obj.org_single.items():
        multiple_text_dict = distinct_map_text_code[v[0].type]["multiple"]

        code_ls =[]
        for km, vm in multiple_text_dict.items():
            if k in km.split(" "):
                if len(code_ls) == 0:
                    code_ls = vm
                else:
                    if vm[1] > code_ls[1]:
                        code_ls = vm
        for vi in v:
            if len(code_ls) > 0:
                vi.ent_code = code_ls[0]
            new_doc_obj.org.append(vi)
    new_doc_obj.org_single = None


    for k, v in new_doc_obj.loc_single.items():
        multiple_text_dict = distinct_map_text_code[v[0].type]["multiple"]

        code_ls =[]
        for km, vm in multiple_text_dict.items():
            if k in km.split(" "):
                if len(code_ls) == 0:
                    code_ls = vm
                else:
                    if vm[1] > code_ls[1]:
                        code_ls = vm
        for vi in v:
            if len(code_ls) > 0:
                vi.ent_code = code_ls[0]
            new_doc_obj.loc.append(vi)
    new_doc_obj.loc_single = None

    return new_doc_obj



def print_complete_docs(new_doc_obj):
    
    # print("key ", new_doc_obj.key)
    # print("title ", new_doc_obj.title)
    # print("& "*50, "\n")  
    # print(new_doc_obj.sents)
    # print("& "*50, "\n")  

    newlist = sorted(new_doc_obj.per, key=lambda x: x.ent_code, reverse=True)
    def print_header():
        line_hd = '{:>20}  {:>20}  {:>20} {:>20}  {:>20}   {:>20}'.format("text", "ent_code", "type", "start", "end", "index_org")
        line_hd2 = '{:>20}  {:>20}  {:>20} {:>20}  {:>20}   {:>20}'.format("-"*10,"-"*10,"-"*10,"-"*10,"-"*10,"-"*10)
        print(line_hd)
        print(line_hd2)
    print_header()
    for i in newlist:
        line_new = '{:>20}  {:>20}  {:>20} {:>20}  {:>20}   {:>20}'.format(i.text, i.ent_code, i.type, i.start, i.end, i.index_org)
        print(line_new)
    
    print("& "*50, "\n")  
    print_header() 
    newlist = sorted(new_doc_obj.org, key=lambda x: x.ent_code, reverse=True)
    for i in newlist:
        line_new = '{:>20}  {:>20}  {:>20} {:>20}  {:>20}   {:>20}'.format(i.text, i.ent_code, i.type, i.start, i.end, i.index_org)
        print(line_new)

    print("& "*50, "\n")  
    newlist = sorted(new_doc_obj.loc, key=lambda x: x.ent_code, reverse=True)
    print_header() 
    for i in newlist:
        line_new = '{:>20}  {:>20}  {:>20} {:>20}  {:>20}   {:>20}'.format(i.text, i.ent_code, i.type, i.start, i.end, i.index_org)
        print(line_new)
    print("& "*50, "\n")  


def get_entity_code(new_doc_obj, index_org):
    for e in new_doc_obj.per:
        if e.index_org == index_org:
            return e.ent_code
    for e in new_doc_obj.org:
        if e.index_org == index_org:
            return e.ent_code
    for e in new_doc_obj.loc:
        if e.index_org == index_org:
            return e.ent_code



def write_append_data_to_txt_file(full_path_to_file, lines):
    with open(full_path_to_file,'a') as out:
        out.write('\n') 
        for l in lines:
            l = l.strip()
            l = replace2symbol(l)
            if l:
                out.write(f'\n{l}')

def write_data_to_new_txt_file(full_path_to_file, lines):
    with open(full_path_to_file,'w') as out:
        # length = len(lines)
        # print(length)
        i = 1
        for l in lines:
            l = l.strip()
            l = replace2symbol(l)
            if l:
                if i == 1:
                    out.write(f'{l}')
                else:
                    out.write(f'\n{l}')
                i+=1


def prepare_lines_to_write(new_doc_obj):

    title = f"{new_doc_obj.key}|t|{new_doc_obj.title}"
    sent = f"{new_doc_obj.key}|a|{new_doc_obj.sents}"
    list_lines = [title, sent]
    # line_hd = '{}\t\t{}\t{}\t{}\t{}\t{}'.format( "start", "end", "text", "ent_code", "type", "index_org")
    # line_hd2 = '{}\t\t{}\t{}\t{}\t{}\t{}'.format("-"*5,"-"*5,"-"*5,"-"*5,"-"*5,"-"*5)
    # print(line_hd)
    # print(line_hd2)
    merge_all_ent = new_doc_obj.per + new_doc_obj.org + new_doc_obj.loc
    merge_all_ent = sorted(merge_all_ent, key=lambda x: int(x.start), reverse=False)
    for i in merge_all_ent:
        line_new = '{}\t{}\t{}\t{}\t{}\t{}'.format(new_doc_obj.key, i.start, i.end, i.text, i.type, i.ent_code)
        list_lines.append(line_new)
    # new_doc_obj.rels = sorted(new_doc_obj.rels, key=lambda x: int(x.start), reverse=False)
    for i in new_doc_obj.rels:
        line_new = '{}\t{}\t{}\t{}'.format(new_doc_obj.key, i.type, i.ent_left_code, i.ent_right_code)
        list_lines.append(line_new)
    return list_lines



def save_single_relation(new_doc_obj, rel, index_org, rel_pair):
    """
    #single:
    rel : AFFILIATION
    rel_pair : 1-190[20_19]|1-197[21_19]|1-201[22_19]|1-206[23_19]
    index_org: 1-153[17_18]
    """

    # set the entitiy code of an relation

    rel_obj = Relation()
    rel_obj.type = rel
    ref_ent_org = rel_pair.split("[")[0]

    # ref_ent = int( ref_ent_org.split("-")[1] )
    # current_ent = int( index_org.split("-")[1] )
    ref_ent = ref_ent_org.split("-")[1] 
    current_ent = index_org.split("-")[1] 

    current_ent_code = get_entity_code(new_doc_obj, index_org)
    ref_ent_code = get_entity_code(new_doc_obj, ref_ent_org)

    if current_ent < ref_ent:
        rel_obj.ent_left_index_org = index_org
        rel_obj.ent_left_code =  current_ent_code

        rel_obj.ent_right_index_org = ref_ent_org
        rel_obj.ent_right_code = ref_ent_code
    else:
        rel_obj.ent_left_index_org = ref_ent_org
        rel_obj.ent_left_code = ref_ent_code

        rel_obj.ent_right_index_org = index_org
        rel_obj.ent_right_code = current_ent_code
    new_doc_obj.rels.append(rel_obj)

    return new_doc_obj


def save_relations_to_docs_obj(new_doc_obj, group_relation):
    """
    # multiple
    new_doc_obj
    rel : PERSONAL - SOCIAL|PERSONAL - SOCIAL|PERSONAL - SOCIAL|PERSONAL - SOCIAL
    rel_pair : 1-190[20_19]|1-197[21_19]|1-201[22_19]|1-206[23_19]
    index_org: [1-176]
    
    #single:
    rel : AFFILIATION
    rel_pair : 1-190[20_19]|1-197[21_19]|1-201[22_19]|1-206[23_19]
    index_org: 1-153[17_18]
    """
    relation_types_ls = [
        "AFFILIATION",
        "LOCATED",
        "PART - WHOLE",
        "PERSONAL - SOCIAL",
    ]

    # set the entitiy code of an relation
    for rel, row in group_relation.iterrows():
        for index_org, rel_pair in zip(row["index_org"], row["rel_pair"]):
            if len(rel.split("|")) ==1:
                if rel.strip() in relation_types_ls:
                    new_doc_obj = save_single_relation(new_doc_obj, rel, index_org, rel_pair)
            else:
                for single_rel, single_rel_pair in zip(rel.split("|"), rel_pair.split("|")):
                    if single_rel.strip() in relation_types_ls:
                        new_doc_obj = save_single_relation(new_doc_obj, single_rel, index_org, single_rel_pair)

    return new_doc_obj


# prepare the data file directory
def process_a_file_for_write_data_txt(path_to_file, sub_folder):
    # path_to_file += sub_folder
    path_to_file = join(path_to_file, sub_folder)
    full_path_to_file = join(path_to_file,"CURATION_USER.tsv")
    if not isfile(full_path_to_file):
        full_path_to_file = join(path_to_file,"CURATION_USER (1).tsv")

    # print("= "*80, '\n'*5)
    # print('\t'*2, "-"*50, " START NEW COMMAND ", "-"*50, '\n'*2)


    # create the main data frame
    sentence_line_number = get_sentence_line_number(full_path_to_file, True)
    tsv_read_df = pd.read_csv(full_path_to_file, sep='\t', encoding = 'utf-8', skiprows=sentence_line_number+1, header=None)

    if len(tsv_read_df.columns) == 6:
        tsv_read_df[6] = pd.Series([None]*len(tsv_read_df))
        tsv_read_df[7] = pd.Series([None]*len(tsv_read_df))

    cols = ["index_org", "start_end", "text", "ent_no", "ent_type", "rel", "rel_pair", "last"]
    tsv_read_df.columns = cols


    # group data frame by the entity type
    cols_slt = ["index_org", "text", "ent_no", "ent_type", "start_end", "rel", "rel_pair"]
    group_ent_name = tsv_read_df[cols_slt].groupby('ent_type', dropna=True).agg(lambda x: list(x))
    group_ent_name = group_ent_name[group_ent_name.index != "_"]


    # create the main Docs object 
    full_st = get_sentence_line_number(full_path_to_file, False)
    # title, full_st = break_title_and_sent(full_st) 
    doc_obj = Doc()
    doc_obj.key=sub_folder.split(".")[0]
    # doc_obj.title= 
    doc_obj.sents= full_st


    # create the entity
    new_doc_obj, distinct_map_text_code = par_ent(doc_obj,group_ent_name,mask_ent_name)
    new_doc_obj = complete_docs(new_doc_obj, distinct_map_text_code)
    # print_complete_docs(new_doc_obj)


    # group data frame by the relation
    # cols_slt = ["index_org", "text", "ent_no", "ent_type", "start_end", "rel", "rel_pair"]
    cols_slt = ["index_org", "rel", "rel_pair"]
    group_relation = tsv_read_df[cols_slt].groupby('rel', dropna=True).agg(lambda x: list(x))
    group_relation = group_relation[group_relation.index != "_"]
    new_doc_obj = save_relations_to_docs_obj(new_doc_obj, group_relation)
    return new_doc_obj
  


def save_excell_for_view(mypath, data_set="dev", exclude_folder_path = None):
    if data_set=="dev":
        mypath_data = f"{mypath}/VLSP2020_RE_dev"
        dev_processed = f"{mypath}/dev_processed"
        folder_PubTator =  f"{dev_processed}/CDR_DevelopmentSet.PubTator.txt"
        all_sentence =  f"{dev_processed}/All_sentence.PubTator.txt"
    else:
        mypath_data = f"{mypath}/VLSP2020_RE_train"
        dev_processed = f"{mypath}/train_processed"
        folder_PubTator =  f"{dev_processed}/CDR_TrainingSet.PubTator.txt"
        all_sentence =  f"{dev_processed}/All_sentence.PubTator.txt"

    with open(folder_PubTator, 'w') as f:
        f.write('')

    with open(all_sentence, 'w') as f:
        f.write('')

    processed_txt = f"{dev_processed}/processed_txt"


    # exclude_folder = read_ignore_file(
    #                                     f"{dev_processed}/double_quote_err.txt", 
    #                                     f"{dev_processed}/no_relation.txt",
    #                                     f"{dev_processed}/data_errors_files.txt"
    #                                 )
    

    exclude_folder = read_ignore_file(
                                        # f"{dev_processed}/no_relation.txt",
                                        f"{dev_processed}/double_quote_err.txt", 
                                        # f"{dev_processed}/data_errors_files.txt"
                                    )
    # exclude_folder = []

    print(">>> "*50)
    print("exclude_folder ", exclude_folder)
    sub_folder_ls = [ d for d in listdir(mypath_data) if ( isdir(join(mypath_data, d)) and d.strip() not in exclude_folder)]

    total= 0
    for fd in sub_folder_ls:

        # 23352734.conll,23352408.conll,23352562.conll,23352561.conll,

        # error_no_rel_list = ["23352816.conll"]
        # if fd in error_no_rel_list:
        #     continue

        error_no_rel_list = \
            ["23357779.conll", "23351945.conll", "23352816.conll", "23351433.conll", 
            "23351610.conll", "23351984.conll", "23356574.conll", "23357000.conll", "23357063.conll"]
        
        # error_no_rel_list = \
        #     ["23357779.conll", "23351945.conll", "23351433.conll", 
        #     "23351610.conll", "23351984.conll", "23356574.conll", "23357000.conll", "23357063.conll"]
        
        # if fd[:8] not in error_no_rel_list:

        # if fd not in error_no_rel_list:
        #     continue
        # print("here ")

        # exclude_folder = ['23352517.conll', '23352414.conll', '23352491.conll', '23352654.conll', '23352410.conll', '23352457.conll', '23352110.conll', '23352600.conll', '23352014.conll', '23352620.conll', '23352337.conll', '23352090.conll', '23352393.conll', '23352605.conll']
        # if fd not in exclude_folder:
        #     continue


        print(f"{total}.__ {data_set}: working on ------------{fd}---")
        full_path_to_file = join(f"{mypath_data}/{fd}","CURATION_USER.tsv")
        if not isfile(full_path_to_file):
            full_path_to_file = join(f"{mypath_data}/{fd}","CURATION_USER (1).tsv")
        
        # try:
        sentence_line_number = get_sentence_line_number(full_path_to_file, True)
        tsv_read_df = pd.read_csv(full_path_to_file, sep='\t', encoding = 'utf-8', skiprows=sentence_line_number+1, header=None) 
        # print(">>> len ", len(tsv_read_df.columns), type(tsv_read_df.columns))
        # use for empty 
        if len(tsv_read_df.columns) == 6:
            tsv_read_df[6] = pd.Series([None]*len(tsv_read_df))
            tsv_read_df[7] = pd.Series([None]*len(tsv_read_df))

        # print(tsv_read_df[1])
        # print(">>> len ", len(tsv_read_df.columns), tsv_read_df.columns)

        tsv_read_df.columns = ["index_org", "start_end", "text", "ent_no", "ent_type", "rel", "rel_pair", "last"]
        # read sentence
        tsv_read_df.to_excel(join(dev_processed,f"worked_files_excell/{fd}.xlsx"), encoding='utf-8', index=False)
    
        new_doc_obj = process_a_file_for_write_data_txt(mypath_data, fd)
        # except Exception as e:
        #     print(fd, str(e))
             
        # write a Docs object to file = 1 document in data
        full_path_to_PubTator = join(processed_txt, f"{fd}.txt")
        merge_all_ent = prepare_lines_to_write(new_doc_obj)
        
        # write to small file
        write_data_to_new_txt_file(full_path_to_PubTator, merge_all_ent)
        # write to big main file
        write_append_data_to_txt_file(folder_PubTator, merge_all_ent)

        with open(all_sentence,'a') as out:
            for l in merge_all_ent:
                l = replace2symbol(l)
                if l[8:11] == "|a|":
                    l = l.strip()
                    out.write(f'\n{l}')

            total+=1

    print("-"*150, '\n'*3)
    print("-"*50, data_set, "-"*50)
    print(f"total: {total}")


# prepare the data file directory
# path_to_file = \
# "/Users/n2t2k/Documents/Studying/Master/Thesis/InProgress/SmallCode/dataProcessing/cleaned_file_to_process/"
# sub_folder = "23351996.conll"
# process_a_file_for_write_data_txt(path_to_file, sub_folder)

# ddee
# dev_test_folder = "/Users/n2t2k/Documents/Studying/Master/Thesis/InProgress/SmallCode/dataProcessing/dev_sample"

# wroking 
dev_test_folder = \
                "/Users/n2t2k/Documents/Studying/Master/Thesis/InProgress/Coding/ORIGIN_RUN_ALL_edge-oriented-graph-master-studying/dataProcessingOfficialCleaned"


save_excell_for_view(dev_test_folder,"dev")
# save_excell_for_view(dev_test_folder,"train")

"""
name of TRAIN CONVERTED TO DEV for quickly use code
"""