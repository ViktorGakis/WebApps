import "bootstrap/dist/css/bootstrap.css";
import React, { useState } from "react";

export { QuestionComponent };

function QuestionComponent({ question }) {
	const { question: questionText, choices, img_url, img_path } = question;
	const [selectedOption, setSelectedOption] = useState(null);

	const handleOptionClick = (option, isCorrect) => {
		setSelectedOption(option);
	};

	return (
		<div className="question">
			<div className="title">
				<h3>{questionText}</h3>
			</div>
			<div className="img">
				{img_url && <img src={img_url} alt="Question Image" />}
			</div>
			<div className="choices">
				<ol>
					{Object.entries(choices).map(
						([option, isCorrect], index) => (
							<li
								key={index}
								onClick={() =>
									handleOptionClick(option, isCorrect)
								}>
								<div className="d-grid gap-2">
									<button
										type="button"
										className={`btn ${
											selectedOption === option
												? isCorrect
													? "btn-outline-success"
													: "btn-outline-danger"
												: "btn-dark"
										}`}>
										{option}
									</button>
								</div>
							</li>
						)
					)}
				</ol>
			</div>
		</div>
	);
}
