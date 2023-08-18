import React, { useState } from 'react';
import InteractiveTable from '@site/src/components/utils/InteractiveTable';

interface Dp06Props {
  children?: React.ReactNode;
}

const Dp06 = ({ children }: Dp06Props) => {
  return (
    <InteractiveTable
      validate={(textInput, index) => {
        // positive integers (may have spaces)
        const regex = /^\s*\d+\s*$/
        if (!regex.test(textInput)) {
          return false;
        }

        // positive integer
        const value = parseInt(textInput);
        if (isNaN(value) || value <= 0) {
          return false;
        }

        return true;
      }}
      getValues={(textInputs) => {
        const dim = textInputs.map(v => parseInt(v));
        const values = Array(dim[0]).fill(null).map(_ => Array(dim[1]).fill(0))
        
        for (let i = 0; i < dim[0]; i++) {
          for (let j = 0; j < dim[1]; j++) {
            if (i === 0 && j === 0) {
              values[i][j] = 1;
            } else if (i === 0) {
              values[i][j] = values[i][j - 1];
            } else if (j === 0) {
              values[i][j] = values[i - 1][j];
            } else {
              values[i][j] = values[i - 1][j] + values[i][j - 1];
            }
          }
        }

        return values;
      }}
      initialTextInputs={['3', '7']}
      children={children}
    />
  );
};

export default Dp06;