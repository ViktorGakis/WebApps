import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import JobCard from "./components/JobCard";

const App = () => {
	function HomePage() {
		return <JobCard />;
	}

	return (
		<Router>
			<Routes>
				<Route path="/" element={<HomePage />} />
			</Routes>
		</Router>
	);
};

export default App;
