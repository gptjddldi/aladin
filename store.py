from book import Book
from dataclasses import dataclass, field

@dataclass(unsafe_hash=True)
class Store:
    url: str
    ship_price: int
    name: str
    books: list[Book] = field(default_factory=list)
    total_price: int = 0
    total_origin_price: int = 0

    def add_book(self, new_book: Book):
        for idx, b in enumerate(self.books):
            if b.title == new_book.title and b.price >= new_book.price:
                self.books[idx] = new_book
                break
            elif b.title == new_book.title and b.price < new_book.price:
                break
        else:
            self.books.append(new_book)

    def discount_rate(self):
        return 100 - int((self.total_price + self.ship_price) / self.total_origin_price * 100)

    def __repr__(self) -> str:
        return f"{self.name}({self.url}) \nbooks: {self.books}\n{(self.total_price + self.ship_price):,}원({self.discount_rate()}% off)\n-------------------------------------------"