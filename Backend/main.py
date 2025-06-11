import logging
import re
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sympy import symbols, diff, sympify, latex, sin, cos, tan, exp, log
from pydantic import BaseModel
from generator import generate_equation  # Import the generator if needed
from steps import get_derivative_steps  # Import from steps.py
from database import Rule, get_db, database
from nll import parse_expression_to_nll, nll_derivative, node_to_sympy

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ExpressionInput(BaseModel):
    expression: str

class GenerateInput(BaseModel):
    rules: list[str]

SYMPY_LOCALS = {
    'sin': sin,
    'cos': cos,
    'tan': tan,
    'exp': exp,
    'log': log
}

def preprocess_expression(expr: str) -> str:
    """Converts user input into a SymPy-compatible string."""
    try:
        expr = sympify(expr, locals=SYMPY_LOCALS)
        return expr
    except Exception as e:
        raise ValueError(f"Invalid expression: {str(e)}")


@app.post("/generate")
async def generate_problem(input: GenerateInput):
    try:
        equation, derivative_latex = generate_equation(input.rules)
        return {"equation": equation, "derivative": derivative_latex}
    except Exception as e:
        logger.error(f"Error generating equation: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Error generating equation: {str(e)}")

@app.post("/solve")
async def solve_expression(data: dict):
    expression = data.get("expression")
    algorithms = data.get("algorithms", [])
    var = symbols("x")

    try:
        if "NLL" in algorithms:
            print("NLL algorithm is being used!")  # <-- Add this line
            expr = sympify(expression, locals=SYMPY_LOCALS)
            nll_tree = parse_expression_to_nll(expr)
            nll_deriv_tree = nll_derivative(nll_tree, var)
            expr = sympify(expression, locals=SYMPY_LOCALS)
            result = node_to_sympy(nll_deriv_tree)
            return {"derivative": latex(result), "algorithm": "NLL"}

        # Default: use SymPy's diff
        print("Sympy ")
        expr = sympify(expression, locals=SYMPY_LOCALS)
        derivative = diff(expr, var)
        derivative_latex = latex(derivative)
        return {"derivative": derivative_latex, "algorithm": "SymPy"}
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Invalid expression: {str(e)}")
    # ...existing logic for AST, DAG, etc...

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
