import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import JobCard from "./components/JobCard";
import DBForm from "./components/DBform";
import React from "react";

function HomePage() {
	return (
		<>
			<JobCard />
			<DBForm
				table="yourTableName"
				cols={["col1", "col2"]}
				col_opers={["oper1", "oper2"]}
			/>
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
