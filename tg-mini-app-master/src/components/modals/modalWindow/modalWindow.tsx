import { RootState } from '@/store';
import { FC, useCallback, useEffect, useState } from 'react';
import { useSelector } from 'react-redux';
import styles from './modalWindow.module.css';

interface ModalWindowProps {
  isOpen: boolean;
  close: () => void;
  children: React.ReactNode;
  fullHeight: boolean;
}

export const ModalWindow: FC<ModalWindowProps> = ({
  isOpen,
  close,
  children,
  fullHeight: allHeight,
}) => {
  const { isConfirmed } = useSelector(
    (state: RootState) => state.modals.confirmBoostModal,
  );
  const { isClosing, isOpen: openCrypto } = useSelector(
    (state: RootState) => state.modals.cryptoTradeModal,
  );
  const { modalType } = useSelector((state: RootState) => state.modals);
  const [exiting, setExiting] = useState(false);
  const [fullHeight, setFullHeight] = useState(false);

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

  useEffect(() => {
    if (openCrypto || allHeight) {
      setFullHeight(true);
    }

    return () => {
      setFullHeight(false);
    };
  }, [openCrypto, allHeight]);

  return (
    isOpen && (
      <div className={styles.modalWindowWrapper}>
        <div
          className={`${styles.modalWindow} ${exiting ? styles.exit : ''}`}
          style={{ height: fullHeight === true ? '100%' : '' }}
        >
          {children}
        </div>
        <div className={styles.background} onClick={handleClose}></div>
      </div>
    )
  );
};
