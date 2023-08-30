import React, { useState } from 'react';
import styles from './styles.module.css';
import InteractiveTable from '@site/src/components/utils/InteractiveTable';

interface Dp08Props {
  children?: React.ReactNode;
}

interface Item {
  weight: number;
  value: number;
}

const parseTextInputs = (textInputs: string[]): [number, Item[]] => {
  const [maxWeight, items] = textInputs;

  if (items.trim() === '') {
    return [parseInt(maxWeight), []];
  }

  return [
    parseInt(maxWeight),
    items.replace(/\s/g, "").slice(1, -1).split('),(').map(item => {
      const [weight, value] = item.split(',');
      return {
        weight: parseInt(weight),
        value: Math.round(parseFloat(value) * 1_000) / 1_000,
      } as Item;
    }),
  ];
};

const getValues = (capacity: number, items: Item[]): number[][] => {
  const values = Array(items.length + 1).fill(null).map(_ => Array(capacity + 1).fill(0));

  for (let i = 1; i <= items.length; i++) {
    for (let w = 1; w <= capacity; w++) {
      if (items[i - 1].weight <= w)
        values[i][w] = Math.max(items[i - 1].value + values[i - 1][w - items[i - 1].weight], values[i - 1][w]);
      else
        values[i][w] = values[i - 1][w];
    }
  }

  return values.map(row => row.map(v => Math.round(v * 1_000) / 1_000));
}

const getPath = (
  capacity: number,
  items: Item[],
  values: number[][],
): [React.ReactElement[], React.ReactElement[][]] => {
  const path = JSON.parse(JSON.stringify(values));
  const choices = items.map((item, index) => <>{`(${item.weight}, ${item.value})`}</>);
  let w = capacity;
  for (let i = items.length; i > 0; i--) {
    path[i][w] = <>{values[i][w]}</>;
    path[i][w] = <b className={styles.path}>{path[i][w]}</b>;
    path[i][w] = <span className={styles.path}>{path[i][w]}</span>;
    if (values[i][w] !== values[i - 1][w]) {
      path[i][w] = <u className={styles.path}>{path[i][w]}</u>;
      w -= items[i - 1].weight;
      choices[i - 1] = <b className={styles.path}>{choices[i - 1]}</b>;
    }
  }

  path[0][0] = <>{values[0][0]}</>;
  path[0][0] = <b className={styles.path}>{path[0][0]}</b>;
  path[0][0] = <span className={styles.path}>{path[0][0]}</span>;

  return [[<></>, ...choices], path];
};

const validate = (textInput: string, index: number): boolean => {
  if (index === 0) {
    // integer
    const regex = /^\s*\d+\s*$/;
    return regex.test(textInput);
  } else if (index === 1) {
    // comma separated list of (integers, floats) (may have spaces)
    const regex = /^\s*(\(\s*\d+\s*,\s*[-+]?\d+(\.\d+)?\s*\)?\s*(,\s*\(\s*\d+\s*,\s*[-+]?\d+(\.\d+)?\s*\)\s*)*)?$/;
    return regex.test(textInput);
  } else {
    return false;
  }
};

const Dp08 = ({ children }: Dp08Props) => {
  const updateValues = (textInputs: string[]) => {
    setValues(getValues(...parseTextInputs(textInputs)));
  };

  const initialTextInputs = ['5', '(2, 20), (1, 10), (4, 30), (3, 15)'];
  const [values, setValues] = useState<number[][]>(getValues(...parseTextInputs(initialTextInputs)));

  return (
    <>
      <InteractiveTable
        validate={validate}
        onChange={updateValues}
        getValues={(textInputs) => getPath(...parseTextInputs(textInputs), values)[1]}
        initialTextInputs={initialTextInputs}
        getColumnHeaders={(textInputs) => Array(parseTextInputs(textInputs)[0] + 1).fill(null).map((_, index) => index)}
        getRowHeaders={(textInputs) => getPath(...parseTextInputs(textInputs), values)[0]}
        children={children}
      />
      <div>
        <p>
          Green bold values form a combination of items to maximize the value of the knapsack,
          and underlined values are where the items were taken.
        </p>
      </div>
    </>
  );
};

export default Dp08;