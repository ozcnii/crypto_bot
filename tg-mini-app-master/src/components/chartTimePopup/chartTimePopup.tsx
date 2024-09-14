import { RootState } from '@/store';
import { setChartTime } from '@/store/chartSlice';
import { useDispatch, useSelector } from 'react-redux';
import styles from './styles.module.css';

const times = [
  {
    id: 1,
    time: '1',
    showTime: '1min',
  },
  {
    id: 2,
    time: '15',
    showTime: '15min',
  },
  {
    id: 3,
    time: '60',
    showTime: '1H',
  },
  {
    id: 4,
    time: '240',
    showTime: '4H',
  },
  {
    id: 5,
    time: 'D',
    showTime: '1D',
  },
];

export const ChartTimePopup = () => {
  const dispatch = useDispatch();
  const { chartTime } = useSelector((state: RootState) => state.chart);
  const changeTime = (time: string) => {
    dispatch(setChartTime(time));
  };
  return (
    <div className={styles.container}>
      {times.map((time) => (
        <div
          key={time.id}
          className={`${styles.time} ${chartTime === time.time ? styles.active : ''}`}
          onClick={() => changeTime(time.time)}
        >
          {time.showTime}
        </div>
      ))}
    </div>
  );
};
