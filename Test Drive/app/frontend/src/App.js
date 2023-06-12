import "bootstrap/dist/css/bootstrap.css";
import React from "react";
import logo from "./logo.svg";
import "./App.css";
// import ApiTester from "./components/apitester.jsx";
import { QuestionForm } from "./components/questionForm";
import { RoadSignsForm } from "./components/roadsignsform";
import { QuestionsFromNotes } from "./components/filterQuestionsByNotes";

const FilterQuestionsEndpoint = "/api/retrieve/questions";

function App() {
	return (
		<div>
			<div className="App">
				<div className="App-header">
					<img src={logo} className="App-logo" alt="logo" />
					<QuestionForm />
					<hr></hr>
					<RoadSignsForm />
					<hr></hr>
					<QuestionsFromNotes
						endpoint={FilterQuestionsEndpoint.toString()}
					/>
				</div>
			</div>
		</div>
	);
}

export default App;
