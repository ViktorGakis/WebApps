import "bootstrap/dist/css/bootstrap.css";
import React from "react";
import logo from "./logo.svg";
import "./App.css";
// import ApiTester from "./components/apitester.jsx";
import { QuestionForm } from "./components/questionForm";


function App() {
	return (
		<div>
			<div className="App">
				<header className="App-header">
					<img src={logo} className="App-logo" alt="logo" />
					<div className="questionsForm">
						<h1>Form Fetch Questions</h1>
						<QuestionForm />
					</div>
				</header>
			</div>
		</div>
	);
}

export default App;