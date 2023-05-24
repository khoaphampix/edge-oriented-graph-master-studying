### VLPS.tvs to Pubtatoe
# replace file name: train as dev 
    - dev: VLSP2020_RE_dev_org_use_TRAIN_as_DEV
    - train: VLSP2020_RE_dev


DEV

total: 250
double_quote: 11
no_relation: 45
skip_review_later: 1
data_errors_: 13
worked_files: 180

TRAIN
total: 506
double_quote: 33
no_relation: 124
skip_review_later: 0
data_errors_: 9
worked_files: 340

WE
total set 521
valid:  329


Pubtator format: 
    23351998|t|
    23351998|a| <passage>
    23351998    <ent>
    23351998    <rel>

# When update code from Working to here (studying)
## rename from/to


"/Users/n2t2k/Documents/Studying/Master/Thesis/InProgress/Coding/ORIGIN_RUN_ALL_edge-oriented-graph-master-studying/dataProcessingOfficialCleaned/dev_processed




view_data.py
    desc: To view all raw VLSP.tsv files, check and filter:
        - valid file --> process this
        - no_relation
        - error_files
        - worked_files_excel
        - skip_review_late



processing_data.py
    desc: To create Pubtator format from raw VLSP.tsv files
    IN:
        <valid files> choosen by the view_data.py

    OUT: 
        vlsp to <pubtator-format> dev_processed/processed_txt


        dev_processed/CDR_DevelopmentSet.PubTator.txt
            merger all <dev_processed/processed_txt> to a file
        
        dev_processed/ All_sentence.PubTator.txt
            merger all <dev_processed/processed_txt> sentence only

        error & except file:
            error

### Main processing file

## 1.split_sentence_from_paragraph.py
## 2.WordEmbeddingPhoBERT.ipynb
## 3.AfterWBProcessBeforeAppliedToGNN.ipynb

## 4.processed.ipynb
### 4.1.pre_processed_slit_docs_and_ent_in_ent.ipynb
### 4.2.pre_processed_ent_not_in_sent.ipynb




## 1.split_sentence_from_paragraph.py

