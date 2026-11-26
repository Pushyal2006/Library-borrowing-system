
from datetime import date, timedelta

from src.models import Member, Book, DigitalResource, Loan
from src.storage import load_data, save_data


class Library:
    def __init__(self):
        self.data = load_data()

    def _find_member(self, member_id):
        for member in self.data["members"]:
            if member["member_id"] == member_id:
                return member
        return None

    def _find_resource(self, resource_id):
        for resource in self.data["resources"]:
            if resource["resource_id"] == resource_id:
                return resource
        return None

    def _find_loan(self, loan_id):
        for loan in self.data["loans"]:
            if loan["loan_id"] == loan_id:
                return loan
        return None

    def add_member(self, member_id, name, email):
        member_id = member_id.strip()
        name = name.strip()
        email = email.strip()

        if not member_id or not name or not email:
            raise ValueError("All member fields are required.")

        if self._find_member(member_id):
            raise ValueError("Member ID already exists.")

        member = Member(member_id, name, email)

        self.data["members"].append({
            "member_id": member.member_id,
            "name": member.name,
            "email": member.email
        })

        save_data(self.data)
        return member

    def add_resource(self, resource_id, title, resource_type):
        resource_id = resource_id.strip()
        title = title.strip()
        resource_type = resource_type.strip().lower()

        if not resource_id or not title:
            raise ValueError("Resource ID and title are required.")

        if self._find_resource(resource_id):
            raise ValueError("Resource ID already exists.")

        if resource_type == "book":
            resource = Book(resource_id, title)
        elif resource_type == "digital":
            resource = DigitalResource(resource_id, title)
        else:
            raise ValueError("Type must be book or digital.")

        self.data["resources"].append({
            "resource_id": resource.resource_id,
            "title": resource.title,
            "type": resource_type,
            "available": True
        })

        save_data(self.data)
        return resource

    def list_members(self):
        return [
            Member(m["member_id"], m["name"], m["email"])
            for m in self.data["members"]
        ]

    def list_resources(self):
        resources = []

        for record in self.data["resources"]:
            if record["type"] == "book":
                resource = Book(
                    record["resource_id"],
                    record["title"]
                )
            else:
                resource = DigitalResource(
                    record["resource_id"],
                    record["title"]
                )

            resource.available = record["available"]
            resources.append(resource)

        return resources

    def search_resources(self, keyword):
        keyword = keyword.strip().lower()

        return [
            resource
            for resource in self.list_resources()
            if keyword in resource.title.lower()
            or keyword in resource.resource_id.lower()
        ]

    def _create_member_object(self, member_id):
        record = self._find_member(member_id)

        if record is None:
            raise ValueError("Member ID not found.")

        return Member(
            record["member_id"],
            record["name"],
            record["email"]
        )

    def _create_resource_object(self, resource_id):
        record = self._find_resource(resource_id)

        if record is None:
            raise ValueError("Resource ID not found.")

        if record["type"] == "book":
            resource = Book(
                record["resource_id"],
                record["title"]
            )
        else:
            resource = DigitalResource(
                record["resource_id"],
                record["title"]
            )

        resource.available = record["available"]
        return resource

    def issue_resource(self, member_id, resource_id, today=None):
        member_record = self._find_member(member_id)
        resource_record = self._find_resource(resource_id)

        if member_record is None:
            raise ValueError("Member ID not found.")

        if resource_record is None:
            raise ValueError("Resource ID not found.")

        if not resource_record["available"]:
            raise ValueError("Resource is already issued.")

        if today is None:
            today = date.today()

        member = self._create_member_object(member_id)
        resource = self._create_resource_object(resource_id)

        due_date = today + timedelta(days=resource.loan_days())

        # Generate a unique loan ID
        loan_numbers = []

        for record in self.data["loans"]:
            loan_id = record["loan_id"]

            if loan_id.startswith("L") and loan_id[1:].isdigit():
                loan_numbers.append(int(loan_id[1:]))

        next_number = max(loan_numbers, default=0) + 1
        loan_id = f"L{next_number:03d}"

        loan = Loan(
            loan_id,
            member,
            resource,
            today,
            due_date
        )

        self.data["loans"].append({
            "loan_id": loan.loan_id,
            "member_id": member_id,
            "resource_id": resource_id,
            "issue_date": today.isoformat(),
            "due_date": due_date.isoformat(),
            "return_date": None,
            "fine_amount": 0.0
        })

        resource_record["available"] = False

        save_data(self.data)
        return loan

    def return_resource(self, loan_id, today=None):
        loan_record = self._find_loan(loan_id)

        if loan_record is None:
            raise ValueError("Loan ID not found.")

        if loan_record["return_date"] is not None:
            raise ValueError("This loan has already been returned.")

        if today is None:
            today = date.today()

        due_date = date.fromisoformat(loan_record["due_date"])
        overdue_days = max(0, (today - due_date).days)

        resource = self._create_resource_object(
            loan_record["resource_id"]
        )

        fine = overdue_days * resource.fine_per_day()

        loan_record["return_date"] = today.isoformat()
        loan_record["fine_amount"] = round(fine, 2)

        resource_record = self._find_resource(
            loan_record["resource_id"]
        )
        resource_record["available"] = True

        save_data(self.data)

        return {
            "loan_id": loan_id,
            "overdue_days": overdue_days,
            "fine": round(fine, 2)
        }

    def list_loans(self):
        loans = []

        for record in self.data["loans"]:
            member = self._create_member_object(record["member_id"])
            resource = self._create_resource_object(record["resource_id"])

            return_date = (
                date.fromisoformat(record["return_date"])
                if record["return_date"] is not None
                else None
            )

            loan = Loan(
                record["loan_id"],
                member,
                resource,
                date.fromisoformat(record["issue_date"]),
                date.fromisoformat(record["due_date"]),
                return_date,
                record["fine_amount"]
            )

            loans.append(loan)

        return loans

    def reconciliation_report(self, today=None):
        if today is None:
            today = date.today()

        issued_count = 0
        returned_count = 0
        overdue_count = 0
        outstanding_fines = 0.0

        for record in self.data["loans"]:
            due_date = date.fromisoformat(record["due_date"])

            if record["return_date"] is None:
                issued_count += 1

                if today > due_date:
                    overdue_count += 1

                    resource = self._create_resource_object(
                        record["resource_id"]
                    )

                    overdue_days = (today - due_date).days

                    outstanding_fines += (
                        overdue_days * resource.fine_per_day()
                    )

            else:
                returned_count += 1
                outstanding_fines += record["fine_amount"]

        return {
            "issued": issued_count,
            "returned": returned_count,
            "overdue": overdue_count,
            "outstanding_fines": round(outstanding_fines, 2)
        }
