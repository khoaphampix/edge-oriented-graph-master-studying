from transformers import PhobertTokenizer, BertModel
import torch
import numpy as np

model_name = 'vinai/phobert-base-v2'
tokenizer = PhobertTokenizer.from_pretrained(model_name)
model = BertModel.from_pretrained(model_name)

# sentence = "This is an example sentence."
sentence = "Chúng_tôi là những nghiên_cứu_viên"
sentence = "Ông Nguyễn_Khắc_Chúc đang làm_việc tại Đại_học Quốc_gia Hà_Nội"
sentence = "bàn thắng Sang hiệp 2 , HLV Vũ_Hồng Việt yêu_cầu các học_trò tấn_công mạnh_mẽ hơn nữa , trong khi U16 Mông_Cổ có dấu_hiệu xuống sức rõ_rệt Những bàn thắng đến như một tất_yếu Riêng ở hiệp đấu này , Chí_Bảo đã ghi tới 4 bàn thắng , giúp U16 Việt_Nam thắng chung_cuộc 9 Như_vậy qua 2 trận đấu , U16 Việt_Nam toàn_thắng , ghi tới 14 bàn và để lọt_lưới 2 , hiệu_số bàn thắng_bại là 12 Tại bảng I lúc này , thầy_trò Vũ_Hồng Việt có cùng điểm_số như U16_Australia nhưng xếp dưới vì kém hiệu_số bàn thắng_bại"


import json
create_ent_sent_json_file = False

def write_append_data_to_txt_file(full_path_to_file, txt):
    with open(full_path_to_file,'a') as out:
        out.write(f'{txt}\n')
        # out.write(f'{txt}')s
        
def clear_file(full_path_to_files_list):
    for _file in full_path_to_files_list:
      with open(_file,'w') as out:
        out.write(f'')




def reduce_emb_vec_org(vt1):
  
  vt1_np = vt1.detach().numpy()
  vt1_mean = vt1_np.reshape(-1, 4).mean(axis=1)
  return vt1_mean

def embedding_sent_to_dict_of_vector_word(sentence):
    # Tokenize the sentence
    # tokens = tokenizer.tokenize(sentence)

    # print("tokens >>> ", tokens)
    # print(sentence)
    tokens = sentence.replace("  "," ").split(" ")



    # Add the special tokens [CLS] and [SEP]
    tokens = ['[CLS]'] + tokens + ['[SEP]']

    # Convert tokens to input IDs and create attention mask
    input_ids = tokenizer.convert_tokens_to_ids(tokens)
    attention_mask = [1] * len(input_ids)

    # Convert lists to tensors
    input_ids = torch.tensor([input_ids])
    attention_mask = torch.tensor([attention_mask])

    # Generate the embeddings
    with torch.no_grad():
        outputs = model(input_ids, attention_mask=attention_mask)
        embeddings = outputs.last_hidden_state[0]

    # Create the word-to-embedding dictionary
    # word_embeddings_dict = {}
    # for i in range(1, len(tokens)-1):
    #     word = tokens[i]
    #     embedding = embeddings[i]
    #     word_embeddings_dict[word] = embedding
        

    # return word_embeddings_dict

    word_embeddingslist = []
    for i in range(1, len(tokens)-1):
        # word = tokens[i]
        # embedding = embeddings[i]
        # word_embeddings_dict[word] = embedding
        vector = embeddings[i]
        # print(vector.shape)
        vt_reduce = reduce_emb_vec_org(vector) 
        print(tokens[i] ,vt_reduce.shape)
        word_embeddingslist.append((tokens[i], vt_reduce))
    return word_embeddingslist


# sent = "bàn thắng Sang hiệp 2 , HLV Vũ_Hồng Việt yêu_cầu các học_trò tấn_công mạnh_mẽ hơn nữa , trong khi U16 Mông_Cổ có dấu_hiệu xuống sức rõ_rệt Những bàn thắng đến như một tất_yếu Riêng ở hiệp đấu này , Chí_Bảo đã ghi tới 4 bàn thắng , giúp U16 Việt_Nam thắng chung_cuộc 9 Như_vậy qua 2 trận đấu , U16 Việt_Nam toàn_thắng , ghi tới 14 bàn và để lọt_lưới 2 , hiệu_số bàn thắng_bại là 12 Tại bảng I lúc này , thầy_trò Vũ_Hồng Việt có cùng điểm_số như U16_Australia nhưng xếp dưới vì kém hiệu_số bàn thắng_bạ"
# eb = embedding_words_in_sents_full_shape(sent)


# print(eb)
already_embedded_set = set()
embedded_file = \
    "/Users/n2t2k/Documents/Studying/Master/Thesis/InProgress/Coding/ORIGIN_RUN_ALL_edge-oriented-graph-master-studying/dataProcessingOfficialCleaned/dev_processed/split_sentence_underthesea/code/BERT_merge_file/data/PubMed-VLSP_origin_after_processed.txt"
clear_file([embedded_file])

error_sent_embedded_file = \
    "/Users/n2t2k/Documents/Studying/Master/Thesis/InProgress/Coding/ORIGIN_RUN_ALL_edge-oriented-graph-master-studying/dataProcessingOfficialCleaned/dev_processed/split_sentence_underthesea/code/BERT_merge_file/BERT_create_corpus/view_data/data/error_sent_embedded_file.txt"
clear_file([error_sent_embedded_file])


out_all_sent = \
    "/Users/n2t2k/Documents/Studying/Master/Thesis/InProgress/Coding/ORIGIN_RUN_ALL_edge-oriented-graph-master-studying/dataProcessingOfficialCleaned/dev_processed/split_sentence_underthesea/code/BERT_merge_file/BERT_create_corpus/view_data/data/all_sent_to_wb.txt"
error_count = 0
total_sent = 0
with open(out_all_sent, 'r') as in_file:
    lines = in_file.readlines()
    for sent in lines:
        total_sent+=1
        sent = sent.replace("\n","")
        # sent = "7 nguyên_nhân khiến Real_Madrid bị Barcelona bỏ_xa tại La_Liga Tờ Marca của Tây Ban_Nha đã chỉ ra những yếu_tố lý_giải cho sự khởi_đầu tệ_hại của Real_Madrid tại La_Liga 20172018"
        try:
            emb_vec_reduce =  embedding_sent_to_dict_of_vector_word(sent.strip())
            # print(emb_vec_reduce)
            for tk, em_w in emb_vec_reduce:
                if tk in already_embedded_set:
                    continue
                already_embedded_set.add(tk)
                em_w_ls = em_w.tolist()
                em_w_ls = " ".join(map(str, em_w_ls))      
                write_append_data_to_txt_file(embedded_file, f"{tk} {em_w_ls}")
        except:
            error_count +=1
            write_append_data_to_txt_file(error_sent_embedded_file, sent)
        # break
        # if error_count == 1:
        #     break

print("already_embedded_set word: ", len(already_embedded_set))
print("total_sent: ", total_sent)
print("error_count sent: ", error_count)

