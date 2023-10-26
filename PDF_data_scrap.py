#PDF scrapping
#This code I was extracting a serie of questions from a PDF file
"""
    Extracts questions and answer options from a given text.

    Parameters:
    text (str): The text from which questions and answer options will be extracted.
    pdf_name (str): The name of the source PDF.

    Returns:
    list: A list of dictionaries, where each dictionary contains a question, its answer options, and the name of the source PDF.

    Output Dictionary Structure:
    {
        "Question": str, # The extracted question.
        "A": str,        # Text of answer option A.
        "B": str,        # Text of answer option B.
        "C": str,        # Text of answer option C.
        "D": str,        # Text of answer option D.
        "Source_PDF": str # Name of the source PDF.
    }

    Usage Example:
    >>> extract_questions_from_text("1. What is the color of the sky? A. Red B. Blue C. Green D. Yellow", "example.pdf")
    [{'Question': 'What is the color of the sky?', 'A': 'Red', 'B': 'Blue', 'C': 'Green', 'D': 'Yellow', 'Source_PDF': 'example.pdf'}]

    Notes:
    - The input text must have a specific format where questions are numbered and answer options are preceded by 'A.', 'B.', 'C.', and 'D.'.
    - The function uses regular expressions to identify and extract the questions and answer options.
    """
import re
import pandas as pd
from PyPDF2 import PdfReader
import openpyxl


def extract_questions_from_text(text, pdf_name):
    blocks = re.split(r'(?<![0-9])(\d{1,3}\.\s)(?![0-9])', text)[1:]
    blocks = [blocks[i] + blocks[i+1] for i in range(0, len(blocks), 2)]

    data = []

    for block in blocks: 
        q_data = {
            "Question": None,
            "A": None,
            "B": None,
            "C": None,
            "D": None,
            "Source_PDF": pdf_name
        }

        # Extract the main question by finding the first option 'A.' and slicing the string
        if 'A.' in block:
            idx = block.index('A.')
            q_data["Question"] = block[:idx].strip()
            options_text = block[idx:]
        else:
            q_data["Question"] = block
            options_text = ''

        # Extract the options
        for option in ['A', 'B', 'C', 'D']:
            opt_match = re.search(r'({}\.\s.+?)(?:{}\.\s|$)'.format(option, chr(ord(option)+1)), options_text, re.DOTALL)
            if opt_match:
                q_data[option] = opt_match.group(1).split('.', 1)[-1].strip()

        data.append(q_data)

    return data

#Bcs I had a lot of PDF's, this code allows to itereate through it all

all_data = []
base_path ="your path"
for i in range(1, 11):  # Numero de PDFS
    pdf_name = f'practice_questions_{i}'
    pdf_path = base_path + f'{pdf_name}.pdf'

    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()

    all_data.extend(extract_questions_from_text(text, pdf_name))

df = pd.DataFrame(all_data)

#saving as excel file

df.to_excel("Questions.xlsx", index=False, engine='openpyxl')


#Extracting Aswers from another PDF

"""
    Extracts and organizes data from a PDF file into a pandas DataFrame.

    Parameters:
    pdf_path (str): The file path to the PDF from which data will be extracted.

    Returns:
    pd.DataFrame: A DataFrame containing the extracted questions, answers, explanations, and source information.

    Output DataFrame Structure:
    | question | answer | explanation | source |
    |----------|--------|-------------|--------|
    | str      | str    | str         | str    |

    Usage Example:
    >>> df = extract_data_from_pdf("/path/to/your/pdf_file.pdf")
    >>> print(df.head())
       question answer explanation             source
    0       ...      A ...                     pdf_file
    1       ...      B ...                     pdf_file
    ...     ...    ... ...                         ...

    Notes:
    - The input PDF must have a specific text structure for the regular expression pattern to successfully extract the data.
    - Ensure to import the necessary libraries and replace `PdfReader` and `page.extract_text()` with the actual classes and methods provided by the PDF reading library you are using.
    - The source column in the output DataFrame contains the name of the PDF file without the '.pdf' extension.
    """

def extract_answers_from_pdf(pdf_path):
    with open(pdf_path, "rb") as file:
        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()

    pattern = re.compile(r'(\d+)\.\s([A-D])\.\s(.+?)(?=\d+\.\s[A-D]\.\s|$)', re.DOTALL)
    matches = pattern.findall(text)

    questions = []
    answers = []
    explanations = []

    for match in matches:
        questions.append(match[0])
        answers.append(match[1])
        explanations.append(match[2].strip())

    df = pd.DataFrame({
        'question': questions,
        'answer': answers,
        'explanation': explanations,
        'source': pdf_path.split('/')[-1].replace('.pdf','')
    })

    return df


dfs = []
for i in range(1, 11):  # input the number of pdf files
    pdf_path = f"{base_path}practice_answers_{i}.pdf"
    dfs.append(extract_answers_from_pdf(pdf_path))

final_df = pd.concat(dfs, ignore_index=True)

#save to excel

final_df.to_excel("answers.xlsx", index=False, engine='openpyxl')
