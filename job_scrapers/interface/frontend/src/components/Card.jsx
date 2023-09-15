import "./card.css";

function Card({ children, className = "", onClick }) {
	const cardClass = `card ${className}`.trim();

	return (
		<article className={cardClass} onClick={onClick}>
			{children}
		</article>
	);
}

export default Card;
