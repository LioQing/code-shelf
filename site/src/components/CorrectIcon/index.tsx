import React from 'react';
import styles from './styles.module.css';
import CheckIcon from '@mui/icons-material/Check';
import ClearIcon from '@mui/icons-material/Clear';

interface CorrectIconProps {
  correct: boolean;
  className?: string;
}

const CorrectIcon = ({correct, className}: CorrectIconProps) => {
  return correct
    ? <CheckIcon className={`${className} ${styles.correct} ${styles.icon}`}/>
    : <ClearIcon className={`${className} ${styles.incorrect} ${styles.icon}`}/>;
};

CorrectIcon.defaultProps = {
  correct: false,
}

export default CorrectIcon;