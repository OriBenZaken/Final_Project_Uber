import sys
import pandas as pd
import utils as ut

def main(argv):
    # read the csv using panda.
    file_name = argv[0]
    data_frame = pd.read_csv(file_name, low_memory=False)
    print data_frame.head()

    data_frame = ut.clean_null_values(data_frame)
    dada_frame = ut.add_fetures(data_frame, 'date_time')
    # special mapping
    data_frame = uber_mapping(dada_frame)
    drop_list = ['date_time']
    data_frame = ut.drop_irrelevant_cols(data_frame, drop_list)
    ut.plot_correlations(data_frame)
    ut.save_filtered_file(file_name, data_frame)


base_code_map = {}
base_code_list = ['B02512', 'B02598', 'B02617', 'B02682', 'B02764', 'B02765', 'B02835', 'B02836']
for i,item in enumerate(base_code_list):
    base_code_map[item] = i

def uber_mapping(data_frame):
    data_frame['Base'] = data_frame.apply(base_code_convert, axis=1)
    return  data_frame

def base_code_convert(row):
    val = str(row['Base'])
    return base_code_map[val]

if __name__ == '__main__':
    main(sys.argv[1:])