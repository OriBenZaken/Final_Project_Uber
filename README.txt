On Uber raw data file (csv format) run:
1. python cleansing_uber.py <uber_raw_data_file>
    -> Functionality: Remove rows with nulls, remove irrelevant cols,
        add time and date col, add is_weekend and is_holiday cols,
        add demand per time interval col (predicted value)
    -> Output: uber_raw_data_file_filtered

2. python splitting.py <uber_raw_data_file_filtered>
    -> Functionality: Splits the data to:
    train file,target train file, test file, target test file
    -> Output: train file,target train file, test file, target test file