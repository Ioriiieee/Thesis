// SolverConfig.jsx
import React from 'react';

const SolverConfig = ({ algorithms, setAlgorithms }) => {
  const handleAlgorithmChange = (e) => {
    setAlgorithms({
      ...algorithms,
      [e.target.name]: e.target.checked,
    });
  };

  return (
    <div className="card p-6 bg-light shadow-lg rounded-lg mt-6 text-dark">
      <h3 className="text-primary mb-4 font-bold text-lg">Solver Configuration</h3>
      <div className="form-group mb-4">
        <label className="font-semibold">Derivative Type:</label>
        <div className="radio-group flex flex-col">
          <label>
            <input type="radio" name="derivative-type" value="ordinary" checked />
            Ordinary (d/dx)
          </label>
          <label>
            <input type="radio" name="derivative-type" value="partial" />
            Partial (∂/∂x)
          </label>
          <label>
            <input type="radio" name="derivative-type" value="higher" />
            Higher Order
          </label>
        </div>
      </div>
      <div className="form-group mb-4">
        <label className="font-semibold">Variables: </label>
        <div className="checkbox-group flex flex-col">
          <label>
            <input type="checkbox" name="variable" value="x" checked />
            x
          </label>
          <label>
            <input type="checkbox" name="variable" value="y" />
            y
          </label>
          <label>
            <input type="checkbox" name="variable" value="z" />
            z
          </label>
        </div>
      </div>
      <div className="mb-4">
        <h3 className="font-semibold mb-2">Select Algorithm(s):</h3>
        <label className="block">
          <input
            type="checkbox"
            name="AST"
            checked={algorithms.AST}
            onChange={handleAlgorithmChange}
          />{' '}
          AST
        </label>
        <label className="block">
          <input
            type="checkbox"
            name="NLL"
            checked={algorithms.NLL}
            onChange={handleAlgorithmChange}
          />{' '}
          NLL (Nested Linked List)
        </label>
        <label className="block">
          <input
            type="checkbox"
            name="DAG"
            checked={algorithms.DAG}
            onChange={handleAlgorithmChange}
          />{' '}
          DAG
        </label>
      </div>
    </div>
  );
};

export default SolverConfig;
