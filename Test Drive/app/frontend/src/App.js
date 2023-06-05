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
				<div className="App-header">
					<img src={logo} className="App-logo" alt="logo" />
					<QuestionForm />
				</div>
			</div>
		</div>
	);
}

export default App;
