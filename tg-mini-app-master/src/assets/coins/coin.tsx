const MainCoin = ({ width, height }: { width: number, height: number }) => {
	return (
		<svg width={width} height={height} viewBox="0 0 10 10" fill="none" xmlns="http://www.w3.org/2000/svg">
			<circle cx="5.25" cy="5.25" r="4.5" fill="url(#paint0_linear_25_1682)" stroke="url(#paint1_linear_25_1682)" strokeWidth="0.5"/>
			<path fillRule="evenodd" clipRule="evenodd" d="M6.65377 3.40438H3.17749V2.97009H7.53021L7.53021 7.53009H7.11567V3.806C5.6314 3.85705 4.71602 4.45653 4.1636 5.18397C3.57874 5.95412 3.38476 6.88937 3.38476 7.53009H2.97021C2.97022 6.81367 3.18387 5.77654 3.83919 4.91359C4.41154 4.15992 5.30902 3.55504 6.65377 3.40438Z" fill="#EEEEEE"/>
			<defs>
				<linearGradient id="paint0_linear_25_1682" x1="0.5" y1="0.5" x2="10" y2="10" gradientUnits="userSpaceOnUse">
					<stop stopColor="#948AFF"/>
					<stop offset="1" stopColor="#040033"/>
				</linearGradient>
				<linearGradient id="paint1_linear_25_1682" x1="0.5" y1="0.5" x2="10.3752" y2="0.907447" gradientUnits="userSpaceOnUse">
					<stop stopColor="#EEEEEE" stopOpacity="0.6"/>
					<stop offset="1" stopColor="#EEEEEE" stopOpacity="0.2"/>
				</linearGradient>
			</defs>
		</svg>
	)
}

export default MainCoin