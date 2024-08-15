const Button = ({ color, onClick }: { color: string, onClick: () => void }) => {
	return (
		<svg width="7" height="12" viewBox="0 0 7 12" fill="none" xmlns="http://www.w3.org/2000/svg" onClick={onClick}>
			<path d="M0.875 1L6 6.125L0.875 11.25" stroke={color} strokeWidth="0.5"/>
		</svg>
	)
}

export default Button