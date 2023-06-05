import "bootstrap/dist/css/bootstrap.css";
import React, { useState } from "react";
import { transformImagePath } from "../js/app_specifics";

export { QuestionComponent };

function QuestionComponent({ question, onAnswer }) {
	const { question: questionText, choices, img_url, img_path } = question;
	const [selectedOption, setSelectedOption] = useState(null);

	const handleOptionClick = (option, isCorrect) => {
		setSelectedOption(option);

		// The onAnswer function is called here every time a choice is clicked.
		// This allows the QuestionForm component to update answeredQuestions
		// and correctAnswers based on the user's selections.
		onAnswer(isCorrect);
	};

	return (
		<div className="question">
			<div className="title">
				<h3>{questionText}</h3>
			</div>
			<div className="img">
				{img_path && (
					<img
						src={transformImagePath(img_path)}
						alt="Question Image"
					/>
				)}
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
													? "btn-success"
													: "btn-danger"
												: "btn-secondary"
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
