class NLLNode:
    def __init__(self, value, children=None):
        self.value = value
        self.children = children or []

def parse_expression_to_nll(expr):
    """
    Recursively parse a sympy expression into a Nested Linked List (NLL) structure.
    """
    from sympy import Basic
    if not isinstance(expr, Basic) or len(expr.args) == 0:
        return NLLNode(expr)
    return NLLNode(expr.func, [parse_expression_to_nll(arg) for arg in expr.args])

def nll_derivative(node, var):
    """
    Recursively compute the derivative of the NLL expression tree.
    """
    from sympy import Symbol, Add, Mul, Pow, sin, cos, diff

    # Leaf node (variable or constant)
    if not node.children:
        if node.value == var:
            return NLLNode(1)
        else:
            return NLLNode(0)

    # Handle basic operations
    if node.value == Add:
        return NLLNode(Add, [nll_derivative(child, var) for child in node.children])
    if node.value == Mul:
        # Product rule: (u*v)' = u'*v + u*v'
        u, v = node.children
        return NLLNode(Add, [
            NLLNode(Mul, [nll_derivative(u, var), v]),
            NLLNode(Mul, [u, nll_derivative(v, var)])
        ])
    if node.value == Pow:
        base, exp = node.children
        # Power rule for x^n
        if exp.children == [] and isinstance(exp.value, (int, float)):
            return NLLNode(Mul, [
                NLLNode(exp.value),
                NLLNode(Pow, [base, NLLNode(exp.value - 1)]),
                nll_derivative(base, var)
            ])
        else:
            # General case: use sympy's diff for complex powers
            from sympy import Pow as SymPyPow
            expr = SymPyPow(base.value, exp.value)
            d = diff(expr, var)
            return parse_expression_to_nll(d)
    if node.value == sin:
        u = node.children[0]
        return NLLNode(Mul, [
            NLLNode(cos, [u]),
            nll_derivative(u, var)
        ])
    if node.value == cos:
        u = node.children[0]
        return NLLNode(Mul, [
            NLLNode(-1),
            NLLNode(sin, [u]),
            nll_derivative(u, var)
        ])
    # Fallback: use sympy's diff for unsupported nodes
    from sympy import Basic
    expr = node_to_sympy(node)
    d = diff(expr, var)
    return parse_expression_to_nll(d)

def node_to_sympy(node):
    """
    Convert an NLLNode back to a sympy expression.
    """
    if not node.children:
        return node.value
    return node.value(*[node_to_sympy(child) for child in node.children])