import MainCoin from '@/assets/coins/coin';
import { RootState } from '@/store';
import { showNotification } from '@/store/notificationSlice';
import { closeOrder, getCurrentOrder } from '@/store/ordersSlice';
import { ThunkDispatch } from '@reduxjs/toolkit';
import { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import css from './styles.module.css';

export const CurrentTrades = () => {
  const dispatch = useDispatch<ThunkDispatch<RootState, any, any>>();
  const { currentOrder, loading } = useSelector(
    (state: RootState) => state.orders,
  );
  const { crypto } = useSelector(
    (state: RootState) => state.modals.cryptoTradeModal,
  );

  useEffect(() => {
    const fetchCurrentOrder = async () => {
      await dispatch(
        getCurrentOrder({
          contract_address: crypto?.contract_address,
        }),
      );
    };

    fetchCurrentOrder();
  }, [dispatch]);

  const onClickCloseOrder = async () => {
    const response = await dispatch(closeOrder(currentOrder?.id));

    if (closeOrder.fulfilled.match(response)) {
      dispatch(
        showNotification({
          message: 'Order closed successfully',
          type: 'success',
          visible: true,
          logo: 'img/bear.png',
        }),
      );
    } else {
      dispatch(
        showNotification({
          message: 'Something went wrong',
          type: 'error',
          visible: true,
          logo: 'img/bear.png',
        }),
      );
    }
  };

  return (
    <div className={css.currentOrder}>
      {currentOrder === null ? (
        <p>No current order</p>
      ) : loading ? (
        <p>Loading...</p>
      ) : (
        <div className={css.order}>
          <div className={css.orderDetails}>
            <h1>{currentOrder?.contract_pair}</h1>
            <div>
              <span>{currentOrder?.direction}</span>
              <p>{currentOrder?.leverage}x</p>
            </div>
            <span>TP&SL</span>
          </div>
          <div className={css.orderAmountDetails}>
            <div className={css.orderAmount}>
              <p>Position amount</p>
              <h1>
                {currentOrder?.amount} <MainCoin width={10} height={10} />
              </h1>
            </div>
            <div className={css.orderEntryRate}>
              <p>Entry rate</p>
              <h1>{currentOrder?.entry_rate.toFixed(2)}</h1>
            </div>
          </div>
          <div className={css.orderStatus}>
            <span>P&L: 31%</span>
            <button
              type="button"
              className={css.close}
              onClick={onClickCloseOrder}
            >
              Close
            </button>
          </div>
        </div>
      )}
    </div>
  );
};
