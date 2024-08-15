import { LeaderBoardList } from '@/components/leaderBoardList'
import { RootState } from '@/store'
import { getLeagueByName, getLeagueClans, getLeagueUsers, getUserLeagueById } from '@/store/leagueSlice'
import { getByJWTUser } from '@/store/userSlice'
import { ThunkDispatch } from '@reduxjs/toolkit'
import { useEffect, useState } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import css from './league.module.css'

const capitalizeFirstLetter = (string: string) => {
  return string?.charAt(0)?.toUpperCase() + string?.slice(1);
};

const leagues = ["Bronze", "Silver", "Gold", "Diamond"];

export const League = () => {
  const dispatch = useDispatch<ThunkDispatch<RootState, unknown, any>>();
  const [background, setBackground] = useState('');
  const { user } = useSelector((state: RootState) => state.user);
  const { userLeague, users_list, clans_list} = useSelector((state: RootState) => state.league)
  const [progress, setProgress] = useState(0);
  const [isMiners, setIsMiners] = useState(true);
  const [isSquads, setIsSquads] = useState(false);
  const [currentLeague, setCurrentLeague] = useState(userLeague.name);
  const [animating, setAnimating] = useState(false);
  const [animationDirection, setAnimationDirection] = useState('');
  const [currentUser, setCurrentUser] = useState(user);

  useEffect(() => {
    const fetchUserData = async () => {
      const userData = await dispatch(getByJWTUser());
      if (getByJWTUser.fulfilled.match(userData)) {
        await dispatch(getUserLeagueById(userData.payload.league_id));
        setProgress((userData.payload.balance / 100000) * 100);
      }
    };
    fetchUserData();
  }, [dispatch]);

  useEffect(() => {
    const fetchLeagueData = async () => {
      await dispatch(getLeagueByName(currentLeague));
    }

    fetchLeagueData();
  }, [currentLeague, dispatch]);

  useEffect(() => {
    const fetchLeagueUsers = async () => {
      await dispatch(getLeagueUsers(currentLeague));
    }
    const fetchLeagueClans = async () => {
      await dispatch(getLeagueClans(currentLeague));
    }

    fetchLeagueUsers();
    fetchLeagueClans();
  }, [currentLeague, dispatch])

	const capitalizedLeagueName = capitalizeFirstLetter(currentLeague);

  useEffect(() => {
    const capitalizedLeagueName = capitalizeFirstLetter(currentLeague);
    const imagePath = `/img/backgrounds/${capitalizedLeagueName}.svg`;
    setBackground(imagePath);
  }, [currentLeague]);

  const handleToggle = () => {
    setIsMiners(!isMiners);
    setIsSquads(!isSquads);
  };

  const handleNextLeague = () => {
    const currentIndex = leagues.indexOf(currentLeague);
    if (currentIndex < leagues.length - 1) {
      setAnimating(true);
      setAnimationDirection('left');
      setTimeout(() => {
        setCurrentLeague(leagues[currentIndex + 1]);
        setAnimating(false);
      }, 300); // Длительность анимации должна совпадать с CSS transition
    }
  };

  const handlePreviousLeague = () => {
    const currentIndex = leagues.indexOf(currentLeague);
    if (currentIndex > 0) {
      setAnimating(true);
      setAnimationDirection('right')
      setTimeout(() => {
        setCurrentLeague(leagues[currentIndex - 1]);
        setAnimating(false);
      }, 300); // Длительность анимации должна совпадать с CSS transition
    }
  };

  const avatars = users_list?.slice(0, 3).map((user, index) => (
    <img
      key={index}
      src={user.avatar_url || 'img/ava.png'}
      alt={`Avatar ${index + 1}`}
      className={css.avatar}
    />
  ));

  useEffect(() => {
    setCurrentUser(users_list?.find((u) => u.id === user.id));
  }, [users_list, user.username]);

	return (
		<div className={css.main} style={{ backgroundImage: `url(${background})`, backgroundSize: 'cover', backgroundPosition: 'center', backgroundRepeat: 'no-repeat' }}>
			<div className={css.playersCount}>
        <div className={css.avatars}>
          {avatars}
        </div>
        <span>{userLeague.user_count} players</span>
      </div>
			<div className={`${css.leagueLogo} ${animating ? (animationDirection === 'left' ? css['logo-exit-left'] : css['logo-exit-right']) : ''}`}>
        <img src={`/img/clanLogos/${capitalizedLeagueName}.png`} alt="League Logo" className={animating ? (animationDirection === 'left' ? css['logo-enter-left'] : css['logo-enter-right']) : ''} />
      </div>
			<h1 className={css.title}>{capitalizedLeagueName} League</h1>
			<div className={css.leagueInfo}>
				<div className={css.countPlayers}>{user.balance} / 100k</div>
				<div className={css.progressContainer}>
					<div className={css.progressBar} style={{ width: `${progress}%` }}></div>
				</div>
			</div>
			<div className={css.buttons}>
				<button type="button" className={isMiners ? css.active : css.inactive} onClick={handleToggle}>Miners</button>
				<button type="button" className={isSquads ? css.active : css.inactive} onClick={handleToggle}>Squads</button>
			</div>
			<LeaderBoardList list={isMiners ? users_list : clans_list} />
			{currentUser && (
        <div className={css.floatingContainer}>
          <div className={css.floating}>
            <div className={css.avatar}>
              <img src={user.avatar_url} alt="Avatar" />
            </div>
            <div className={css.aboutInfo}>
              <h1>{user.username} <span>(You)</span></h1>
              <p>1th</p>
            </div>
          </div>
          <div className={css.balance}>
            <img src="img/vector.svg" alt="Vector" className={css.vector1} />
            <p>{user.balance?.toLocaleString('de-DE')}</p>
          </div>
        </div>
      )}
			<div className={`${css.arrowLeft} ${currentLeague === 'Bronze' ? css.disabled : ''}`} onClick={handlePreviousLeague}>
				<img src="img/arrowLeft.svg" alt="Arrow Left" />
			</div>
			<div className={`${css.arrowRight} ${currentLeague === 'Diamond' ? css.disabled : ''}`} onClick={handleNextLeague}>
				<img src="img/arrowRight.svg" alt="Arrow Right" />
			</div>
		</div>
	)
}