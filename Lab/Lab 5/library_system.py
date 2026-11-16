"""Library fine calculation and book renewal system."""
import datetime
import json

LOANS_FILE = "loans.json"
loans = {}


def issue_book(student_id, book_id, days=14, tags=None):
    """Issue a book to a student for a specified loan duration."""
    if tags is None:
        tags = []
    due = datetime.date.today() + datetime.timedelta(days=days)
    if student_id not in loans:
        loans[student_id] = []
    loans[student_id].append({"book_id": book_id, "due": str(due), "tags": tags})
    loan_count = len(loans[student_id])
    print(f"{student_id} borrowed {book_id} (books on loan: {loan_count})")


def return_book(student_id, book_id):
    """Return a borrowed book and remove record if all books are returned."""
    if student_id not in loans:
        return
    loans[student_id] = [b for b in loans[student_id] if b["book_id"] != book_id]
    if not loans[student_id]:
        del loans[student_id]


def days_overdue(due_date_str):
    """Calculate days overdue from an ISO format date string."""
    due = datetime.date.fromisoformat(due_date_str)
    return max(0, (datetime.date.today() - due).days)


def renew_book(student_id, book_id, extra_days=14):
    """Extend the due date of an active loan by a given number of days."""
    if student_id not in loans:
        return False
    for book in loans[student_id]:
        if book["book_id"] == book_id:
            due = datetime.date.fromisoformat(book["due"])
            book["due"] = str(due + datetime.timedelta(days=extra_days))
            return True
    return False


def calculate_fine(days, rate=0.50):
    """Return the fine for overdue days (never negative)."""
    return max(0.0, days * rate)


def save_loans():
    """Persist current loan records to a JSON file."""
    with open(LOANS_FILE, "w", encoding="utf-8") as file:
        json.dump(loans, file)


def load_loans():
    """Load loan records from JSON file into memory."""
    global loans
    try:
        with open(LOANS_FILE, "r", encoding="utf-8") as file:
            loans = json.load(file)
    except FileNotFoundError:
        loans = {}


def fine_from_rule(rate_per_day, days):
    """Safely compute fine without using eval."""
    return float(rate_per_day) * max(0, int(days))


def print_summary():
    """Print a summary of active loans and overdue statuses."""
    for student_id, books in loans.items():
        for book in books:
            overdue = days_overdue(book["due"])
            fine = calculate_fine(overdue)
            print(f"{student_id} has {book['book_id']}: {overdue}d overdue, fine ${fine:.2f}")


if __name__ == "__main__":
    issue_book("S001", "B101", days=7)
    issue_book("S002", "B102", days=0)
    print_summary()
