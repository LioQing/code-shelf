import React from 'react';
import clsx from 'clsx';
import styles from './styles.module.css';

export interface TextInputProps extends React.HTMLProps<HTMLInputElement> {
}

const TextInput = (props: TextInputProps) => {
  return (
    <input
      type='text'
      {...props}
      className={clsx(styles["text-input"], props.className)}
    />
  );
};

export default TextInput;