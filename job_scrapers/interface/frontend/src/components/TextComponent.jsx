import { useState, useEffect } from "react";

function TextComponent({ text, isExpanded, limit = 50 }) {
	const [expanded, setExpanded] = useState(isExpanded);

	useEffect(() => {
		setExpanded(isExpanded);
	}, [isExpanded]);

	const handleExpand = () => {
		setExpanded(!expanded);
	};

	const shouldTruncate = text.length > limit;
	const truncatedText =
		shouldTruncate && !expanded ? `${text.slice(0, limit)}...` : text;

	// console.log("TextComponent: expanded:", expanded);

	return (
		<div
			className={`container__text ${expanded ? "expanded" : ""}`}
			onClick={handleExpand}
		>
			{truncatedText}
		</div>
	);
}

export default TextComponent;
