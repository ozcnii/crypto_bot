import { BoosterCard } from '@/components/boosterCard';
import { ConfirmSlider } from '@/components/confirmSlider';
import { Loader } from '@/components/loader';
import { RootState } from '@/store';
import { useEffect, useRef, useState } from 'react';
import { useSelector } from 'react-redux';
import css from './confirmBoostModal.module.css';

export const ConfirmBoostModal = () => {
  const { boost, isConfirmed } = useSelector(
    (state: RootState) => state.modals.confirmBoostModal,
  );
  const { error } = useSelector((state: RootState) => state.boosters);
  const [isLoading, setIsLoading] = useState(false);
  const [showResult, setShowResult] = useState(false);
  const modalRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (isConfirmed) {
      setIsLoading(true);
      setShowResult(false);
      const timer = setTimeout(() => {
        setIsLoading(false);
        setShowResult(true);
      }, 1000);

      return () => clearTimeout(timer);
    }
  }, [isConfirmed]);

  useEffect(() => {
    if (showResult && isConfirmed) {
      modalRef.current?.style.setProperty('padding-block-end', '30.5px');
    } else {
      modalRef.current?.style.removeProperty('padding-block-end');
    }
  }, [showResult, isConfirmed]);

  return (
    <div className={css.modal} ref={modalRef}>
      <div className={css.modalImgContainer}>
        <img src="img/modal.svg" alt="modal" className={css.modalImg} />
      </div>
      <div className={css.headerTitle}>
        <h1>Confirm Action</h1>
        <p>Wallet:</p>
      </div>
      <BoosterCard item={boost} />
      {!isConfirmed ? (
        <ConfirmSlider type={boost.name.toLowerCase()} />
      ) : isLoading ? (
        <Loader />
      ) : showResult && error === null ? (
        <div className={css.confirmed}>
          <img src="img/confirmed.png" alt="Confirmed" />
          <h1>Done</h1>
        </div>
      ) : (
        <div className={css.failed}>
          <img src="img/fail.png" alt="Failed" />
          <h1>Fail</h1>
        </div>
      )}
    </div>
  );
};
