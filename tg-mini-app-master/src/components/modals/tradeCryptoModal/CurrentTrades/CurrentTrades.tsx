import MainCoin from '@/assets/coins/coin';
import { RootState } from '@/store';
import { showNotification } from '@/store/notificationSlice';
import { closeOrder, getCurrentOrder } from '@/store/ordersSlice';
import { WS_URL } from '@/utils/constants';
import { ThunkDispatch } from '@reduxjs/toolkit';
import { memo, useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import css from './styles.module.css';

export const CurrentTrades = memo(() => {
  const dispatch = useDispatch<ThunkDispatch<RootState, any, any>>();
  const { currentOrder, loading } = useSelector(
    (state: RootState) => state.orders,
  );
  const { crypto } = useSelector(
    (state: RootState) => state.modals.cryptoTradeModal,
  );

  const [pnlPercent, setPnlPercent] = useState<number | null>(null);
  const [pnlValue, setPnlValue] = useState<number | null>(null);

  useEffect(() => {
    const fetchCurrentOrder = async () => {
      await dispatch(
        getCurrentOrder({
          contract_address: crypto?.contract_address,
        }),
      );
    };

    fetchCurrentOrder();
  }, [dispatch, crypto?.contract_address]);

  useEffect(() => {
    const ws = new WebSocket(
      `${WS_URL}/api/v.1.0/ws/orders/pnl/${currentOrder?.id}?api_key=${localStorage.getItem(
        'api_key',
      )}&client_id=1`,
    );

    // Открываем соединение
    ws.onopen = () => {
      if (crypto?.contract_address) {
        ws.send(
          JSON.stringify({
            action: 'subscribe',
            contract: crypto.contract_address,
          }),
        );
      }
    };

    // Обрабатываем сообщения с обновлением P&L
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setPnlPercent(data.pnl_percent);
      setPnlValue(data.pnl_value);
    };

    // Закрываем соединение при размонтировании компонента
    return () => {
      ws.close();
    };
  }, [currentOrder?.id, crypto?.contract_address]);

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
        <div className={css.noCurrentOrder}>
          <span>🧸</span>
          <p>No current order yet</p>
        </div>
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
              <h1>{currentOrder?.entry_rate?.toFixed(2)}</h1>
            </div>
          </div>
          <div className={css.orderStatus}>
            <div>
              P&L:{' '}
              <span className={pnlPercent > 0 ? css.green : css.red}>
                {pnlPercent !== null
                  ? `${pnlPercent > 0 ? '+' : ''} ${pnlPercent.toFixed(2)}%`
                  : 'Loading'}
              </span>
            </div>
            <span className={pnlValue > 0 ? css.green : css.red}>
              {pnlValue !== null
                ? `${pnlValue > 0 ? '+' : ''} ${pnlValue.toFixed(2)}`
                : 'Loading'}
              <MainCoin width={10} height={10} />
            </span>
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
});

CurrentTrades.displayName = 'CurrentTrades';
