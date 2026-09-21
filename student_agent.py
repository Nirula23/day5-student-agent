import os
import sqlite3

from langchain.tools import tool
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI


DB_NAME = "students.db"


if "GOOGLE_API_KEY" not in os.environ:
    raise ValueError(
        "GOOGLE_API_KEY is not set. "
        "Set it in your terminal before running the program."
    )


@tool
def get_student_info(student_id: str) -> str:
    """
    Get the student's name and department using their student ID.
    Use this tool when the user asks for a student's name,
    department, or basic student information.
    """
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT name, department
        FROM students
        WHERE student_id = ?
    """, (student_id,))

    result = cursor.fetchone()
    connection.close()

    if result is None:
        return f"No student found with ID {student_id}."

    name, department = result

    return (
        f"Student ID: {student_id}\n"
        f"Name: {name}\n"
        f"Department: {department}"
    )


@tool
def get_student_marks(student_id: str) -> str:
    """
    Get the student's marks in Python, Database, AI, and Web
    using their student ID. Use this tool whenever marks are
    required for calculations or academic evaluation.
    """
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT python, database_mark, ai, web
        FROM students
        WHERE student_id = ?
    """, (student_id,))

    result = cursor.fetchone()
    connection.close()

    if result is None:
        return f"No student found with ID {student_id}."

    python_mark, database_mark, ai_mark, web_mark = result

    return (
        f"Student ID: {student_id}\n"
        f"Python: {python_mark}\n"
        f"Database: {database_mark}\n"
        f"AI: {ai_mark}\n"
        f"Web: {web_mark}"
    )


@tool
def calculator(expression: str) -> str:
    """
    Calculate a mathematical expression.
    Use this tool to calculate total marks and average marks.
    """
    try:
        allowed_characters = "0123456789+-*/(). "

        if not all(
            character in allowed_characters
            for character in expression
        ):
            return "Invalid mathematical expression."

        result = eval(expression, {"__builtins__": {}}, {})
        return f"Result: {result}"

    except Exception as error:
        return f"Calculation error: {error}"


@tool
def get_passing_rules() -> str:
    """
    Get the university passing rules.
    The student must have a minimum overall average of 40%
    and a minimum mark of 35% in every subject.
    """
    return (
        "University Passing Rules:\n"
        "1. Minimum overall average: 40%\n"
        "2. Minimum mark in each subject: 35%"
    )


llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)

tools = [
    get_student_info,
    get_student_marks,
    calculator,
    get_passing_rules,
]

agent = create_agent(
    model=llm,
    tools=tools,
)


def ask_agent(question: str):
    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": question,
                }
            ]
        }
    )

    return result["messages"][-1].content


if __name__ == "__main__":
    print("=" * 70)
    print("STUDENT INFORMATION AGENT")
    print("=" * 70)

    print("\nExample questions:")
    print("1. What is the name and department of student 22CS045?")
    print("2. What are the marks of 22CS047?")
    print("3. What is the total and average mark of 22CS045?")
    print("4. Is 22CS045 eligible to pass according to the university rules?")
    print("5. I am 22CS045. Tell me my complete academic information.")
    print("\nType 'exit' to quit.")

    while True:
        question = input("\nYou: ")

        if question.lower() == "exit":
            print("Goodbye!")
            break

        try:
            answer = ask_agent(question)
            print("\nAgent:")
            print(answer)

        except Exception as error:
            print(f"\nError: {error}")
