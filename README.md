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
  --model MODEL         Model server to use. (Use ls to find the model names).
  --batch_size BATCH_SIZE
                        Number of data to handle per batch transaction.
  --start_id START_ID   Specify ID for starting index for batch processing.
  --job_size JOB_SIZE   How many samples to submit per job.
```
