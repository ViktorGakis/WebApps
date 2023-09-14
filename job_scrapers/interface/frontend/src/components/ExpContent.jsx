import React, { useState } from "react";
import { FaExpandArrowsAlt } from "react-icons/fa";
import { IoContract } from "react-icons/io5";

function ExpContent({ summary, content }) {
	const [isExpanded, setIsExpanded] = useState(false);

	const toggleExpansion = () => {
		setIsExpanded(!isExpanded);
	};

	return (
		<div>
			<div onClick={toggleExpansion}>
				<div style={{ display: "flex" }}>
					{summary}
					<span style={{ cursor: "pointer" }}>
						{isExpanded ? <IoContract /> : <FaExpandArrowsAlt />}{" "}
					</span>
				</div>
			</div>
			{isExpanded && (
				<div>
					{typeof content === "string" ? (
						<div dangerouslySetInnerHTML={{ __html: content }} />
					) : (
						content
					)}
				</div>
			)}
		</div>
	);
}

export default ExpContent;
