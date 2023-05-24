#!/usr/bin/env python
# coding: utf-8

# In[1]:


from underthesea import sent_tokenize, word_tokenize

PhoBERT_base_fairseq_path = \
"/Users/n2t2k/Documents/Studying/Master/Thesis/InProgress/edge-oriented-graph-master-WORKING/PhoBERT_base_fairseq"

# PhoBERT_base_fairseq_path = \
# "/Users/n2t2k/Documents/Studying/Master/Thesis/InProgress/Coding/PhoBERT_large_fairseq"

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


import torch
import matplotlib.pyplot as plt

def draw_tensor(tensor):
    # Define the tensor

    # Convert the tensor to a NumPy array
    tensor_array = tensor.numpy()

    # Create a figure and axis
    fig, ax = plt.subplots()

    # Plot the tensor values
    ax.plot(tensor_array)

    # Set the labels and title
    ax.set_xlabel('Index')
    ax.set_ylabel('Value')
    ax.set_title('Tensor Visualization')

    # Display the plot
    plt.show()


# tensor = torch.randn(1024)
# print(tensor.shape)
# draw_tensor(tensor)


# In[5]:


import torch
import numpy as np
from sklearn.random_projection import SparseRandomProjection

def compress_vector(input_vector, input_dim, output_dim):
    # Convert the input tensor to a NumPy array
    vector = input_vector.detach().numpy()

    # Create a SparseRandomProjection object with the desired output dimensionality
    random_projection = SparseRandomProjection(n_components=output_dim)

    # Fit the random projection model to the vector and transform it to the reduced dimensionality
    compressed_vector = random_projection.fit_transform(vector.reshape(1, -1))

    # Flatten the compressed vector to a 1D list
    compressed_vector = compressed_vector.flatten()

    # Convert the compressed vector back to a PyTorch tensor
    compressed_vector = torch.from_numpy(compressed_vector)


    return compressed_vector


# input_vector = torch.randn(input_dim)
# print(input_vector.shape)
# print(input_vector)

# print(input_vector.size())
# # input_dim = 1024
# # output_dim = 128

# compressed_vector = compress_vector(input_vector, input_dim, output_dim)
# print(compressed_vector)
# print(len(compressed_vector))


# In[6]:


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
  # print("* "*100)
  # print("IN >> ", vt1)
  # print("IN >> ", vt1.shape,vt1.shape[0],  type(vt1))

  # print(vt1.shape, type(vt1))
  # input_dim = 1024
  input_dim = vt1.shape[0]
  output_dim = 192
  vt1_mean = compress_vector(vt1, input_dim, output_dim)

  # print("OUT >> ", vt1_mean.shape)
  # print("\n\n", "* "*40)
  # draw_tensor(vt1)
  # vt1 =  vt1.detach().to(torch.float64)
  # draw_tensor(vt1)
  # draw_tensor(vt1_mean)

  # print(vt1)
  # print(vt1_mean)
  # print(type(vt1), vt1.shape)
  vt1_mean = vt1_mean.numpy()
  print(type(vt1_mean), vt1_mean.shape)

  

  return vt1_mean


# def reduce_emb_vec(vt1):
#   print("* "*100)
#   # print("IN >> ", vt1)
#   # print("IN >> ", vt1.shape, type)

#   vt1_np = vt1.detach().numpy()
#   vt1_mean = vt1_np.reshape(-1, 4).mean(axis=1)
#   # print("OUT >> ", vt1_mean.shape)


#   print(type(vt1), vt1.shape)
#   print(type(vt1_mean), vt1_mean.shape)

#   return vt1_mean

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


# In[7]:


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


# In[8]:


# sent = "bàn thắng Sang hiệp 2 , HLV Vũ_Hồng Việt yêu_cầu các học_trò tấn_công mạnh_mẽ hơn nữa , trong khi U16 Mông_Cổ có dấu_hiệu xuống sức rõ_rệt Những bàn thắng đến như một tất_yếu Riêng ở hiệp đấu này , Chí_Bảo đã ghi tới 4 bàn thắng , giúp U16 Việt_Nam thắng chung_cuộc 9 Như_vậy qua 2 trận đấu , U16 Việt_Nam toàn_thắng , ghi tới 14 bàn và để lọt_lưới 2 , hiệu_số bàn thắng_bại là 12 Tại bảng I lúc này , thầy_trò Vũ_Hồng Việt có cùng điểm_số như U16_Australia nhưng xếp dưới vì kém hiệu_số bàn thắng_bạ"
# sent = " HLV Vũ_Hồng Việt yêu_cầu các học_trò"
# eb = embedding_words_in_sents_full_shape(sent)



# In[9]:


# print(eb[1])
# print(eb[1][1].shape)
# print(eb["bàn"])
# print(eb[0].shape)



# In[10]:


sent = "bàn thắng Sang hiệp 2 , HLV Vũ_Hồng Việt yêu_cầu các học_trò tấn_công mạnh_mẽ hơn nữa , trong khi U16 Mông_Cổ có dấu_hiệu xuống sức rõ_rệt Những bàn thắng đến như một tất_yếu Riêng ở hiệp đấu này , Chí_Bảo đã ghi tới 4 bàn thắng , giúp U16 Việt_Nam thắng chung_cuộc 9 Như_vậy qua 2 trận đấu , U16 Việt_Nam toàn_thắng , ghi tới 14 bàn và để lọt_lưới 2 , hiệu_số bàn thắng_bại là 12 Tại bảng I lúc này , thầy_trò Vũ_Hồng Việt có cùng điểm_số như U16_Australia nhưng xếp dưới vì kém hiệu_số bàn thắng_bạ"
eb = embedding_words_in_sents_full_shape(sent)


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
            emb_vec_reduce =  embedding_words_in_sents_full_shape(sent.strip())
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



# In[ ]:




