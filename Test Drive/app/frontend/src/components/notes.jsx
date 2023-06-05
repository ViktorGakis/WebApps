import React, { useState } from "react";
import { fetchAPI } from "../js/utils";

export { NotesComponent };

async function handleSave(content, question) {
	await fetchAPI(
		"api/save/note",
		undefined,
		{ content: content, question: question },
		"POST"
	);
}

async function handleLoad(question) {
	const note = await fetchAPI(
		"api/load/note",
		{ question: question },
		undefined,
		"GET"
	);
	return note.note;
}

function NotesComponent(question) {
	const [content, setContent] = useState("");
	const actual_question = question.question.question;

	const save = async () => {
		await handleSave(content, actual_question);
	};

	const load = async () => {
		const note = await handleLoad(actual_question);
		setContent(note);
	};

	const handleChange = (e) => {
		setContent(e.target.value);
	};

	return (
		<div className="notes">
			<textarea
				value={content}
				onChange={handleChange}
				className="stretch"
				// contentEditable={true}
			/>
			<div className="d-grid gap-1">
				<button onClick={save} className="btn btn-primary">
					Save
				</button>
				<button onClick={load} className="btn btn-primary">
					Load
				</button>
			</div>
		</div>
	);
}
