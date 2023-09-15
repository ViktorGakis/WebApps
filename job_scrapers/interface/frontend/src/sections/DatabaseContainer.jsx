import React, { useEffect, useRef, useState } from "react";
import Paginator from "../components/Paginator";
import JobCard from "../components/JobCard";
import DBForm from "../components/DBform";

function JobsContainer({ data }) {
	const [jobs, setJobs] = useState(data.items);

	useEffect(() => {
		setJobs(data.items);
	}, [data]);

	const handleRemoveJob = (jobId) => {
		setJobs((prevJobs) => prevJobs.filter((job) => job.id !== jobId));
	};

	return (
		<div className="jobs-container">
			<h1>Jobs Found:</h1>
			{jobs && jobs.length > 0 ? (
				jobs.map((job) => (
					<JobCard
						key={job.id}
						job={job}
						onRemove={handleRemoveJob}
					/>
				))
			) : (
				<p>No jobs available.</p>
			)}
		</div>
	);
}

export default function DataBaseContainer({
	table,
	formEndpoint,
	cols_endpoint,
	opers_endpoint,
	distinctv_endpoint,
}) {
	const [data, setData] = useState([]);
	const formRef = useRef(null);

	const updateData = (newData) => {
		setData(newData);
	};

	return (
		<div>
			<DBForm
				table={table}
				formEndpoint={formEndpoint}
				cols_endpoint={cols_endpoint}
				opers_endpoint={opers_endpoint}
				distinctv_endpoint={distinctv_endpoint}
				formRef={formRef}
				onUpdateData={updateData}
			/>
			{Array.isArray(data.items) && data.items.length > 0 && (
				<Paginator
					data={data}
					formEndpoint={formEndpoint}
					formRef={formRef}
					onUpdateData={updateData}
				/>
			)}
			{Array.isArray(data.items) && data.items.length > 0 && (
				<JobsContainer data={data} />
			)}
		</div>
	);
}
