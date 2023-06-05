import React, { useState } from "react";
import { fetchAPI } from "../js/utils";

export { NotesComponent };

async function handleSave(content) {
	await fetchAPI("api/save/note", undefined, { data: content }, "POST");
}

function NotesComponent() {
	const [content, setContent] = useState("");

	const save = async () => {
		await handleSave(content);
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
				contentEditable={true}
			/>
			<button onClick={save} className="btn btn-primary">Save</button>
		</div>
	);
}
