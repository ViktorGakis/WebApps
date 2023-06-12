import React, { useState } from "react";

export function DataFetcher({endpoint, fetchData, handleData}) {
	const [inputValue, setInputValue] = useState("");
	const [loading, setLoading] = useState(false);
	const [responseData, setResponseData] = useState(null);

	const handleSubmit = async (e) => {
		e.preventDefault();
		setLoading(true);

		try {
			const payload = { data: inputValue };
			const response = await fetchData(endpoint, {}, payload, "POST");
			setResponseData(response.data);
		} catch (error) {
			console.error("Error:", error);
		} finally {
			setLoading(false);
		}
	};
	console.log("responseData: ", responseData)
	return (
		<div>
			<form onSubmit={handleSubmit}>
				<input
					type="text"
					value={inputValue}
					onChange={(e) => setInputValue(e.target.value)}
				/>
				<button type="submit">Submit</button>
			</form>
			{loading ? (
				<div>Loading...</div>
			) : responseData ? (
				<div>{handleData(responseData)}</div>
			) : null}
		</div>
	);
}
