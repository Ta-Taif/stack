"""Stack ADT implemented as an adapter over a Python list."""


class Stack:
    """LIFO collection. The list inside is an implementation detail."""

    def __init__(self):
        self._items = []

    def push(self, item):
        """Add item to the top of the stack."""
        self._items.append(item)

    def pop(self):
        """Remove and return the top item. Raises IndexError if empty."""
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self._items.pop()

    def peek(self):
        """Return the top item without removing it. Raises IndexError if empty."""
        if self.is_empty():
            raise IndexError("peek at empty stack")
        return self._items[-1]

    def is_empty(self):
        """Return True if the stack has no items."""
        return len(self._items) == 0

    def size(self):
        """Return the number of items in the stack."""
        return len(self._items)


if __name__ == "__main__":
    s = Stack()
    assert s.is_empty() and s.size() == 0
    s.push(1)
    assert not s.is_empty() and s.size() == 1
    s.push(2)
    s.push(3)
    assert s.size() == 3
    assert s.peek() == 3 and s.size() == 3
    assert s.pop() == 3
    assert s.pop() == 2
    assert s.pop() == 1
    assert s.is_empty() and s.size() == 0
    for operation in (s.pop, s.peek):
        try:
            operation()
            raise AssertionError("expected IndexError")
        except IndexError as error:
            print(f"{operation.__name__}() on empty stack -> IndexError: {error}")
    print("All Stack tests passed.")
