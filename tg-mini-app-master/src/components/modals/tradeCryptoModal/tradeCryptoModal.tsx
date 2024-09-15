import CandleStick from '@/assets/chart/candleStick';
import Line from '@/assets/chart/line';
import MainCoin from '@/assets/coins/coin';
import { ChartTimePopup } from '@/components/chartTimePopup';
import { Loader } from '@/components/loader';
import { RootState } from '@/store';
import { getUserBoosters } from '@/store/boostersSlice';
import { showNotification } from '@/store/notificationSlice';
import { createOrder } from '@/store/ordersSlice';
import { useGetSymbolPair, useLevelRestrictions } from '@/utils/hooks';
import { ThunkDispatch } from '@reduxjs/toolkit';
import { initHapticFeedback } from '@telegram-apps/sdk';
import React, {
  lazy,
  Suspense,
  useCallback,
  useEffect,
  useMemo,
  useRef,
  useState,
} from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { ClosedTrades } from './ClosedTrades/ClosedTrades';
import { CurrentTrades } from './CurrentTrades/CurrentTrades';
import css from './tradeCryptoModal.module.css';

const Chart = lazy(() =>
  import('@/components/chart').then(({ Chart }) => ({ default: Chart })),
);

const MAX_SIZE = 8;

export const TradeCryptoModal: React.FC = () => {
  const hapticFeedback = initHapticFeedback();
  const dispatch = useDispatch<ThunkDispatch<RootState, any, any>>();
  const { crypto } = useSelector(
    (state: RootState) => state.modals.cryptoTradeModal,
  );
  const { user } = useSelector((state: RootState) => state.user);
  const { boosters } = useSelector((state: RootState) => state.boosters);
  const inputRef = useRef<HTMLDivElement>(null);
  const originalScrollPosition = useRef(0);
  const { chartTime } = useSelector((state: RootState) => state.chart);
  const [isOpen, setIsOpen] = useState(false);
  const [mode, setMode] = useState<'candleStick' | 'line'>('line');
  const [localSliderValue, setLocalSliderValue] = useState(1);
  const [currentButton, setCurrentButton] = useState<'current' | 'closed'>(
    'current',
  );
  const [maxAmount, setMaxAmount] = useState<number | null>(null);
  const [maxLeverage, setMaxLeverage] = useState<number | null>(null);
  const [formData, setFormData] = useState({
    amount: 0,
    leverage: 1,
    direction: '',
    contract_pair: crypto.contract_address,
  });

  useEffect(() => {
    const fetchBoosters = async () => {
      try {
        const resultAction = await dispatch(getUserBoosters());
        if (getUserBoosters.fulfilled.match(resultAction)) {
          // Вызвать хук и обновить стейт после успешного выполнения экшна
          const { maxAmount, maxLeverage } = useLevelRestrictions({
            balance: user?.balance,
            levels: {
              range_lvl: resultAction.payload['range']?.lvl,
              leverage_lvl: resultAction.payload['leverage']?.lvl,
            },
            freeBoosters: {
              turbo_range: boosters['freeBoosters']?.turbo_range,
              x_leverage: boosters['freeBoosters']?.x_leverage,
            },
          });
          setMaxAmount(maxAmount?.toFixed(2));
          setMaxLeverage(maxLeverage);
        }
      } catch (err) {
        console.error('Failed to load boosters: ', err);
      }
    };

    if (Object.keys(boosters).length === 0) {
      fetchBoosters();
    } else {
      const { maxAmount, maxLeverage } = useLevelRestrictions({
        balance: user?.balance,
        levels: {
          range_lvl: boosters['range']?.lvl,
          leverage_lvl: boosters['leverage']?.lvl,
        },
        freeBoosters: {
          turbo_range: boosters['freeBoosters']?.turbo_range,
          x_leverage: boosters['freeBoosters']?.x_leverage,
        },
      });
      setMaxAmount(maxAmount?.toFixed(2));
      setMaxLeverage(maxLeverage);
    }
  }, [dispatch, boosters]);

  const marks = useMemo(
    () => Array.from({ length: MAX_SIZE }, (_, index) => index + 1),
    [],
  );

  const pair = useGetSymbolPair({ contract: crypto.contract_address });

  const adjustedHeight = useMemo(
    () => ((localSliderValue - 1) / (MAX_SIZE - 1)) * 100,
    [localSliderValue],
  );

  const handleSliderChange = useCallback(
    (event: React.ChangeEvent<HTMLInputElement>) => {
      const newLeverage = Math.min(event.target.valueAsNumber, maxLeverage);
      setFormData((prevData) => ({
        ...prevData,
        leverage: newLeverage,
      }));
      setLocalSliderValue(event.target.valueAsNumber);
      hapticFeedback.selectionChanged();
    },
    [maxLeverage],
  );

  const handleAmountChange = useCallback(
    (event: React.ChangeEvent<HTMLInputElement>) => {
      const newAmount = Math.min(parseInt(event.target.value, 10), maxAmount);
      setFormData((prevData) => ({
        ...prevData,
        amount: newAmount,
      }));
    },
    [maxAmount],
  );

  const handleChooseDirection = useCallback((direction: 'long' | 'short') => {
    setFormData((prevData) => ({
      ...prevData,
      direction,
    }));
  }, []);

  const handleCreateOrder = useCallback(async () => {
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
        ...formData,
        amount: 0,
        leverage: marks[0],
        direction: 'long',
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
  }, [formData, dispatch]);

  const handleFocus = useCallback(() => {
    originalScrollPosition.current = window.scrollY;
    inputRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }, []);

  const handleBlur = useCallback(() => {
    window.scrollTo({
      top: originalScrollPosition.current,
      behavior: 'smooth',
    });
  }, []);

  const handleClick = useCallback(() => {
    setCurrentButton((prev) => (prev === 'current' ? 'closed' : 'current'));
  }, []);

  const cryptoNames = {
    'Wrapped Ether': 'Ethereum',
    'BTCB Token': 'Bitcoin',
    'Wrapped SOL': 'Solana',
  };

  const togglePopup = () => {
    setIsOpen(!isOpen);
  };

  return (
    <div className={css.modal}>
      <div className={css.headerContainer}>
        <div className={css.modalImgContainer}>
          <img src="img/modal.svg" alt="modal" className={css.modalImg} />
        </div>
        <div className={css.header}>
          <div className={css.headerTitle}>
            <img src={crypto.logo} alt={crypto.name} />
            <div className={css.headerText}>
              <h1>
                {cryptoNames[crypto.name]
                  ? cryptoNames[crypto.name]
                  : crypto.name}
              </h1>
              <p>{crypto.shortName}</p>
            </div>
          </div>
          <div className={css.headerCostPrice}>
            <div>
              <button
                type="button"
                className={css.headerBtn}
                onClick={togglePopup}
              >
                <img src="img/arrowDown.svg" alt="arrow" />
              </button>
              {isOpen && <ChartTimePopup />}
            </div>
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
                {crypto.shortName === 'DOGS' || crypto.shortName === 'NOT'
                  ? parseFloat(crypto.price.toFixed(3)).toLocaleString('de-DE')
                  : parseFloat(crypto.price.toFixed(2)).toLocaleString('de-DE')}
                $
              </h3>
              <div className={css.cryptoChange}>
                <img
                  src={
                    crypto.percent_change_24h > 0
                      ? 'img/up.svg'
                      : 'img/down.svg'
                  }
                  alt="arrow"
                />
                <p
                  className={
                    crypto.percent_change_24h > 0 ? css.positive : css.negative
                  }
                >
                  {crypto.percent_change_24h > 0 ? '+' : ''}
                  {crypto.percent_change_24h.toFixed(2).replace('.', ',')}%
                </p>
              </div>
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
          className={`${css.longBtn} ${formData.direction === 'long' ? css.activeDirection : ''}`}
          onClick={() => handleChooseDirection('long')}
        >
          Long
        </button>
        <button
          type="button"
          className={`${css.shortBtn} ${formData.direction === 'short' ? css.activeDirection : ''}`}
          onClick={() => handleChooseDirection('short')}
        >
          Short
        </button>
      </div>
      <div className={css.amountContainer}>
        <div className={css.amount} ref={inputRef}>
          <input
            type="number"
            inputMode="decimal"
            placeholder="Amount"
            className={css.input}
            min={0}
            max={maxAmount}
            value={formData.amount}
            onChange={handleAmountChange}
            onFocus={handleFocus}
            onBlur={handleBlur}
          />
          <p>
            Max allowed: {maxAmount} <MainCoin width={10} height={10} />
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
              max={maxLeverage}
              value={formData.leverage}
              onChange={handleSliderChange}
              className={css.rangeInput}
            />
            <label
              htmlFor="range"
              className={css.rangeLabel}
              // style={{ left: `${adjustedHeight}%` }}
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
          className={`${css.orderBtn} ${formData.direction !== '' && formData.amount > 0 ? css.activeOrder : ''} `}
          onClick={handleCreateOrder}
          disabled={formData.direction === '' || formData.amount === 0}
        >
          Place Order
          {boosters['freeBoosters']?.turbo_range >= 1 ? <span>🚀</span> : null}
          {boosters['freeBoosters']?.x_leverage >= 1 ? <span>💥</span> : null}
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

export default TradeCryptoModal;
