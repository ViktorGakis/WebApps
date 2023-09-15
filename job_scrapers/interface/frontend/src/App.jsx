import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import JobCard from "./components/JobCard";
import DBForm from "./components/DBform";
import React from "react";

const apiBaseUrl = process.env.REACT_APP_API_BASE_URL;
const saveEndpoint = "/jobs/api/item/save";
const likeEndpoint = "/jobs/api/item/like";
const applyEndpoint = "/jobs/api/item/like";
const expiredEndpoint = "/jobs/api/item/like";
const api_cols = "/jobs/api/items/cols";
const api_oper = "/jobs/api/items/opers";
const api_items = "/jobs/api/items";
const distinctv_endpoint = "/jobs/api/distinct_values";

function HomePage() {
	return (
		<>
			<DBForm
				table="db.models.jobsch.Job"
				form_endpoint={apiBaseUrl + api_items}
				cols_endpoint={apiBaseUrl + api_cols}
				opers_endpoint={apiBaseUrl + api_oper}
				distinctv_endpoint={apiBaseUrl + distinctv_endpoint}
				// cols={["col1", "col2"]}
				// col_opers={["oper1", "oper2"]}
			/>
			<JobCard />
		</>
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
