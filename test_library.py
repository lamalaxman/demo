from library import PrintedBook, InMemoryBookRepository, LibraryService, CashPayment

def test_add_and_list_books():
    repo = InMemoryBookRepository()
    service = LibraryService(repo)
    book = PrintedBook("B001", "The Alchemist", "Paulo Coelho", 208)
    service.add_book(book)
    all_books = repo.find_all()
    assert len(all_books) == 1
    assert all_books[0].get_title() == "The Alchemist"

def test_return_book_fee():
    repo = InMemoryBookRepository()
    service = LibraryService(repo)
    book = PrintedBook("B002", "1984", "George Orwell", 328)
    service.add_book(book)
    book.set_borrowed(True)
    fee = service.return_book_and_pay_fine("B002", 4, CashPayment())
    assert fee == 2.0
