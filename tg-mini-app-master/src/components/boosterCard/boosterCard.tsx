import MainCoin from '@/assets/coins/coin';
import { RootState } from '@/store';
import { FC, useEffect, useState } from 'react';
import { useSelector } from 'react-redux';
import css from './boosterCard.module.css';

interface BoosterCardProps {
  item: {
    id: number;
    img: string;
    name: string;
    cost: number;
    lvl: number;
  };
}

export const BoosterCard: FC<BoosterCardProps> = ({
  item,
}: BoosterCardProps) => {
  const { user } = useSelector((state: RootState) => state.user);
  const [nextLevel, setNextLevel] = useState(item.lvl);
  useEffect(() => {
    setNextLevel(item.cost === 'Free' ? item.lvl - 1 : item.lvl + 1);
  }, [item.lvl]);
  return (
    <div className={css.boosterCard}>
      <div className={css.icon}>
        <span>{item.img}</span>
      </div>
      <div className={css.details}>
        <p>{item.name}</p>
        <div className={css.levels}>
          {item.cost === 'Free' ? (
            <span>{item.lvl}/3</span>
          ) : (
            <span>{item.lvl} lvl</span>
          )}
          <span style={{ margin: '0 5px' }} className={css.arrow}>
            ➟
          </span>
          {item.cost === 'Free' ? (
            <span>{nextLevel}/3</span>
          ) : (
            <span>{nextLevel} lvl</span>
          )}
        </div>
      </div>
      <div className={css.cost}>
        <span>{item.cost}</span>
        <MainCoin width={15} height={15} />
      </div>
    </div>
  );
};
