import React, { useRef } from "react";

function DBField({ field, table = null }) {
	const formAction = table ? `${table}_api_distinct_values` : undefined;

	return (
		<>
			<input
				type="text"
				name={field}
				placeholder="value"
				aria-label={field}
				list={`${field}_list`}
				className="form-control btn btn-outline-primary field"
				formAction={formAction}
				autoComplete="off"
			/>
			<datalist id={`${field}_list`}></datalist>
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

export default function DBForm({ table, cols = [], col_opers = [] }) {
	const actionUrl = `${table}_api_items`;
	const formRef = useRef(null);
	return (
		<div id="form_db">
			<div className="table-responsive">
				<form
					ref={formRef}
					method="GET"
					action={actionUrl}
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
										<DBField field={field} table={table} />
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
										{/* <button
											type="btn-primary btn-block"
											id="clear_job_filters"
											form="db_query"
											className="btn btn-primary clear_form">
											Clear
										</button> */}
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
