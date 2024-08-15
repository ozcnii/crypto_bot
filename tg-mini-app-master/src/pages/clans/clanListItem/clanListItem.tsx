import { ClanList } from '@/utils/types/clan'
import { FC } from 'react'
import { useNavigate } from 'react-router'
import css from './clanListItem.module.css'

export const ClanListItem: FC<ClanList> = ({ id, name, logo_url, league }) => {
	const navigate = useNavigate()

	return (
		<div className={css.clanListItem} onClick={() => navigate(`/clans/${id}`)}>
			<div className={css.logoContainer}>
				<img src={logo_url ? logo_url : 'img/noClan.png'} alt="clanLogo" className={css.logo} />
			</div>
			<div className={css.clanInfo}>
				<div className={css.clanName}>{name}</div>
				<span className={css.league}>
					<p>{league}</p>
					<img src={`img/clanLogos/${league}.png`} alt="clanLeague" />
				</span>
			</div>
			<button className={css.arrowRight} type="button"><img src='img/arrowRight.svg' alt='arrowRight' /></button>
		</div>
	)
}