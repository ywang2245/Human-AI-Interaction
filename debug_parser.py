import os
import sys
from docx import Document
import re

def parse_dialogue_debug(doc_path):
    """
    Parses a .docx file and prints all raw paragraphs for debugging,
    then extracts the conversation history.
    """
    try:
        doc = Document(doc_path)
        paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
    except Exception as e:
        print(f"Error reading {doc_path}: {e}")
        return []

    print("--- RAW PARAGRAPHS READ FROM DOCX ---")
    for i, p in enumerate(paragraphs):
        print(f"[{i+1}]: {p}")
    print("-------------------------------------\n")

    dialogue_history = []
    student_text = []
    gpt_text = []
    state = 0  # 0=pre-convo, 1=student, 2=gpt

    for para in paragraphs:
        is_student_start = para.lower() == "you said:"
        is_gpt_start = para.lower() == "chatgpt said:"

        if state == 0:
            if is_student_start:
                state = 1
        elif state == 1:
            if is_gpt_start:
                state = 2
            else:
                student_text.append(para)
        elif state == 2:
            if is_student_start:
                dialogue_history.append({
                    "student": "\n".join(student_text).strip(),
                    "gpt": "\n".join(gpt_text).strip()
                })
                student_text, gpt_text = [], []
                state = 1
            else:
                gpt_text.append(para)

    if state == 2 and (student_text or gpt_text):
        dialogue_history.append({
            "student": "\n".join(student_text).strip(),
            "gpt": "\n".join(gpt_text).strip()
        })
    
    # We are now keeping all rounds.
    final_history = dialogue_history
    for i, turn in enumerate(final_history):
        turn["round"] = i + 1
    
    return final_history

def find_file_for_id(student_id):
    """Finds the docx file for a given student ID in the Conversations - Cleaned directory."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    conv_dir = os.path.join(os.path.dirname(script_dir), "Conversations - Cleaned")
    if not os.path.isdir(conv_dir):
        print(f"Error: Directory not found at {conv_dir}")
        return None
    for f in os.listdir(conv_dir):
        if f.endswith('.docx') and not f.startswith('._'):
            if re.search(f'\\bID{student_id}\\b', f, re.IGNORECASE):
                return os.path.join(conv_dir, f)
    return None

def main():
    if len(sys.argv) != 2 or not sys.argv[1].isdigit():
        print("Usage: python debug_parser.py <student_id>")
        return
    student_id_to_debug = sys.argv[1]
    conv_file = find_file_for_id(student_id_to_debug)
    if not conv_file:
        print(f"Error: Could not find conversation file for student ID '{student_id_to_debug}'.")
        return
    print(f"\n--- PARSING DEBUG FOR STUDENT ID: {student_id_to_debug} ---")
    print(f"--- File: {os.path.basename(conv_file)} ---\n")
    parsed_dialogue = parse_dialogue_debug(conv_file)
    if not parsed_dialogue:
        print("The script did not parse any dialogue rounds.")
    else:
        for round_data in parsed_dialogue:
            print(f"*** ROUND {round_data['round']} ***")
            print("[STUDENT]:")
            print(round_data['student'])
            print("-----------------")
            print("[GPT]:")
            print(round_data['gpt'])
            print("\n=================================\n")

if __name__ == "__main__":
    main() 