# Human-AI Collaboration Research: Data Processing and Analysis

This project provides a complete workflow for processing, evaluating, and analyzing a dataset from a human-AI collaboration study. The scripts automate the cleaning of raw dialogue data, the evaluation of student submissions using a large language model (LLM), the calculation of semantic similarity between student and AI text, and the final conversion of results into an Excel format for analysis.

## Project Workflow

The project is designed to be run sequentially, with each script producing an output file that serves as the input for the next step.

1.  **Data Extraction (`process_data.py`)**:
    *   **Input**: Raw `.docx` conversation and answer files from the `Conversations - Cleaned` and `Answers - Cleaned` directories.
    *   **Process**: Cleans and parses the raw conversation files, correctly handling multi-line dialogue turns. It extracts the student ID, task type, final submission, and a structured dialogue history.
    *   **Output**: `gpt_student_conversations_and_results.json`

2.  **LLM-Based Evaluation (`evaluate_results_llm.py`)**:
    *   **Input**: `gpt_student_conversations_and_results.json`
    *   **Process**: For each student, it constructs a detailed prompt containing the task requirements, the student's final submission, and their complete dialogue history. It then calls the OpenAI API (`gpt-4o`) to get a structured evaluation.
    *   **Output**: `student_evaluation_llm.json`

3.  **Similarity Analysis (`calculate_similarity.py`)**:
    *   **Input**: `gpt_student_conversations_and_results.json`
    *   **Process**: Uses the `sentence-transformers` library (`all-MiniLM-L6-v2` model) to calculate the cosine similarity between the student's entire conversational input and the AI's entire conversational output for Tasks B and C.
    *   **Output**: `student_similarity_scores.json`

4.  **Excel Conversion (`convert_to_excel.py`)**:
    *   **Input**: `student_evaluation_llm.json` and `student_similarity_scores.json`.
    *   **Process**: Reads the two final JSON result files and converts them into a single, user-friendly Excel file with two separate sheets.
    *   **Output**: `final_project_results.xlsx`

## Setup and Installation

1.  **Clone the Repository**:
    ```bash
    git clone <your-repo-url>
    cd <your-repo-directory>/src
    ```

2.  **Install Dependencies**:
    Make sure you have Python 3.8+ installed. Then, install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set Up API Key**:
    This project requires an OpenAI API key.
    *   Create a file named `openai_key.txt` in the `src` directory.
    *   Paste **only your OpenAI API key** into this file and save it. The script `evaluate_results_llm.py` will read the key directly from this file.

## How to Run

Execute the scripts in the following order from the `src` directory:

```bash
# 1. Process the raw data
python process_data.py

# 2. Run the LLM evaluation
python evaluate_results_llm.py

# 3. Calculate the similarity scores
python calculate_similarity.py

# 4. Convert the final JSON results to Excel
python convert_to_excel.py
```

## LLM Evaluation Criteria

The `evaluate_results_llm.py` script uses a detailed system prompt to guide the `gpt-4-1106-preview` model, ensuring that all student submissions are evaluated against the same objective standard.

### Core Evaluation Framework

The model is given the following core instructions for every evaluation:

1.  **Role**: Act as an expert evaluator.
2.  **Output Format**: Respond **only** in a structured JSON format with two keys: `"score"` and `"feedback"`.
3.  **Score (`score`)**: An integer from 0 to 100.
4.  **Feedback (`feedback`)**: A detailed string explaining the score, citing examples from the student's work and dialogue history. The feedback must analyze *how* the student used the AI.

### Task-Specific Evaluation Guidelines

In addition to the core framework, the model is provided with the specific requirements for each task.

*   **Task A (Number Sequence)**:
    *   **Objective**: Correctly identify the next number in the series: `2, 6, 12, 20, 30, ____?`
    *   **Correct Answer**: 42.
    *   **Evaluation Focus**: The model primarily checks for the correct numerical answer. However, the feedback and score also consider whether the student correctly identified the underlying pattern (the difference between consecutive numbers increases by 2).

*   **Task B (Project Proposal)**:
    *   **Objective**: Write a business proposal for a "smart art frame" project, addressing budget and resource constraints.
    *   **Evaluation Dimensions**: The proposal is judged on its completeness, feasibility, and detail. A high-quality submission must include specific, actionable ideas for:
        1.  Obtaining additional funding.
        2.  Reducing the project scope and/or prioritizing features.
        3.  Securing alternative resources or suppliers.

*   **Task C (Language Learning Plan)**:
    *   **Objective**: Create a personalized plan to learn a new language of the student's choice.
    *   **Evaluation Dimensions**: This task is assessed on the quality, realism, and comprehensiveness of the learning plan. It is **not** judged on the specific language chosen. A good plan should include:
        1.  Specific, achievable daily or weekly goals.
        2.  A variety of learning methods (e.g., apps, conversation practice, media consumption).
        3.  A clear progression from basic to more advanced concepts.

This detailed, two-layer approach ensures that evaluations are both consistent in format and specifically tailored to the requirements of each task.

## Considerations

- **Automated Evaluation**: Provides consistent and scalable evaluation, reducing manual grading workload.
- **Feedback Generation**: Offers detailed feedback based on task requirements.
- **Scoring**: Ensures objective and fair assessment.
- **Security**: Uses environment variables for secure API access.

## Running the Script

1. Ensure the `.env` file is correctly configured with your API key.
2. Run the evaluation script:
   ```bash
   python evaluate_results_llm.py
   ```

## Troubleshooting

- Ensure all dependencies are installed and the `.env` file is correctly configured.
- Check for any errors in the console output and address them as needed.

## License

This project is licensed under the MIT License.

## LLM Model Used

- The evaluation process utilizes the `llama3.3:latest` model by default. You can override this by setting the environment variable `UNIVERSITY_LLM_MODEL` (e.g., `UNIVERSITY_LLM_MODEL=llama3.2:latest`). This model is accessed via the university's LLM API and is pre-trained to handle various language processing tasks. The `:latest` tag ensures that the most recent version of the specified model is used during evaluations. 