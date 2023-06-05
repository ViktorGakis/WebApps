import React from "react";
import { transformImagePath } from "../js/app_specifics";

export { RoadSigns };

function RoadSign(roadsign) {
	const { src, alt, name, descr } = roadsign.roadsign;

	return (
		<div className="card shadow-sm h-100 text-bg-secondary mb-3">
			{src && (
				<img
					src={transformImagePath(src)}
					alt={alt}
					className="img-fluid lazyload mx-auto w-lg-60 w-md-75 w-50 mt-4"
				/>
			)}
			<div className="card-body">
				<h5 className="card-title">{name}</h5>
				<p className="card-text x1_4 mt-4">{descr}</p>
			</div>
		</div>
	);
}

function RoadSigns({ roadsigns, formKey }) {
	return (
		<div id="roadsigns" className="card-body">
			<div className="row row-cols-1 row-cols-sm-2 row-cols-md-3 row-cols-lg-4 row-cols-xl-5 g-4">
				{roadsigns.map((roadsign, index) => (
					<div className="col" key={index}>
						<RoadSign key={index} roadsign={roadsign} />
					</div>
				))}
			</div>
		</div>
	);
}
