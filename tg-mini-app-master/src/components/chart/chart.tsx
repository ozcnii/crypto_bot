import { Candles } from '@/utils/types/coin'
import { CategoryScale, Chart as ChartJS, Legend, LinearScale, LineElement, PointElement, Title, Tooltip } from 'chart.js'
import { FC } from 'react'
import { Line } from 'react-chartjs-2'
import { CandleStickChart } from './candleStickChart/candleStickChart'
import css from './chart.module.css'

ChartJS.register(CategoryScale, LinearScale, LineElement, PointElement, Title, Tooltip, Legend);

interface ChartProps {
	mode: 'candleStick' | 'line',
	candles: Candles[]
}

const createScales = (count: number, className: string) => {
  return Array.from({ length: count }).map((_, index) => (
    <div key={index} className={className}></div>
  ));
};

export const Chart: FC<ChartProps> = ({ mode, candles }) => {

	const chartData = {
    labels: candles.map((candle) => candle.timestamp),
    datasets: [
      {
        data: candles.map((candle) => candle.close),
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

	return (
		<div className={css.cryptoChart}>
      <img src="img/cryptoNet.svg" alt="net" className={css.net} />
      <div className={css.scalesLeftContainer}>
        {createScales(7, css.scaleLeft)}
      </div>
      <div className={css.scalesBottomContainer}>
        {createScales(12, css.scaleBottom)}
      </div>
      {mode === 'candleStick' && <CandleStickChart data={candles} />}
			{mode === 'line' && <Line data={chartData} options={options} />}
    </div>
	)
}