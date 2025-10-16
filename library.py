from abc import ABC, abstractmethod

class Book(ABC):
    def __init__(self, book_id, title, author):
        self.id = book_id
        self.title = title
        self.author = author
        self.borrowed = False

    def get_id(self): return self.id
    def get_title(self): return self.title
    def get_author(self): return self.author
    def is_borrowed(self): return self.borrowed
    def set_borrowed(self, val): self.borrowed = val

    @abstractmethod
    def calculate_late_fee(self, days_late): pass


class EBook(Book):
    def __init__(self, book_id, title, author, download_url):
        super().__init__(book_id, title, author)
        self.download_url = download_url
    def calculate_late_fee(self, days_late): return max(0, days_late) * 0.10


class PrintedBook(Book):
    def __init__(self, book_id, title, author, num_pages):
        super().__init__(book_id, title, author)
        self.num_pages = num_pages
    def calculate_late_fee(self, days_late): return max(0, days_late) * 0.50


class Payment(ABC):
    @abstractmethod
    def pay(self, amount): pass


class CardPayment(Payment):
    def __init__(self, card_number): self.card_number = card_number
    def pay(self, amount):
        print(f"Processing card payment of ${amount:.2f} for card ****-****-****-{self.card_number[-4:]}")
        return True


class CashPayment(Payment):
    def pay(self, amount):
        print(f"Processing cash payment of ${amount:.2f}")
        return True


class BookRepository(ABC):
    @abstractmethod
    def save(self, book): pass
    @abstractmethod
    def find_by_id(self, book_id): pass
    @abstractmethod
    def find_all(self): pass


class InMemoryBookRepository(BookRepository):
    def __init__(self): self.storage = {}
    def save(self, book): self.storage[book.get_id()] = book
    def find_by_id(self, book_id): return self.storage.get(book_id)
    def find_all(self): return list(self.storage.values())


class LibraryService:
    def __init__(self, repo): self.repo = repo

    def add_book(self, book): self.repo.save(book)

    def borrow_book(self, book_id):
        b = self.repo.find_by_id(book_id)
        if b is None: return None
        if b.is_borrowed(): raise Exception("Book already borrowed!")
        b.set_borrowed(True); return b

    def return_book_and_pay_fine(self, book_id, days_late, payment):
        b = self.repo.find_by_id(book_id)
        if b is None: raise Exception("Book not found!")
        fee = b.calculate_late_fee(days_late)
        success = payment.pay(fee)
        if success: b.set_borrowed(False)
        return fee if success else -1

    def list_books(self):
        print("\n--- Library Books ---")
        for b in self.repo.find_all():
            print(f"ID: {b.get_id()} | Title: {b.get_title()} | Author: {b.get_author()} | Borrowed: {'Yes' if b.is_borrowed() else 'No'}")
        print("----------------------")


def main():
    repo = InMemoryBookRepository()
    service = LibraryService(repo)
    while True:
        print("\nLIBRARY MANAGEMENT SYSTEM")
        print("1. Add Printed Book")
        print("2. Add EBook")
        print("3. List All Books")
        print("4. Borrow Book")
        print("5. Return Book")
        print("6. Exit")
        try: choice = int(input("Enter your choice: "))
        except ValueError:
            print("Invalid input! Please enter a number."); continue

        if choice == 1:
            book_id = input("Enter Book ID: "); title = input("Enter Title: "); author = input("Enter Author: ")
            pages = int(input("Enter Number of Pages: "))
            service.add_book(PrintedBook(book_id, title, author, pages))
            print("Printed Book added successfully!")
        elif choice == 2:
            book_id = input("Enter Book ID: "); title = input("Enter Title: "); author = input("Enter Author: ")
            url = input("Enter Download URL: ")
            service.add_book(EBook(book_id, title, author, url))
            print("EBook added successfully!")
        elif choice == 3: service.list_books()
        elif choice == 4:
            book_id = input("Enter Book ID to borrow: ")
            try:
                book = service.borrow_book(book_id)
                print(f"You borrowed: {book.get_title()}" if book else "Book not found!")
            except Exception as e: print(f"Error: {e}")
        elif choice == 5:
            book_id = input("Enter Book ID to return: ")
            days_late = int(input("Enter days late: "))
            pay_choice = input("Payment method (1 = Cash, 2 = Card): ")
            payment = CardPayment(input("Enter Card Number: ")) if pay_choice == "2" else CashPayment()
            try:
                fee = service.return_book_and_pay_fine(book_id, days_late, payment)
                print(f"Book returned. Late fee paid: ${fee:.2f}")
            except Exception as e: print(f"Error: {e}")
        elif choice == 6:
            print("Exiting... Goodbye!"); break
        else: print("Invalid choice, try again!")


if __name__ == "__main__": main()
