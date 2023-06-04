import "bootstrap/dist/css/bootstrap.css";
import React, { useState } from "react";

function refreshCssComponent() {
	const [refreshKey, setRefreshKey] = useState(0);

	const handleRefresh = () => {
		setRefreshKey((prevKey) => prevKey + 1);
	};

	return (
		<div key={refreshKey}>
			{/* Your component content */}
			<button onClick={handleRefresh}>Refresh CSS</button>
		</div>
	);
}
