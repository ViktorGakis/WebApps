This is my code 

[function ToggleBtn({
	job,
	endpoint,
	setState,
	job_id,
	col_name,
	class_value,
	icon,
}) {
	const buildClass = (jobData) => {
		const baseClass = "btn ";
		if (jobData[col_name]) {
			return baseClass + class_value;
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
		/>
	);
}

export default function JobCard({
	job,
	onRemove,
	saveEndpoint,
	likeEndpoint,
	disLikeEndpoint,
	applyEndpoint,
	expiredEndpoint,
}) {
	const [jobData, setJobData] = useState(job);

	useEffect(() => {
		// 3. Re-run whenever jobData changes.
		// This is just an illustration. Currently, this useEffect doesn't
		// do much since setting state already causes a re-render.
		// But you can put logic here if you want to perform side-effects
		// whenever jobData changes.
	}, [jobData]);

	if (!job || typeof job.id === "undefined") {
		return <div>Error: Invalid job data {job}</div>;
	}

	return (
		<Card className="job_card">
			<div className="job_header">
				<div>
					<h3>{job.id}.</h3>
				</div>
				<TitleHeader job={job} />
			</div>
			<PseudoFooter job={job} />
			<div className="btns_group">
				<LikeButton
					job={jobData}
					endpoint={likeEndpoint}
					setState={setJobData}
				/>
				<DisLikeButton
					job={jobData}
					endpoint={disLikeEndpoint}
					setState={setJobData}
				/>
				{/* <SaveButton job={jobData} endpoint={saveEndpoint} />
				<ApplyButton job={jobData} endpoint={applyEndpoint} /> */}
				<CloseButton jobId={job.id} onRemove={onRemove} />
			</div>
		</Card>
	);
}
]. 
It works ok but when I press the like or dislike button both btns are either activated together or deactivated together. Why is that? Only one of them should be activated.