import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import React from "react";
import DataBaseContainer from "./sections/DatabaseContainer";

const apiBaseUrl = process.env.REACT_APP_API_BASE_URL;
const saveEndpoint = "/jobs/api/item/save";
const likeEndpoint = "/jobs/api/item/like";
const dislikeEndpoint = "/jobs/api/item/dislike";
const applyEndpoint = "/jobs/api/item/apply";
const expiredEndpoint = "/jobs/api/item/expire";
const colsEndpoint = "/jobs/api/items/cols";
const operEndpoint = "/jobs/api/items/opers";
const itemsEndpoint = "/jobs/api/items";
const distinctvEndpoint = "/jobs/api/distinct_values";
const table = "db.models.jobsch.Job";

function HomePage() {
	return (
		<DataBaseContainer
			table={table}
			formEndpoint={apiBaseUrl + itemsEndpoint}
			colsEndpoint={apiBaseUrl + colsEndpoint}
			opersEndpoint={apiBaseUrl + operEndpoint}
			distinctvEndpoint={apiBaseUrl + distinctvEndpoint}
			saveEndpoint={apiBaseUrl + saveEndpoint}
			likeEndpoint={apiBaseUrl + likeEndpoint}
			disLikeEndpoint={apiBaseUrl + dislikeEndpoint}
			applyEndpoint={apiBaseUrl + applyEndpoint}
			expiredEndpoint={apiBaseUrl + expiredEndpoint}
		/>
	);
}

function App() {
	return (
		<Router>
			<Routes>
				<Route path="/" element={<HomePage />} />
			</Routes>
		</Router>
	);
}

export default App;
