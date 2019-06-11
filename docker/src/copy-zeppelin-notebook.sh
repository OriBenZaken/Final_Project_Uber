#!/bin/bash

FILES="UberRecord.SCALA
IntializeUberRecordType.SCALA
LoadTrainDataToSpace.py"

toReplace='"'
replaceStr='\"'

# Create notebook in Zeppelin
NOTE_ID=$(curl -d '{"name" : myNotebook}' -X POST http://localhost:9090/api/notebook | python3 -c "import sys,json; print(json.load(sys.stdin)['body'])")

for f in $FILES
do
    printf "inserting paragraph: %s\n" "$f"
    # Get paragraph content
    FILE_CONTENT=$(cat /usr/local/$f)
    FILE_CONTENT="${FILE_CONTENT//$toReplace/$replaceStr}"

    # Create json input for Create Paragarph POST method
    printf -v data '{"title": "title", "text": "%s"}' "$FILE_CONTENT"

    # Create paragarph in Zeppelin notebook
    curl -d "$data" -X POST http://localhost:9090/api/notebook/$NOTE_ID/paragraph

    printf "\n"
done

# Run all Zeppelin notebook paragraphs
curl -i -X POST http://localhost:9090/api/notebook/job/$NOTE_ID

printf "\n"
