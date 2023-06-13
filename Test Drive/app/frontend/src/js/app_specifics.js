import { fetchAPI } from "./utils";

export {
	fetchChapterItems,
	fetchChapters,
	fetchChapterData,
	handleChapterQuestionFetch,
	transformImagePath,
	handleChapterRoadSignsFetch,
};

async function fetchChapters(chapter_type) {
	if (chapter_type === "quiz") {
		return await fetchAPI("/api/chapters/quiz");
	} else if (chapter_type === "roadsigns") {
		return await fetchAPI("/api/chapters/roadsigns");
	}
}

async function fetchChapterItems(chapter, chapter_type) {
	if (chapter_type === "quiz") {
		return await fetchAPI("/api/chapters/quiz/questions", {
			chapter: chapter,
		});
	} else if (chapter_type === "roadsigns") {
		return await fetchAPI("/api/chapters/roadsigns/signs", {
			chapter: chapter,
		});
	}
}

// Fetch chapters data and set the chapters state.
async function fetchChapterData(setChapters, chapter_type) {
	try {
		const data = await fetchChapters(chapter_type);
		setChapters(data);
	} catch (error) {
		console.error("Error fetching chapters:", error);
	}
}

// Fetch selected chapter questions and set the questions and currentQuestionIndex state.
async function handleChapterRoadSignsFetch(selectedOption, setQuestions) {
	try {
		let rsp = await fetchChapterItems(selectedOption, "roadsigns");
		let response = rsp.data[0];
		// console.log("handleChapterRoadSignsFetch response:", response);
		setQuestions(response);
	} catch (error) {
		console.log("Error:", error.message);
	}
}

// Fetch selected chapter questions and set the questions and currentQuestionIndex state.
async function handleChapterQuestionFetch(
	selectedOption,
	setQuestions,
	setCurrentQuestionIndex
) {
	try {
		let rsp = await fetchChapterItems(selectedOption, "quiz");
		let response = rsp.data[0];
		// console.log("handleChapterQuestionFetch response:", response);
		setQuestions(response);
		setCurrentQuestionIndex(1);
	} catch (error) {
		console.log("Error:", error.message);
	}
}

function transformImagePath(imagePath) {
	// Replace backslashes with forward slashes
	const normalizedPath = imagePath.replace(/\\/g, "/");

	// Concatenate the base URL with the normalized path
	const baseUrl = "http://localhost:8000/";
	const transformedUrl = baseUrl + normalizedPath;

	return transformedUrl;
}
