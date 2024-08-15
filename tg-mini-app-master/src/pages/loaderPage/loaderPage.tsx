import css from './loaderPage.module.css'

export const LoaderPage = () => {
	return (
		<div className={css.container}>
			<svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg" className={css.spinner}>
			<path fillRule="evenodd" clipRule="evenodd" d="M8 2C4.66375 2 2 4.66375 2 8C2 11.3363 4.66375 14 8 14C11.3363 14 14 11.3363 14 8C14 4.66375 11.3363 2 8 2ZM0 8C0 3.58172 3.58172 0 8 0C12.4183 0 16 3.58172 16 8C16 12.4183 12.4183 16 8 16C3.58172 16 0 12.4183 0 8Z" fill="white" className={css.track} />
			<path fillRule="evenodd" clipRule="evenodd" d="M14 8C14 4.68629 11.3137 2 8 2V0C12.4183 0 16 3.58172 16 8H14Z" fill="#276EF1" className={css.rotate} />
		</svg>
	</div>
	);
}