import openai
import json
import os
import sys
import time
from typing import Dict, List, Any

def get_openai_api_key():
    """Reads the OpenAI API key from openai_key.txt."""
    try:
        with open("openai_key.txt", "r") as f:
            key = f.read().strip()
            if not key:
                print("Error: openai_key.txt is empty.")
                sys.exit(1)
            return key
    except FileNotFoundError:
        print("Error: openai_key.txt not found. Please create this file and paste your API key in it.")
        sys.exit(1)

api_key = get_openai_api_key()
client = openai.OpenAI(api_key=api_key)

def get_completion(prompt: List[Dict[str, str]], model: str = "gpt-4-1106-preview") -> str:
    """Sends a prompt to the OpenAI API and gets a completion."""
    try:
        response = client.chat.completions.create(
            model=model,
            messages=prompt,
            temperature=0.1,
            response_format={"type": "json_object"}
        )
        return response.choices[0].message.content
    except openai.RateLimitError:
        print("Rate limit exceeded. Waiting 60 seconds...")
        time.sleep(60)
        return get_completion(prompt, model)
    except Exception as e:
        print(f"API call error: {e}")
        return json.dumps({"error": f"API Call Failed: {str(e)}"})

def load_requirements() -> Dict[str, str]:
    """Loads task requirements from .docx files."""
    requirements = {}
    from docx import Document
    for task in ["A", "B", "C"]:
        try:
            doc_path = f"Task {task}.docx"
            if not os.path.exists(doc_path):
                 doc_path = f"../Task {task}.docx"
                 if not os.path.exists(doc_path): raise FileNotFoundError
            doc = Document(doc_path)
            requirements[f"TASK_{task}"] = "\\n".join([p.text for p in doc.paragraphs if p.text.strip()])
        except Exception:
            print(f"Warning: Could not load requirements for Task {task}.")
            requirements[f"TASK_{task}"] = ""
    return requirements

def build_prompt(task_name: str, requirement_text: str, student_submission: str, dialogue_history: List[Dict[str, Any]]) -> List[Dict[str, str]]:
    """Builds the detailed prompt for the LLM evaluation."""
    system_message = """
You are an expert evaluator assessing a student's submission based on a set of requirements. Your goal is to provide a structured, objective evaluation in JSON format. The evaluation should contain two main keys: "score" and "feedback".
- "score": An integer from 0 to 100, where 0 is a complete failure and 100 is a perfect submission meeting all requirements.
- "feedback": A detailed string explaining the score. It should cite specific examples from the student's submission and the conversation history to justify the rating. Explain what the student did well and what they missed or could have done better.

Analyze the provided conversation history to understand the context of the student's submission. Did the student effectively use the AI's help? Did they iterate and improve? Mention this in your feedback.
"""
    formatted_dialogue = "\\n".join([f"Round {turn.get('round', 'N/A')}: Student: {turn.get('student', '')}\\nAI: {turn.get('gpt', '')}" for turn in dialogue_history])
    if not formatted_dialogue:
        formatted_dialogue = "No conversation history provided."

    user_message = f"""
Please evaluate the following student submission.

### Task Name
{task_name}

### Task Requirements
{requirement_text}

### Student's Final Submission
{student_submission if student_submission else "The student did not provide a final answer for this task."}

### Full Conversation History
{formatted_dialogue}
---
Based on all the above information, please provide your evaluation in a valid JSON object with the keys "score" and "feedback".
"""
    return [{"role": "system", "content": system_message}, {"role": "user", "content": user_message}]

def main():
    """Main function to orchestrate the LLM evaluation process."""
    json_file = '../final_project_data.json'
    output_file = 'student_evaluation_llm.json'

    if not os.path.exists(json_file):
        raise FileNotFoundError(f"Data file '{json_file}' not found.")

    requirements = load_requirements()
    with open(json_file, encoding="utf-8") as f:
        students = json.load(f)

    all_eval_results = {}
    for student in students:
        student_id = student.get("student_id")
        task_type = student.get("task_type")
        submission = student.get("final_submission")
        dialogue_history = student.get("dialogue_history", [])

        if not all([student_id, task_type, submission]):
            continue

        print(f"--- Evaluating Student ID: {student_id} (Task {task_type}) ---")
        requirement_key = f"TASK_{task_type}"
        requirement_text = requirements.get(requirement_key)

        if not requirement_text:
            all_eval_results[student_id] = {"error": f"Requirements for {requirement_key} not found."}
            continue
        
        prompt_messages = build_prompt(f"Task {task_type}", requirement_text, submission, dialogue_history)
        result_json_str = get_completion(prompt_messages)

        try:
            evaluation = json.loads(result_json_str)
        except json.JSONDecodeError:
            evaluation = {"error": "Invalid JSON from LLM", "raw": result_json_str}
        
        all_eval_results[student_id] = {"task_type": task_type, "evaluation": evaluation}
        print(f"--- Finished Student ID: {student_id}. Waiting 1 second. ---")
        time.sleep(1)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_eval_results, f, indent=4, ensure_ascii=False)
    print(f"\\nEvaluation complete. Results saved to '{output_file}'.")

if __name__ == "__main__":
    main() 