import json

def diagnose_first_student_data(file_path):
    """
    Reads the first student's data from the JSON file and prints its structure,
    focusing on the dialogue history.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            # Load the entire file since it contains a list of objects
            data = json.load(f)
            
            if not data:
                print("File is empty or not a valid JSON list.")
                return

            # Get the first student's record
            first_student = data[0]
            
            print("--- DIAGNOSING FIRST STUDENT RECORD ---")
            print(f"Student ID: {first_student.get('student_id')}")
            print("\\n--- Keys available for this student ---")
            print(list(first_student.keys()))
            
            dialogue_history = first_student.get('dialogue_history')
            
            print("\\n--- Dialogue History ---")
            if dialogue_history:
                print(f"Number of turns: {len(dialogue_history)}")
                # Print the first turn to see its keys
                if len(dialogue_history) > 0:
                    print("\\n--- Keys in the first turn of dialogue history ---")
                    print(list(dialogue_history[0].keys()))
                    print("\\n--- Full first turn data ---")
                    print(json.dumps(dialogue_history[0], indent=2))
                else:
                    print("Dialogue history is an empty list.")
            else:
                print("'dialogue_history' key not found or is null.")

            print("\\n--- DIAGNOSIS COMPLETE ---")

    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Point to the final data file in the parent directory
    diagnose_first_student_data('../final_project_data.json') 