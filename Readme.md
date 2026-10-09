Lightweight Shift Scheduling API

A lightweight Flask REST API for managing employee shift assignments, validating business logic rules, and retrieving eligible staff.

1. Run the program

python app.py

2. Run the test

python -m unittest test_app.py

Tradeoffs and Key decisions:

- Using FLASK to make the REST API's

- Skipped E2E tests

- Used data.json for data instead of databases or more recommended solutions

- Used easy, built-in modules

Scope & Future Enhancements

- cut E2E tests
- Made the base, then slowly upgraded methods (mostly of storing data)

What i'd do next time

- I think i handled this really well, i started simple and worked my way up.
- Understanding the assignment from a different perspective, not just as code

Issue: two planners assign the same employee to two overlapping shifts at the same moment. What happens in your implementation?

-both requests see the employee as available, return 200 OK, and double-book the employee.

Solution

-Make Users have synced data so not every user sees their own data.json

Use of AI
I used gemini for the introduction of API's, correction of syntax and also a lot of explaining of small functions
