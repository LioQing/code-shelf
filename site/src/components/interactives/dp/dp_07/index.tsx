import React, { useEffect, useState } from 'react';
import InteractiveTable from '@site/src/components/utils/InteractiveTable';

interface Dp07Props {
  children?: React.ReactNode;
}

const getValues = (textInputs: string[]) => {
  const values = Array(textInputs[0].length + 1).fill(null).map(_ => Array(textInputs[1].length + 1).fill(0))
  
  for (let i = 0; i <= textInputs[0].length; i++) {
    for (let j = 0; j <= textInputs[1].length; j++) {
      if (i === 0 && j === 0)
        values[i][j] = 0;
      else if (i === 0)
        values[i][j] = j;
      else if (j === 0)
        values[i][j] = i;
      else if (textInputs[0][i - 1] === textInputs[1][j - 1])
        values[i][j] = values[i - 1][j - 1];
      else
        values[i][j] = 1 + Math.min(values[i - 1][j - 1], values[i - 1][j], values[i][j - 1]);
    }
  }

  return values;
};

const getPath = (textInputs: string[], values: number[][]): [string[], React.ReactElement[][]] => {
  let i = textInputs[0].length;
  let j = textInputs[1].length;
  const operations = [];
  const path = JSON.parse(JSON.stringify(values));
  while (i > 0 || j > 0) {
    path[i][j] = <>{values[i][j]}</>;
    if (i === 0) {
      path[i][j] = <u>{values[i][j]}</u>;
      operations.push(`Insert ${textInputs[1][j - 1]}`);
      j--;
    } else if (j === 0) {
      path[i][j] = <u>{values[i][j]}</u>;
      operations.push(`Delete ${textInputs[0][i - 1]}`);
      i--;
    } else if (textInputs[0][i - 1] === textInputs[1][j - 1]) {
      path[i][j] = <u>{values[i][j]}</u>;
      i--;
      j--;
    } else if (values[i][j] === values[i - 1][j] + 1) {
      path[i][j] = <i><u>{values[i][j]}</u></i>;
      operations.push(`Delete ${textInputs[0][i - 1]}`);
      i--;
    } else if (values[i][j] === values[i][j - 1] + 1) {
      path[i][j] = <i><u>{values[i][j]}</u></i>;
      operations.push(`Insert ${textInputs[1][j - 1]}`);
      j--;
    } else if (values[i][j] === values[i - 1][j - 1] + 1) {
      path[i][j] = <i><u>{values[i][j]}</u></i>;
      operations.push(`Replace ${textInputs[0][i - 1]} with ${textInputs[1][j - 1]}`);
      i--;
      j--;
    }
  }

  path[0][0] = <u>{values[0][0]}</u>;
  
  operations.reverse();

  if (operations.length === 0) {
    operations.push('No operations needed');
  }

  return [operations, path];
};

const Dp07 = ({ children }: Dp07Props) => {
  const updateValues = (textInputs: string[]) => {
    setValues(getValues(textInputs));
    setOperations(getPath(textInputs, getValues(textInputs))[0]);
  };

  const initialTextInputs = ['sunny', 'snowy'];
  const [values, setValues] = useState<number[][]>(getValues(initialTextInputs));
  const [operations, setOperations] = useState<string[]>(
    getPath(initialTextInputs, getValues(initialTextInputs))[0]
  );

  return (
    <>
      <InteractiveTable
        validate={(textInput, index) => {
          // english letters and digits
          const regex = /^\s*[a-zA-Z0-9]*\s*$/
          if (!regex.test(textInput)) {
            return false;
          }

          return true;
        }}
        onChange={updateValues}
        getValues={(textInputs) => getPath(textInputs, values)[1]}
        initialTextInputs={initialTextInputs}
        getColumnHeaders={(textInputs) => ['', ...textInputs[1].split('')]}
        getRowHeaders={(textInputs) => ['', ...textInputs[0].split('')]}
        children={children}
      />
      <div>
        <p>
          The underlined values are the path of the operations below,
          and italic values are where operations are applied.
        </p>
        <p>Operations:</p>
        <ul>
          {operations.map((v, i) => <li key={i}>{v}</li>)}
        </ul>
      </div>
    </>
  );
};

export default Dp07;