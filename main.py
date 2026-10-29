"""Demonstration of the Stack, PostfixEvaluator and InfixToPostfixConverter."""

from infix_converter import InfixToPostfixConverter
from postfix_evaluator import PostfixEvaluator


def show_evaluations(evaluator, expressions):
    for expression in expressions:
        try:
            print(f"[{expression}] = {evaluator.evaluate(expression)}")
        except (ValueError, ZeroDivisionError) as error:
            print(f"[{expression}] -> ERROR: {error}")


def show_conversions(converter, expressions):
    for expression in expressions:
        try:
            print(f"[{expression}] -> [{converter.convert(expression)}]")
        except ValueError as error:
            print(f"[{expression}] -> ERROR: {error}")


def main():
    evaluator = PostfixEvaluator()
    converter = InfixToPostfixConverter()

    print("----- Postfix Evaluator -----")
    show_evaluations(evaluator, [
        "5 3 +", "8 2 - 3 +", "5 3 8 * + 2 /", "35 27 + 3 *", "8 2 + 3 6 * -"])

    print("\n----- Postfix Evaluator: errors -----")
    show_evaluations(evaluator, ["5 +", "2 3 4 +", "8 0 /", "3 4 &", "3 + 4"])

    print("\n----- Infix to Postfix Converter -----")
    show_conversions(converter, [
        "A + B", "A + B * C", "( A + B ) * C", "A * ( B + C ) / D",
        "( A + B * ( C - D ) ) / E", "A - B + C"])

    print("\n----- Infix to Postfix Converter: errors -----")
    show_conversions(converter, [
        "A + * B", "( A + B", "A + B )", "A + B ; C", "A B + C", "A +", ""])

    print("\n----- Integrated: infix -> postfix -> value -----")
    for infix in ["( 5 + 3 ) * 2", "10 - 4 - 3", "20 / ( 2 + 3 )", "8 / ( 4 - 4 )"]:
        try:
            postfix = converter.convert(infix)
            print(f"[{infix}] -> [{postfix}] = {evaluator.evaluate(postfix)}")
        except (ValueError, ZeroDivisionError) as error:
            print(f"[{infix}] -> ERROR: {error}")


if __name__ == "__main__":
    main()
