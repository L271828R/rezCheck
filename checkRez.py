import openai
import fitz

# Set your OpenAI API key
def validate_text(variable, max_words):
    if not isinstance(variable, str):
        print("Error: Variable is not a string.")
        return False

    words = variable.split()
    if len(words) > max_words:
        print(f"Error: Text exceeds {max_words} words.")
        return False

    return True

def extract_text_from_file(file_path):
    with open(file_path, 'r') as file:
        text = file.read()
    return text

def extract_text_from_pdf(pdf_path):
    with fitz.open(pdf_path) as pdf_doc:
        num_pages = pdf_doc.page_count
        for page_num in range(num_pages):
            page = pdf_doc[page_num]
            text = page.get_text()
        return(f"\n{text}\n")

def check_spelling_and_grammar(text):
    # Call OpenAI API for spelling and grammar check
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an American speaker with a background in technology and as an English teacher who enjoys reviewing resumes."},
            {"role": "user", "content": f"can you explain in a list what specific text is either misspelled or is difficult to undertand: {text}, keep in mind the reader of the resume is highly technical as well."}
        ]
    )
    corrected_text = response.choices[0].message
    return corrected_text

def compare_resumes(resume_text, job_requirements_text):
    # Call OpenAI API to compare resumes
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a American native speaker with a background in technology and as an English teacher"},
            {"role": "user", "content": f"Compare the applicant's resume to the job requirements:\nResume: {resume_text}\nJob Requirements: {job_requirements_text}"}
        ]
    )
    comparison_score = response.choices[0].message
    return comparison_score

# Example usage
resume_path = 'resume.pdf'
job_requirements_path = 'requirements.txt'

resume_text = extract_text_from_pdf(resume_path)
if (validate_text(resume_text, 400)):
    print("text is good");
    corrected_resume = check_spelling_and_grammar(resume_text)
    print("-----------")
    print(corrected_resume)
else:
    print(f"text failed, word count = {len(resume_text)}")
# job_requirements_text = extract_text_from_file(job_requirements_path)


# print (resume_text)
# Functionality 1: Check spelling and grammar
# corrected_resume = check_spelling_and_grammar(resume_text)
# print(f"Corrected Resume:\n{corrected_resume}\n")
# 
# # Functionality 2: Compare resumes
# score = compare_resumes(resume_text, job_requirements_text)
# print(f"Resume Similarity Score: {score}")

