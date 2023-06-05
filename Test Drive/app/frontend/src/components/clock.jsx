import React, { useState, useEffect } from "react";

export { Clock };

function Clock() {
	const [time, setTime] = useState(0);
	const [isRunning, setIsRunning] = useState(true);

	useEffect(() => {
		let intervalId;

		if (isRunning) {
			intervalId = setInterval(() => {
				setTime((prevTime) => prevTime + 10);
			}, 10);
		}

		return () => {
			clearInterval(intervalId);
		};
	}, [isRunning]);

	const formatTime = (time) => {
		const milliseconds = time % 1000;
		const seconds = Math.floor((time / 1000) % 60);
		const minutes = Math.floor((time / 1000 / 60) % 60);
		const hours = Math.floor(time / 1000 / 60 / 60);

		return `${padNumber(hours)}:${padNumber(minutes)}:${padNumber(
			seconds
		)}.${padNumber(milliseconds, 3)}`;
	};

	const padNumber = (number, length = 2) => {
		return number.toString().padStart(length, "0");
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
		<div id="clock">
			<div>{formatTime(time)}</div>
			<button className="btn btn-success" onClick={handleStart}>
				Start
			</button>
			<button className="btn btn-danger" onClick={handleStop}>
				Stop
			</button>
			<button className="btn btn-warning" onClick={handleReset}>
				Reset
			</button>
		</div>
	);
}
