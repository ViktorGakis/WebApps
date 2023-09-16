import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import React from "react";
import DataBaseContainer from "./sections/DatabaseContainer";

const apiBaseUrl = process.env.REACT_APP_API_BASE_URL;
const SaveApiEndpoint = "/jobs/api/item/save";
const LikeApiEndpoint = "/jobs/api/item/like";
const ApplyApiEndpoint = "/jobs/api/item/like";
const ExpiredApiEndpoint = "/jobs/api/item/like";
const ColsApiEndpoint = "/jobs/api/items/cols";
const OperApiEndpoint = "/jobs/api/items/opers";
const ItemsApiEndpoint = "/jobs/api/items";
const DistinctvApiEndpoint = "/jobs/api/distinct_values";
const table = "db.models.jobsch.Job";

function HomePage() {
	return (
		<DataBaseContainer
			table={table}
			formEndpoint={apiBaseUrl + ItemsApiEndpoint}
			colsEndpoint={apiBaseUrl + ColsApiEndpoint}
			opersEndpoint={apiBaseUrl + OperApiEndpoint}
			distinctvEndpoint={apiBaseUrl + DistinctvApiEndpoint}
			saveEndpoint={apiBaseUrl + SaveApiEndpoint}
			likeEndpoint={apiBaseUrl + LikeApiEndpoint}
			applyEndpoint={apiBaseUrl + ApplyApiEndpoint}
			expiredEndpoint={apiBaseUrl + ExpiredApiEndpoint}
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
