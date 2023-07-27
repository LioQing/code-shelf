import React, { useState } from 'react';
import styles from './styles.module.css';
import Table from '@site/src/components/utils/Table';
import { TextInputState } from '@site/src/components/utils/TextInput';

interface MinCostClimbingStairsProps {
  children?: React.ReactNode;
}

const isTextInput = (child: React.ReactNode) => React.isValidElement(child) && (child as React.ReactElement).props['mdxType'] === 'TextInput';

const MinCostClimbingStairs = ({ children }: MinCostClimbingStairsProps) => {
  const childrenArray = React.Children.toArray(children);

  const [costTextInput, setCostTextInput] = useState('1,5,2,4,3');
  const [inputState, setInputState] = useState(TextInputState.Default);
  const [cost, setCost] = useState([1, 5, 2, 4, 3]);

  const textInput = childrenArray
    .map((child, index) => {
      if (isTextInput(child)) {
        const newProps = {
          key: index,
          value: costTextInput,
          state: inputState,
          className: styles['text-input'],
          onChange: (event: React.ChangeEvent<HTMLInputElement>) => {
            setCostTextInput(event.target.value);

            // comma separated list of integers (may have spaces)
            const regex = /^\s*(\d+\s*,\s*)*\d+\s*$/
            if (regex.test(event.target.value)) {
              setCost(event.target.value.split(',').map(v => parseInt(v.trim())));
              setInputState(TextInputState.Default);
            } else {
              setInputState(TextInputState.Incorrect);
            }
          },
          onBlur: () => {
            setCostTextInput(cost.join(','));
            setInputState(TextInputState.Default);
          },
        };

        const newElement = React.cloneElement(child as React.ReactElement, newProps);

        return newElement;
      }
    })
    .filter(child => child)[0];

  // algorithm
  const values = Array(cost.length + 1).fill(0);
  values[0] = 0;
  values[1] = 0;
  for (let i = 2; i < cost.length + 1; i++) {
    values[i] = Math.min(values[i - 1] + cost[i - 1], values[i - 2] + cost[i - 2]);
  }

  const addStrings = cost.map((v, i) => (v + values[i]).toString()).concat(['']);
  const costStrings = cost.map(c => c.toString()).concat(['']);

  return (
    <>
      <div className={styles["input-prompt"]}>
        {childrenArray.map((child, index) => {
          if (isTextInput(child)) {
            return textInput;
          }
          return <span key={index}>{child}</span>;
        })}
      </div>

      <Table
        values={[costStrings, values, addStrings]}
        rowHeaders={['cost', 'dp', 'cost + dp']}
      />
    </>
  );
};

export default MinCostClimbingStairs;