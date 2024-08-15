import { useState } from 'react'
import Select from 'react-select'
import css from './inputWithSelect.module.css'

const options = [
  { value: 'ton', label: 'TON', icon: 'img/toncoin.svg' },
  { value: 'btc', label: 'BTC', icon: 'img/bitcoin.svg' },
  { value: 'eth', label: 'ETH', icon: 'img/ethereum.svg' },
  // Добавьте другие опции
];

const customSingleValue = ({ data }) => (
  <div>
    <img src={data.icon} alt={data.label} style={{ width: "7.25px", marginRight: "1.25px" }} />
    {data.label}
  </div>
);

export const InputWithSelect = () => {
  const [selectedOption, setSelectedOption] = useState(options[0]);

  const handleChange = (selectedValue) => {
    setSelectedOption(selectedValue);
  };

  return (
    <div className={css.container}>
      <input type="number" className={css.input} placeholder="Amount" />
			<Select
        value={selectedOption}
        onChange={handleChange}
        options={options}
        className={css.select}
        classNamePrefix="react-select"
        components={{ SingleValue: customSingleValue }}
				styles={{
          control: (base) => ({ ...base, backgroundColor: '#2c2c2e', borderColor: 'transparent', color: '#fff' }),
          menu: (base) => ({ ...base, backgroundColor: '#2c2c2e' }),
          singleValue: (base) => ({ ...base, color: '#fff' }),
        }}
      />
    </div>
  );
};