import json
from sentence_transformers import SentenceTransformer, util
import os

def calculate_similarity(model, text1, text2):
    """Calculates the cosine similarity between two texts."""
    # If either text is empty, similarity is not meaningful.
    if not text1 or not text2:
        return 0.0
    
    embedding1 = model.encode(text1, convert_to_tensor=True)
    embedding2 = model.encode(text2, convert_to_tensor=True)
    
    cosine_scores = util.cos_sim(embedding1, embedding2)
    return cosine_scores.item()

def extract_texts(dialogue_history: list) -> (str, str):
    """
    Extracts and separates all student text and all GPT text from the clean dialogue.
    """
    student_texts = []
    gpt_texts = []

    for turn in dialogue_history:
        if turn.get("student"):
            student_texts.append(turn["student"])
        if turn.get("gpt"):
            gpt_texts.append(turn["gpt"])

    return " ".join(student_texts), " ".join(gpt_texts)


def main():
    """
    Main function to load data, process it, and save similarity scores.
    """
    print("Loading sentence transformer model...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    print("Model loaded.")

    # Point to the correct, final data file in the parent directory
    input_json_path = "../final_project_data.json"
    if not os.path.exists(input_json_path):
        print(f"Error: Input file not found at {input_json_path}")
        return

    with open(input_json_path, 'r', encoding='utf-8') as f:
        student_data = json.load(f)

    similarity_results = []

    print(f"Processing {len(student_data)} students...")
    for student in student_data:
        task_type = student.get("task_type")
        student_id = student.get("student_id")
        dialogue_history = student.get("dialogue_history", [])
        
        # Extract all student text and all GPT text from the dialogue
        student_text, gpt_text = extract_texts(dialogue_history)
        
        # Only calculate similarity if both parties have contributed text
        if student_text and gpt_text:
            score = calculate_similarity(model, student_text, gpt_text)
        else:
            score = 0.0
        
        similarity_results.append({
            "student_id": student_id,
            "task_type": task_type,
            "similarity_score": round(score, 4)
        })
        
        print(f"  - Calculated similarity for student {student_id} (Task {task_type}): {score:.4f}")

    output_json_path = "student_similarity_scores.json"
    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(similarity_results, f, indent=2, ensure_ascii=False)

    print(f"\nSimilarity analysis complete. Results saved to {output_json_path}")

if __name__ == "__main__":
    main() 