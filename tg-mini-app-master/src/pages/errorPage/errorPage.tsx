import css from './errorPage.module.css'
export const ErrorPage = () => {
	return (
		<div className={css.container}>
			<h1>404</h1>
			<p>User not found or service is not available</p>
		</div>
	)
}