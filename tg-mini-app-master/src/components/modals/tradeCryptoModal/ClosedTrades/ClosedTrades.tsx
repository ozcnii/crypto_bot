import MainCoin from '@/assets/coins/coin';
import { RootState } from '@/store';
import { getOrders } from '@/store/ordersSlice';
import { ThunkDispatch } from '@reduxjs/toolkit';
import { memo, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import styles from './styles.module.css';

export const ClosedTrades = memo(() => {
  const dispatch = useDispatch<ThunkDispatch<RootState, any, any>>();
  const { orders, loading } = useSelector((state: RootState) => state.orders);
  const { crypto } = useSelector(
    (state: RootState) => state.modals.cryptoTradeModal,
  );
  useEffect(() => {
    const fetchOrders = async () => {
      await dispatch(
        getOrders({
          contract_pair: crypto?.contract_address,
        }),
      );
    };

    fetchOrders();
  }, []);

  return (
    <div className={styles.container}>
      {orders.length === 0 ? (
        <div className={styles.noOrders}>
          <span>🧸</span>
          <p>No orders yet</p>
        </div>
      ) : loading ? (
        <p>Loading...</p>
      ) : (
        orders.map((order) => (
          <div className={styles.order} key={order.id}>
            <div className={styles.orderDetails}>
              <h1>{order?.contract_pair}</h1>
              <div>
                <span>{order?.direction}</span>
                <p>{order?.leverage}x</p>
              </div>
              <span>TP&SL</span>
            </div>
            <div className={styles.orderAmountDetails}>
              <div className={styles.orderAmount}>
                <p>Position amount</p>
                <h1>
                  {order?.amount} <MainCoin width={10} height={10} />
                </h1>
              </div>
              <div className={styles.orderEntryRate}>
                <p>Entry rate</p>
                <h1>
                  {order?.entry_rate
                    ? order?.entry_rate.toFixed(2)
                    : order?.entry_rate}
                </h1>
              </div>
            </div>
            <div className={styles.orderStatus}>
              <span>P&L: {order.pnl_percentage?.toFixed(2)}%</span>
              <span>{order.pnl_value?.toFixed(2)}</span>
            </div>
          </div>
        ))
      )}
    </div>
  );
});

ClosedTrades.displayName = 'ClosedTrades';
