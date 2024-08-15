import MainCoin from '@/assets/coins/coin'
import { RootState } from '@/store'
import { getUserLeague } from '@/store/leagueSlice'
import { ThunkDispatch } from '@reduxjs/toolkit'
import { useEffect } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { useNavigate } from 'react-router'
import { Link } from 'react-router-dom'
import css from './header.module.css'

export const Header = () => {
  const dispatch = useDispatch<ThunkDispatch<RootState, null, any>>()
  const { user } = useSelector((state: RootState) => state.user)
  const { clan, status, error, loading } = useSelector((state: RootState) => state.clans)
  const { userLeague, clanLeague } = useSelector((state: RootState) => state.league)
  const navigate = useNavigate()

  const handleOnClick = () => {
    if (!loading) {
      if (status === '404' && error === 'Clan not found') {
        navigate('/clans')
      } else {
        navigate(`/clans/${clan.id}`)
      }
    }
  }

  useEffect(() => {
    const fetchUserLeague = async () => {
      await dispatch(getUserLeague())
    }
    fetchUserLeague()
  }, [])

  return (
    <header className={css.wrapper}>
      <div className={css.info}>
        <Link to={`/league`}>
          <img src={user.avatar_url} alt="аватар" className={css.avatar} />
        </Link>
        <div className={css.statistics}>
          {user.balance ? <p className={css.balance}>{user.balance.toLocaleString('en-US')}</p> : <p className={css.balance}>0</p>}
          <div className={css.divider}>
            <div className={css.league}>
              {userLeague && <img src={`img/leagueLogos/${userLeague.name}.png`} alt="лого лиги" className={css.leagueLogo} />}
              <span className={css.leagueName}>{userLeague ? userLeague.name : 'No'} League</span>
            </div>
            <p className={css.pnl}>P&L: {user.p_n_l ? <span className={user.p_n_l > 0 ? css.green : css.red}>{user.p_n_l > 0 ? `+${user.p_n_l}` : user.p_n_l}</span> : '0'}</p> 
          </div>
        </div>
      </div>
      <div className={css.clan} onClick={handleOnClick}>
        {clan.logo_url ? <img src={clan.logo_url} alt="лого клана" className={css.clanLogo} /> : 
          (
            <div className={css.noClanLogo}>
              <img src="img/noClan.png" alt="лого клана" className={css.noClanLogoImg} />
            </div>
          )
        }
        <div className={css.clanInfo}>
          <p className={css.clanName}>{clan.name ? clan.name : 'No clan yet'}</p>
          <div className={css.clanStatistics}>
            <p className={css.clanBalance}> 
              {/* <div className={css.clanBalanceIcon}>
                <img src="img/clanBalance.svg" alt="баланс клана" className={css.clanBalanceLogo} />
                <img src="img/clanBalanceVector.svg" alt="вектор баланса" className={css.clanBalanceVector} />
              </div> */}
              <MainCoin height={8} width={8} />
              <span className={css.clanBalanceValue}>
                {clan.balance != null 
                  ? clan.balance 
                  : <div className={css.noClanBalance}></div>
                }
              </span>
            </p>
            <p className={css.clanLeague}>
              <img src={clanLeague.name ? `img/clanLogos/${clanLeague.name}.png` : 'img/clanLogos/Gold.png'} alt="лого лиги" className={css.clanLeagueLogo} />
              <span className={css.clanLeagueName}>{clanLeague.name ? clanLeague.name + ' League' : <div className={css.noClanLeague}></div>}</span>
            </p>
          </div>
        </div>
      </div>
    </header>
  )
}
