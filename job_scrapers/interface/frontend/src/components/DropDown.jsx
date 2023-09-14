import { useState } from "react";

const DropdownButton = ({ options, onSelect }) => {
	const [isOpen, setIsOpen] = useState(false);
	const [selectedOption, setSelectedOption] = useState(null);

	const handleOptionSelect = (option) => {
		setSelectedOption(option);
		onSelect(option);
		setIsOpen(false);
	};

	return (
		<div className="dropdown">
			<button
				className="dropdown-toggle"
				onClick={() => setIsOpen(!isOpen)}
			>
				{selectedOption || "Select an option"}
			</button>
			{isOpen && (
				<ul className="dropdown-menu">
					{options.map((option) => (
						<li
							key={option}
							className="dropdown-item"
							onClick={() => handleOptionSelect(option)}
						>
							{option}
						</li>
					))}
				</ul>
			)}
		</div>
	);
};

export default DropdownButton;
