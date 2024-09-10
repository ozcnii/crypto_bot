import { RootState } from '@/store';
import { FC, useCallback, useEffect, useState } from 'react';
import { useSelector } from 'react-redux';
import styles from './modalWindow.module.css';

interface ModalWindowProps {
  isOpen: boolean;
  close: () => void;
  children: React.ReactNode;
}

export const ModalWindow: FC<ModalWindowProps> = ({
  isOpen,
  close,
  children,
}) => {
  const { isConfirmed } = useSelector(
    (state: RootState) => state.modals.confirmBoostModal,
  );
  const { isClosing } = useSelector(
    (state: RootState) => state.modals.cryptoTradeModal,
  );
  const [exiting, setExiting] = useState(false);

  const handleClose = useCallback(() => {
    setExiting(true);
    setTimeout(() => {
      setExiting(false);
      close();
    }, 300); // Matches the slideDown animation time
  }, [close]);

  useEffect(() => {
    if (isConfirmed) {
      setTimeout(handleClose, 2500);
    }
  }, [isConfirmed, handleClose]);

  useEffect(() => {
    if (isClosing) {
      handleClose();
    }
  }, [isClosing, handleClose]);

  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = 'unset';
    }
    return () => {
      document.body.style.overflow = 'unset';
    };
  }, [isOpen]);

  return (
    isOpen && (
      <div className={styles.modalWindowWrapper}>
        <div className={`${styles.modalWindow} ${exiting ? styles.exit : ''}`}>
          {children}
        </div>
        <div className={styles.background} onClick={handleClose}></div>
      </div>
    )
  );
};
