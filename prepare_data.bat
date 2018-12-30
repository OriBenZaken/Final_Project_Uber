echo off
echo Prepare model data from Uber raw files:

echo Cleansing the data and adding features. This phase may take some time...
python cleansing.py src_files filtered_data

echo Concatinating all filtered data files
python concat_files.py filtered_data

echo Splitting the data to training data and testing data
python splitting.py filtered_data\unified.csv

echo Done!
pause