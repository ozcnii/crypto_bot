import { Loader, Modal } from '@/components';
import { RootState } from '@/store';
import { getClanList } from '@/store/clanSlice';
import { openCreateClanModal } from '@/store/modalsSlice';
import { ThunkDispatch } from '@reduxjs/toolkit';
import { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { ClanListItem } from './clanListItem/clanListItem';
import css from './clans.module.css';

export const Clans = () => {
  const dispatch = useDispatch<ThunkDispatch<RootState, null, any>>();
  const { clans, clan, loading } = useSelector(
    (state: RootState) => state.clans,
  );
  const { user } = useSelector((state: RootState) => state.user);

  const handleOnClick = () => {
    dispatch(openCreateClanModal());
  };

  useEffect(() => {
    const fetchClanList = async () => {
      await dispatch(getClanList());
    };
    fetchClanList();
  }, []);
  return (
    <div className={css.main}>
      <div className={css.noClanLogo}>
        <img src="img/noClan.png" alt="noClan" className={css.noClan} />
      </div>
      <div className={css.title}>
        <h1>Clans</h1>
        <div className={css.inputWrapper}>
          <div className={css.inputLogo}>
            <img src="img/magnifier.png" alt="magnifier" />
          </div>
          <input type="text" placeholder="Search for a clan..." />
          <button className={css.arrowRight} type="button">
            <img src="img/arrowRight.svg" alt="arrowRight" />
          </button>
        </div>
        <p>
          Lorem ipsum dolor sit amet consectetur. Elementum lorem massa
          consectetur id scelerisque in egestas amet rhoncus.
        </p>
      </div>
      <div className={css.clansList}>
        <h1>Party Kings</h1>
        {loading ? (
          <Loader />
        ) : clans.length > 0 ? (
          clans.map((item, index) => <ClanListItem key={index} {...item} />)
        ) : (
          <div className={css.noClans}>
            <span>🐥</span>
            <p>No clans yet</p>
          </div>
        )}
      </div>
      {clan.admin !== user.chat_id && (
        <button
          type="button"
          className={css.floatingButton}
          onClick={handleOnClick}
        >
          Create your clan
        </button>
      )}
      <Modal />
    </div>
  );
};
