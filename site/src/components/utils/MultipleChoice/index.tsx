import React, {useState} from 'react';
import styles from './styles.module.css';
import Button from '@site/src/components/utils/Button';
import CorrectIcon from '@site/src/components/utils/CorrectIcon';

interface OptionProps {
  option: string;
  index: number;
  answer: number;
  selected: number | null;
  onSelect: (index: number) => void;
}

const Option = ({ option, index, answer, selected, onSelect }: OptionProps) => {
  const selectedClass = selected === index ? styles.selected : '';
  const onClick = () => selected === null ? onSelect(index) : {};

  const correctIcon = selected === null || selected !== index
    ? null
    : <CorrectIcon correct={selected === answer} />;

  return (
    <div className={styles['option-wrapper']}>
      <Button
        key={index}
        className={`${styles.option} ${selectedClass}`}
        onClick={onClick}>
        <div className={styles['option-inner-wrapper']}>
          {option}
          {correctIcon}
        </div>
      </Button>
    </div>
  );
};

interface MultipleChoiceProps {
  options: string[];
  answer: number;
  explanation: string;
  children?: React.ReactNode;
}

const MultipleChoice = ({options, answer, explanation, children}: MultipleChoiceProps) => {
  const [selected, setSelected] = useState<number | null>(null);

  const Explanation = () => {
    const correct = selected === answer
      ? 'Correct!'
      : 'Incorrect.';

    return (
      <div className={styles.result}>
        <h4 className={styles['correct-tag']}>{correct}</h4>
        {explanation}
      </div>
    );
  };

  return (
    <>
      {children}

      <div className={styles.wrapper}>
        {options.map((option, index) => (
          <Option
            key={index}
            option={option}
            index={index}
            answer={answer}
            selected={selected}
            onSelect={setSelected}
          />
        ))}
      </div>

      {selected === null ? null : <Explanation />}

      {selected === null
        ? null
        : <Button
            onClick={() => setSelected(null)}>
            Retry
          </Button>
      }
    </>
  );
}

export default MultipleChoice;