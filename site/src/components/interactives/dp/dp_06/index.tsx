import React, { useState } from 'react';
import styles from './styles.module.css';
import Table from '@site/src/components/utils/Table';
import { TextInputState } from '@site/src/components/utils/TextInput';
import { isComponent } from '@site/src/utils';

interface Dp06Props {
  children?: React.ReactNode;
}

const Dp06 = ({ children }: Dp06Props) => {
  const childrenArray = React.Children.toArray(children);

  const [dimTextInput, setDimTextInput] = useState(['3', '7']);
  const [inputState, setInputState] = useState(TextInputState.Default);
  const [dimension, setDimension] = useState([3, 7]);

  var textInputCount = 0;
  const textInput = childrenArray
    .map((child, index) => {
      if (isComponent(child, 'TextInput')) {
        const textInputIndex = textInputCount;
        const newProps = {
          key: index,
          value: dimTextInput[textInputIndex],
          state: inputState,
          onChange: (event: React.ChangeEvent<HTMLInputElement>) => {
            setDimTextInput(dimTextInput.map((x, i) => i === textInputIndex ? event.target.value : x));

            // positive integers (may have spaces)
            const regex = /^\s*\d+\s*$/
            if (!regex.test(event.target.value)) {
              setInputState(TextInputState.Incorrect);
              return;
            }

            // positive integer
            const value = parseInt(event.target.value);
            if (isNaN(value) || value <= 0) {
              setInputState(TextInputState.Incorrect);
              return;
            }

            setDimension(dimension.map((x, i) => i === textInputIndex ? value : x));
            setInputState(TextInputState.Default);
          },
          onBlur: () => {
            setDimTextInput(dimension.map(x => x.toString()));
            setInputState(TextInputState.Default);
          },
        };

        const newElement = React.cloneElement(child as React.ReactElement, newProps);
        textInputCount++;

        return newElement;
      }
    });

    // algorithm
  const values = Array(dimension[0]).fill(null).map(_ => Array(dimension[1]).fill(0))
  
  for (let i = 0; i < dimension[0]; i++) {
    for (let j = 0; j < dimension[1]; j++) {
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

  return (
    <>
      <div className={styles['input-prompt']}>
        {childrenArray.map((child, index) => {
          if (textInput[index]) {
            return textInput[index];
          }
          return <span key={index}>{child}</span>;
        })}
      </div>

      <Table
        values={values}
      />
    </>
  );
};

export default Dp06;