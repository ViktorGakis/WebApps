import React, { useState } from "react";
import { fetchAPI } from "../js/utils";

export { NotesComponent };

async function handleSave(content, question) {
	await fetchAPI("api/save/note", undefined, { content: content, question: question }, "POST");
}

function NotesComponent(question) {
	const [content, setContent] = useState("");

	const save = async () => {
		await handleSave(content, question.question.question);
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
			<button onClick={save} className="btn btn-primary">Save</button>
		</div>
	);
}
