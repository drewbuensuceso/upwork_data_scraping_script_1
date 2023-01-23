# install requirements

pip install -r requirements.txt

# how to run (NOTE: INSTALL THE REQUIREMENTS FIRST USING THE COMMAND ABOVE (ON LINUX SYSTEMS), FOR WINDOWS, USE WSL2)

1) PUT your ISIN list in folder reference_files
2) RUN xid_extractor.py
    - first, edit out line 61 with the path of the new ISINs.csv file which you put in step 1
    - python3 xid_extractor.py
3) RUN processor.py
    - python3 processor.py