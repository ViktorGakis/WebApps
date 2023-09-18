import React, { useEffect, useRef, useState } from "react";
import JobCard from "../components/JobCard";

export default function JobsContainer({
	data,
	saveEndpoint,
	likeEndpoint,
	disLikeEndpoint,
	applyEndpoint,
	expiredEndpoint,
}) {
	const [jobs, setJobs] = useState(data.items);

	useEffect(() => {
		setJobs(data.items);
	}, [data]);

	const handleRemoveJob = (jobId) => {
		setJobs((prevJobs) => prevJobs.filter((job) => job.id !== jobId));
	};

	return (
		<div className="jobs">
			<h1>Jobs Found:</h1>
			<div className="container">
				{jobs && jobs.length > 0 ? (
					jobs.map((job) => (
						<div className="job" key={job.id}>
							<JobCard
								key={job.id}
								job={job}
								onRemove={handleRemoveJob}
								saveEndpoint={saveEndpoint}
								likeEndpoint={likeEndpoint}
								disLikeEndpoint={disLikeEndpoint}
								applyEndpoint={applyEndpoint}
								expiredEndpoint={expiredEndpoint}
							/>
						</div>
					))
				) : (
					<p>No jobs available.</p>
				)}
			</div>
		</div>
	);
}
