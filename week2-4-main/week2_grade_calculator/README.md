# Student Grade Calculator

**Week 2 — Making Decisions & Repeating Tasks in Python**

## Project overview
This command-line application asks for a student's name and marks, validates the marks, calculates a grade, and displays an encouraging message.

## Grading logic
- **A:** 90–100
- **B:** 80–89
- **C:** 70–79
- **D:** 60–69
- **F:** 0–59

The `calculate_grade(marks)` function uses `if` / `elif` / `else` statements to return a grade and message.

## Features
- Uses functions to keep the program organised.
- Uses a `while` loop to repeat prompts for invalid input.
- Handles non-numeric input with `try` / `except`.
- Rejects marks below 0 or above 100.
- Rejects a blank student name.

## Requirements
- Python 3.8 or newer
- No third-party packages required

## Setup and run
1. Install Python from https://www.python.org/downloads/ if needed.
2. Download or clone this repository.
3. Open a terminal in the project folder.
4. Run `python grade_calculator.py` (or `python3 grade_calculator.py`).

## Code structure
```text
week2-grade-calculator/
├── README.md
├── grade_calculator.py
├── test_cases.txt
└── screenshots/
    └── screenshot.png
```

## Functions and technical details
- `calculate_grade(marks)`: accepts a validated integer and returns a `(grade, message)` tuple.
- `get_valid_marks()`: loops until the user enters a whole number from 0 through 100.
- `main()`: coordinates input, calculation, and output.
- `if __name__ == "__main__":`: runs `main()` when executed directly.

The program uses simple conditional ranges; no external libraries are needed.

## Testing
Use the cases in `test_cases.txt`. Confirm valid marks receive the expected grade, and invalid input is rejected until valid marks are entered.

## What I learned
I practiced comparison operators, `if` / `elif` / `else`, `while` loops, functions, returning multiple values as a tuple, and error handling with `try` / `except`.

## Screenshot
The screenshot in `screenshots/` is illustrative. Run the program and capture your own terminal output before final submission.
