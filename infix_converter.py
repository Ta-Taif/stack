"""Convert infix expressions to postfix with the shunting-yard algorithm."""

import re

from stack import Stack

PRECEDENCE = {"+": 1, "-": 1, "*": 2, "/": 2}
TOKEN = re.compile(r"\s*(?:([A-Za-z0-9_.]+)|([-+*/()])|(\S))")


class InfixToPostfixConverter:
    """Converts infix expressions (left-associative + - * /) to postfix."""

    def convert(self, expression):
        """Return the postfix form of an infix expression as a string.

        Operands are letters or numbers. Raises ValueError for an empty or
        incomplete expression, an invalid token, a misplaced operator or
        operand, or mismatched parentheses.
        """
        tokens = self._tokenize(expression)
        if not tokens:
            raise ValueError("empty expression")

        output = []
        operators = Stack()
        expect_operand = True
        previous = None

        for token in tokens:
            if token in PRECEDENCE:
                if expect_operand:
                    raise ValueError(
                        f"misplaced operator '{token}': missing operand before it")
                while (not operators.is_empty()
                       and operators.peek() in PRECEDENCE
                       and self._precedence(operators.peek()) >= self._precedence(token)):
                    output.append(operators.pop())
                operators.push(token)
                expect_operand = True
            elif token == "(":
                if not expect_operand:
                    raise ValueError("misplaced '(': missing operator before it")
                operators.push(token)
            elif token == ")":
                if expect_operand:
                    if previous == "(":
                        raise ValueError("empty parentheses")
                    raise ValueError("misplaced operator: missing operand before ')'")
                while not operators.is_empty() and operators.peek() != "(":
                    output.append(operators.pop())
                if operators.is_empty():
                    raise ValueError("mismatched parentheses: extra ')'")
                operators.pop()
            else:
                if not expect_operand:
                    raise ValueError(f"misplaced operand '{token}': missing operator before it")
                output.append(token)
                expect_operand = False
            previous = token

        if expect_operand:
            raise ValueError("incomplete expression: missing operand at the end")

        while not operators.is_empty():
            top = operators.pop()
            if top == "(":
                raise ValueError("mismatched parentheses: missing ')'")
            output.append(top)
        return " ".join(output)

    @staticmethod
    def _precedence(operator):
        """Return 2 for * and /, 1 for + and -."""
        return PRECEDENCE[operator]

    @staticmethod
    def _tokenize(expression):
        tokens = []
        position = 0
        text = expression.rstrip()
        while position < len(text):
            match = TOKEN.match(text, position)
            if match.group(3):
                raise ValueError(f"invalid token '{match.group(3)}'")
            tokens.append(match.group(1) or match.group(2))
            position = match.end()
        return tokens
