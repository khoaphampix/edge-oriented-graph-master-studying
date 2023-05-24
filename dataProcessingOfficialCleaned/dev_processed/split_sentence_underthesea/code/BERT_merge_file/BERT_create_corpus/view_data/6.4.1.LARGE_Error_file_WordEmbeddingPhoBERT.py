#!/usr/bin/env python
# coding: utf-8

# In[1]:


from underthesea import sent_tokenize, word_tokenize

# PhoBERT_base_fairseq_path = \
# "/Users/n2t2k/Documents/Studying/Master/Thesis/InProgress/edge-oriented-graph-master-WORKING/PhoBERT_base_fairseq"


PhoBERT_base_fairseq_path = \
"/Users/n2t2k/Documents/Studying/Master/Thesis/InProgress/Coding/PhoBERT_large_fairseq"


from fairseq.models.roberta import RobertaModel
phoBERT = RobertaModel.from_pretrained(PhoBERT_base_fairseq_path, checkpoint_file='model.pt')
phoBERT.eval()  # disable dropout (or leave in train mode to finetune
import torch
from fairseq.models.roberta import alignment_utils
from fairseq.models import roberta 
from typing import Tuple, List
from fairseq.data.encoders.fastbpe import fastBPE


# In[2]:


from collections import Counter
from typing import List
import torch

def align_bpe_to_words(roberta, bpe_tokens: torch.LongTensor, other_tokens: List[str]):
    """
    Helper to align GPT-2 BPE to other tokenization formats (e.g., spaCy).

    Args:
        roberta (RobertaHubInterface): RoBERTa instance
        bpe_tokens (torch.LongTensor): GPT-2 BPE tokens of shape `(T_bpe)`
        other_tokens (List[str]): other tokens of shape `(T_words)`

    Returns:
        List[str]: mapping from *other_tokens* to corresponding *bpe_tokens*.
    """
    assert bpe_tokens.dim() == 1
    assert bpe_tokens[0] == 0

    def clean(text):
        return text.strip()

    # remove whitespaces to simplify alignment
    bpe_tokens = [roberta.task.source_dictionary.string([x]) for x in bpe_tokens]
    bpe_tokens = [
        clean(roberta.bpe.decode(x) if x not in {"<s>", ""} else x) for x in bpe_tokens
    ]
    other_tokens = [clean(str(o)) for o in other_tokens]

    # strip leading <s>
    bpe_tokens = bpe_tokens[1:]
    assert "".join(bpe_tokens) == "".join(other_tokens)

    # create alignment from every word to a list of BPE tokens
    alignment = []
    bpe_toks = filter(lambda item: item[1] != "", enumerate(bpe_tokens, start=1))
    j, bpe_tok = next(bpe_toks)

    for other_tok in other_tokens:
        # print("other_tok ", other_tok)
        bpe_indices = []
        while True:
            if other_tok.startswith(bpe_tok):
                bpe_indices.append(j)
                other_tok = other_tok[len(bpe_tok) :]
                try:
                    j, bpe_tok = next(bpe_toks)
                except StopIteration:
                    j, bpe_tok = None, None
            elif bpe_tok.startswith(other_tok):
                # other_tok spans multiple BPE tokens
                bpe_indices.append(j)
                bpe_tok = bpe_tok[len(other_tok) :]
                other_tok = ""
            else:
                raise Exception('Cannot align "{}" and "{}"'.format(other_tok, bpe_tok))
            if other_tok == "":
                break
        assert len(bpe_indices) > 0
        alignment.append(bpe_indices)
    assert len(alignment) == len(other_tokens)

    return alignment


# In[3]:


def extract_aligned_roberta(roberta, sentence: str, 
                            tokens: List[str], 
                            return_all_hiddens=False):
    ''' Code inspired from: 
       https://github.com/pytorch/fairseq/blob/master/fairseq/models/roberta/hub_interface.py
    
    Aligns roberta embeddings for an input tokenization of words for a sentence
    
    Inputs:
    1. roberta: roberta fairseq class
    2. sentence: sentence in string
    3. tokens: tokens of the sentence in which the alignment is to be done
    
    Outputs: Aligned roberta features 
    '''

    # tokenize both with GPT-2 BPE and get alignment with given tokens
    
    
    # print("* "*50)
    # print(sentence)
    # print(tokens)
    
    
    bpe_toks = roberta.encode(sentence)
    # alignment = alignment_utils.align_bpe_to_words(roberta, bpe_toks, tokens)
    alignment = align_bpe_to_words(roberta, bpe_toks, tokens)
    # extract features and align them
    features = roberta.extract_features(bpe_toks, return_all_hiddens=return_all_hiddens)
    features = features.squeeze(0)   #Batch-size = 1
    aligned_feats = alignment_utils.align_features_to_words(roberta, features, alignment)
    return aligned_feats[1:-1]  #exclude <s> and </s> tokens

