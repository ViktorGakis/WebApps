import { fetchAPI } from "./utils";

export { fetchChapterQuestions, fetchChapters, fetchChapterData, handleChapterQuestionFetch };

async function fetchChapters() {
	return await fetchAPI("api/chapters");
}

async function fetchChapterQuestions(chapter) {
	return await fetchAPI("api/chapter/questions", { chapter: chapter });
}

// Fetch chapters data and set the chapters state.
async function fetchChapterData(setChapters) {
	try {
		const data = await fetchChapters();
		setChapters(data);
	} catch (error) {
		console.error("Error fetching chapters:", error);
	}
}

// Fetch selected chapter questions and set the questions and currentQuestionIndex state.
async function handleChapterQuestionFetch(
	selectedOption,
	setQuestions,
	setCurrentQuestionIndex
) {
	try {
		let rsp = await fetchChapterQuestions(selectedOption);
		let response = rsp.data[0];
		setQuestions(response);
		setCurrentQuestionIndex(1);
	} catch (error) {
		console.log("Error:", error.message);
	}
}
