import React from 'react';
import styles from './styles.module.css';
import InteractiveTable from '@site/src/components/utils/InteractiveTable';

interface Dp05Props {
  children?: React.ReactNode;
}

const Dp05 = ({ children }: Dp05Props) => {
  return (
    <>
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
          const path = Array(costs.length + 1).fill(false);
          values[0] = 0;
          values[1] = 0;
          for (let i = 2; i < costs.length + 1; i++) {
            if (values[i - 1] + costs[i - 1] < values[i - 2] + costs[i - 2]) {
              values[i] = values[i - 1] + costs[i - 1];
              path[i - 1] = true;
            } else {
              values[i] = values[i - 2] + costs[i - 2];
              path[i - 2] = true;
            }
          }
          path[costs.length] = true;

          const addStrings = costs.map((v, i) => (v + values[i]).toString()).concat(['']);
          const costStrings = costs.map(c => c.toString()).concat(['']);

          const pathValues = values.map((v, i) => path[i] ? <b className={styles.path}>{v}</b> : v);
          const pathAdd = addStrings.map((v, i) => path[i] ? <b className={styles.path}>{v}</b> : v);

          return [costStrings, pathValues, pathAdd];
        }}
        initialTextInputs={['1,5,2,4,3']}
        getRowHeaders={(textInputs) => ['cost', 'dp', 'cost + dp']}
        children={children}
      />
      <div>
        <p>
          Green bold values forms the path of the minimum cost to reach that step.
        </p>
      </div>
    </>
  );
};

export default Dp05;