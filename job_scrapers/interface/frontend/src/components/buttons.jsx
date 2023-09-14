import { TfiSave, TfiClose } from "react-icons/tfi";
import { AiFillLike, AiFillDislike, AiOutlineCheck } from "react-icons/ai";
import { AiOutlineCloseCircle } from "react-icons/ai";
import fetchAPI from "../js/fetchapi";
import React from "react";
export {
	SaveButton,
	ApplyButton,
	CloseButton,
	LikeButton,
	DisLikeButton,
	ExpiredButton,
};

function SaveButton({ job, endpoint }) {
	// Check if the job is saved and set the appropriate button class
	const isSaved = job.saved;
	const buttonClass = `btn save_btn ${
		isSaved ? "btn-outline-info" : "btn-outline-secondary"
	} btn-block`;

	return (
		<a
			type="submit"
			name={job.job_id}
			href={endpoint}
			className={buttonClass}>
			<TfiSave />
		</a>
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

function CloseButton({ addAttr }) {
	// Check if additional attributes are provided
	const additionalAttributes = addAttr || {};
	const handleClick = (event) => {
		let currentElement = event.target;

		while (currentElement) {
			if (
				currentElement.classList.contains("card") &&
				currentElement.classList.contains("job_card") &&
				currentElement.tagName.toLowerCase() === "article"
			) {
				currentElement.remove();
				return; // Stop searching once the article is found and removed
			}
			currentElement = currentElement.parentElement;
		}
	};
	return (
		<button
			type="button"
			className="btn btn_close"
			onClick={handleClick}
			{...additionalAttributes}>
			<AiOutlineCloseCircle />
		</button>
	);
}

function LikeButton({ job, endpoint }) {
	// Check if the job is in the 'fav' state and set the appropriate class
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
	// Check if the job is in the 'fav' state and set the appropriate class
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
	// Check if the job is in the 'expired' state and set the appropriate class
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
