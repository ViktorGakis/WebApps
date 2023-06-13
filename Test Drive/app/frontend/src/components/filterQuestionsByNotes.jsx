import { fetchAPI } from "../js/utils";
import React, { useEffect, useState } from "react";
import { DisplayQuestionSection } from "./questionSection";

async function fetchData(endpoint, params, payload, method) {
	return await fetchAPI(endpoint.toString(), params, payload, method);
}

// Main component.
export function QuestionsFromNotes({ endpoint }) {
	const [questions, setQuestions] = useState([]);
	const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
	const [answeredQuestions, setAnsweredQuestions] = useState(
		Array(questions.length).fill(false)
	);
	const [correctAnswers, setCorrectAnswers] = useState(
		Array(questions.length).fill(false)
	);
	const [formKey, setFormKey] = useState(0); // Add formKey state
	const [inputValue, setInputValue] = useState("");
	const [loading, setLoading] = useState(false);

	const handleSubmit = async (e) => {
		e.preventDefault();
		setLoading(true);

		try {
			const payload = { data: inputValue };
			const response = await fetchData(endpoint, {}, payload, "POST");
			setQuestions(response.data);
		} catch (error) {
			console.error("Error:", error);
		} finally {
			setLoading(false);
		}
	};

	useEffect(() => {
		// console.log("questions (inside useEffect): ", questions);
	}, [questions]); // Watch for changes in the questions state

	const handleFormSubmit = function (e) {
		handleSubmit(e);
		setAnsweredQuestions(Array(questions.length).fill(false));
		setCorrectAnswers(Array(questions.length).fill(false));
		setFormKey((prevKey) => prevKey + 1); // Update formKey on form submit
		setCurrentQuestionIndex(1);
	};

	return (
		<div>
			<h1>Retrieve questions from notes</h1>
			<div id="form-container">
			<form className="form button-container" onSubmit={handleFormSubmit}>
				<input
					type="text"
					value={inputValue}
					onChange={(e) => setInputValue(e.target.value)}
				/>
				<button className="btn btn-primary" type="submit">
					Submit
				</button>
			</form>
			</div>
			{loading ? (
				<div>Loading...</div>
			) : questions ? (
				<div>
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
			) : null}
		</div>
	);
}
