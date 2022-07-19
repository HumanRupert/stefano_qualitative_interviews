The scripts to convert surveys of Afghan Ministry of Education about ghost workers from Word to CSV.

## Script Assumptions ##
The `transform_load` function in `load.py` works for any series of inputs as long as they're Word documents and have the following properties:
- There is only one table in the document.
- Tables all have the same format and order.
- There are 27 interviewee questions, 5 construal questions, and table fields as described in `COLUMNS` constant.
- Questions are worded properly and according to the list of questions in `QUESTIONS` and `CONSTRUAL_QUESTIONS` constants. Because the wording of the questions differ in some files, Levenshtein Distance percentage between simplified strings (that is, the string without dashes, spaces, commas, and lowercased) is used to identify them. The similiarity (`(1-lev)/len(paragraph)`) must be greater than or equal to 70%. The next question must be between the end of the answer to the current question and the end of the file (the list of indices of questions will be strictly increasing). If there are multiple matches, the most similar is used.
- Every paragraph between the current and the next question is the answer to the current question. For the last interviewee question, everything up to the first blank paragraph is the answer. For the last construal question, everything until the end of the file is the answer.
- Construal questions come after interviewee questions and are the last thing in the file.
- Paragraphs starting with "On" and "Regarding" are metadata and disposable.
- In some of the files, there's a line break in the 4th construal question. The script tolerates the incosistency using `_fix_inconsistent_qs` method.
- In some of the files, q22 is worded such that q23 has a lower Levenshtein Distance to the original question. The script tolerates it by removing "revenue office" instances from all paragraphs. The procedure might interrupt other questions that include the phrase.
  
## Directory structure ##
It doesn't matter how the files and folders are placed in the root folder. The script uses `glob` and runs a recursive sub-folder search to find all the files that satisfy a regex expression.

### A Note About Kabul ###
All the files for Kabul region that need to be transformed should include "translated" (case insensitive) in their name. Rest of the files should not include translated or they'll be processed by the algorithm, too (which will probably cause an error). Originally, however, Kabul files are not named consistently. You may need to rename files manually to make them comply with the requirements.

A couple of surveys (*تحریری Education Council Memeber* and *NGO (تحریریM Arif Parsa GIZ Program Assisstant)*) have separate files for the table and the questions. You should manually merge them before running the script.