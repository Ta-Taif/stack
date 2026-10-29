"""Evaluate postfix (RPN) expressions with numeric operands."""

import re

from stack import Stack

NUMBER = re.compile(r"\d+(\.\d+)?$")
OPERATORS = "+-*/"


class PostfixEvaluator:
    """Evaluates a postfix expression using a Stack of operands."""

    def evaluate(self, expression):
        """Return the numeric value of a space-separated postfix expression.

        Raises ValueError for an empty expression, an invalid token,
        too few operands, or too many operands. Raises ZeroDivisionError
        when dividing by zero.
        """
        tokens = expression.split()
        if not tokens:
            raise ValueError("empty expression")

        operands = Stack()
        for token in tokens:
            if NUMBER.match(token):
                operands.push(self._to_number(token))
            elif token in OPERATORS:
                if operands.size() < 2:
                    raise ValueError(
                        f"insufficient operands for operator '{token}'")
                right = operands.pop()
                left = operands.pop()
                operands.push(self._apply(token, left, right))
            else:
                raise ValueError(f"invalid token '{token}'")

        if operands.size() != 1:
            raise ValueError("too many operands: expression is malformed")
        return operands.pop()

    @staticmethod
    def _to_number(token):
        return float(token) if "." in token else int(token)

    @staticmethod
    def _apply(operator, left, right):
        """Compute left <operator> right."""
        if operator == "+":
            return left + right
        if operator == "-":
            return left - right
        if operator == "*":
            return left * right
        if right == 0:
            raise ZeroDivisionError("division by zero")
        return left / right


if __name__ == "__main__":
    evaluator = PostfixEvaluator()

    valid = [
        ("5 3 +", 8), ("8 2 - 3 +", 9), ("5 3 8 * +", 29), ("6 2 / 3 +", 6.0),
        ("5 8 + 3 -", 10), ("5 3 + 8 *", 64), ("8 2 3 * + 6 -", 8),
        ("5 3 8 * + 2 /", 14.5), ("8 2 + 3 6 * -", -8), ("5 3 + 8 2 / -", 4.0),
        ("35 27 + 3 * ", 186), ("23 30 15 * /", 23 / (30 * 15)),
        ("8 2 -", 6), ("8 2 /", 4.0), ("12", 12),
    ]
    for expression, expected in valid:
        actual = evaluator.evaluate(expression)
        assert actual == expected, (expression, actual, expected)
        print(f"[{expression}] = {actual}")

    invalid = [
        ("26 28 + 32 2 ; - 5 /", ValueError, "invalid token"),
        ("2 3 4 +", ValueError, "too many operands"),
        ("20 29 9 * ;", ValueError, "invalid token"),
        ("25 23 - +", ValueError, "insufficient operands"),
        ("8 0 /", ZeroDivisionError, "division by zero"),
        ("5 +", ValueError, "insufficient operands"),
        ("3 + 4", ValueError, "insufficient operands"),
        ("", ValueError, "empty expression"),
    ]
    for expression, error_type, text in invalid:
        try:
            evaluator.evaluate(expression)
            raise AssertionError(f"[{expression}] should have failed")
        except error_type as error:
            assert text in str(error), (expression, str(error))
            print(f"[{expression}] -> {error_type.__name__}: {error}")
    print("All PostfixEvaluator tests passed.")
