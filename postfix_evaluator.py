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
