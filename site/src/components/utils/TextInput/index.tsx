import React from 'react';
import clsx from 'clsx';
import styles from './styles.module.css';

export interface TextInputProps extends React.HTMLProps<HTMLInputElement> {
  state: TextInputState;
  width?: string;
  subtitle?: string;
}

export enum TextInputState {
  Default = "default",
  Correct = "correct",
  Incorrect = "incorrect",
  Warning = "warning",
}

const TextInput = (props: TextInputProps) => {
  return (
    <input
      type='text'
      {...props}
      style={{ width: props.width ?? '200px' }}
      className={clsx(
        styles["text-input"],
        styles[props.state],
        styles["border"],
        props.className,
      )}
    />
  );
};

TextInput.defaultProps = {
  state: TextInputState.Default,
};

export default TextInput;