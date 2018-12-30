import pandas as pd
import numpy as np
import holidays
import sys
import os
import utils as ut
import utils as ut


def green_clean(file_name,data_frame):
    drop_list = ['store_and_fwd_flag', 'vendor_id','ehail_fee','distance_between_service','time_between_service']
    data_frame = ut.drop_irrelevant_cols(data_frame,drop_list)
    data_frame = ut.clean_null_values(data_frame)
    dada_frame = ut.add_fetures(data_frame)
    data_frame = ut.remove_rows_with_zero_fare_amount(data_frame)
    #special mapping
    #todo: trip type
    #data_frame = yellow_mapping(dada_frame)
    ut.save_file(file_name, data_frame)
