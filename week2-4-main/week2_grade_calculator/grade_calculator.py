"""
Student Grade Calculator
Week 2 — Making Decisions & Repeating Tasks in Python
"""

def calculate_grade(marks):
    """Return the grade and an encouraging message for marks from 0 to 100."""
    if 90 <= marks <= 100:
        return "A", "Excellent work! Keep shining!"
    elif 80 <= marks < 90:
        return "B", "Very Good! Keep it up!"
    elif 70 <= marks < 80:
        return "C", "Good effort! Keep practicing!"
    elif 60 <= marks < 70:
        return "D", "You're making progress. Keep working!"
    else:
        return "F", "Don't give up. Review, practice, and try again!"


def get_valid_marks():
    """Keep asking until the user enters a whole number between 0 and 100."""
    while True:
        raw_marks = input("Enter marks (0-100): ").strip()
        try:
            marks = int(raw_marks)
        except ValueError:
            print("Invalid input. Please enter a whole number, such as 85.")
            continue

        if 0 <= marks <= 100:
            return marks

        print("Marks must be between 0 and 100. Please try again.")


def main():
    print("=" * 42)
    print("         STUDENT GRADE CALCULATOR")
    print("=" * 42)

    name = input("Enter student name: ").strip()
    while not name:
        print("Name cannot be empty.")
        name = input("Enter student name: ").strip()

    marks = get_valid_marks()
    grade, message = calculate_grade(marks)

    print("\n" + "-" * 42)
    print(f"📊 RESULT FOR {name.upper()}")
    print(f"Marks: {marks}/100")
    print(f"Grade: {grade}")
    print(f"Message: {message}")
    print("-" * 42)


if __name__ == "__main__":
    main()
