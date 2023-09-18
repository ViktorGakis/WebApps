import React, { useEffect, useRef, useState } from "react";
import Paginator from "../components/Paginator";
import DBForm from "../components/DBform";
import JobsContainer from "../components/JobsContainer";

export default function DataBaseContainer({
	table,
	formEndpoint,
	colsEndpoint,
	opersEndpoint,
	distinctvEndpoint,
	saveEndpoint,
	likeEndpoint,
	disLikeEndpoint,
	applyEndpoint,
	expiredEndpoint,
}) {
	const [data, setData] = useState([]);
	const formRef = useRef(null);
	const [formEndpointUpd, setformEndpointUpd] = useState(
		formEndpoint + "?table=" + table
	);
	const [colsEndpointUpd, setcolsEndpointUpd] = useState(
		colsEndpoint + "?table=" + table
	);
	const [opersEndpointUpd, setopersEndpointUpd] = useState(opersEndpoint);
	const [distinctvEndpointUpd, setdistinctvEndpointUpd] = useState(
		distinctvEndpoint + "?table=" + table
	);
	const [saveEndpointUpd, setsaveEndpointUpd] = useState(
		saveEndpoint + "?table=" + table
	);
	const [LikeEndpointUpd, setLikeEndpointUpd] = useState(
		likeEndpoint + "?table=" + table
	);
	const [disLikeEndpointUpd, setdisLikeEndpointUpd] = useState(
		disLikeEndpoint + "?table=" + table
	);
	const [ApplyApiEndpointUpd, setApplyApiEndpointUpd] = useState(
		applyEndpoint + "?table=" + table
	);
	const [ExpiredApiEndpointUpd, setExpiredApiEndpointUpd] = useState(
		expiredEndpoint + "?table=" + table
	);

	useEffect(() => {
		setformEndpointUpd(formEndpoint + "?table=" + table);
		setcolsEndpointUpd(colsEndpoint + "?table=" + table);
		// setopersEndpointUpd(opersEndpointUpd + "?table=" + table);
		setdistinctvEndpointUpd(distinctvEndpoint + "?table=" + table);
		setsaveEndpointUpd(saveEndpoint + "?table=" + table);
		setLikeEndpointUpd(likeEndpoint + "?table=" + table);
		setdisLikeEndpointUpd(disLikeEndpoint + "?table=" + table);
		setApplyApiEndpointUpd(applyEndpoint + "?table=" + table);
		setExpiredApiEndpointUpd(expiredEndpoint + "?table=" + table);
	}, [table]);

	const updateData = (newData) => {
		setData(newData);
	};

	return (
		<div>
			<DBForm
				table={table}
				formEndpoint={formEndpointUpd}
				cols_endpoint={colsEndpointUpd}
				opers_endpoint={opersEndpointUpd}
				distinctv_endpoint={distinctvEndpointUpd}
				formRef={formRef}
				onUpdateData={updateData}
			/>
			{Array.isArray(data.items) && data.items.length > 0 && (
				<Paginator
					data={data}
					formEndpoint={formEndpointUpd}
					formRef={formRef}
					onUpdateData={updateData}
				/>
			)}
			{Array.isArray(data.items) && data.items.length > 0 && (
				<JobsContainer
					data={data}
					saveEndpoint={saveEndpointUpd}
					likeEndpoint={LikeEndpointUpd}
					disLikeEndpoint={disLikeEndpointUpd}
					applyEndpoint={ApplyApiEndpointUpd}
					expiredEndpoint={ExpiredApiEndpointUpd}
				/>
			)}
		</div>
	);
}