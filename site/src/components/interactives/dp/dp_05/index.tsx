import React, { useState } from 'react';
import InteractiveTable from '@site/src/components/utils/InteractiveTable';

interface Dp05Props {
  children?: React.ReactNode;
}

const Dp05 = ({ children }: Dp05Props) => {
  return (
    <InteractiveTable
      validate={(textInput, index) => {
        // comma separated list of integers (may have spaces)
        const regex = /^\s*([-+]?\d+\s*,\s*)*[-+]?\d+\s*$/
        if (!regex.test(textInput)) {
          return false;
        }

        return true;
      }}
      getValues={(textInputs) => {
        const costs = textInputs[0].split(',').map(v => parseInt(v.trim()));
        const values = Array(costs.length + 1).fill(0);
        values[0] = 0;
        values[1] = 0;
        for (let i = 2; i < costs.length + 1; i++) {
          values[i] = Math.min(values[i - 1] + costs[i - 1], values[i - 2] + costs[i - 2]);
        }

        const addStrings = costs.map((v, i) => (v + values[i]).toString()).concat(['']);
        const costStrings = costs.map(c => c.toString()).concat(['']);

        return [costStrings, values, addStrings];
      }}
      initialTextInputs={['1,5,2,4,3']}
      getRowHeaders={(textInputs) => ['cost', 'dp', 'cost + dp']}
      children={children}
    />
  );
};

export default Dp05;