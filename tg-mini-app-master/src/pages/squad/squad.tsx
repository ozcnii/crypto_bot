import MainCoin from '@/assets/coins/coin';
import { LeaderBoardList } from '@/components/leaderBoardList';
import { RootState } from '@/store';
import {
  deleteUserClan,
  getClanById,
  getUserClan,
  joinUserClan,
  leaveUserClan,
} from '@/store/clanSlice';
import { getClanLeagueById } from '@/store/leagueSlice';
import { getByJWTUser } from '@/store/userSlice';
import { getIconPath } from '@/utils/getIcon';
import { ClanListUsers } from '@/utils/types/clan';
import { ThunkDispatch } from '@reduxjs/toolkit';
import { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useNavigate, useParams } from 'react-router';
import css from './squad.module.css';

export const Squad = () => {
  const dispatch = useDispatch<ThunkDispatch<RootState, null, any>>();
  const { user } = useSelector((state: RootState) => state.user);
  const { clanById, status, clan } = useSelector(
    (state: RootState) => state.clans,
  );
  const { clanLeague } = useSelector((state: RootState) => state.league);
  const [isDaily, setIsDaily] = useState(true);
  const [isAllTime, setIsAllTime] = useState(false);
  const [currentUser, setCurrentUser] = useState({} as ClanListUsers);
  const navigate = useNavigate();
  const { id } = useParams();

  useEffect(() => {
    const fetchClanData = async () => {
      const response = await dispatch(getClanById(id));
      if (getClanById.fulfilled.match(response)) {
        await dispatch(getClanLeagueById(response.payload.league_id));
      }
    };
    fetchClanData();
  }, [id, dispatch]);

  useEffect(() => {
    const fetchUserClan = async () => {
      await dispatch(getUserClan());
    };
    const fetchUserData = async () => {
      await dispatch(getByJWTUser());
    };
    fetchUserData();
    fetchUserClan();
  }, []);

  useEffect(() => {
    console.log(clan, user);
  }, []);

  const handleToggle = () => {
    setIsDaily(!isDaily);
    setIsAllTime(!isAllTime);
  };

  const deleteClan = async () => {
    await dispatch(deleteUserClan(clanById.link));
    navigate('/');
  };

  const joinClan = async () => {
    await dispatch(joinUserClan(clanById.id));
  };

  const leaveClan = async () => {
    await dispatch(leaveUserClan());
    navigate('/');
  };
  const usersList = [
    {
      id: 1,
      username: 'user1',
      avatar_url: 'img/ava.png',
      balance: 1000,
    },
    {
      id: 2,
      username: 'user2',
      avatar_url: 'img/ava.png',
      balance: 1000,
    },
    {
      id: 3,
      username: 'user3',
      avatar_url: 'img/ava.png',
      balance: 1000,
    },
  ];

  const avatars = clanById.usersList
    ?.slice(0, 3)
    .map((user, index) => (
      <img
        key={index}
        src={getIconPath(user.avatar_url) || 'img/ava.png'}
        alt={`Avatar ${index + 1}`}
        className={css.avatar}
      />
    ));

  useEffect(() => {
    setCurrentUser(
      clanById.usersList?.find((clan) => clan.name === user.username) ||
        ({} as ClanListUsers),
    );
  }, []);

  return (
    <div className={css.squadWrapper}>
      <header className={css.header}>
        <div className={css.playersCount}>
          <div className={css.avatars}>{avatars}</div>
          <span>{clanById.users} players</span>
        </div>
        <div className={css.clanLogoWrapper}>
          <img
            src={
              clanById.logo_url
                ? getIconPath(clanById.logo_url)
                : 'img/noClan.png'
            }
            alt="Clan Logo"
            className={css.clanLogo}
          />
        </div>
        <div className={css.clanNameContainer}>
          <h1 className={css.clanName}>{clanById.name}</h1>
          <a
            href={`https://${clanById.link}`}
            target="_blank"
            rel="noreferrer"
            className={css.link}
          >
            <img src="img/link.png" alt="Link" />
          </a>
        </div>
        <div className={css.blockContainer}>
          <div className={css.firstBlock}>
            <div className={css.firstBlockUpper}>
              <div className={css.scoreBlock}>
                <div className={css.logo}>
                  <MainCoin width={16} height={16} />
                </div>
                <div className={css.totalScore}>
                  <div className={css.score}>
                    {clanById?.balance?.toLocaleString('en-US')}
                  </div>
                  <p>Total Score</p>
                </div>
              </div>
            </div>
            <div className={css.firstBlockLower}></div>
          </div>
          <div className={css.secondBlock}>
            <div className={css.league}>
              <img
                src={`img/clanLogos/${clanLeague.name}.png`}
                alt={`${clanLeague.name} Logo`}
              />
              <p>{clanLeague.name} League</p>
            </div>
            <button
              type="button"
              className={
                user.id === clanById.owner_id
                  ? css.delete
                  : user.clan_id === clanById.id
                    ? css.leave
                    : css.join
              }
              onClick={
                clanById.owner_id === user.id
                  ? () => deleteClan()
                  : user.clan_id === clanById.id
                    ? () => leaveClan()
                    : () => joinClan()
              }
            >
              {clanById.owner_id === user.id
                ? 'Delete'
                : user.clan_id === clanById.id
                  ? 'Leave'
                  : 'Join'}
            </button>
          </div>
        </div>
        <div className={css.timeToggle}>
          <button
            type="button"
            className={isDaily ? css.active : css.inactive}
            onClick={handleToggle}
          >
            Daily
          </button>
          <button
            type="button"
            className={isAllTime ? css.active : css.inactive}
            onClick={handleToggle}
          >
            All time
          </button>
        </div>
      </header>
      <LeaderBoardList list={clanById.usersList} />
      {currentUser.name ? (
        <div className={css.floatingContainer}>
          <div className={css.floating}>
            <div className={css.avatar}>
              <img
                src={getIconPath(currentUser.avatar_url)}
                alt="Avatar"
                className={css.playerAvatar}
              />
            </div>
            <div className={css.aboutInfo}>
              <h1>
                {currentUser.name} <span>(You)</span>
              </h1>
              <p>1th</p>
            </div>
          </div>
          <div className={css.balance}>
            <img src="img/vector.svg" alt="Vector" className={css.vector1} />
            <p>{currentUser?.balance?.toLocaleString('de-DE')}</p>
          </div>
        </div>
      ) : null}
    </div>
  );
};
