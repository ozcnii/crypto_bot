import MainCoin from '@/assets/coins/coin'
import Completed from '@/assets/task/complete'
import { RootState } from '@/store'
import { completeUserTask, getUserTasks } from '@/store/tasksSlice'
import { ThunkDispatch } from '@reduxjs/toolkit'
import { useEffect } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { useNavigate } from 'react-router-dom'
import css from './tasks.module.css'

export const Tasks = () => {
	const dispatch = useDispatch<ThunkDispatch<RootState, null, any>>()
	const { tasks } = useSelector((state: RootState) => state.tasks)
	const navigate = useNavigate()

	const taskTypes = {
		'earn_coins': '💴',
		'invite_friends': '👥',
		'join_squad': '⛺'
	}
	
	useEffect(() => {
		const fetchTasksList = async () => {
			await dispatch(getUserTasks())
		}

		fetchTasksList()
	}, [])

	const completeTasksHandle = async (taskId: number) => {
		await dispatch(completeUserTask(taskId))
	}

	return (
		<div className={css.container}>
			<div className={css.content}>
				<h1>Earn more</h1>
				<p>Lorem ipsum dolor sit amet consectetur. Elementum lorem massa consectetur id scelerisque in egestas amet rhoncus.</p>
			</div>
			<div className={css.inviter}>
				<div className={css.clanListItem} onClick={() => navigate('/fellows')}>
					<div className={css.logoContainer}>
						👤 
					</div> 
					<div className={css.clanInfo}>
						<div className={css.clanName}>Invite friends</div>
						<span className={css.league}>
							<p>up to 100k</p>
							<MainCoin height={10} width={10} />
						</span>
					</div>
					<button className={css.arrowRight} type="button"><img src='img/arrowRight.svg' alt='arrowRight' /></button>
				</div>
			</div>
			<div className={css.tasks}>
				<h1>Tasks</h1>
				{tasks?.map((task) => (
					<div className={`${css.task} ${task.completed ? css.taskCompleted : ''}`} key={task.id} onClick={() => completeTasksHandle(task.id)}>
						<div className={css.logoContainer}>
							{taskTypes[task.task_type]}
						</div>
						<div className={css.taskInfo}>
							<h2>{task.name}</h2>
							<span>
								<p>+{task.reward}</p>
								<MainCoin height={10} width={10} />
							</span>
						</div>
						{task.completed ? <Completed /> : <button className={css.arrowRight} type="button"><img src='img/arrowRight.svg' alt='arrowRight' /></button>}
					</div>
				))}
			</div>
		</div> 
	)
}