import { FC, useEffect, useRef } from 'react';
import styles from './chart.module.css';

interface ChartProps {
  mode: 'candleStick' | 'line';
  symbol: string;
}

const createScales = (count: number, className: string) => {
  return Array.from({ length: count }).map((_, index) => (
    <div key={index} className={className}></div>
  ));
};

export const Chart: FC<ChartProps> = ({ mode, symbol }) => {
  const container = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // Clean up the previous chart by removing the script and its content
    if (container.current) {
      container.current.innerHTML = ''; // Clear previous chart
    }

    // Create the new chart
    const script = document.createElement('script');
    script.src =
      'https://s3.tradingview.com/external-embedding/embed-widget-advanced-chart.js';
    script.type = 'text/javascript';
    script.async = true;
    script.innerHTML = `
      {
        "symbol": "${symbol}",
        "interval": "1",
        "timezone": "Etc/UTC",
        "theme": "dark",
        "style": "${mode === 'candleStick' ? '1' : '2'}",
        "locale": "en",
        "hide_top_toolbar": true,
        "hide_legend": true,
        "allow_symbol_change": false,
        "save_image": false,
        "calendar": false,
        "hide_volume": true,
        "support_host": "https://www.tradingview.com"
      }`;

    container.current?.appendChild(script);
  }, [mode, symbol]);

  return (
    // <div className={css.cryptoChart}>
    //   {/* <img src="img/cryptoNet.svg" alt="net" className={css.net} />
    //   <div className={css.scalesLeftContainer}>
    //     {createScales(7, css.scaleLeft)}
    //   </div>
    //   <div className={css.scalesBottomContainer}>
    //     {createScales(12, css.scaleBottom)}
    //   </div>
    //   {mode === 'candleStick' && <CandleStickChart data={candles} />}
    // 	{mode === 'line' && <Line data={chartData} options={options} />} */}
    // </div>
    <div
      className={`tradingview-widget-container ${styles.cryptoChart}`}
      ref={container}
    >
      <div className="tradingview-widget-container__widget"></div>
    </div>
  );
};
