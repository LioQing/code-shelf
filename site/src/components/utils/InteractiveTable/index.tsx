import React, { useState } from 'react';
import styles from './styles.module.css';
import Table from '@site/src/components/utils/Table';
import { TextInputState } from '@site/src/components/utils/TextInput';
import { isComponent } from '@site/src/utils';

interface InteractiveTableProps {
  validate: (textInput: string, index: number) => boolean;
  getValues: (textInputs: string[]) => React.ReactNode[][];
  initialTextInputs: string[];
  onChange?: (textInputs: string[], changed: number) => void;
  getColumnHeaders?: (textInputs: string[]) => React.ReactNode[];
  getRowHeaders?: (textInputs: string[]) => React.ReactNode[];
  children?: React.ReactNode;
}

const InteractiveTable = ({
  validate, getValues, initialTextInputs, onChange,
  getColumnHeaders, getRowHeaders, children,
}: InteractiveTableProps) => {
  const childrenArray = React.Children.toArray(children);

  const [textInput, setTextInput] = useState(initialTextInputs);
  const [lastValidText, setLastValidText] = useState(initialTextInputs);
  const [inputState, setInputState] = useState(TextInputState.Default);

  var textInputCount = 0;
  const textInputChildren = childrenArray
    .map((child, index) => {
      if (isComponent(child, 'TextInput')) {
        const textInputIndex = textInputCount;
        const newProps = {
          key: index,
          value: textInput[textInputIndex],
          state: inputState,
          onChange: (event: React.ChangeEvent<HTMLInputElement>) => {
            const newTextInput = textInput.map((x, i) => i === textInputIndex ? event.target.value : x);
            setTextInput(newTextInput);

            // validation
            if (!validate(event.target.value, textInputIndex)) {
              setInputState(TextInputState.Incorrect);
              return;
            }

            onChange?.(newTextInput, textInputIndex);
            setLastValidText(newTextInput);
            setInputState(TextInputState.Default);
          },
          onBlur: () => {
            setTextInput(lastValidText);
            setInputState(TextInputState.Default);
          },
        };

        const newElement = React.cloneElement(child as React.ReactElement, newProps);
        textInputCount++;

        return newElement;
      }
    });

  // algorithm
  const values = getValues(lastValidText);

  return (
    <>
      <div className={styles['input-prompt']}>
        {childrenArray.map((child, index) => {
          if (textInputChildren[index]) {
            return textInputChildren[index];
          }
          return <span key={index}>{child}</span>;
        })}
      </div>

      <Table
        className={styles['interactive-table']}
        values={values}
        columnHeaders={getColumnHeaders?.(lastValidText)}
        rowHeaders={getRowHeaders?.(lastValidText)}
      />
    </>
  );
};

export default InteractiveTable;