The scripts to convert surveys of Afghan Ministry of Education about ghost workers from Word to CSV.

## How to Run ##
Download the files from Dropbox and put them (without the parent directory) in `data/`. `REGIONS` and their file loading methods are set up in `files.py`. To transform data for a region, pass their `Region` instance to `transform_load` method in `load.py`. To add a new region, you just have to define a function that lists the address of the documents that need to be processed (as a list of strings), create a `Region` instance with it, and feed it to `transform_load`. The output is saved in `out/` as a CSV file with the name of the region.

## Script Assumptions ##
The `transform_load` function in `load.py` works for any series of inputs as long as they're Word documents and have the following properties:
- There is only one table in the document.
- Tables all have the same format and order.
- There are 27 interviewee questions, 5 construal questions, and table fields as described in `COLUMNS` constant.
- Questions are worded properly and according to the list of questions in `QUESTIONS` and `CONSTRUAL_QUESTIONS` constants. Because the wording of the questions differ in some files, Levenshtein Distance percentage between simplified strings (that is, the string without dashes, spaces, commas, and lowercased) is used to identify them. The similiarity (`(1-lev)/len(paragraph)`) must be greater than or equal to 70%. The next question must be between the end of the answer to the current question and the end of the file (the list of indices of questions will be strictly increasing). If there are multiple matches, the most similar is used.
- Every paragraph between the current and the next question is the answer to the current question. For the last interviewee question, everything up to the first blank paragraph is the answer. For the last construal question, everything until the end of the file is the answer.
- Construal questions come after interviewee questions and are the last thing in the file.
- Questions and their answers are in separate, consequent paragraphs.
- Paragraphs starting with "On" and "Regarding" are metadata and disposable.
- In some of the files, there's a line break in the 4th construal question. The script tolerates the incosistency using `_fix_inconsistent_qs` method.
- In some of the files, q22 is worded such that q23 has a lower Levenshtein Distance to the original question. The script tolerates it by removing "revenue office" instances from all paragraphs. The procedure might interrupt other questions that include the phrase.
  
## Directory structure ##
It doesn't matter how the files and folders are placed in the root folder. The script uses `glob` and runs a recursive sub-folder search to find all the Word documents (.docx extension) that satisfy a regex expression.
- Kabul: Filename should include "translated"
- Kandahar: Filename should include "eng"
- Nangrahar: Filename should include "English"
- Parwan: Filename should NOT include "رضایت"
  
You may have to manually rename the files to make them comply with the requirements.

## Notes About Kabul ##
A couple of surveys (*تحریری Education Council Memeber* and *NGO (تحریریM Arif Parsa GIZ Program Assisstant)*) have separate files for the table and the questions. You should manually merge them before running the script.

## Notes about Parwan ##
In some of the files, the answer to construal questions are in the same line as the question. You may have to manually edit them and put a line break between the questions and responses.