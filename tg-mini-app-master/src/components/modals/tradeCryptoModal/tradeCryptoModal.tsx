import CandleStick from '@/assets/chart/candleStick';
import Line from '@/assets/chart/line';
import MainCoin from '@/assets/coins/coin';
import { Chart } from '@/components/chart';
import { Loader } from '@/components/loader';
import { RootState } from '@/store';
import { showNotification } from '@/store/notificationSlice';
import { createOrder } from '@/store/ordersSlice';
import { useGetSymbolPair } from '@/utils/hooks';
import { ThunkDispatch } from '@reduxjs/toolkit';
import { postEvent } from '@telegram-apps/sdk';
import { Suspense, useRef, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { ClosedTrades } from './ClosedTrades/ClosedTrades';
import { CurrentTrades } from './CurrentTrades/CurrentTrades';
import css from './tradeCryptoModal.module.css';

const MAX_SIZE = 7;

export const TradeCryptoModal = () => {
  const dispatch = useDispatch<ThunkDispatch<RootState, any, any>>();
  const { crypto } = useSelector(
    (state: RootState) => state.modals.cryptoTradeModal,
  );
  const { user } = useSelector((state: RootState) => state.user);
  const inputRef = useRef<HTMLInputElement>(null);
  const originalScrollPosition = useRef(0);
  const [mode, setMode] = useState<'candleStick' | 'line'>('line');
  const cleanedName = crypto.name.replace('Wrapped ', '').replace(' Token', '');
  const marks = Array.from({ length: MAX_SIZE }, (_, index) => index + 1);
  const [localSliderValue, setLocalSliderValue] = useState(marks[0]);
  const [amount, setAmount] = useState(0);
  const [currentButton, setCurrentButton] = useState('current');
  const pair = useGetSymbolPair({ contract: crypto.contract_address });

  const [formData, setFormData] = useState({
    amount: 0,
    leverage: marks[0],
    direction: 'long',
    contract_pair: crypto.contract_address,
  });

  const handleSliderChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      leverage: parseInt(event.target.value, 10),
    });
    postEvent('web_app_trigger_haptic_feedback', {
      type: 'selection_change',
    });
  };

  const adjustedHeight = ((localSliderValue - 1) / (MAX_SIZE - 1)) * 100;

  const handleAmountChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      amount: parseInt(event.target.value, 10),
    });
  };

  const handleFocus = (event: React.FocusEvent<HTMLInputElement>) => {
    originalScrollPosition.current = window.scrollY;

    inputRef.current?.scrollIntoView({ behavior: 'smooth', block: 'center' });
  };

  const handleBlur = (event: React.FocusEvent<HTMLInputElement>) => {
    window.scrollTo({
      top: originalScrollPosition.current,
      behavior: 'smooth',
    });
  };

  const handleClick = () => {
    if (currentButton === 'current') {
      setCurrentButton('closed');
    } else {
      setCurrentButton('current');
    }
  };

  const handleChooseDirection = (direction: 'long' | 'short') => {
    setFormData({
      ...formData,
      direction,
    });
  };

  const handleCreateOrder = async () => {
    if (formData.amount <= 0) {
      dispatch(
        showNotification({
          message: 'Amount must be greater than 0',
          type: 'error',
          visible: true,
          logo: 'img/brokenhouse.png',
        }),
      );
      return;
    }
    const response = await dispatch(createOrder(formData));

    if (response.meta.requestStatus === 'fulfilled') {
      dispatch(
        showNotification({
          message: 'Order created successfully',
          type: 'success',
          visible: true,
          logo: 'img/bear.png',
        }),
      );
      setFormData({
        amount: 0,
        leverage: marks[0],
        direction: 'long',
        contract_pair: crypto.contract_address,
      });
    } else {
      dispatch(
        showNotification({
          message: 'Failed to create order',
          type: 'error',
          visible: true,
          logo: 'img/brokenhouse.png',
        }),
      );
    }
  };

  return (
    <div className={css.modal}>
      <div className={css.modalImgContainer}>
        <img src="img/modal.svg" alt="modal" className={css.modalImg} />
      </div>
      <div className={css.header}>
        <div className={css.headerTitle}>
          <img src={crypto.logo} alt={crypto.name} />
          <div className={css.headerText}>
            <h1>
              {crypto.name === 'Wrapped Ether'
                ? 'Ethereum'
                : cleanedName === 'BTCB'
                  ? 'Bitcoin'
                  : cleanedName}
            </h1>
            <p>{crypto.network_slug.split(' ')[0]}</p>
          </div>
        </div>
        <div className={css.headerCostPrice}>
          <button type="button" className={css.headerBtn}>
            <img src="img/arrowDown.svg" alt="arrow" />
          </button>
          <div className={css.toggleSwitch}>
            <div
              className={`${css.candleStickMode} ${mode === 'candleStick' ? css.active : ''}`}
              onClick={() => setMode('candleStick')}
            >
              <CandleStick
                fill={mode === 'candleStick' ? '#EEEEEE' : '#101010'}
              />
            </div>
            <div
              className={`${css.lineMode} ${mode === 'line' ? css.active : ''}`}
              onClick={() => setMode('line')}
            >
              <Line fill={mode === 'line' ? '#EEEEEE' : '#101010'} />
            </div>
          </div>
          <div className={css.cryptoPrice}>
            <h3>
              {parseFloat(crypto.price.toFixed(2)).toLocaleString('de-DE')}$
            </h3>
            <div className={css.cryptoChange}>
              <img
                src={
                  crypto.percent_change_24h > 0 ? 'img/up.svg' : 'img/down.svg'
                }
                alt="arrow"
                className={css.arrow}
              />
              <p
                className={
                  crypto.percent_change_24h > 0 ? css.positive : css.negative
                }
              >
                {crypto.percent_change_24h > 0 ? '+' : ''}{' '}
                {crypto.percent_change_24h.toFixed(2).replace('.', ',')}%
              </p>
            </div>
          </div>
        </div>
      </div>
      <Suspense fallback={<Loader />}>
        <Chart mode={mode} symbol={pair} />
      </Suspense>
      <div className={css.buttons}>
        <button
          type="button"
          className={css.longBtn}
          onClick={() => handleChooseDirection('long')}
        >
          Long
        </button>
        <button
          type="button"
          className={css.shortBtn}
          onClick={() => handleChooseDirection('short')}
        >
          Short
        </button>
      </div>
      <div className={css.amountContainer}>
        <div className={css.amount}>
          <div className={css.inputContainer}>
            <input
              type="number"
              inputMode="decimal"
              placeholder="0.00"
              className={css.input}
              min={0}
              step={0.01}
              max={user.balance}
              value={formData.amount}
              onChange={handleAmountChange}
              onFocus={handleFocus}
              onBlur={handleBlur}
              name="amount"
              id="amount"
              autoComplete="off"
              required
              ref={inputRef}
            />
          </div>
          <p>
            Balance: {user.balance} <MainCoin width={10} height={10} />
          </p>
        </div>
        <div className={css.rangeWithScale}>
          <div className={css.scaleValues}>
            {marks.map((mark) => (
              <span key={mark} className={css.mark}></span>
            ))}
          </div>
          <div className={css.rangeContainer}>
            <input
              type="range"
              id="range"
              min={marks[0]}
              max={marks[marks.length - 1]}
              value={formData.leverage}
              onChange={handleSliderChange}
              className={css.rangeInput}
            />
            <label
              htmlFor="range"
              className={css.rangeLabel}
              style={{ left: `${adjustedHeight}%` }}
            >
              {formData.leverage}x
            </label>
          </div>
        </div>
      </div>
      <div className={css.orderBtnContainer}>
        <button type="button" className={css.orderBtnDown}>
          <img src="img/arrowDown.svg" alt="arrow" />
        </button>
        <button
          type="button"
          className={css.orderBtn}
          onClick={handleCreateOrder}
        >
          Place Order
        </button>
      </div>
      <div className={css.tradesContainer}>
        <button
          type="button"
          className={`${css.tradeBtn} ${currentButton === 'current' ? css.activeTradeBtn : ''}`}
          onClick={handleClick}
        >
          Current trade
        </button>
        <button
          type="button"
          className={`${css.tradeBtn} ${currentButton === 'closed' ? css.activeTradeBtn : ''}`}
          onClick={handleClick}
        >
          Closed trades
        </button>
      </div>
      <div className={css.trades}>
        {currentButton === 'current' ? <CurrentTrades /> : <ClosedTrades />}
      </div>
    </div>
  );
};