# Khởi tạo Byte Pair Encoding cho PhoBERT
class BPE():
  bpe_codes = PhoBERT_base_fairseq_path+'/bpe.codes'

args = BPE()
phoBERT.bpe = fastBPE(args) #Incorporate the BPE encoder into PhoBERT


# In[4]:


import numpy as np

def sentence_with_word_tokenize(sentence_org):
    sentence = word_tokenize(sentence_org, format="text")
    # tokens = sentence.split(" ")
    # print(sentence)
    # print(sentence_org)
    # print("len(sentence) != len(sentence_org)", len(sentence) != len(sentence_org))
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
    # print(sentence)
    return sentence

def reduce_emb_vec_org(vt1):
  
  vt1_np = vt1.detach().numpy()
  vt1_mean = vt1_np.reshape(-1, 4).mean(axis=1)
  return np.hstack((vt1_mean, np.zeros(8))) # 200-192
  # return vt1_mean

def reduce_emb_vec(vt1):
  vt1_np = vt1.detach().numpy()
  vt1_mean = vt1_np.reshape(-1, 4).mean(axis=1)
  return vt1_mean

def embedding_words_in_sents_full_shape(sentence):
  tokens = sentence.split(" ")
  # print("* "*40)
  # print(sentence)
  # print("sentence ", sentence)
  # print("tokens ", tokens)
  # print("* "*50)
  # *the last sentence char is "", fx: "Hello is this "
  if tokens and tokens[-1] == "":
    tokens = tokens[:-1]
  
  w = extract_aligned_roberta(phoBERT, sentence, tokens,False)

  emb_vec_reduce = [] 
  for tk, word in list(zip(tokens, w)):
    emb_vec_reduce.append((tk, reduce_emb_vec(word)))
  return emb_vec_reduce

# def write_append_data_to_txt_file(full_path_to_file, txt):
#     with open(full_path_to_file,'a') as out:
#         out.write(f'{txt}\n')
#         # out.write(f'{txt}')s
        
# def clear_file(full_path_to_files_list):
#     for _file in full_path_to_files_list:
#       with open(_file,'w') as out:
#         out.write(f'')


# In[5]:


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

def split_sentence(sentence, max_words):
    words = sentence.split()
    sub_sentences = []
    current_sub_sentence = []
    
    for word in words:
        current_sub_sentence.append(word)
        
        if len(current_sub_sentence) == max_words:
            sub_sentences.append(' '.join(current_sub_sentence))
            current_sub_sentence = []
    
    # Add any remaining words as the last sub-sentence
    if current_sub_sentence:
        sub_sentences.append(' '.join(current_sub_sentence))
    
    return sub_sentences


# In[6]:


sent = "bàn thắng Sang hiệp 2 , HLV Vũ_Hồng Việt yêu_cầu các học_trò tấn_công mạnh_mẽ hơn nữa , trong khi U16 Mông_Cổ có dấu_hiệu xuống sức rõ_rệt Những bàn thắng đến như một tất_yếu Riêng ở hiệp đấu này , Chí_Bảo đã ghi tới 4 bàn thắng , giúp U16 Việt_Nam thắng chung_cuộc 9 Như_vậy qua 2 trận đấu , U16 Việt_Nam toàn_thắng , ghi tới 14 bàn và để lọt_lưới 2 , hiệu_số bàn thắng_bại là 12 Tại bảng I lúc này , thầy_trò Vũ_Hồng Việt có cùng điểm_số như U16_Australia nhưng xếp dưới vì kém hiệu_số bàn thắng_bạ"
# eb = embedding_words_in_sents_full_shape(sent)

# print(eb)
already_embedded_set = set()
embedded_file = \
    "/Users/n2t2k/Documents/Studying/Master/Thesis/InProgress/Coding/ORIGIN_RUN_ALL_edge-oriented-graph-master-studying/dataProcessingOfficialCleaned/dev_processed/split_sentence_underthesea/code/BERT_merge_file/data/PubMed-VLSP_origin_after_processed_ERROR.txt"
clear_file([embedded_file])

# error_sent_embedded_file = \
#     "/Users/n2t2k/Documents/Studying/Master/Thesis/InProgress/Coding/ORIGIN_RUN_ALL_edge-oriented-graph-master-studying/dataProcessingOfficialCleaned/dev_processed/split_sentence_underthesea/code/BERT_merge_file/BERT_create_corpus/view_data/data/error_sent_embedded_file.txt"
# clear_file([error_sent_embedded_file])


