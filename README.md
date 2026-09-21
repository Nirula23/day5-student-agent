# Student Information LangChain Agent

A LangChain agent powered by Gemini that answers student-related questions using SQLite and four tools.

## Tools

1. `get_student_info(student_id)`
2. `get_student_marks(student_id)`
3. `calculator(expression)`
4. `get_passing_rules()`

The Gemini agent decides which tools to use based on the user's question.

## Project Structure

```text
student-agent/
├── setup_database.py
├── student_agent.py
├── requirements.txt
├── README.md
└── students.db
```

## Setup

### 1. Install dependencies

```powershell
pip install -r requirements.txt
```

### 2. Create the database

```powershell
python setup_database.py
```

### 3. Set the Gemini API key

PowerShell:

```powershell
$env:GOOGLE_API_KEY="YOUR_GEMINI_API_KEY"
```

### 4. Run the agent

```powershell
python student_agent.py
```

## Test Questions

```text
What is the name and department of student 22CS045?
```

```text
What are the marks of 22CS047?
```

```text
What is the total and average mark of 22CS045?
```

```text
Is 22CS045 eligible to pass according to the university rules?
```

Challenge:

```text
I am 22CS045. Tell me my name, department, total marks, average marks, and whether I satisfy the university passing requirements.
```

## Passing Rules

- Minimum overall average: 40%
- Minimum mark in each subject: 35%

## Learning Objective

The important part of this assignment is that the tools are not manually called in a fixed sequence. The Gemini agent decides which tool or tools are needed based on the user's question.
