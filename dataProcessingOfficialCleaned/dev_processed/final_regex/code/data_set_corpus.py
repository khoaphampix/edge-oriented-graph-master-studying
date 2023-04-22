
import json



def write_append_data_to_txt_file(full_path_to_file, txt):
    with open(full_path_to_file,'a') as out:
        # out.write(f'{txt}\n')
        out.write(f'{txt}')

folder = \
    "/Users/n2t2k/Documents/Studying/Master/Thesis/InProgress/Coding/ORIGIN_RUN_ALL_edge-oriented-graph-master-studying/dataProcessingOfficialCleaned/dev_processed/final_regex/data_set"


filename = f"{folder}/All_sentence.PubTator.txt"
corpust_all_sentence_file = f"{folder}/corpust_all_sentence.txt"


def corpust_all_sentence(filename, out_put):

    with open(out_put,'w') as out:
        out.write("")

    with open(filename, "r") as file:
        count = 0
        full_set = set()
        for line in file:
            line = line[11:]
            new_set = line.split(" ")
            full_set.update(new_set)
        for w in full_set:
            count=+1
            write_append_data_to_txt_file(out_put, w)
    print("total: ", count)
               
corpust_all_sentence(filename, corpust_all_sentence_file)