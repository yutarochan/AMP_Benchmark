# DS320
Anti-Microbial Peptide Classification Benchmark Utility

## Setup
All code developed under this repository were executed under Python 3.6.6.
To run the code in this repository, you must have the following dependencies installed.

**Package Dependencies**
```
bs4 == 0.0.1
requests == 2.18.4
selenium == 3.14.1
```
To install the listed dependencies above you can use the following command from `pip`:

```
sudo pip install -r requirements.txt
```

**Selenium WebDriver Installation**

To install `selenimum`, you must also have a client browser driver installed.

In our implementation, we have utilized the Chrome WebDrivers, which you can find
instructions for your corresponding operating system environment.

http://chromedriver.chromium.org/downloads

## File Structure
The project utilizes the following file structure and organization. Here we provide
a brief description for each folder and code within the file.

```
/data:  Folder for all data used in project.
    /fasta:     FASTA formatted datasets.
    /proc:      Output location for preprocessed datasets.
    /raw:       Source for raw dataset sources.
    /result:    All server side results reside here with each sub directory containing folders for each FASTA file,
                within it contains result output from each model in their respective folders. All merged files are
                located within the root of the respective FASTA file.
/docs:  Gitpages for project.
/files: Contains any reference materials, instructional documents, and project papers (LaTeX files).
/src:   Source code and utility scripts for project.
    /server:    All code for individual server models.
    /util:      Dataset preprocessing, merging, and file assertion scripts.
    main.py     Main CLI script used for running jobs.
```

## Program Execution
To run the program and begin submitting a batch job you can use the following command line options:
```
usage: main.py [-h] [--ls] [--data DATA] [--out OUT] [--model MODEL]
               [--batch_size BATCH_SIZE] [--start_id START_ID]
               [--job_size JOB_SIZE]

optional arguments:
  -h, --help            show this help message and exit
  --ls                  List all available servers.
  --data DATA           Path to dataset (Must be in FASTA format).
  --out OUT             Path to result output.
  --model MODEL         Model server to use. (Use --ls to find the model names).
  --batch_size BATCH_SIZE
                        Number of data to handle per batch transaction.
  --start_id START_ID   Specify ID for starting index for batch processing.
  --job_size JOB_SIZE   How many samples to submit per job.
```

## Server Scrape Process
The following section describes the whole scraping process and explains how to utilize the scripts in this repository.

1. The initial scraping process can be performed by running the following script:
```
python3 main.py --data <path-to-fasta-txt> --out <path-to-result-folder> --model <model name> --batch_size <use 10000>
```
Note that you don't have to specify the `--start_id` for first time runs, as it will always start at the first record in the dataset.

2. For subsequent runs, run the following script by adding the `--start_id` flag followed by the `PepID` you want to start running the script from. You can find the corresponding next PepID by going into the results, finding the last `PepID` and just shifting the index up by 1. For example, say if the last batch ended with `A00100`, then the next `--start_id` would have the value `A001001`.
```
python3 main.py --data <path-to-fasta-txt> --out <path-to-result-folder> --model <model name> --batch_size <use 10000> --start_id <PepID start index>
```

3. Always check to see if there are any odd signs of failure - there can be cases where a whole mini-batch may have failed (i.e. some blocks of -999 has occured). In this case you may have to wait for a bit (due to server overload), and re-run that particular set again. (More on this during our next meeting).

4. Make sure you frequently pull + push to this repository so that the results you have are constantly backed up and synced up.

## Scrape Status
| Dataset                    | Status                       |
|----------------------------|------------------------------|
| data.fasta.txt/ADAM_HMM    | Complete                     |
| data.fasta.txt/ADAM_SVM    | Complete                     |
| data.fasta.txt/AMPA        | Complete                     |
| data.fasta.txt/CAMPR3-ANN  | Complete                     |
| data.fasta.txt/CAMPR3-DA   | Complete                     |
| data.fasta.txt/CAMPR3-RF   | Complete                     |
| data.fasta.txt/CAMPR3-SVM  | Complete                     |
| data.fasta.txt/DBAASP      | Need to Process Missing List |
| data2.fasta.txt/ADAM_HMM   | In Progress                  |
| data2.fasta.txt/ADAM_SVM   | Not Initialized              |
| data2.fasta.txt/AMPA       | In Progress                  |
| data2.fasta.txt/CAMPR3-ANN | In Progress                  |
| data2.fasta.txt/CAMPR3-DA  | Not Initialized              |
| data2.fasta.txt/CAMPR3-RF  | Not Initialized              |
| data2.fasta.txt/CAMPR3-SVM | Not Initialized              |
| data2.fasta.txt/DBAASP     | Not Initialized              |
