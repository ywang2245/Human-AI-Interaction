import json
import pandas as pd
import os

def convert_json_to_excel():
    """
    Loads the two final JSON result files (evaluations and similarities),
    and saves them as two separate sheets in a single Excel file.
    """
    eval_json_path = "student_evaluation_llm.json"
    sim_json_path = "student_similarity_scores.json"
    output_excel_path = "final_project_results.xlsx"

    # --- Verify input files exist ---
    if not os.path.exists(eval_json_path):
        print(f"Error: Evaluation file not found at '{eval_json_path}'")
        return
    if not os.path.exists(sim_json_path):
        print(f"Error: Similarity file not found at '{sim_json_path}'")
        return

    # --- Process Evaluation Data ---
    with open(eval_json_path, 'r', encoding='utf-8') as f:
        eval_data = json.load(f)

    # Flatten the nested 'evaluation' dictionary into separate columns
    # This makes the Excel sheet much easier to read and analyze
    normalized_eval_data = []
    for student_id, record in eval_data.items():
        flat_record = {
            "student_id": student_id,
            "task_type": record.get("task_type"),
            "eval_score": record.get("evaluation", {}).get("score"),
            "eval_pass": record.get("evaluation", {}).get("pass"),
            "eval_feedback": record.get("evaluation", {}).get("feedback"),
            "eval_error": record.get("evaluation", {}).get("error"),
            "eval_raw": record.get("evaluation", {}).get("raw")
        }
        normalized_eval_data.append(flat_record)
    
    eval_df = pd.DataFrame(normalized_eval_data)

    # --- Process Similarity Data ---
    with open(sim_json_path, 'r', encoding='utf-8') as f:
        sim_data = json.load(f)
    sim_df = pd.DataFrame(sim_data)

    # --- Write to separate CSV files ---
    eval_csv_path = "student_evaluation_llm.csv"
    sim_csv_path = "student_similarity_scores.csv"

    print(f"Writing data to {eval_csv_path} and {sim_csv_path}...")
    eval_df.to_csv(eval_csv_path, index=False, encoding='utf-8')
    sim_df.to_csv(sim_csv_path, index=False, encoding='utf-8')
    
    print("Successfully converted JSON files to CSV.")
    print(f"Evaluation results are in '{eval_csv_path}'.")
    print(f"Similarity scores are in '{sim_csv_path}'.")

if __name__ == "__main__":
    convert_json_to_excel() 