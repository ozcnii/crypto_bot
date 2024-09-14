import { RootState } from '@/store';
import { closeModal } from '@/store/modalsSlice';
import { useCallback } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { ConfirmBoostModal } from './confirmBoostModal/confirmBoostModal';
import { CreateClanModal } from './createClanModal/createClanModal';
import { ModalWindow } from './modalWindow/modalWindow';
import { TradeCryptoModal } from './tradeCryptoModal/tradeCryptoModal';

export const Modal = () => {
  const dispatch = useDispatch();
  const { isOpen, modalType } = useSelector((state: RootState) => state.modals);
  const closeCallback = useCallback(() => {
    dispatch(closeModal());
  }, [dispatch]);
  return (
    <ModalWindow
      isOpen={isOpen}
      close={closeCallback}
      fullHeight={modalType === 'CREATECLAN'}
    >
      {modalType === 'CONFIRMBOOST' && <ConfirmBoostModal />}
      {modalType === 'TRADECRYPTO' && <TradeCryptoModal />}
      {modalType === 'CREATECLAN' && <CreateClanModal />}
    </ModalWindow>
  );
};
