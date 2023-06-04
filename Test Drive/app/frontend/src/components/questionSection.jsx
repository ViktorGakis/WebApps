import React from "react";
import { QuestionComponent } from "./questionComponent";

export { QuestionSection, displayQuestionSection };

function QuestionSection({
	currentQuestionIndex,
	loadedQuestions,
	question,
	setCurrentQuestionIndex,
}) {
	const handleNextQuestion = () => {
		if (currentQuestionIndex < loadedQuestions) {
			setCurrentQuestionIndex((prevIndex) => prevIndex + 1);
		}
	};

	const handlePreviousQuestion = () => {
		if (currentQuestionIndex > 1) {
			setCurrentQuestionIndex((prevIndex) => prevIndex - 1);
		}
	};

	return (
		<div className="questions">
			<p>
				{currentQuestionIndex}/{loadedQuestions}
			</p>
			<div className="question-nav">
				<button
					onClick={handlePreviousQuestion}
					disabled={currentQuestionIndex === 1}>
					Previous
				</button>

				<button
					onClick={handleNextQuestion}
					disabled={currentQuestionIndex === loadedQuestions}>
					Next
				</button>
			</div>
			<QuestionComponent question={question} />
		</div>
	);
}

// Display the question section if questions are available.
function displayQuestionSection(
	questions,
	currentQuestionIndex,
	setCurrentQuestionIndex
) {
	if (
		questions.length > 0 &&
		currentQuestionIndex >= 1 &&
		currentQuestionIndex <= questions.length
	) {
		return (
			<QuestionSection
				currentQuestionIndex={currentQuestionIndex}
				loadedQuestions={questions.length}
				setCurrentQuestionIndex={setCurrentQuestionIndex}
				question={questions[currentQuestionIndex - 1]}
			/>
		);
	}
	return null;
}
