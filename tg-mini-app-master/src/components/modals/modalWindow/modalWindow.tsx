import { RootState } from '@/store'
import { ReactNode, useEffect, useState } from 'react'
import { useSelector } from 'react-redux'
import css from './modalWindow.module.css'

interface ModalWindowProps {
  isOpen: boolean;
  close: () => void;
  children: ReactNode;
}

export const ModalWindow = ({ isOpen, close, children }) => {
  const { isConfirmed } = useSelector((state: RootState) => state.modals.confirmBoostModal);
  const { isClosing } = useSelector((state: RootState) => state.modals.cryptoTradeModal);
  const [exiting, setExiting] = useState(false);
  const [contentVisible, setContentVisible] = useState(false);

  const handleClose = () => {
    setExiting(true);
    setTimeout(() => {
      setExiting(false);
      close();
    }, 300);
  };

  useEffect(() => {
    if (isConfirmed) {
      setTimeout(() => {
        handleClose();
      }, 2500);
    }
  }, [isConfirmed]);

  useEffect(() => {
    if (isClosing) {
      handleClose();
    }
  }, [isClosing]);

  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = 'hidden';
      // Отложенный рендеринг содержимого после завершения анимации
      setTimeout(() => {
        setContentVisible(true);
      }, 300); // Время должно совпадать с длительностью анимации
    } else {
      setContentVisible(false);
      document.body.style.overflow = 'unset';
    }

    // Clean up the overflow style on unmount
    return () => {
      document.body.style.overflow = 'unset';
    };
  }, [isOpen]);

  return (
    isOpen && (
      <div className={css.modalWindowWrapper}>
        <div className={`${css.modalWindow} ${exiting ? css.exit : ''}`}>{children}</div>
        <div className={css.background} onClick={handleClose}></div>
      </div>
    )
  );
};