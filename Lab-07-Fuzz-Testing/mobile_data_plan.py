
import math


def parse_plan(text):
    try:
        if not isinstance(text, str):
            return ("", 0.0)

        parts = text.split(":")
        if len(parts) != 2:
            return ("", 0.0)

        plan, gb = parts
        plan = plan.strip()
        gb = float(gb.strip())

        if not plan or not math.isfinite(gb) or gb < 0:
            return ("", 0.0)

        return plan.title(), gb

    except (ValueError, TypeError, AttributeError, OverflowError):
        return ("", 0.0)


def usage_average(usage_csv):
    try:
        if not isinstance(usage_csv, str) or not usage_csv.strip():
            return 0

        values = [int(x.strip()) for x in usage_csv.split(",")]

        if not values or any(x < 0 for x in values):
            return 0

        return sum(values) // len(values)

    except (ValueError, TypeError, AttributeError, OverflowError):
        return 0


def payable_bill(text):
    try:
        if not isinstance(text, str):
            return 0.0

        parts = text.split("|")
        if len(parts) != 2:
            return 0.0

        bill, discount = map(float, parts)

        if not math.isfinite(bill) or not math.isfinite(discount):
            return 0.0

        if bill < 0 or discount < 0:
            return 0.0

        return max(bill * 1.18 - discount, 0.0)

    except (ValueError, TypeError, AttributeError, OverflowError):
        return 0.0


def main():
    print("==== Running parse_plan ====")
    user_input = input("Enter plan:data in GB (e.g. standard:5): ")
    print("Plan and Data:", parse_plan(user_input))

    print("\n==== Running usage_average ====")
    user_input = input("Enter daily usage in MB as CSV (e.g. 300,450,800): ")
    print("Average Usage:", usage_average(user_input))

    print("\n==== Running payable_bill ====")
    user_input = input("Enter bill|discount (e.g. 399|50): ")
    print("Payable Bill:", payable_bill(user_input))


if __name__ == "__main__":
    main()
