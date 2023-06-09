import React, { useState } from "react";

function actualSelectForm(
	data,
	selectedOption,
	setSelectedOption,
	handleSubmit,
	method,
	url,
	id
) {
	const handleFormSubmit = async (e) => {
		e.preventDefault();
		await handleSubmit(e, selectedOption); // Pass the event object and selectedOption as arguments to the handleSubmit function
	};

	return (
		<form
			className="form button-container"
			onSubmit={handleFormSubmit}
			method={method}
			action={url}
			id={id}>
			<div className="form-group">
				<select
					className="form-control"
					value={selectedOption}
					onChange={(e) => setSelectedOption(e.target.value)}>
					{data.map((item, index) => {
						return (
							<option key={index} value={item}>
								{item}
							</option>
						);
					})}
				</select>
			</div>
			<button className="btn btn-primary" type="submit">
				Submit
			</button>
		</form>
	);
}

function FormSelect({ data, url, method, handleSubmit, id }) {
	const [selectedOption, setSelectedOption] = useState(data[0] || "");

	return actualSelectForm(
		data,
		selectedOption,
		setSelectedOption,
		handleSubmit,
		method,
		url,
		id
	);
}

export { FormSelect };
