import React, { useEffect, useState } from "react";
import { FormSelect } from "./formSelect";
import {
	fetchChapterData,
	handleChapterRoadSignsFetch,
} from "../js/app_specifics";
import { RoadSigns } from "./roadsignsComponent";

export { RoadSignsForm };

// Main component.
function RoadSignsForm() {
	const [chapters, setChapters] = useState([]);
	const [roadsigns, setRoadsigns] = useState([]);
	const [formKey, setFormKey] = useState(0); // Add formKey state

	useEffect(() => {
		fetchChapterData(setChapters, "roadsigns");
	}, []);

	const handleSubmit = function (e, selectedOption) {
		e.preventDefault();
		handleChapterRoadSignsFetch(
			selectedOption,
			setRoadsigns,
		);
	};

	const handleFormSubmit = function (e, selectedOption) {
		handleSubmit(e, selectedOption);
		setFormKey((prevKey) => prevKey + 1); // Update formKey on form submit
	};

	return (
		<div id="main">
			<h1>Choose Roadsign Category</h1>
			{chapters.length > 0 ? (
				<div id="form-container">
					<FormSelect
						data={chapters}
						url="/api/chapters/roadsigns"
						method="GET"
						handleSubmit={handleFormSubmit} // Modified to use handleFormSubmit
						id={'roadsignForm'}
					/>
				</div>
			) : (
				<div>Loading...</div>
			)}
			<hr></hr>
			<RoadSigns roadsigns={roadsigns} formKey={formKey} />
		</div>
	);
}
