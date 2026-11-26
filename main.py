
from src.library import Library


def display_menu():
    print("\n========== LIBRARY MANAGEMENT SYSTEM ==========")
    print("1. Add Member")
    print("2. Add Resource")
    print("3. List Members")
    print("4. List Resources")
    print("5. Search Resources")
    print("6. Issue Resource")
    print("7. Return Resource")
    print("8. List Loans")
    print("9. Reconciliation Report")
    print("0. Exit")
    print("============================================")


def add_member_menu(library):
    member_id = input("Member ID: ")
    name = input("Name: ")
    email = input("Email: ")

    try:
        member = library.add_member(member_id, name, email)
        print("\nMember added successfully!")
        print(member)
    except ValueError as error:
        print(f"\nError: {error}")


def add_resource_menu(library):
    resource_id = input("Resource ID: ")
    title = input("Title: ")
    resource_type = input("Type (book/digital): ")

    try:
        resource = library.add_resource(
            resource_id, title, resource_type
        )
        print("\nResource added successfully!")
        print(resource)
    except ValueError as error:
        print(f"\nError: {error}")


def list_members_menu(library):
    members = library.list_members()

    print("\n========== MEMBERS ==========")

    if not members:
        print("No members found.")
        return

    for member in members:
        print(member)


def list_resources_menu(library):
    resources = library.list_resources()

    print("\n========== RESOURCES ==========")

    if not resources:
        print("No resources found.")
        return

    for resource in resources:
        print(resource)


def search_resources_menu(library):
    keyword = input("Enter title or resource ID to search: ")
    results = library.search_resources(keyword)

    print("\n========== SEARCH RESULTS ==========")

    if not results:
        print("No matching resources found.")
        return

    for resource in results:
        print(resource)


def issue_resource_menu(library):
    member_id = input("Enter Member ID: ")
    resource_id = input("Enter Resource ID: ")

    try:
        loan = library.issue_resource(member_id, resource_id)

        print("\nResource issued successfully!")
        print(loan)
        print(f"Due Date: {loan.due_date}")

    except ValueError as error:
        print(f"\nError: {error}")


def return_resource_menu(library):
    loan_id = input("Enter Loan ID: ")

    try:
        result = library.return_resource(loan_id)

        print("\nResource returned successfully!")
        print(f"Loan ID: {result['loan_id']}")
        print(f"Overdue Days: {result['overdue_days']}")
        print(f"Fine: Rs. {result['fine']:.2f}")

    except ValueError as error:
        print(f"\nError: {error}")


def list_loans_menu(library):
    loans = library.list_loans()

    print("\n========== LOANS ==========")

    if not loans:
        print("No loans found.")
        return

    for loan in loans:
        print(loan)

        if loan.is_returned():
            print(f"Fine: Rs. {loan.fine_amount:.2f}")


def reconciliation_menu(library):
    report = library.reconciliation_report()

    print("\n====== DAILY RECONCILIATION REPORT ======")
    print(f"Currently Issued: {report['issued']}")
    print(f"Returned: {report['returned']}")
    print(f"Overdue: {report['overdue']}")
    print(
        f"Outstanding Fines: Rs. "
        f"{report['outstanding_fines']:.2f}"
    )


def main():
    library = Library()

    while True:
        display_menu()
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_member_menu(library)

        elif choice == "2":
            add_resource_menu(library)

        elif choice == "3":
            list_members_menu(library)

        elif choice == "4":
            list_resources_menu(library)

        elif choice == "5":
            search_resources_menu(library)

        elif choice == "6":
            issue_resource_menu(library)

        elif choice == "7":
            return_resource_menu(library)

        elif choice == "8":
            list_loans_menu(library)

        elif choice == "9":
            reconciliation_menu(library)

        elif choice == "0":
            print("Thank you for using Library Management System!")
            break

        else:
            print("Invalid choice. Please enter a number from 0 to 9.")


if __name__ == "__main__":
    main()
