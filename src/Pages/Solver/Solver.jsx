// Solver.jsx
import React, { useState } from 'react';
import { MathJaxContext, MathJax } from "better-react-mathjax";
import Navbar from '../../Components/Navbar';
import Bottomcontent from '../../Components/Bottomcontent';
import InputField from './InputField';
import SolverConfig from './SolverConfig';
import SolutionDisplay from './SolutionDisplay';
import StepByStep from './StepByStep';

const Solver = () => {
  const [input, setInput] = useState('');
  const [derivative, setDerivative] = useState('');
  const [algorithms, setAlgorithms] = useState({
    AST: false,
    NLL: false,
    DAG: false,
  });

  const handleInputChange = (e) => {
    setInput(e.target.value);

  };

  const insertSymbol = (symbol) => {
    const inputField = document.getElementById('equation-input');
    const start = inputField.selectionStart;
    const end = inputField.selectionEnd;
    const newValue = input.substring(0, start) + symbol + input.substring(end);
    setInput(newValue);
    inputField.focus();
    inputField.setSelectionRange(start + symbol.length, start + symbol.length);
  };

  const formatForMathJax = (text) => {
    return text
      .replace(/\\sqrt\(([^)]+)\)/g, "\\sqrt{$1}")
      .replace(/\\sqrt([a-zA-Z0-9]+)/g, "\\sqrt{$1}")
      .replace(/([^\s]+)\/([^\s]+)/g, "\\frac{$1}{$2}")
      .replace(/(\w+)\^(\d+)/g, "$1^{$2}");
  };

  const solveExpression = async () => {
    if (!input.trim()) {
      alert("Please enter a function to solve.");
      return;
    }

    const parsedInput = input.replace(/√/g, "sqrt");

    try {
      const solveResponse = await fetch("http://127.0.0.1:8000/solve", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ 
          expression: parsedInput,
          algorithms: Object.keys(algorithms).filter(key => algorithms[key])
        }),
      });

      if (!solveResponse.ok) throw new Error("Failed to fetch derivative");
      const solveData = await solveResponse.json();
      setDerivative(solveData.derivative);
    } catch (error) {
      console.error("Error:", error);
      alert("Error processing the expression. Please check your input.");
    }
  };

  return (
    <MathJaxContext>
      <div className="bg-bgcolor min-h-screen w-full flex flex-col">
        <Navbar />
        <h1 className="font-bold text-2xl text-dark text-center mt-10 mb-4">Derivative Solver</h1>
        
        <div className="flex flex-col md:flex-row gap-8 p-6 w-2/3 justify-center mx-auto">
          <div className="w-full md:w-1/3">
            <InputField 
              input={input}
              handleInputChange={handleInputChange}
              setInput={setInput}
              solveExpression={solveExpression}
              insertSymbol={insertSymbol}
              formatForMathJax={formatForMathJax}
            />
            <SolverConfig algorithms={algorithms} setAlgorithms={setAlgorithms} />
          </div>

          <div className="w-full md:w-2/3">
            <SolutionDisplay 
              derivative={derivative}
              formatForMathJax={formatForMathJax}
            />
            <StepByStep />
          </div>
        </div>

        <Bottomcontent />
      </div>
    </MathJaxContext>
  );
};

export default Solver;