"""
DESC : split sentence smartly by underthesea
        split to sentence smartly by underthesea (recognize 20.10, TP.HCM ...)
        replace xa0 (bug by text after processed by underthesea)
    to create:
        - split sentence 
        - split sentence with vn token _ (viet_nam)

INPUT: 
    - all docs, 1 paragraph - 1 line (filter (no-relation) raw data without any processing like: remove dot, quote ...)
    - All_sentence.PubTator.txt
    
OUTPUT: 
    - all docs, 1 paragraph - with splited sentences with struct: <code><$$##$$$$##$$><sent><$$##$$$$##$$><sent>
        <split_sentence_from_paragraph.txt>
        <docs/split_sentence_with_token_from_paragraph.txt>


## 2.WordEmbeddingPhoBERT.ipynb

 OUT:
    - err_code_docs.txt"
    - valid_embedded_files_list.txt'
    - word_embedded_files/<single-files-by-docs-code>


## 3.AfterWBProcessBeforeAppliedToGNN.ipynb

IN:
    split_sentence_with_token_from_paragraph.txt'
    valid_embedded_files_list.txt'

OUT:
    full_dict_for_replace_token.json'






## 4.processed.ipynb

IN:
common_info_embedd_files/split_passage_for_final_processed"

OUT 
    - processed_OUT_PATH vlsp.data"
    - common_info_embedd_files/processed_error_files.data"

    Intermediate <feedback> <re-run-until-clean>
    -  error_not_found_ent_in_msg_to_half_manual_edit_words_in_doc



2


YES. Increasing number of epochs over-fits the CNN model. This happens because of lack of train data or model is too complex with millions of parameters. To handle this situation the options are

we need to come-up with a simple model with less number of parameters to learn
add more data by augmentation
add noise to dense or convolution layers
add drop-out layers
add l1 or l2 regularizers
add early stopping
check the model accuracy on validation data
early stopping will tell you appropriate epochs without overfitting the model

https://www.v7labs.com/blog/overfitting

https://sisyphus.gitbook.io/project/deep-learning-basics/basics/multi-class-and-cross-entropy-loss

https://devblogs.microsoft.com/cse/2016/09/13/training-a-classifier-for-relation-extraction-from-medical-literature/



Reduce the batch size: This is the most common solution to the "CUDA out of memory" error. Try reducing the batch size until the error goes away. You can experiment with different batch sizes to find the largest size that does not produce the error.

Reduce the complexity of the model: If reducing the batch size does not work, you may need to reduce the complexity of your model. Try simplifying your model architecture, removing unnecessary layers or parameters, or using a smaller pre-trained model.

Use a larger GPU: If your current GPU does not have enough memory to train your model, you can try upgrading to a larger GPU with more memory.

Use gradient checkpointing: Gradient checkpointing is a technique that allows you to trade off memory usage for computation time. It does this by recomputing certain intermediate values during the backward pass, rather than storing them in memory. This can help reduce the memory usage of your model.

Use mixed-precision training: Mixed-precision training is a technique that uses lower-precision data types (e.g., float16 instead of float32) to reduce the memory usage of your model. This can significantly reduce the memory requirements of your model, allowing you to train larger models with the same hardware.

Free up GPU memory: You can also try freeing up GPU memory by deleting unnecessary variables or tensors, or by using PyTorch's memory management functions (e.g., torch.cuda.empty_cache()).


### IMPORTANCE NOTE WHEN CLEAN DATA - ENTITY BY 4.2 & 4

1. back up a version (WORKED FILES of "split_passage_for_final_processed")

PATH: dataProcessingOfficialCleaned/dev_processed/split_sentence_underthesea/docs/common_info_embedd_files/split_passage_for_final_processed

2. MERGE old - new --> reuse the old result
3. NOTE to clear ALL related word, entit, in a docs that "repeatly exist on error" 
ON "ent_not_in_set"

PATH: dataProcessingOfficialCleaned/dev_processed/split_sentence_underthesea/error/manuall_edited/ent_not_in_set
fx: Song Hong | Tong cong ty cap nuoc Song Hong


## FOR BIG FILE --> REDUCE FILE SIZE
TWO function to check:
1. doc with many relation - ON split_passage_for_final_processed
2. size/number char (len) of a doc after process - ON vlsp.data


ssh -p 8964 root@sshe.jarvislabs.ai
ssh -p 8966 root@sshe.jarvislabs.ai

scp -P 8962 /Users/n2t2k/Documents/Studying/Master/Thesis/InProgress/Coding/ORIGIN_RUN_ALL_edge-oriented-graph-master-studying/data/VLSP/processed.zip  root@sshe.jarvislabs.ai:/home/edge-oriented-graph-master-studying/data/VLSP/processed

scp /Users/n2t2k/Documents/Studying/Master/Thesis/InProgress/Coding/ORIGIN_RUN_ALL_edge-oriented-graph-master-studying/dataProcessingOfficialCleaned/dev_processed/split_sentence_underthesea/code/BERT_merge_file/data/PubMed-VLSP.txt.zip root@65.108.32.172:/home/edge-oriented-graph-master-studying/embeds/PubMed-VLSP.txt.zip



unzip processed
cp processed/* .

ssh -p 8962 root@sshe.jarvislabs.ai

scp -P 8962 /Users/n2t2k/Documents/Studying/Master/Thesis/InProgress/Coding/ORIGIN_RUN_ALL_edge-oriented-graph-master-studying/dataProcessingOfficialCleaned/dev_processed/split_sentence_underthesea/code/BERT_merge_file/data/PubMed-VLSP.txt.zip root@sshe.jarvislabs.ai:/home/edge-oriented-graph-master-studying/embeds/PubMed-VLSP.txt.zip



case check split sentence manually
[.][\s][A-Z]

[ ][.][|][0-9][ ][.][|]

\.|\b\w{1,9}\.|

.|- ? .|
 

[ ][.][|]\- ? [ ][.][|]

ssh -p 8962 root@sshe.jarvislabs.ai

scp /Users/n2t2k/Documents/Studying/Master/Thesis/InProgress/Coding/ORIGIN_RUN_ALL_edge-oriented-graph-master-studying/dataProcessingOfficialCleaned/dev_processed/split_sentence_underthesea/code/BERT_merge_file/data/PubMed-VLSP.txt.zip root@65.108.32.172:/home/edge-oriented-graph-master-studying/embeds/PubMed-VLSP.txt.zip


scp -P 8962 /Users/n2t2k/Documents/Studying/Master/Thesis/InProgress/Coding/ORIGIN_RUN_ALL_edge-oriented-graph-master-studying/data/VLSP/processed_copy_big.zip root@sshe.jarvislabs.ai:/home/edge-oriented-graph-master-studying/data/VLSP/processed_copy_big.zip

/home/edge-oriented-graph-master-studying/dataProcessingOfficialCleaned/dev_processed/split_sentence_underthesea/code/BERT_merge_file/BERT_create_corpus/


scp /Users/n2t2k/Documents/Studying/Master/Thesis/InProgress/Coding/ORIGIN_RUN_ALL_edge-oriented-graph-master-studying/dataProcessingOfficialCleaned/dev_processed/split_sentence_underthesea/code/BERT_merge_file/BERT_create_corpus/view_data/server_code/6.3.WordEmbeddingPhoBERT.ipynb root@65.108.32.184:/home/edge-oriented-graph-master-studying/dataProcessingOfficialCleaned/dev_processed/split_sentence_underthesea/code/BERT_merge_file/BERT_create_corpus/view_data/server_code



scp /Users/n2t2k/Documents/Studying/Master/Thesis/InProgress/Coding/ORIGIN_RUN_ALL_edge-oriented-graph-master-studying/dataProcessingOfficialCleaned/dev_processed/split_sentence_underthesea/code/BERT_merge_file/BERT_create_corpus/view_data/server_code/python_.py root@65.108.32.184:/home/edge-oriented-graph-master-studying/dataProcessingOfficialCleaned/dev_processed/split_sentence_underthesea/code/BERT_merge_file/BERT_create_corpus/view_data/server_code


scp /Users/n2t2k/Documents/Studying/Master/Thesis/InProgress/Coding/ORIGIN_RUN_ALL_edge-oriented-graph-master-studying/dataProcessingOfficialCleaned/dev_processed/split_sentence_underthesea/code/BERT_merge_file/data.zip  root@65.108.32.184:/home/edge-oriented-graph-master-studying/dataProcessingOfficialCleaned/dev_processed/split_sentence_underthesea/code/BERT_merge_file/


scp /Users/n2t2k/Documents/Studying/Master/Thesis/InProgress/Coding/ORIGIN_RUN_ALL_edge-oriented-graph-master-studying/dataProcessingOfficialCleaned/dev_processed/split_sentence_underthesea/code/BERT_merge_file/BERT_create_corpus/view_data/data.zip root@65.108.32.184:/home/edge-oriented-graph-master-studying/dataProcessingOfficialCleaned/dev_processed/split_sentence_underthesea/code/BERT_merge_file/BERT_create_corpus/view_data/



jupyter nbconvert --execute --to python /home/edge-oriented-graph-master-studying/dataProcessingOfficialCleaned/dev_processed/split_sentence_underthesea/code/BERT_merge_file/BERT_create_corpus/view_data/server_code/6.3.WordEmbeddingPhoBERT.ipynb



jupyter nbconvert --execute --to python /home/edge-oriented-graph-master-studying/dataProcessingOfficialCleaned/dev_processed/split_sentence_underthesea/code/BERT_merge_file/BERT_create_corpus/view_data/server_code/6.3.WordEmbeddingPhoBERT.ipynb


cd /home/edge-oriented-graph-master-studying/dataProcessingOfficialCleaned/dev_processed/split_sentence_underthesea/code/BERT_merge_file/BERT_create_corpus/view_data

jupyter nbconvert --execute 6.4.LARGE_WordEmbeddingPhoBERT.ipynb



scp /Users/n2t2k/Documents/Studying/Master/Thesis/InProgress/Coding/ORIGIN_RUN_ALL_edge-oriented-graph-master-studying/dataProcessingOfficialCleaned/dev_processed/split_sentence_underthesea/code/BERT_merge_file/BERT_create_corpus/view_data/PubMed-VLSP-v1.2-large-192.txt.zip  root@65.108.32.175:/home/edge-oriented-graph-master-studying/embeds


scp /Users/n2t2k/Documents/Studying/Master/Thesis/InProgress/Coding/ORIGIN_RUN_ALL_edge-oriented-graph-master-studying/dataProcessingOfficialCleaned/dev_processed/split_sentence_underthesea/code/BERT_merge_file/BERT_create_corpus/view_data/data.zip  root@65.108.32.175:/home/edge-oriented-graph-master-studying/embeds


scp /Users/n2t2k/Documents/Studying/Master/Thesis/InProgress/edge-oriented-graph-master-WORKING/dataProcessingOfficial/dev_processed/split_sentence_underthesea/code/BERT_merge_file/data/PubMed-VLSP-new-final-standard-256-large-24-05-23_.txt.zip root@65.108.32.175:/home/edge-oriented-graph-master-studying/embeds

scp /Users/n2t2k/Documents/Studying/Master/Thesis/InProgress/Coding/ORIGIN_RUN_ALL_edge-oriented-graph-master-studying/data/BERT_embedded_words/PubMed-VLSP_256-large-24-05-23.txt.zip root@65.108.33.66:/home/edge-oriented-graph-master-studying/embeds