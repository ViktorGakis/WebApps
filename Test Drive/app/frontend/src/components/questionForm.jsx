import React, { useEffect, useState } from "react";
import { FormSelect } from "./formSelect";
import { displayQuestionSection } from "./questionSection";
import {
	fetchChapterData,
	handleChapterQuestionFetch,
} from "../js/app_specifics";

export { QuestionForm };

// Main component.
function QuestionForm() {
	const [chapters, setChapters] = useState([]);
	const [questions, setQuestions] = useState([]);
	const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
	const [answeredQuestions, setAnsweredQuestions] = useState(Array(questions.length).fill(false));
	const [correctAnswers, setCorrectAnswers] = useState(Array(questions.length).fill(false));

	useEffect(() => {
		fetchChapterData(setChapters);
	}, []);

	useEffect(() => {
		setAnsweredQuestions(Array(questions.length).fill(false));
		setCorrectAnswers(Array(questions.length).fill(false));
	}, [questions]);

	const handleSubmit = function (e, selectedOption) {
		e.preventDefault();
		handleChapterQuestionFetch(
			selectedOption,
			setQuestions,
			setCurrentQuestionIndex
		);
	};

	return (
		<div id="main">
			<h1>Choose Chapter</h1>		
			{chapters.length > 0 ? (
				<div id="form-container">
					<FormSelect
						data={chapters}
						url="api/chapter/questions"
						method="GET"
						handleSubmit={handleSubmit}
					/>
				</div>
			) : (
				<div>Loading...</div>
			)}
			<hr></hr>
			{displayQuestionSection(
				questions,
				currentQuestionIndex,
				setCurrentQuestionIndex,
				answeredQuestions,
				setAnsweredQuestions,
				correctAnswers,
				setCorrectAnswers
			)}
		</div>
	);
}
