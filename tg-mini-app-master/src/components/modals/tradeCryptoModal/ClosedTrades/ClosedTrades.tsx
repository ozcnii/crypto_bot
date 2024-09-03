import { RootState } from '@/store';
import { getOrders } from '@/store/ordersSlice';
import { ThunkDispatch } from '@reduxjs/toolkit';
import { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import styles from './styles.module.css';

export const ClosedTrades = () => {
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
              <h1>{order.contract_pair}</h1>
              <span>{order.status}</span>
            </div>
            <div className={styles.orderEntryRate}>
              <p>Entry rate:</p>
              <h1>{order.entry_rate}</h1>
            </div>
            <div className={styles.orderExitRate}>
              <p>Exit rate:</p>
              <h1>{order.exit_rate}</h1>
            </div>
          </div>
        ))
      )}
    </div>
  );
};
