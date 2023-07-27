import React from 'react';
import styles from './styles.module.css';
import CorrectIcon from '@site/src/components/utils/CorrectIcon';
import TextInput from '@site/src/components/utils/TextInput';

export interface BlankProps {
  answer: string;
  value?: string;
  correct?: boolean;
  readOnly: boolean;
  onChange?: (event: React.ChangeEvent<HTMLInputElement>) => void;
}

const Blank = ({ answer, value, correct, readOnly, onChange }: BlankProps) => {
  return (
    <div className={styles.wrapper}>
      <TextInput
        value={value}
        className={correct === undefined ? '' : styles.checked}
        onChange={onChange}
        readOnly={readOnly}
      />
      {correct === undefined
        ? null
        : <CorrectIcon correct={correct} className={styles.icon} />
      }
    </div>
  );
};

Blank.defaultProps = {
  readOnly: false,
};

export default Blank;