import React from 'react';
import styles from './styles.module.css';

interface ButtonProps {
  onClick: () => void;
  className?: string;
  children?: React.ReactNode;
}

const Button = ({onClick, className, children}: ButtonProps) => {
  const onKeyDown = (event: React.KeyboardEvent<HTMLDivElement>) => {
    if (event.key === 'Enter') {
      onClick();
    }
  };

  return (
    <div
      className={`${className} ${styles.button}`}
      onClick={onClick}
      onKeyDown={onKeyDown}
      tabIndex={0}
      role='button'>
      {children}
    </div>
  );
};

export default Button;