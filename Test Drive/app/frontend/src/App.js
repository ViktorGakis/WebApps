import "bootstrap/dist/css/bootstrap.css";
import React, { useState } from "react";
import logo from "./logo.svg";
import "./App.css";
import ApiTester from "./components/apitester.jsx";
import { FormFetchQuestions } from "./components/ChapterQuestionsFetch";

function App() {
	const [refreshKey, setRefreshKey] = useState(0);

	const handleRefresh = () => {
		setRefreshKey((prevKey) => prevKey + 1);
	};

	return (
		<div>
			<div className="App">
				<header className="App-header">
					{/* <div className="sticky-bar">
						<button className="end-button" onClick={handleRefresh}>
							Refresh CSS
						</button>
					</div> */}
					<img src={logo} className="App-logo" alt="logo" />
					<div className="questionsForm">
						<h1>Form Fetch Questions</h1>
						<FormFetchQuestions />
					</div>
				</header>
			</div>
		</div>
	);
}

export default App;
