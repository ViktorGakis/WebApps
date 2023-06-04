import React from "react";
import { QuestionComponent } from "./questionComponent";

// export { QuestionSection, displayQuestionSection };

// function QuestionSection({
// 	currentQuestionIndex,
// 	loadedQuestions,
// 	question,
// 	setCurrentQuestionIndex,
// }) {
// 	const handleNextQuestion = () => {
// 		if (currentQuestionIndex < loadedQuestions) {
// 			setCurrentQuestionIndex((prevIndex) => prevIndex + 1);
// 		}
// 	};

// 	const handlePreviousQuestion = () => {
// 		if (currentQuestionIndex > 1) {
// 			setCurrentQuestionIndex((prevIndex) => prevIndex - 1);
// 		}
// 	};

// 	return (
// 		<div className="questions">
// 			<p>
// 				{currentQuestionIndex}/{loadedQuestions}
// 			</p>
// 			<div className="question-nav">
// 				<button
// 					onClick={handlePreviousQuestion}
// 					disabled={currentQuestionIndex === 1}>
// 					Previous
// 				</button>

// 				<button
// 					onClick={handleNextQuestion}
// 					disabled={currentQuestionIndex === loadedQuestions}>
// 					Next
// 				</button>
// 			</div>
// 			<QuestionComponent question={question} />
// 		</div>
// 	);
// }

// // Display the question section if questions are available.
// function displayQuestionSection(
// 	questions,
// 	currentQuestionIndex,
// 	setCurrentQuestionIndex
// ) {
// 	if (
// 		questions.length > 0 &&
// 		currentQuestionIndex >= 1 &&
// 		currentQuestionIndex <= questions.length
// 	) {
// 		return (
// 			<QuestionSection
// 				currentQuestionIndex={currentQuestionIndex}
// 				loadedQuestions={questions.length}
// 				setCurrentQuestionIndex={setCurrentQuestionIndex}
// 				question={questions[currentQuestionIndex - 1]}
// 			/>
// 		);
// 	}
// 	return null;
// }

function countTrueValues(array) {
	return array.filter(Boolean).length;
}

function QuestionSection({
	currentQuestionIndex,
	loadedQuestions,
	question,
	setCurrentQuestionIndex,
	answeredQuestions,
	setAnsweredQuestions,
	correctAnswers,
	setCorrectAnswers,
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

	const handleAnswer = (isCorrect) => {
		// This function is passed down to the QuestionComponent
		// and is called every time a choice is clicked.

		// When called, it updates the answeredQuestions and correctAnswers state
		// at the index of the current question to reflect the user's most recent choice.

		const newAnsweredQuestions = [...answeredQuestions];
		newAnsweredQuestions[currentQuestionIndex - 1] = true;
		setAnsweredQuestions(newAnsweredQuestions);

		const newCorrectAnswers = [...correctAnswers];
		newCorrectAnswers[currentQuestionIndex - 1] = isCorrect;
		setCorrectAnswers(newCorrectAnswers);
	};

	return (
		<div className="questions">
			<QuestionComponent question={question} onAnswer={handleAnswer} />
			<div className="button-container">
				<button
					className="btn btn-primary stretch-button"
					onClick={handlePreviousQuestion}
					disabled={currentQuestionIndex === 1}>
					<span className="enlarged-symbol">&laquo;</span>
				</button>
				<button
					className="btn btn-primary stretch-button"
					onClick={handleNextQuestion}
					disabled={currentQuestionIndex === loadedQuestions}>
					<span className="enlarged-symbol">&raquo;</span>
				</button>
			</div>
			<span>
				{currentQuestionIndex}/{loadedQuestions}
			</span>
			<div>
				<span className="correct">
					{countTrueValues(correctAnswers)}
				</span>
				/<span>{countTrueValues(answeredQuestions)}</span>
			</div>
            <div className="notes">
                <textarea contentEditable="true" className="stretch"></textarea>
            </div>
		</div>
	);
}

// Display the question section if questions are available.
function displayQuestionSection(
	questions,
	currentQuestionIndex,
	setCurrentQuestionIndex,
	answeredQuestions,
	setAnsweredQuestions,
	correctAnswers,
	setCorrectAnswers
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
				answeredQuestions={answeredQuestions}
				setAnsweredQuestions={setAnsweredQuestions}
				correctAnswers={correctAnswers}
				setCorrectAnswers={setCorrectAnswers}
			/>
		);
	}
	return null;
}

export { displayQuestionSection };
