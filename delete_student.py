import json
import sys

def remove_student_by_id(file_path, student_id_to_remove):
    """
    Reads a JSON file containing a list of student data, removes the
    entry for a specific student ID, and writes the data back to the file.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from '{file_path}'.")
        sys.exit(1)

    # Ensure student_id_to_remove is a string for consistent comparison
    student_id_to_remove = str(student_id_to_remove)

    original_count = len(data)
    # Rebuild the list, excluding the student to be removed
    updated_data = [student for student in data if str(student.get('student_id')) != student_id_to_remove]
    new_count = len(updated_data)

    if new_count == original_count:
        print(f"Warning: Student ID '{student_id_to_remove}' not found in the file. No changes made.")
    else:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(updated_data, f, indent=4)
            print(f"Successfully removed Student ID '{student_id_to_remove}' and saved the updated data to '{file_path}'.")
        except Exception as e:
            print(f"Error writing the updated data back to '{file_path}': {e}")
            sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python delete_student.py <student_id_to_remove>")
        sys.exit(1)
    
    # The JSON file is in the parent directory
    json_file_path = '../final_project_data.json'
    student_id = sys.argv[1]
    
    remove_student_by_id(json_file_path, student_id) 