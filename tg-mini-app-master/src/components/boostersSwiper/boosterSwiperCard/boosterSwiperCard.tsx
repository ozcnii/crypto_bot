import MainCoin from '@/assets/coins/coin';
import { RootState } from '@/store';
import { openConfirmBoostModal } from '@/store/modalsSlice';
import { ThunkDispatch } from '@reduxjs/toolkit';
import { FC } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import css from './boosterSwiperCard.module.css';

interface BoosterSwiperCardProps {
  item: {
    id: number;
    name: string;
    img: string;
  };
}

export const BoosterSwiperCard: FC<BoosterSwiperCardProps> = ({
  item,
}: BoosterSwiperCardProps) => {
  const dispatch = useDispatch<ThunkDispatch<RootState, unknown, any>>();
  const { boosters, loading } = useSelector(
    (state: RootState) => state.boosters,
  );

  const handleOnClick = () => {
    dispatch(
      openConfirmBoostModal({
        isConfirmed: false,
        boost: {
          ...item,
          lvl:
            item.name === 'Trading Bot'
              ? '1'
              : boosters[item.name.toLowerCase()].lvl,
          cost:
            item.name === 'Trading Bot'
              ? '100'
              : boosters[item.name.toLowerCase()].nextPrice,
        },
      }),
    );
  };

  return (
    <div className={css.boosterCard} onClick={handleOnClick}>
      <div className={css.boosterInfo}>
        <div className={css.boosterImg}>
          <span>{item.img}</span>
        </div>
        <div className={css.boosterName}>
          <h1>{item.name}</h1>
          <p className={css.boosterCost}>
            <MainCoin width={13} height={13} />
            <span>
              {item.name === 'Trading Bot' ? (
                '100'
              ) : loading ? (
                <div className={css.loadingContainer}>
                  <div className={css.wave}></div>
                </div>
              ) : (
                boosters[item.name.toLowerCase()]?.nextPrice
              )}
            </span>
            |
            <p>
              {item.name === 'Trading Bot' ? (
                '1'
              ) : loading ? (
                <div className={css.loadingContainer}>
                  <div className={css.wave}></div>
                </div>
              ) : (
                boosters[item.name.toLowerCase()]?.lvl
              )}
            </p>
            lvl
          </p>
        </div>
      </div>
      <button type="button" className={css.confirmButton}>
        <img src="img/boosterVector.svg" alt="booster" />
      </button>
    </div>
  );
};
