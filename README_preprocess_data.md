# When update code from Working to here (studying)
## rename from/to
edge-oriented-graph-master-WORKING/dataProcessingOfficial
ORIGIN_RUN_ALL_edge-oriented-graph-master-studying/dataProcessingOfficialCleaned



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
        dev_processed/processed_txt
            format: 
                23351998|t|
                23351998|a| <passage>
                23351998    <ent>
                23351998    <rel>

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