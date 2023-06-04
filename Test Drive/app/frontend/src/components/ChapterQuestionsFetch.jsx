import "bootstrap/dist/css/bootstrap.css";
import React, { useState, useEffect } from "react";
import { FormSelect } from "./formselect";
import { fetchChapters, fetchChapterQuestions } from "../js/app_specifics";
import { QuestionComponent } from "./questionComponent";


export { FormFetchQuestions };


function FormFetchQuestions() {
	const fetchChaptersData = async () => {
		const chapterData = await fetchChapters();
		return chapterData;
	};

	const [chapters, setChapters] = useState([]);
	const [questionComponents, setQuestionComponents] = useState(null);

	const handleSubmit = async (e, selectedOption) => {
		e.preventDefault();
		console.log("Selected option:", selectedOption);

		try {
			let rsp = await fetchChapterQuestions(selectedOption);
			console.log("rsp:", rsp);

			let response = rsp.data[0]; // Access the first element of the questions list
			console.log("Questions:", response);

			// Create an array of QuestionComponent elements
			const components = response.map((question, index) => (
				<QuestionComponent key={index} question={question} />
			));

			// Set the QuestionComponent elements in the state
			setQuestionComponents(components);
		} catch (error) {
			console.log("Error:", error.message);
		}
	};

	useEffect(() => {
		const fetchData = async () => {
			try {
				const data = await fetchChaptersData();
				setChapters(data);
			} catch (error) {
				console.error("Error fetching chapters:", error);
			}
		};

		fetchData();
	}, []);

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
			{/* Render the QuestionComponent elements */}
			{questionComponents && (
				<div className="questions">{questionComponents}</div>
			)}
		</div>
	);
}

export default FormFetchQuestions;
