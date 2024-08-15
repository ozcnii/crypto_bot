import MainCoin from '@/assets/coins/coin'
import NotFound from '@/assets/notFound'
import { ClanListUsers } from '@/utils/types/clan'
import { Clan, User } from '@/utils/types/league'
import css from './leaderBoardList.module.css'

interface LeaderBoardListProps {
	list: User[] | Clan[] | ClanListUsers[]
}

export const LeaderBoardList = ({ list }: LeaderBoardListProps) => {
  const top = {
    '1': '🥇',
    '2': '🥈',
    '3': '🥉'
  }
	return (
		<div className={`${css.leaderBoard} ${list?.length > 0 ? '' : css.noLeaders}`}>
      {list?.length > 0 ? (
        list?.map((player, index) => (
          <div key={index} className={css.player}>
            <div className={css.rankInfo}>
              <span className={css.rank}>{top[index + 1] || index + 1}</span>
              <div className={css.avatar}>
                <img src={player.avatar_url} alt="Avatar" className={css.avatarImg} />
              </div>
            </div>
            <div className={css.balanceInfo}>
              <span className={css.playerName}>{player.name}</span>
              <span className={css.playerScore}><MainCoin width={10} height={10} />{player.balance.toLocaleString('de-DE')}</span>
            </div>
          </div>
        ))
      ) : (
        <div className={css.noInfo}>
					<NotFound />
					<p>No clans yet</p>
				</div>
      )} 
    </div>
	)
}