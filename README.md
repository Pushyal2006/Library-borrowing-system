
# Case Study 05: Library Borrowing, Membership and Fine Reconciliation

## Objective
Develop a Python-based library management application to manage members,
resources, borrowing, returns, overdue fines and reconciliation reports.

## Features
- Register library members
- Add books and digital resources
- Search library resources
- Issue resources to members
- Return resources
- Calculate overdue fines
- Display members, resources and loans
- Generate reconciliation reports
- Store records in JSON
- Validate inputs and handle invalid operations
- Automated unit tests

## OOP Concepts
- Classes and objects
- Inheritance
- Composition
- Polymorphism
- Encapsulation
- __str__ methods

## Fine Rules
Book:
- Loan period: 14 days
- Fine: Rs. 2 per overdue day

Digital Resource:
- Loan period: 7 days
- Fine: Rs. 1 per overdue day

These rules are defined for this educational project.

## Technologies
- Python 3
- JSON
- unittest
- datetime

No external packages required.

## Run the Application
Open the project folder in VS Code and run:

python main.py

## Run Automated Tests
python -m unittest -v

## Data Storage
Records are stored in:

data/library_data.json

## Limitations
- Command-line application
- JSON file storage
- No authentication or access control
- No online fine payment
- Not designed for simultaneous users
- Sample fine rules only
