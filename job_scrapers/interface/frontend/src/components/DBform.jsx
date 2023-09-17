import React, { useEffect, useState } from "react";

import fetchAPI, { handleFormRequest } from "../js/fetchapi";
import ExpContent from "./ExpContent";
import Card from "./Card";

async function get_distinct_v(table, field, distinctv_endpoint) {
	const rsp = await fetchAPI(`${distinctv_endpoint}&field=${field}`);
	// console.log("rspv");
	// console.log(rsp.data);
	return rsp.data;
}

function DBField({ field, table = null, distinctv_endpoint }) {
	const [htmlText, setHtmlText] = useState(field);
	const fetchData = async () => {
		// Fetch cols
		const htmlText = await get_distinct_v(table, field, distinctv_endpoint);
		// console.log("htmlText");
		// console.log(htmlText);
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
	// and also add as an attr in the actual form
	// ref={formRef}
	const handleClear = () => {
		if (formRef.current) {
			formRef.current.reset();
		}
	};

	return (
		<button
			type="button"
			className="btn"
			onClick={handleClear}
			style={{
				flex: "1",
			}}>
			Clear
		</button>
	);
}

async function get_cols(table, endpoint) {
	const rsp = await fetchAPI(endpoint);
	return rsp.cols;
}

async function get_col_opers(endpoint) {
	const rsp = await fetchAPI(endpoint);
	return rsp.col_opers;
}

function ColumnSelector({
	cols,
	visibleColumns,
	onToggle,
	onToggleAll,
	onTogglePredefined,
	usePredefinedCols,
}) {
	return (
		<div className="column-selector">
			<div style={{ display: "inline-block", marginRight: "10px" }}>
				<input
					type="checkbox"
					id="selectAll"
					checked={cols.length === visibleColumns.length}
					onChange={onToggleAll}
				/>
				<label htmlFor="selectAll">Select All</label>
			</div>
			<div style={{ display: "inline-block", marginRight: "10px" }}>
				<input
					type="checkbox"
					id="selectPredefined"
					checked={usePredefinedCols}
					onChange={onTogglePredefined}
				/>
				<label htmlFor="selectPredefined">Use Predefined</label>
			</div>

			{cols.map((col) => (
				<div
					key={col}
					style={{ display: "inline-block", marginRight: "10px" }}>
					<input
						type="checkbox"
						id={col}
						checked={visibleColumns.includes(col)}
						onChange={() => onToggle(col)}
					/>
					<label htmlFor={col}>{col}</label>
				</div>
			))}
		</div>
	);
}

function DBFieldRow({ field, col_opers, table, distinctv_endpoint }) {
	return (
		<tr scope="row">
			<th scope="row">{field}</th>
			<td>
				<DBFieldOper field={field} col_opers={col_opers} />
			</td>
			<td>
				<DBField
					field={field}
					table={table}
					distinctv_endpoint={distinctv_endpoint}
				/>
			</td>
		</tr>
	);
}

function DBUtilsRow(formRef) {
	return (
		<>
			<tr scope="row">
				<th colSpan="1">
					<input
						type="number"
						name="per_page"
						placeholder="results_per_page"
						className="form-control btn btn-outline-primary field_oper"
					/>
				</th>
				<th>
					<DBFieldOrderCol />
				</th>
				<th>
					<DBFieldOrderMode />
				</th>
			</tr>
			<tr scope="row">
				<th colSpan="3">
					<div
						className="d-grid"
						style={{
							display: "flex",
							justifyContent: "space-between",
						}}>
						<button
							type="btn-primary"
							id="get_jobs"
							form="db_query"
							className="btn btn-primary btn-block"
							style={{
								flex: "1",
							}}>
							GET JOBS
						</button>
						<ClearForm formRef={formRef} />
					</div>
				</th>
			</tr>
		</>
	);
}

function DBFormTable({
	table,
	visibleColumns,
	col_opers,
	distinctv_endpoint,
	formRef,
}) {
	return (
		<table className="table table-hover table-bordered border-5 table-dark caption-top">
			<caption>
				<h1>{`Table: ${
					table.charAt(0).toUpperCase() + table.slice(1)
				}`}</h1>
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
				{visibleColumns.map((field) => (
					<DBFieldRow
						key={field}
						field={field}
						col_opers={col_opers}
						table={table}
						distinctv_endpoint={distinctv_endpoint}
					/>
				))}
				<DBUtilsRow formRef={formRef} />
			</tbody>
		</table>
	);
}

export default function DBForm({
	table,
	formEndpoint,
	cols_endpoint,
	opers_endpoint,
	distinctv_endpoint,
	formRef,
	onUpdateData,
	predefinedCols = {
		title: true,
		company_name: true,
		place: true,
		is_active: true,
		job_id: true,
		template: true,
		applied: true,
		saved: true,
		liked: true,
		expired: true,
	},
}) {
	// Initialize state variables for cols and col_opers
	const [cols, setCols] = useState([]);
	const [col_opers, setColOpers] = useState([]);
	const [visibleColumns, setVisibleColumns] = useState(cols);
	const [usePredefinedCols, setUsePredefinedCols] = useState(false);

	// Handler for when a column is toggled in the ColumnSelector
	const handleColumnToggle = (col) => {
		setVisibleColumns((prevCols) => {
			if (prevCols.includes(col)) {
				return prevCols.filter((column) => column !== col);
			} else {
				return [...prevCols, col];
			}
		});
	};

	// Handler to toggle all columns
	const handleToggleAll = () => {
		if (visibleColumns.length < cols.length) {
			setVisibleColumns(cols);
		} else {
			setVisibleColumns([]);
		}
		// Ensure that 'Use Predefined' is unchecked when 'Select All' is toggled
		setUsePredefinedCols(false);
	};

	const handleTogglePredefined = () => {
		if (usePredefinedCols) {
			// From predefined to all columns
			setVisibleColumns(cols);
		} else {
			// From all columns to predefined
			const initialVisibleColumns = cols.filter(
				(col) => predefinedCols[col]
			);
			setVisibleColumns(initialVisibleColumns);
		}
		setUsePredefinedCols((prev) => !prev);
	};

	const handleFormSubmit = async (e, page = 1) => {
		const options = {
			formEndpoint: formEndpoint,
			page: page,
		};
		const rsp = await handleFormRequest(e, formRef, options);
		onUpdateData(rsp.data);
	};

	// Use the useEffect hook to run asynchronous operations
	useEffect(() => {
		const fetchData = async () => {
			// Fetch cols
			const colsData = await get_cols(table, cols_endpoint);
			setCols(colsData);

			// Set predefined columns
			const initialVisibleColumns = colsData.filter(
				(col) => predefinedCols[col] !== false
			);

			// Initially set all columns to visible
			setVisibleColumns(colsData);

			// Fetch col_opers
			const colOpersData = await get_col_opers(opers_endpoint);

			setColOpers(colOpersData);
		};

		fetchData();
	}, [table, cols_endpoint, opers_endpoint]); // dependencies ensure the effect runs when these props change

	return (
		<div id="form_db">
			<Card>
				<ExpContent
					summary={"Column Selection"}
					content={
						<ColumnSelector
							cols={cols}
							visibleColumns={visibleColumns}
							onToggle={handleColumnToggle}
							onToggleAll={handleToggleAll}
							onTogglePredefined={handleTogglePredefined}
							usePredefinedCols={usePredefinedCols}
						/>
					}
				/>
			</Card>
			<Card>
				<ExpContent
					summary={"DB FORM"}
					content={
						<div className="table-responsive">
							<form
								ref={formRef}
								onSubmit={handleFormSubmit}
								method="GET"
								action={formEndpoint}
								id="db_query"
								name="db_query">
								<DBFormTable
									table={table}
									visibleColumns={visibleColumns}
									col_opers={col_opers}
									distinctv_endpoint={distinctv_endpoint}
									formRef={formRef}
								/>
							</form>
						</div>
					}
				/>
			</Card>
		</div>
	);
}
