import pandas as pd
import json
import os
import sys

def verify_prompt_counts():
    """
    Verifies that the number of conversation rounds in the generated JSON file
    matches the ground truth count from 'Raw Data.xlsx'.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(script_dir)

    # We now verify the new file created by our build script
    json_path = os.path.join(base_dir, "final_project_data.json")
    excel_path = os.path.join(base_dir, "Raw Data.xlsx")

    if not os.path.exists(json_path):
        print(f"ERROR: The data file 'final_project_data.json' was not found.", file=sys.stderr)
        sys.exit(1)
    if not os.path.exists(excel_path):
        print(f"ERROR: Ground truth file 'Raw Data.xlsx' not found.", file=sys.stderr)
        sys.exit(1)

    print("--- Starting Verification ---")
    print(f"Loading generated data from: {os.path.basename(json_path)}")
    print(f"Loading ground truth from: {os.path.basename(excel_path)}\\n")

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            generated_data = json.load(f)
        
        generated_counts = {
            str(student['student_id']): len(student['dialogue_history'])
            for student in generated_data
        }

        df = pd.read_excel(excel_path, engine='openpyxl')
        id_col_name = next((col for col in df.columns if col.lower() in ['id', 'student id', 'studentid']), None)
        prompt_col_name = "# of prompts"
        df.dropna(subset=[id_col_name, prompt_col_name], inplace=True)
        ground_truth_counts = df.set_index(id_col_name)[prompt_col_name].to_dict()
        ground_truth_counts = {str(int(k)): int(v) for k, v in ground_truth_counts.items()}
        
        mismatched_students = []
        all_students = sorted(list(set(ground_truth_counts.keys()) | set(generated_counts.keys())), key=int)
        
        print(f"{'Student ID':<12} | {'Expected Rounds':<18} | {'Actual Rounds':<16} | {'Status'}")
        print("-" * 68)

        for student_id in all_students:
            expected = ground_truth_counts.get(student_id)
            actual = generated_counts.get(student_id)
            
            # Per your instruction, we ignore cases where the Excel file has no data (N/A)
            if expected is None:
                status = "✅ OK (No ground truth)"
            elif actual is None:
                 status = "❌ MISMATCH"
                 mismatched_students.append(student_id)
            elif expected == actual:
                status = "✅ OK"
            else:
                status = "❌ MISMATCH"
                mismatched_students.append(student_id)

            expected_str = str(expected) if expected is not None else "N/A"
            actual_str = str(actual) if actual is not None else "N/A"
            print(f"{student_id:<12} | {expected_str:<18} | {actual_str:<16} | {status}")

        print("\\n--- Verification Summary ---")
        if not mismatched_students:
            print("✅ Success! All student round counts match the ground truth.")
        else:
            print(f"❌ Failure! Found mismatches for {len(mismatched_students)} students.")
            print("Mismatched IDs:", ", ".join(sorted(mismatched_students, key=int)))
        print("----------------------------\\n")

    except Exception as e:
        print(f"\\nAn unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    verify_prompt_counts() 