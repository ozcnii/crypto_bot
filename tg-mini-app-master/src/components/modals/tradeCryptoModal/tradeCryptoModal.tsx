import CandleStick from '@/assets/chart/candleStick'
import Line from '@/assets/chart/line'
import { Chart } from '@/components/chart'
import { Loader } from '@/components/loader'
import { RootState } from '@/store'
import { postEvent } from '@telegram-apps/sdk'
import { Suspense, useState } from 'react'
import { useSelector } from 'react-redux'
import css from './tradeCryptoModal.module.css'

const MAX_SIZE = 7;

export const TradeCryptoModal = () => {
	const { crypto } = useSelector((state: RootState) => state.modals.cryptoTradeModal);
	const [mode, setMode] = useState<'candleStick' | 'line'>('line');
	const cleanedName = crypto.name.replace("Wrapped ", "").replace(" Token", "");
	const marks = Array.from({ length: MAX_SIZE }, (_, index) => index + 1);
  const [localSliderValue, setLocalSliderValue] = useState(marks[0]);

  const handleSliderChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const newValue = parseInt(event.target.value, 10);
    setLocalSliderValue(newValue);
		postEvent('web_app_trigger_haptic_feedback', {
			type: 'selection_change',
		});
	};

  const adjustedHeight = ((localSliderValue - 1) / (MAX_SIZE - 1)) * 100;

	return (
		<div className={css.modal}>
			<div className={css.modalImgContainer}>
				<img src='img/modal.svg' alt="modal" className={css.modalImg} />
			</div>
			<div className={css.header}>
				<div className={css.headerTitle}>
					<img src={crypto.logo} alt={crypto.name} />
					<div className={css.headerText}>
						<h1>{crypto.name === 'Wrapped Ether' ? 'Ethereum' : cleanedName === 'BTCB' ? 'Bitcoin' : cleanedName}</h1>
						<p>{crypto.network_slug.split(' ')[0]}</p>
					</div>		
				</div>
				<div className={css.headerCostPrice}>
					<button type="button" className={css.headerBtn}>
						<img src="img/arrowDown.svg" alt="arrow" />
					</button>
					<div className={css.toggleSwitch}>
							<div className={`${css.candleStickMode} ${mode === 'candleStick' ? css.active : ''}`} onClick={() => setMode('candleStick')}>
								<CandleStick fill={mode === 'candleStick' ? '#EEEEEE' : '#101010'} />
							</div>
							<div className={`${css.lineMode} ${mode === 'line' ? css.active : ''}`} onClick={() => setMode('line')}>
								<Line fill={mode === 'line' ? '#EEEEEE' : '#101010'} />
							</div>
					</div>
					<div className={css.cryptoPrice}>
						<h3>{parseFloat(crypto.price.toFixed(2)).toLocaleString('de-DE')}$</h3>
						<div className={css.cryptoChange}>
							<img src={crypto.percent_change_24h > 0 ? 'img/up.svg' : 'img/down.svg'} alt="arrow" className={css.arrow} />
							<p className={crypto.percent_change_24h > 0 ? css.positive : css.negative}>{crypto.percent_change_24h > 0 ? '+' : ''} {crypto.percent_change_24h.toFixed(2).replace('.', ',')}%</p>
						</div>
					</div>
				</div>
			</div>
			<Suspense fallback={<Loader />}>
				<Chart mode={mode} candles={crypto.candles} />
			</Suspense>
			<div className={css.buttons}>
				<button type="button" className={css.longBtn}>Long</button>
				<button type="button" className={css.shortBtn}>Short</button>
			</div>
			<div className={css.amountContainer}>
				<div className={css.amount}>
					<div className={css.inputContainer}>
						<input
							type="number"
							placeholder="0.00"
							className={css.input}
							min={0}
							step={0.1}
							max={1000}
							value={100}
							name="amount"
							id="amount"
							autoComplete="off"
							required
						/>
						<select className={css.select} name="currency" id="currency" value={'TON'}>
							<option>TON</option>
						</select>
					</div>
					<p>Balance: 34TON</p>
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
              value={localSliderValue}
              onChange={handleSliderChange}
              className={css.rangeInput}
            />
            <label
              htmlFor="range"
              className={css.rangeLabel}
              style={{ left: `${adjustedHeight}%` }}
            >
              {localSliderValue}x
            </label>
          </div>
        </div>
			</div>
			<div className={css.orderBtnContainer}>
				<button type="button" className={css.orderBtnDown}>
					<img src="img/arrowDown.svg" alt="arrow" />
				</button>
				<button type="button" className={css.orderBtn}>Place Order</button>
			</div>
			<div className={css.tradesContainer}></div>
		</div>
	)
}