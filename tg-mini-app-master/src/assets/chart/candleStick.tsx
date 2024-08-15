
const CandleStick = ({ fill }: { fill: string }) => {
	return (
		<svg width="15" height="13" viewBox="0 0 15 13" fill="none" xmlns="http://www.w3.org/2000/svg">
		<rect x="0.5" y="3.5" width="2" height="8.75" rx="0.25" fill={fill} />
		<rect x="13" y="3.5" width="2" height="8.75" rx="0.25" fill={fill}/>
		<rect x="3.5" width="2" height="5.75" rx="0.25" fill={fill}/>
		<rect x="6.5" y="5.25" width="2" height="5" rx="0.25" fill={fill}/>
		<rect x="9.5" y="1.25" width="2" height="7.5" rx="0.25" fill={fill}/>
		</svg>
	)
}

export default CandleStick