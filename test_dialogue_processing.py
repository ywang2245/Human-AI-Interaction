import json

def process_dialogue(dialogue_history):
    """Process dialogue history and return formatted conversation."""
    dialogue_text = ""
    i = 0
    while i < len(dialogue_history):
        turn = dialogue_history[i]
        
        # When we see "You said:", the student's input is in the current turn's gpt_response
        if turn["student_prompt"] == "You said:":
            dialogue_text += f"Student: {turn['gpt_response'].strip()}\n"
            
        # When we see "ChatGPT said:", look for the next non-marker turn
        elif turn["student_prompt"] == "ChatGPT said:":
            # Find the next turn that contains the actual GPT response
            j = i + 1
            while j < len(dialogue_history):
                next_turn = dialogue_history[j]
                if next_turn["student_prompt"] not in ["You said:", "ChatGPT said:"]:
                    dialogue_text += f"GPT: {next_turn['student_prompt'].strip()}"
                    if next_turn["gpt_response"] and next_turn["gpt_response"] not in ["You said:", "ChatGPT said:"]:
                        dialogue_text += f" {next_turn['gpt_response'].strip()}"
                    dialogue_text += "\n"
                    break
                j += 1
            i = j  # Skip the processed turns
            
        i += 1
    
    return dialogue_text

def main():
    # Load student data
    with open("gpt_student_conversations_and_results.json", encoding="utf-8") as f:
        students = json.load(f)
    
    # Process first 5 students as examples
    for student in students[:5]:
        print(f"\n{'='*50}")
        print(f"Student ID: {student['student_id']}")
        print(f"Task Type: {student['task_type']}")
        print(f"{'='*50}")
        
        dialogue_text = process_dialogue(student["dialogue_history"])
        print("\nProcessed Dialogue:")
        print(dialogue_text)
        
        print("\nFinal Submission:")
        print(student.get("final_submission", "No final submission"))
        print(f"{'='*50}\n")

if __name__ == "__main__":
    main() 