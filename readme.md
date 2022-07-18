The scripts to convert surveys of Afghan Ministry of Education about ghost workers from Word to CSV.

Note that conversion scripts for each district is unique, as the data have not been consistently collected. Each data collection script makes certain assumptions about the input.

## Script Assumptions ##
The `transform_load` function in `load.py` works for any series of inputs as long as they're Word documents and have the following properties:
- There is only one table in the document.
- Tables all have the same format and order.
- There are 27 interviewee questions, 5 construal questions, and table fields as described in `COLUMNS` constant.
- Questions are worded properly and according to the list of questions in `QUESTIONS` and `CONSTRUAL_QUESTIONS` constants. In one of the questions, reluctant is spelled "relunctant", the script tolerates the difference.
- Every paragraph between the current and the next question is the answer to the current question. For the last interviewee question, everything up to the first blank paragraph is the answer. For the last construal question, everything until the end of the file is the answer.
- Paragraphs starting with "On" are metadata and disposable.