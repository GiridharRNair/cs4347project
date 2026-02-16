import itertools
import re

def convert_expression(expr):
    expr = expr.replace(" ", "")

    # Replace NOT (C' → (not C))
    expr = re.sub(r"([A-Z])'", r"(not \1)", expr)

    # Replace OR
    expr = expr.replace("+", " or ")

    # Replace implicit AND between ALL adjacent capitals
    expr = re.sub(r"(?<=[A-Z])(?=[A-Z])", " and ", expr)

    # Insert AND where needed (between operands)
    expr = re.sub(r"(?<=[A-Z\)])(?=[A-Z\(])", " and ", expr)

    return expr

def generate_truth_table(equations, base_vars, final_expression=None):
    """
    equations: dict of name -> algebraic expression
    base_vars: list defining variable order (e.g. ["C","A","G","E"])
    final_expression: optional extra expression
    """

    print("Base variables:", base_vars)
    print()

    combinations = list(itertools.product([0,1], repeat=len(base_vars)))

    headers = base_vars + list(equations.keys())
    if final_expression:
        headers.append("FINAL")

    print(" | ".join(headers))
    print("-" * (len(headers) * 6))

    for combo in combinations:
        values = dict(zip(base_vars, combo))

        # Evaluate intermediate equations
        for name, expr in equations.items():
            py_expr = convert_expression(expr)
            values[name] = int(eval(py_expr, {}, values))

        # Evaluate final expression if given
        if final_expression:
            py_final = convert_expression(final_expression)
            values["FINAL"] = int(eval(py_final, {}, values))

        row = [str(values[h]) for h in headers]
        print(" | ".join(row))

# -----------------------------------
# Example using YOUR equations
# -----------------------------------

equations = {
    "Q": "C'",
    "W": "A'",
    "R": "G'",
    "Y": "E'",
    "U": "Q + A + E",
    "O": "W + G + Y",
    "P": "C + W + R",
    "S": "C + A + E",
    "D": "UOPS"
}

base_variables = ["C", "A", "G", "E"]

generate_truth_table(equations, base_variables, final_expression="AG'E' + A'E + CAG + CAE' + CGE")

