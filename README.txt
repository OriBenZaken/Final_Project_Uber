On Uber raw data file (csv format) run:

1. python cleansing.py <source_dir> <target_dir>
    -> Functionality: Remove rows with nulls, remove irrelevant cols,
        add time and date col, add is_weekend and is_holiday cols,
        add demand per time interval col (predicted value)
    -> Output: filtered data files inside the specified target dir

2. python concat_files <dir_name>
    -> Functionality: concat all the files in the specified dir
    -> Output: concatenated file

3. python splitting.py <data_file_filtered>
    -> Optional parameters and flags:
       -resample=<number of examples> : takes specified number of representative examples
       -target_dir=<target_dir_name> : name of the directory to same the model data. Default
                    name of the directory is "model_data"
    -> Functionality: Splits the data to:
       train file,target train file, test file, target test file
    -> Output: train file,target train file, test file, target test file

