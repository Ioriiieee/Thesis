from sympy import Add, Mul, Pow, sin, cos, tan, exp, log, diff

class NLLNode:
    def __init__(self, value, children=None):
        self.value = value
        self.children = children or []

def parse_expression_to_nll(expr):
    """
    Recursively parse a sympy expression into a Nested Linked List (NLL) structure.
    """
    if not hasattr(expr, 'args') or not expr.args:
        return NLLNode(expr)
    return NLLNode(expr.func, [parse_expression_to_nll(arg) for arg in expr.args])

def nll_derivative(node, var):
    """
    Recursively compute the derivative of the NLL expression tree.
    """
    # Leaf node (variable or constant)
    if not node.children:
        if node.value == var:
            return NLLNode(1)
        else:
            return NLLNode(0)

    # Addition: (u + v)' = u' + v'
    if node.value == Add:
        return NLLNode(Add, [nll_derivative(child, var) for child in node.children])

    # Multiplication: (u * v)' = u'*v + u*v'
    if node.value == Mul:
        terms = []
        n = len(node.children)
        for i in range(n):
            d_terms = []
            for j, child in enumerate(node.children):
                d_terms.append(nll_derivative(child, var) if i == j else child)
            terms.append(NLLNode(Mul, d_terms))
        return NLLNode(Add, terms)

    # Power: (u^v)' = v*u^(v-1)*u' if v is constant, else use general rule
    if node.value == Pow:
        base, exp = node.children
        if not exp.children:  # exp is constant
            return NLLNode(Mul, [
                exp,
                NLLNode(Pow, [base, NLLNode(exp.value - 1)]),
                nll_derivative(base, var)
            ])
        else:
            # General case: d/dx u^v = u^v * (v'*log(u) + v*u'/u)
            return NLLNode(Mul, [
                NLLNode(Pow, [base, exp]),
                NLLNode(Add, [
                    NLLNode(Mul, [nll_derivative(exp, var), NLLNode(log, [base])]),
                    NLLNode(Mul, [exp, nll_derivative(base, var), NLLNode(Pow, [base, NLLNode(-1)])])
                ])
            ])

    # Trigonometric and exponential/logarithmic functions
    if node.value == sin:
        u = node.children[0]
        return NLLNode(Mul, [NLLNode(cos, [u]), nll_derivative(u, var)])
    if node.value == cos:
        u = node.children[0]
        return NLLNode(Mul, [NLLNode(-1), NLLNode(sin, [u]), nll_derivative(u, var)])
    if node.value == tan:
        u = node.children[0]
        return NLLNode(Mul, [NLLNode(Pow, [NLLNode(sec, [u]), NLLNode(2)]), nll_derivative(u, var)])
    if node.value == exp:
        u = node.children[0]
        return NLLNode(Mul, [NLLNode(exp, [u]), nll_derivative(u, var)])
    if node.value == log:
        u = node.children[0]
        return NLLNode(Mul, [NLLNode(Pow, [u, NLLNode(-1)]), nll_derivative(u, var)])

    # Fallback: use SymPy's diff for unsupported nodes
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