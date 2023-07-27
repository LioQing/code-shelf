import React, { useState } from 'react';
import styles from './styles.module.css';
import { BlankProps } from '@site/src/components/utils/Blank';
import Button from '@site/src/components/utils/Button';

interface FillInTheBlankProps {
  explanation: string;
  children?: React.ReactNode;
}

const isBlank = (child: React.ReactNode) => React.isValidElement(child) && (child as React.ReactElement).props['mdxType'] === 'Blank';

const isCorrect = (answer: string, blank: React.ReactElement<BlankProps>) => answer.trim() === blank.props.answer;

const FillInTheBlank = ({ explanation, children }: FillInTheBlankProps) => {
  const childrenArray = React.Children.toArray(children);

  const [answers, setAnswers] = useState<{ [id: string]: string }>(Object.fromEntries(childrenArray
    .map((child, index) => {
      if (isBlank(child)) {
        return [index.toString(), ''];
      }
    })
    .filter(child => child)
  )); // index: answer

  const [checked, setChecked] = useState(false);

  const blanks = Object.fromEntries(childrenArray
    .map((child, index) => {
      if (isBlank(child)) {
        const newProps = {
          key: index,
          value: answers[index.toString()],
          correct: checked ? isCorrect(answers[index.toString()], child as React.ReactElement<BlankProps>) : undefined,
          readOnly: checked,
          onChange: (event: React.ChangeEvent<HTMLInputElement>) => {
            setAnswers({ ...answers, [index.toString()]: event.target.value });
          },
        };

        const newElement = React.cloneElement<BlankProps>(child as React.ReactElement, newProps);

        return [index.toString(), newElement];
      }
    })
    .filter(child => child)
  ); // index: Blank

  const Explanation = () => {
    const answerResults = childrenArray
      .map((child, index) => {
        if (isBlank(child)) {
          return isCorrect(answers[index.toString()], child as React.ReactElement<BlankProps>);
        }
      })
      .filter(child => child !== undefined);

    const numCorrect = answerResults.filter(result => result).length;

    const correct = `${numCorrect} out of ${answerResults.length} correct!`;

    return (
      <div className={styles.result}>
        <h4 className={styles['correct-tag']}>{correct}</h4>
        {explanation}
      </div>
    );
  };

  const onClick = () => {
    if (checked) {
      setAnswers(Object.fromEntries(childrenArray
        .map((child, index) => {
          if (isBlank(child)) {
            return [index.toString(), ''];
          }
        })
        .filter(child => child)
      ));
    }
    setChecked(!checked);
  };

  return (
    <>
      <div className={styles.question}>
        {childrenArray.map((child, index) => {
          if (blanks.hasOwnProperty(index)) {
            return blanks[index.toString()];
          }
          return <span key={index}>{child}</span>;
        })}
      </div>

      {checked && <Explanation />}

      <Button onClick={onClick}>
        {checked ? 'Retry' : 'Check'}
      </Button>
    </>
  );
};

export default FillInTheBlank;