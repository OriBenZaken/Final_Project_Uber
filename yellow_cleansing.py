import pandas as pd
import numpy as np
import holidays
import sys
import os
import utils as ut
import utils as ut


def yellow_clean(file_name,data_frame):
    data_frame = ut.clean_null_values(data_frame)
    drop_list = ['store_and_fwd_flag', 'vendor_id']
    data_frame = ut.drop_irrelevant_cols(data_frame,drop_list)
    dada_frame = ut.add_fetures(data_frame)
    #special mapping
    data_frame = yellow_mapping(dada_frame)
    ut.save_filtered_file(file_name,data_frame)

def yellow_mapping(data_frame):
    # payment_type mapping
    data_frame['payment_type'] = data_frame.apply(paymet_type_convert, axis=1)
    return  data_frame

def paymet_type_convert(row):
    val = str(row['payment_type']).lower()
    return payment_type_rep_to_code[val]

payment_type_rep_to_code = {}
for rep in ["credit", "crd", "cre","1"]:
    payment_type_rep_to_code[rep] = 1
for rep in ["cash", "cas", "csh","2"]:
    payment_type_rep_to_code[rep] = 2
for rep in ["no charge", "noc", "no","3"]:
    payment_type_rep_to_code[rep] = 3
for rep in ["dispute", "dis","4"]:
    payment_type_rep_to_code[rep] = 4
for rep in ["unk","5"]:
    payment_type_rep_to_code[rep] = 5
payment_type_rep_to_code["6"] = 6