out_all_sent = \
    "/Users/n2t2k/Documents/Studying/Master/Thesis/InProgress/Coding/ORIGIN_RUN_ALL_edge-oriented-graph-master-studying/dataProcessingOfficialCleaned/dev_processed/split_sentence_underthesea/code/BERT_merge_file/BERT_create_corpus/view_data/data/error_sent_embedded_file.txt"
error_count = 0
total_sent = 0
with open(out_all_sent, 'r') as in_file:
    lines = in_file.readlines()
    for sent_ls in lines:
        total_sent+=1
        sent_ls = sent_ls.replace("\n","").strip()
        # sent = "7 nguyên_nhân khiến Real_Madrid bị Barcelona bỏ_xa tại La_Liga Tờ Marca của Tây Ban_Nha đã chỉ ra những yếu_tố lý_giải cho sự khởi_đầu tệ_hại của Real_Madrid tại La_Liga 20172018"
        
        split_sent_word = sent_ls.split(" ")
        if len(split_sent_word) > 200:
            sent_ls = split_sentence(sent_ls, 200)
        else:
            sent_ls = [sent_ls]
        for sent in sent_ls:
            # try:
            if 1:
                worked = False
                print("processing ....sent ", sent)
                try:
                    emb_vec_reduce =  embedding_words_in_sents_full_shape(sent)
                except:
                    pass
                if not worked:
                    try:
                        sent = sent.replace(" Yingluk ", " ")
                        emb_vec_reduce =  embedding_words_in_sents_full_shape(sent)
                        worked = True
                    except:
                        pass

                if not worked:
                    try:
                        sent = sent.replace(" - "," ")              
                        emb_vec_reduce =  embedding_words_in_sents_full_shape(sent)
                        worked = True
                    except:
                        pass
                
                if not worked:
                    try:
                        sent = sent.replace("_"," ")              
                        emb_vec_reduce =  embedding_words_in_sents_full_shape(sent)
                        worked = True
                    except:
                        pass

                # print(emb_vec_reduce)
                for tk, em_w in emb_vec_reduce:
                    if tk in already_embedded_set:
                        continue
                    already_embedded_set.add(tk)
                    em_w_ls = em_w.tolist()
                    em_w_ls = " ".join(map(str, em_w_ls))      
                    write_append_data_to_txt_file(embedded_file, f"{tk} {em_w_ls}")
            # except:
            #     error_count +=1
                # write_append_data_to_txt_file(error_sent_embedded_file, sent)
                print(sent, "\n")
            # break
            if error_count == 1:
                break

print("already_embedded_set word: ", len(already_embedded_set))
print("total_sent: ", total_sent)
print("error_count sent: ", error_count)



# In[7]:


# s = "Phạm tội thuộc một trong các trường hợp sau đây , thì bị phạt tù từ bảy năm đến mười lăm năm a Có tổ chức b Phạm tội nhiều lần c Lợi dụng chức vụ , quyền hạn d Lợi dụng danh nghĩa cơ quan , tổ chức đ Vận chuyển , mua bán qua biên giới e Sử dụng trẻ em vào việc phạm tội hoặc bán ma tuý cho trẻ em g Nhựa thuốc phiện , nhựa cần sa hoặc cao côca có trọng lượng từ năm trăm gam đến dưới một kilôgam h Hêrôin hoặc côcain có trọng lượng từ năm gam đến dưới ba mươi gam i Lá , hoa , quả cây cần sa hoặc lá cây côca có trọng lượng từ mười kilôgam đến dưới hai mươi lăm kilôgam k Quả thuốc phiện khô có trọng lượng từ năm mươi kilôgam đến dưới hai trăm kilôgam l Quả thuốc phiện tươi có trọng lượng từ mười kilôgam đến dưới năm mươi kilôgam m Các chất ma tuý khác ở thể rắn có trọng lượng từ hai mươi gam đến dưới một trăm gam n Các chất ma tuý khác ở thể lỏng từ một trăm mililít đến dưới hai trăm năm mươi mililít o Có từ hai chất ma tuý trở lên mà tổng số lượng của các chất đó tương đương với số lượng chất ma tuý quy định tại một trong các điểm từ điểm g đến điểm n khoản 2 Điều này p Tái phạm nguy hiểm"

# sent_ls = split_sentence(s, 255)
# print(sent_ls)
sent = \
    "Các nhà điều tra bắt đầu thẩm vấn 3 nhân viên cảnh sát trong đó có viên sĩ quan cảnh sát nói trên vào tối 21 9 về việc bà Yingluk trốn thoát"
sent = sent.replace(" Yingluk ", " ")
emb_vec_reduce =  embedding_words_in_sents_full_shape(sent)

