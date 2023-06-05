import React, { useEffect, useState } from "react";
import { FormSelect } from "./formSelect";
import { DisplayQuestionSection } from "./questionSection";
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
	const [answeredQuestions, setAnsweredQuestions] = useState(
		Array(questions.length).fill(false)
	);
	const [correctAnswers, setCorrectAnswers] = useState(
		Array(questions.length).fill(false)
	);

	const [formKey, setFormKey] = useState(0); // Add formKey state

	useEffect(() => {
		fetchChapterData(setChapters);
	}, []);

	const handleSubmit = function (e, selectedOption) {
		e.preventDefault();
		handleChapterQuestionFetch(
			selectedOption,
			setQuestions,
			setCurrentQuestionIndex
		);
	};

	const handleFormSubmit = function (e, selectedOption) {
		handleSubmit(e, selectedOption);
		setAnsweredQuestions(Array(questions.length).fill(false));
		setCorrectAnswers(Array(questions.length).fill(false));
		setFormKey((prevKey) => prevKey + 1); // Update formKey on form submit
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
						handleSubmit={handleFormSubmit} // Modified to use handleFormSubmit
						id={'questionForm'}
					/>
				</div>
			) : (
				<div>Loading...</div>
			)}
			<hr></hr>
			{DisplayQuestionSection(
				questions,
				currentQuestionIndex,
				setCurrentQuestionIndex,
				answeredQuestions,
				setAnsweredQuestions,
				correctAnswers,
				setCorrectAnswers,
				formKey // Pass formKey as a prop to DisplayQuestionSection
			)}
		</div>
	);
}
