import React from 'react';

interface AuthButtonProps {
  text: string;
  onClick: () => void;
}

const AuthButton: React.FC<AuthButtonProps> = ({ text, onClick }) => {
  return (
    <button style={styles.button} onClick={onClick}>
      {text}
    </button>
  );
};

const styles = {
  button: {
    backgroundColor: '#64b5f6',
    color: '#fff',
    padding: '12px 20px',
    border: 'none',
    borderRadius: '5px',
    cursor: 'pointer',
    fontSize: '1em',
    transition: 'background-color 0.3s ease, transform 0.2s ease',
    ':hover': {
        backgroundColor: '#90caf9',
        transform: 'scale(1.05)',
    },
    ':active': {
        transform: 'scale(0.95)',
    }
  },
};

export default AuthButton;
