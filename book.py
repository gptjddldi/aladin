from dataclasses import dataclass

@dataclass(unsafe_hash=True)
class Book:
    title: str
    price: int
    url: str = ''
    page_cnt: int = 0

    def __repr__(self) -> str:
        return f"{self.title}({self.price:,}원)"