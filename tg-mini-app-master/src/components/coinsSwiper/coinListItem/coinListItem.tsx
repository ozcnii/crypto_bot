import { openCryptoTradeModal } from '@/store/modalsSlice';
import { Coin } from '@/utils/types/coin';
import {
  CategoryScale,
  Chart as ChartJS,
  Legend,
  LinearScale,
  LineElement,
  PointElement,
  Title,
  Tooltip,
} from 'chart.js';
import React from 'react';
import { Line } from 'react-chartjs-2';
import { useDispatch } from 'react-redux';
import css from './coinListItem.module.css';

// Регистраци
ChartJS.register(
  CategoryScale,
  LinearScale,
  LineElement,
  PointElement,
  Title,
  Tooltip,
  Legend,
);

interface CoinListItemProps {
  item: Coin;
}

export const CoinListItem: React.FC<CoinListItemProps> = ({
  item,
}: CoinListItemProps) => {
  const dispatch = useDispatch();
  const chartData = {
    labels: item.candles.map((candle) => candle.timestamp),
    datasets: [
      {
        data: item.candles.map((candle) => candle.close),
        fill: false,
        backgroundColor: '#FF6384',
        borderColor: '#2916FF',
        pointRadius: 0,
        pointBorderWidth: 0,
        borderWidth: 1,
      },
    ],
  };

  const options = {
    scales: {
      x: { display: false, beginAtZero: true },
      y: { display: false },
    },
    plugins: {
      legend: { display: false },
    },
    responsive: true,
    mountainAspectRatio: false,
  };

  const handleOnClick = () => {
    dispatch(openCryptoTradeModal(item));
  };

  const cryptoNames = {
    'Wrapped Ether': 'Ethereum',
    'BTCB Token': 'Bitcoin',
    'Wrapped SOL': 'Solana',
  };

  return (
    <div className={css.cryptoCard} onClick={handleOnClick}>
      <div className={css.cryptoStart}>
        <img src={item.logo} alt={item.name} className={css.cryptoImg} />
        <div className={css.cryptoInfo}>
          <h2>{cryptoNames[item.name] ? cryptoNames[item.name] : item.name}</h2>
          <p>{item.shortName}</p>
        </div>
      </div>
      <div className={css.cryptoEnd}>
        <div className={css.cryptoChart}>
          <img src="img/net.svg" alt="net" className={css.net} />
          <Line data={chartData} options={options} className={css.chart} />
        </div>
        <div className={css.cryptoPrice}>
          <h3>{parseFloat(item.price.toFixed(2)).toLocaleString('de-DE')}$</h3>
          <div className={css.cryptoChange}>
            <img
              src={item.percent_change_24h > 0 ? 'img/up.svg' : 'img/down.svg'}
              alt="arrow"
              className={css.arrow}
            />
            <p
              className={
                item.percent_change_24h > 0 ? css.positive : css.negative
              }
            >
              {item.percent_change_24h > 0 ? '+' : ''}
              {item.percent_change_24h.toFixed(2).replace('.', ',')}%
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};
