import React, { useState, useEffect } from "react";

export { Clock };

function Clock() {
	const [time, setTime] = useState(0);
	const [isRunning, setIsRunning] = useState(false);

	useEffect(() => {
		let intervalId;

		if (isRunning) {
			intervalId = setInterval(() => {
				setTime((prevTime) => prevTime + 1);
			}, 1000);
		}

		return () => {
			clearInterval(intervalId);
		};
	}, [isRunning]);

	const formatTime = (time) => {
		const hours = Math.floor(time / 3600);
		const minutes = Math.floor((time % 3600) / 60);
		const seconds = time % 60;

		return `${hours}:${padNumber(minutes)}:${padNumber(seconds)}`;
	};

	const padNumber = (number) => {
		return number.toString().padStart(2, "0");
	};

	const handleStart = () => {
		setIsRunning(true);
	};

	const handleStop = () => {
		setIsRunning(false);
	};

	const handleReset = () => {
		setIsRunning(false);
		setTime(0);
	};

	return (
		<div id='clock'>
			<div>{formatTime(time)}</div>
			<button className="btn btn-success" onClick={handleStart}>Start</button>
			<button className="btn btn-danger" onClick={handleStop}>Stop</button>
			<button className="btn btn-warning" onClick={handleReset}>Reset</button>
		</div>
	);
}
