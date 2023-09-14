import React, { useRef, useEffect, useState } from "react";

import fetchAPI from "../js/fetchapi";

async function get_distinct_v(table, field, distinctv_endpoint) {
	const rsp = await fetchAPI(
		`${distinctv_endpoint}?table=${table}&field=${field}`
	);
    console.log('rspv')
    console.log(rsp.data)
	return rsp.data;
}

function DBField({ field, table = null, distinctv_endpoint }) {
	const [htmlText, setHtmlText] = useState(field);
	const fetchData = async () => {
		// Fetch cols
		const htmlText = await get_distinct_v(table, field, distinctv_endpoint);
		console.log("htmlText");
		console.log(htmlText);
		setHtmlText(htmlText);
	};

	return (
		<>
			<input
				type="text"
				name={field}
				placeholder="value"
				aria-label={field}
				list={`${field}_list`}
				className="form-control btn btn-outline-primary field"
				formAction={distinctv_endpoint}
				autoComplete="off"
				onClick={fetchData}
			/>
			<datalist
				id={`${field}_list`}
				dangerouslySetInnerHTML={{ __html: htmlText }}></datalist>
		</>
	);
}

function DBFieldOper({ field, col_opers = [] }) {
	if (!col_opers) {
		return null;
	}
	return (
		<>
			<input
				type="text"
				className="form-control btn btn-outline-primary field_oper"
				name={`${field}_oper`}
				placeholder="operator"
				list={`${field}_oper_list`}
				autoComplete="off"
			/>
			<datalist id={`${field}_oper_list`}>
				{col_opers.map((oper) => (
					<option key={oper}>{oper}</option>
				))}
			</datalist>
		</>
	);
}

function DBFieldOrderCol({ cols = [] }) {
	if (!cols) {
		return null;
	}
	return (
		<>
			<input
				className="form-control btn btn-outline-primary field_oper"
				type="text"
				list="order_by_cols_list"
				id="order_by_cols"
				name="order_by_cols"
				placeholder="order_by_cols"
				autoComplete="off"
			/>
			<datalist id="order_by_cols_list">
				{cols.map((field) => (
					<option key={field}>{field}</option>
				))}
			</datalist>
		</>
	);
}

function DBFieldOrderMode() {
	return (
		<>
			<input
				className="form-control btn btn-outline-primary field_oper"
				type="text"
				list="order_by_mode_list"
				id="order_by_mode"
				name="order_by_mode"
				placeholder="order_by_mode"
				autoComplete="off"
			/>
			<datalist id="order_by_mode_list">
				<option>asc</option>
				<option>desc</option>
			</datalist>
		</>
	);
}

function ClearForm({ formRef }) {
	// need to define
	// const formRef = useRef(null);
	// in the component that contains the form
	// and also add as an attr in the form
	// ref={formRef}
	const handleClear = () => {
		if (formRef.current) {
			formRef.current.reset();
		}
	};

	return (
		<button type="button" className="btn" onClick={handleClear}>
			Clear
		</button>
	);
}

async function get_cols(table, endpoint) {
	const rsp = await fetchAPI(endpoint + `?table=${table}`);
	return rsp.cols;
}

async function get_col_opers(endpoint) {
	const rsp = await fetchAPI(endpoint);
	return rsp.col_opers;
}

export default function DBForm({
	table,
	form_endpoint,
	cols_endpoint,
	opers_endpoint,
	distinctv_endpoint,
	// cols = [],
	// col_opers = [],
}) {
	const formRef = useRef(null);
	// Initialize state variables for cols and col_opers
	const [cols, setCols] = useState([]);
	const [col_opers, setColOpers] = useState([]);

	// Use the useEffect hook to run asynchronous operations
	useEffect(() => {
		const fetchData = async () => {
			// Fetch cols
			const colsData = await get_cols(table, cols_endpoint);
			setCols(colsData);

			// Fetch col_opers
			const colOpersData = await get_col_opers(opers_endpoint);

			setColOpers(colOpersData);
		};

		fetchData();
	}, [table, cols_endpoint, opers_endpoint]); // dependencies ensure the effect runs when these props change

	return (
		<div id="form_db">
			<div className="table-responsive">
				<form
					ref={formRef}
					method="GET"
					action={form_endpoint}
					id="db_query"
					name="db_query">
					<table className="table table-hover table-bordered border-5 table-dark caption-top">
						<caption>
							<h1>{`${
								table.charAt(0).toUpperCase() + table.slice(1)
							} db query form`}</h1>
						</caption>
						<thead>
							<tr scope="row">
								<th scope="col">
									<h3>Field</h3>
								</th>
								<th scope="col">
									<h3>Operator</h3>
								</th>
								<th scope="col">
									<h3>Value</h3>
								</th>
							</tr>
						</thead>
						<tbody className="table-group-divider table-dark">
							{cols.map((field) => (
								<tr scope="row" key={field}>
									<th scope="row">{field}</th>
									<td>
										<DBFieldOper
											field={field}
											col_opers={col_opers}
										/>
									</td>
									<td>
										<DBField
											field={field}
											table={table}
											distinctv_endpoint={
												distinctv_endpoint
											}
										/>
									</td>
								</tr>
							))}
							<tr scope="row">
								<th scope="row">Order</th>
								<td>
									<DBFieldOrderCol />
								</td>
								<td>
									<DBFieldOrderMode />
								</td>
							</tr>
							<tr scope="row">
								<td></td>
								<td></td>
								<td></td>
							</tr>
							<tr scope="row">
								<th colSpan="2">
									<input
										type="number"
										name="per_page"
										placeholder="results_per_page"
										className="form-control btn btn-outline-primary field_oper"
									/>
								</th>
								<td>
									<div className="d-grid">
										<ClearForm formRef={formRef} />
									</div>
								</td>
							</tr>
							<tr scope="row">
								<th colSpan="3">
									<div className="d-grid">
										<button
											type="btn-primary"
											id="get_jobs"
											form="db_query"
											className="btn btn-primary btn-block">
											GET JOBS
										</button>
									</div>
								</th>
							</tr>
						</tbody>
					</table>
				</form>
			</div>
		</div>
	);
}
