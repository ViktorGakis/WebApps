import { TfiSave } from "react-icons/tfi";
import { AiFillLike, AiFillDislike, AiOutlineCheck } from "react-icons/ai";
import { AiOutlineCloseCircle } from "react-icons/ai";
import { BsExclamationTriangle } from "react-icons/bs";
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

function ToggleBtn({
	job,
	endpoint,
	setState,
	job_id,
	col_name,
	class_value,
	class_trigger_value,
	icon,
}) {
	const buildClass = (jobData) => {
		const baseClass = "btn";
		if (jobData[col_name] == class_trigger_value) {
			return baseClass + " " + class_value;
		}
		return baseClass;
	};

	const buildEndpoint = (jobData) => {
		return `${endpoint}&${job_id}=${jobData[job_id]}`;
	};

	const [currentEndpoint, setCurrentEndpoint] = useState(buildEndpoint(job));
	const [currentClass, setCurrentClass] = useState(buildClass(job));
	const [isLoading, setIsLoading] = useState(false);

	useEffect(() => {
		setCurrentClass(buildClass(job));
		setCurrentEndpoint(buildEndpoint(job));
	}, [job]);

	const toggleButton = async (e) => {
		e.preventDefault();
		setIsLoading(true);
		try {
			const updatedJob = await fetchAPI(currentEndpoint);
			setState(updatedJob);
		} catch (error) {
			console.error(`Error toggling ${col_name} state:`, error);
		} finally {
			setIsLoading(false);
		}
	};

	return (
		<div>
			<a
				type="submit"
				name={job.job_id}
				href={currentEndpoint}
				className={currentClass}
				onClick={toggleButton}>
				{isLoading ? <span>Loading...</span> : icon}
			</a>
		</div>
	);
}

function LikeButton({ job, endpoint, setState }) {
	return (
		<ToggleBtn
			job={job}
			endpoint={endpoint}
			setState={setState}
			job_id={"job_id"}
			col_name={"liked"}
			class_value={"success"}
			icon={<AiFillLike />}
			class_trigger_value={1}
		/>
	);
}

function DisLikeButton({ job, endpoint, setState }) {
	return (
		<ToggleBtn
			job={job}
			endpoint={endpoint}
			setState={setState}
			job_id={"job_id"}
			col_name={"liked"}
			class_value={"failure"}
			icon={<AiFillDislike />}
			class_trigger_value={-1}
		/>
	);
}

function SaveButton({ job, endpoint, setState }) {
	return (
		<ToggleBtn
			job={job}
			endpoint={endpoint}
			setState={setState}
			job_id={"job_id"}
			col_name={"saved"}
			class_value={"success"}
			icon={<TfiSave />}
			class_trigger_value={1}
		/>
	);
}

function ApplyButton({ job, endpoint, setState }) {
	return (
		<ToggleBtn
			job={job}
			endpoint={endpoint}
			setState={setState}
			job_id={"job_id"}
			col_name={"applied"}
			class_value={"success"}
			icon={<AiOutlineCheck />}
			class_trigger_value={1}
		/>
	);
}

function ExpiredButton({ job, endpoint, setState }) {
	return (
		<ToggleBtn
			job={job}
			endpoint={endpoint}
			setState={setState}
			job_id={"job_id"}
			col_name={"expired"}
			class_value={"failure"}
			icon={<BsExclamationTriangle />}
			class_trigger_value={1}
		/>
	);
}
