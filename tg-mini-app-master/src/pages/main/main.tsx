import Power from '@/assets/power';
import Thunder from '@/assets/thunder';
import { CoinsSwiper, Modal } from '@/components';
import { LoadingStatus } from '@/constants';
import { Header } from '@/pages/main/header/header.tsx';
import { RootState } from '@/store';
import { getUserClan } from '@/store/clanSlice';
import { getClanLeagueById } from '@/store/leagueSlice';
import { getByJWTUser } from '@/store/userSlice';
import { ThunkDispatch } from '@reduxjs/toolkit';
import { useEffect, useRef, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import css from './main.module.css';

export const Main = () => {
  const dispatch = useDispatch<ThunkDispatch<unknown, unknown, unknown>>();
  const location = useLocation();
  const [wrapperHeight, setWrapperHeight] = useState('auto');
  const headerRef = useRef<HTMLDivElement>(null);
  const footerRef = useRef<HTMLDivElement>(null);
  const { user, status } = useSelector((state: RootState) => state.user);
  const { loading } = useSelector((state: RootState) => state.coin);
  const navigate = useNavigate();

  useEffect(() => {
    const updateHeight = () => {
      const headerHeight = headerRef.current?.offsetHeight || 0;
      const footerHeight = footerRef.current?.offsetHeight || 0;
      setWrapperHeight(
        `calc(var(--tg-viewport-height) - ${headerHeight + footerHeight + 105}px)`,
      );
    };

    updateHeight();
    window.addEventListener('resize', updateHeight);
    return () => window.removeEventListener('resize', updateHeight);
  }, []);

  useEffect(() => {
    const fetchUserData = async () => {
      await dispatch(getByJWTUser());
    };
    const fetchUserClanData = async () => {
      const response = await dispatch(getUserClan());
      if (getUserClan.fulfilled.match(response)) {
        await dispatch(getClanLeagueById(response.payload.league_id));
      }
    };
    fetchUserData();
    fetchUserClanData();
  }, [dispatch]);

  useEffect(() => {
    if (status === LoadingStatus.rejected) {
      navigate('/error');
    }
  }, [status, navigate]);

  return (
    <div className={css.main}>
      <div className={css.header}>
        <Header />
        <div className={css.listWrapper}>
          <h2 className={css.listHeading}>Coins</h2>
          <button className={css.plusButton} type="button">
            +
          </button>
        </div>
      </div>
      <div className={`${css.coinsWrapper}`}>
        <CoinsSwiper />
      </div>
      <div className={css.footer}>
        <div className={css.footerEnergy}>
          <Thunder />
          <div className={css.energyCount}>
            <Power power={user?.power} />
          </div>
        </div>
        <div className={css.footerList}>
          <Link to="/fellows">
            <div
              className={`${css.fellows} ${location.pathname === '/fellows' ? css.active : ''}`}
            >
              <img
                src="img/fellows.png"
                alt="fellows"
                className={css.fellowsImg}
              />
              <p className={css.fellowsText}>Fellows</p>
            </div>
          </Link>
          <Link to="/tasks">
            <div
              className={`${css.build} ${location.pathname === '/' ? css.active : ''}`}
            >
              <img src="build.png" alt="build" className={css.buildImg} />
              <p className={css.buildText}>Build</p>
            </div>
          </Link>
          <Link to="/boost">
            <div
              className={`${css.boost} ${location.pathname === '/boost' ? css.active : ''}`}
            >
              <img src="boost.png" alt="boost" className={css.boostImg} />
              <p className={css.boostText}>Boost</p>
            </div>
          </Link>
        </div>
      </div>
      <Modal />
    </div>
  );
};
