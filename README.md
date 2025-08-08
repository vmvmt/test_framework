
# 🧪 Vehicle Test Metrics Engineer Intern Task: Test Runner with Error Classification

## 📝 Task Description

You are provided with a set of test cases defined in the attached JSON file. These test cases simulate different types of testing scenarios (e.g., type checks, unit conversions, null checks). Your task is to build a **robust test execution framework** that can:

1. **Parse and run each test case** based on its `type`.
2. **Catch and classify errors** through tests written by you (e.g., type mismatch, missing data, configuration errors).
3. **Generate a clear report** of passed and failed test cases, including reasons for failure.
4. (Optional Bonus) Suggest a fix or root cause for each error based on heuristics.

## 📂 Provided

- `test_cases_input.json`: A file with 30 test cases in inconsistent structures.

Each test case includes:
- `case_id`: A unique ID
- `type`: One of `unit_conversion`, `type_check`, or `required_field`
- `data`: The input to be tested (can be a primitive or a dict)
- `config`: Optional configuration parameters (may be missing or incomplete)

## ✅ Requirements

You should:

- Design your code for modularity, easy readability
- Write the tests required for checking the test cases
- Catch and categorize errors such as:
  - Type mismatches
  - Missing keys or null values
  - Value constraint violations
- Output a **summary report** showing:
  - Which test cases passed
  - Which failed, and why (categorized)
- Write clean, well-documented code

## ⭐ Bonus

You can earn bonus points by:
- Suggesting possible fixes for errors (e.g., "expected int, got str")
- Logging details like input values and config in the error report
- Using a simple plugin-like architecture for test logic dispatch
- Log your thought process, by providing a my_thoughts.txt file in which you describe your thoughts regarding the task, mention aspects that were boring/interesting/challenging or just simply a first time to do


## 🚀 Submission

- Submit a `.zip` file that includes each and every file that is necessary for evaluating your solution.
- Include your report output (in any form of your preference)
- Include a MY_REDAME.md file in which you describe the required steps for installing and executing your solution.

Make sure:
- Your code runs with standard Python 3
- All dependencies and their versions are noted in a requirements.txt file

## 📧 Questions?

Feel free to contact me for clarification at mark.oravecz@aimotive.com!
