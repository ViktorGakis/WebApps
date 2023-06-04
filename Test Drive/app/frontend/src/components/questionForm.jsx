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

	return (
		<div>
			{chapters.length > 0 ? (
				<FormSelect
					data={chapters}
					url="api/chapter/questions"
					method="GET"
					handleSubmit={handleSubmit}
				/>
			) : (
				<div>Loading...</div>
			)}
			{displayQuestionSection(
				questions,
				currentQuestionIndex,
				setCurrentQuestionIndex
			)}
		</div>
	);
}
