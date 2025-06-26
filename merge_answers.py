import os
import json
from docx import Document
import re
import sys

def extract_task_type(filename):
    """Extracts task type (A, B, C) from filename."""
    match = re.search(r'Task\s*([ABC])', filename, re.IGNORECASE)
    return match.group(1).upper() if match else None

def extract_student_id(filename):
    """Extracts student ID from filename."""
    match = re.search(r'ID(\d+)', filename)
    return match.group(1) if match else None

def get_answer_from_doc(file_path):
    """Extracts the final answer from the last paragraph of a .docx file."""
    try:
        doc = Document(file_path)
        # It's safer to find the last non-empty paragraph
        text = ""
        for p in reversed(doc.paragraphs):
            if p.text.strip():
                text = p.text.strip()
                break
        return text
    except Exception as e:
        print(f"  -> Could not process answer file {os.path.basename(file_path)}: {e}")
        return ""

def main():
    """
    Merges student answers from the 'Answers - Cleaned' directory into the
    main project JSON file.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(script_dir)
    
    json_path = os.path.join(base_dir, 'final_project_data.json')
    answers_dir = os.path.join(base_dir, 'Answers - Cleaned')

    if not os.path.exists(json_path):
        print(f"ERROR: Main data file not found at '{json_path}'")
        sys.exit(1)
    if not os.path.isdir(answers_dir):
        print(f"ERROR: Answers directory not found at '{answers_dir}'")
        sys.exit(1)
        
    # 1. Load the main JSON data
    print(f"Loading data from '{os.path.basename(json_path)}'...")
    with open(json_path, 'r', encoding='utf-8') as f:
        student_data = json.load(f)
    
    # Create a dictionary for easy lookup by student_id
    student_map = {str(s['student_id']): s for s in student_data}
    
    # 2. Process the answers directory
    print(f"Processing answers from '{os.path.basename(answers_dir)}' directory...")
    answers_found = 0
    for filename in os.listdir(answers_dir):
        if filename.endswith('.docx') and not filename.startswith('~'):
            student_id = extract_student_id(filename)
            task_type = extract_task_type(filename)
            
            if student_id and task_type:
                if student_id in student_map:
                    answer_path = os.path.join(answers_dir, filename)
                    submission = get_answer_from_doc(answer_path)
                    
                    # 3. Add the data to the student's record
                    student_map[student_id]['task_type'] = task_type
                    student_map[student_id]['final_submission'] = submission
                    answers_found += 1
                else:
                    print(f"  - Warning: Found answer for ID {student_id}, but this ID is not in the main JSON file.")

    print(f"Merged answers for {answers_found} students.")

    # 4. Save the updated data back to the file
    print(f"Saving updated data back to '{os.path.basename(json_path)}'...")
    # The student_data list is already updated because student_map holds references
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(student_data, f, indent=4)
        
    print("Merge complete.")

if __name__ == "__main__":
    main() 