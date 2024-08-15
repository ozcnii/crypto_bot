import { Candles } from '@/utils/types/coin'
import { Chart } from 'chart.js/auto'
import 'chartjs-adapter-date-fns'
import { CandlestickController, CandlestickElement } from 'chartjs-chart-financial'
import { FC, useEffect, useRef } from 'react'

// Регистрация финансовых контроллеров и элементов
Chart.register(CandlestickController, CandlestickElement);

interface CandleStickChartProps {
  data: Candles[]
}

export const CandleStickChart: FC<CandleStickChartProps> = ({ data }) => {
  const chartRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const ctx = chartRef.current!.getContext('2d');

    const chart = new Chart(ctx!, {
      type: 'candlestick',
      data: {
        datasets: [
          {
            data: data.map(item => ({
              x: new Date(item.timestamp).getTime(),
              o: item.open,
              h: item.high,
              l: item.low,
              c: item.close,
            })),
            backgroundColor: '#2916FF',
            borderWidth: 1,
            // backgroundColors: {
            //   up: '#2916FF',
            //   down: '#2916FF',
            //   unchanged: '#2916FF',
            // }
          },
        ],
      },
      options: {
        scales: {
          x: { display: false, beginAtZero: true },
          y: { display: false },
        },
        plugins: {
          legend: { display: false },
        },
        responsive: true,
        maintainAspectRatio: true,
      }
    });
    return () => {
      chart.destroy();
    };
  }, [data]);

  return (
    <canvas ref={chartRef}></canvas>
  );
};