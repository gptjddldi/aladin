from book import Book
from dataclasses import dataclass, field

@dataclass(unsafe_hash=True)
class Store:
    url: str
    ship_price: int
    name: str
    books: list[Book] = field(default_factory=list)

    def add_book(self, new_book: Book):
        for idx, b in enumerate(self.books):
            if b.title == new_book.title and b.price >= new_book.price:
                self.books[idx] = new_book
                break
            elif b.title == new_book.title and b.price < new_book.price:
                break
        else:
            self.books.append(new_book)