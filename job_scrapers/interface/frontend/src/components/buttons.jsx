import { TfiSave } from "react-icons/tfi";
import { AiFillLike, AiFillDislike, AiOutlineCheck } from "react-icons/ai";
import { AiOutlineCloseCircle } from "react-icons/ai";
import fetchAPI from "../js/fetchapi";
import React, { useState, useEffect } from "react";
export {
	SaveButton,
	ApplyButton,
	CloseButton,
	LikeButton,
	DisLikeButton,
	ExpiredButton,
};

function SaveButton({ job, endpoint }) {
	const buildClass = (jobData) => {
		return `btn ${jobData.saved ? "success" : "neutral"}`;
	};

	const buildEndpoint = (jobData) => {
		return `${endpoint}&job_id=${jobData.job_id}&saved=${Number(
			jobData.saved
		)}`;
	};

	const [currentJob, setCurrentJob] = useState(job);
	const [currentEndpoint, setCurrentEndpoint] = useState(buildEndpoint(job));
	const [currentClass, setCurrentClass] = useState(buildClass(job));
	const [isLoading, setIsLoading] = useState(false);

	useEffect(() => {
		setCurrentClass(buildClass(currentJob));
		setCurrentEndpoint(buildEndpoint(currentJob));
	}, [currentJob]);

	const toggleSaved = async (e) => {
		e.preventDefault();
		setIsLoading(true);
		try {
			const response = await fetchAPI(currentEndpoint);
			const updatedJob = { ...currentJob, saved: response.saved };
			setCurrentJob(updatedJob);
		} catch (error) {
			console.error("Error toggling saved state:", error);
		} finally {
			setIsLoading(false);
		}
	};

	return (
		<div>
			<a
				type="submit"
				name={currentJob.job_id}
				href={currentEndpoint}
				className={currentClass}
				onClick={toggleSaved}>
				{isLoading ? <span>Loading...</span> : <TfiSave />}
			</a>
		</div>
	);
}

function ApplyButton({ job, endpoint }) {
	// Check if the job is applied and set the appropriate button class
	const isApplied = job.applied;
	const buttonClass = `btn apply_btn ${
		isApplied ? "btn-outline-success" : "btn-outline-secondary"
	} btn-block`;

	return (
		<a
			type="button"
			name={job.job_id}
			href={endpoint}
			className={buttonClass}>
			<AiOutlineCheck />
		</a>
	);
}

function CloseButton({ jobId, onRemove }) {
	const handleClick = () => {
		if (onRemove) {
			onRemove(jobId);
		}
	};
	return (
		<button type="button" className="btn btn_close" onClick={handleClick}>
			<AiOutlineCloseCircle />
		</button>
	);
}

function LikeButton({ job, endpoint }) {
	const isFav = job.liked;
	const buttonClass = `btn like_btn btn-outline-secondary ${
		isFav ? "dis_state" : ""
	} btn-block`;

	return (
		<a
			type="button"
			name={job.job_id}
			href={endpoint}
			className={buttonClass}>
			<AiFillLike />
		</a>
	);
}

function DisLikeButton({ job, endpoint }) {
	const isFav = job.liked;
	const buttonClass = `btn like_btn btn-outline-secondary ${
		isFav ? "dis_state" : ""
	} btn-block`;

	return (
		<a
			type="button"
			name={job.job_id}
			href={endpoint}
			className={buttonClass}>
			<AiFillDislike />
		</a>
	);
}

function ExpiredButton({ job, endpoint }) {
	const isExpired = job.expired;
	const buttonClass = `btn expire_btn btn-outline-secondary ${
		isExpired ? "expired_state" : ""
	} btn-block`;

	return (
		<a
			type="submit"
			name={job.job_id}
			href={endpoint}
			className={buttonClass}>
			<span>
				<i className="fa-solid fa-triangle-exclamation fa-2x"></i>
			</span>
		</a>
	);
}
