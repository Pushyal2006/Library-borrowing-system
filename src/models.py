
from datetime import date


class Member:
    def __init__(self, member_id, name, email):
        self.member_id = member_id
        self.name = name
        self.email = email

    def __str__(self):
        return f"{self.member_id} | {self.name} | {self.email}"


class Resource:
    def __init__(self, resource_id, title):
        self.resource_id = resource_id
        self.title = title
        self.available = True

    def loan_days(self):
        raise NotImplementedError

    def fine_per_day(self):
        raise NotImplementedError

    def __str__(self):
        status = "Available" if self.available else "Issued"
        return f"{self.resource_id} | {self.title} | {status}"


class Book(Resource):
    def loan_days(self):
        return 14

    def fine_per_day(self):
        return 2.0


class DigitalResource(Resource):
    def loan_days(self):
        return 7

    def fine_per_day(self):
        return 1.0


class Loan:
    def __init__(
        self,
        loan_id,
        member,
        resource,
        issue_date,
        due_date,
        return_date=None,
        fine_amount=0.0
    ):
        self.loan_id = loan_id
        self.member = member
        self.resource = resource
        self.issue_date = issue_date
        self.due_date = due_date
        self.return_date = return_date
        self.fine_amount = fine_amount

    def is_returned(self):
        return self.return_date is not None

    def is_overdue(self, today=None):
        if self.is_returned():
            return False

        if today is None:
            today = date.today()

        return today > self.due_date

    def __str__(self):
        status = "Returned" if self.is_returned() else "Active"

        return (
            f"{self.loan_id} | {self.member.name} | "
            f"{self.resource.title} | Due: {self.due_date} | {status}"
        )
