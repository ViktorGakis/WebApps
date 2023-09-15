import {
	ApplyButton,
	CloseButton,
	DisLikeButton,
	ExpiredButton,
	LikeButton,
	SaveButton,
} from "./buttons";

import "./jobcard.css";

import Card from "./Card";

import React from "react";
import ExpandableContent from "./ExpContent";
import CondElem from "./CondElem";
import ExpContent from "./ExpContent";
import { MdLocationOn, MdDescription } from "react-icons/md";
import { IoMdBusiness } from "react-icons/io";

const apiBaseUrl = process.env.REACT_APP_API_BASE_URL;
const saveEndpoint = "/jobs/api/item/save";
const likeEndpoint = "/api/item/like";
const applyEndpoint = "/api/item/like";
const expiredEndpoint = "/api/item/like";

// const job = {
// 	title: "Internships Global Specialized Solutions department (m/f/d)",
// 	publication_date: "2023-09-12T15:38:47+02:00",
// 	publication_end_date: "2024-09-13",
// 	company_name: "Georg Fischer Rohrleitungssysteme (Schweiz) AG",
// 	place: "Switzerland, Schaffhausen",
// 	is_active: true,
// 	job_id: "66860bad-5f40-4a65-84a9-90aa0d2f5c93",
// 	preview:
// 		"Basic, Design, Deutsch, Englisch, Gewissenhaftigkeit, IT-Netzwerk, Kommunikationsfähigkeit, Nachhaltigkeitsorientierung, TARGET, Teamfähigkeit, ...",
// 	company_logo_file: "",
// 	slug: "66860bad-5f40-4a65-84a9-90aa0d2f5c93-internships-global-specialized-solutions-department-m-f-d",
// 	company_slug: "",
// 	company_id: "",
// 	company_segmentation: "kmu",
// 	employment_position_ids: "[2]",
// 	employment_grades: "[100]",
// 	contact_person: "[]",
// 	is_paid: false,
// 	work_experience: "[]",
// 	language_skills: "[]",
// 	url_en: "https://www.jobs.ch/en/vacancies/detail/66860bad-5f40-4a65-84a9-90aa0d2f5c93/",
// 	url_de: "https://www.jobs.ch/de/stellenangebote/detail/66860bad-5f40-4a65-84a9-90aa0d2f5c93/",
// 	url_fr: "https://www.jobs.ch/fr/offres-emplois/detail/66860bad-5f40-4a65-84a9-90aa0d2f5c93/",
// 	url_api:
// 		"https://www.jobs.ch/api/v1/public/search/job/66860bad-5f40-4a65-84a9-90aa0d2f5c93",
// 	application_url:
// 		"https://live.solique.ch/georgfischer/job/details/3405269/",
// 	external_url: "https://live.solique.ch/georgfischer/job/details/3405269/",
// 	template:
// 		'<h3>We are offering following internships:<i></i><ul>\n <li><i></i>Global Service and Support - focusing on Process Automation (fluid control and technical services)</li>\n <li><i></i>Global Service and Support - focusing on Technical Product Support (mechanical characteristics and quality services)</li>\n <li><i></i>Global Solutions Development - focusing on creating new customer offerings based on latest technologies for engineering, design and Off-Site manufacturing execution</li>\n <li><i></i>Global Service Operations - focusing on customer projects involving execution of pre-fabricated solutions engineering, production and project management</li>\n</ul><h3>Your tasks &amp; profile<i></i></h3><ul>\n <li><i></i>Co-work the existing teams to support them in their daily work</li>\n <li><i></i>Be responsible for your delegated own tasks and projects</li>\n <li><i></i>Help our teams to design, test and validate new solutions</li>\n <li><i></i>Active participation in design thinking projects, harmonization activities, business development across our global network</li>\n <li><i></i>Interaction with internal / external stakeholders from procurement to field experts</li>\n <li><i></i>You are studying for University or University of applied sciences with the target to finish with a degree in chemical process engineering or mechanical engineering</li>\n <li><i></i>In addition to fluent business English and likely also basic German, you have strong communication skills, reliability and team spirit</li>\n</ul><h3>Benefits</h3><p> Clear vision and purpose  "We are a sustainability and innovation leader providing superior customer value" is our vision and this is what guides us. Our purpose "becoming better every day - since 1802" is what inspires us in our daily work. <i></i> Sustainability and innovation focus  We have high sustainability and innovation goals. Let\'s work towards a sustainable future together. <i></i> Excellent learning tools  At GF we provide development opportunities for everyone. We offer global learning tools as well as trainings and specialized courses. <i></i> Great career opportunities  GF as a global acting company provides many opportunities regarding career growth. We also offer a dedicated talent management process (MyNextBigStep@GF) to boost your career. <i></i> Mobile discount  We are offering discounts for Sunrise mobile subscriptions. <i></i> Sport Activities  We support the purchase of a fitness studio membership from the center of your choice with a subsidy. We also offer active health promotion with other sport activities. <i></i>\n</p><h3>Your contact</h3><p>Kristina PericHR Services Specialist<i></i>+41&nbsp;52&nbsp;631&nbsp;32&nbsp;25<i></i>Web<i></i> Amsler-Laffon-Strasse 9<br>8201 Schaffhausen<br>Switzerland View larger map\n</p><h3>Your work route</h3><i></i><i></i><i></i><p>Apply now\n</p><h3>Who we are</h3><p> GF Piping Systems is the world\'s leading supplier of piping systems. We enable the safe and sustainable transport of fluids. Our business is driven by industry-leading sustainability levels, innovation through digital solutions and investment in a culture based on performance, learning and caring. <i></i><i></i><i></i><i></i><i></i></p></h3>\n',
// 	template_profession:
// 		"Internships Global Specialized Solutions department (m/f/d)",
// 	template_text:
// 		'<h3>We are offering following internships:<i> </i> </h3> <ul> <br />\n <li> <i> </i>Global Service and Support - focusing on Process Automation (fluid control and technical services)</li> <br />\n <li> <i> </i>Global Service and Support - focusing on Technical Product Support (mechanical characteristics and quality services)</li> <br />\n <li> <i> </i>Global Solutions Development - focusing on creating new customer offerings based on latest technologies for engineering, design and Off-Site manufacturing execution</li> <br />\n <li> <i> </i>Global Service Operations - focusing on customer projects involving execution of pre-fabricated solutions engineering, production and project management</li> <br />\n</ul> <h3>Your tasks &amp; profile<i> </i> </h3> <ul> <br />\n <li> <i> </i>Co-work the existing teams to support them in their daily work</li> <br />\n <li> <i> </i>Be responsible for your delegated own tasks and projects</li> <br />\n <li> <i> </i>Help our teams to design, test and validate new solutions</li> <br />\n <li> <i> </i>Active participation in design thinking projects, harmonization activities, business development across our global network</li> <br />\n <li> <i> </i>Interaction with internal / external stakeholders from procurement to field experts</li> <br />\n <li> <i> </i>You are studying for University or University of applied sciences with the target to finish with a degree in chemical process engineering or mechanical engineering</li> <br />\n <li> <i> </i>In addition to fluent business English and likely also basic German, you have strong communication skills, reliability and team spirit</li> <br />\n</ul> <h3>Benefits</h3> <p> Clear vision and purpose  "We are a sustainability and innovation leader providing superior customer value" is our vision and this is what guides us. Our purpose "becoming better every day - since 1802" is what inspires us in our daily work. <i> </i> Sustainability and innovation focus  We have high sustainability and innovation goals. Let\'s work towards a sustainable future together. <i> </i> Excellent learning tools  At GF we provide development opportunities for everyone. We offer global learning tools as well as trainings and specialized courses. <i> </i> Great career opportunities  GF as a global acting company provides many opportunities regarding career growth. We also offer a dedicated talent management process (MyNextBigStep@GF) to boost your career. <i> </i> Mobile discount  We are offering discounts for Sunrise mobile subscriptions. <i> </i> Sport Activities  We support the purchase of a fitness studio membership from the center of your choice with a subsidy. We also offer active health promotion with other sport activities. <i> </i> <br />\n</p> <h3>Your contact</h3> <p>Kristina PericHR Services Specialist<i> </i>+41 52 631 32 25<i> </i>Web<i> </i> Amsler-Laffon-Strasse 9<br />8201 Schaffhausen<br />Switzerland View larger map<br />\n</p> <h3>Your work route</h3> <i> </i> <i> </i> <i> </i> <p>Apply now<br />\n</p> <h3>Who we are</h3> <p> GF Piping Systems is the world\'s leading supplier of piping systems. We enable the safe and sustainable transport of fluids. Our business is driven by industry-leading sustainability levels, innovation through digital solutions and investment in a culture based on performance, learning and caring. <i> </i> <i> </i> <i> </i> <i> </i> <i> </i> </p><br />\n',
// 	template_lead_text: "",
// 	headhunter_application_allowed: true,
// 	applied: null,
// 	saved: 1,
// 	liked: null,
// 	expired: null,
// 	request_id: 2,
// 	sub_request_id: 2,
// 	status: 200,
// 	id: 19,
// 	created_at: "2023-09-13T21:11:27",
// 	updated_at: "2023-09-13T21:11:36",
// };

function CompanyInfo({ job }) {
	return (
		<>
			<div className="company_info">
				<ExpandableContent
					summary={<h3>{job.company_name}</h3>}
					content={
						<div>
							<CondElem
								tagName="div"
								data={job}
								key="company_slug"
								attributes={undefined}
							/>
							<CondElem
								tagName="div"
								data={job}
								key="company_id"
								attributes={undefined}
							/>
							<CondElem
								tagName="div"
								data={job}
								key="company_segmentation"
								attributes={undefined}
							/>
						</div>
					}
				/>
			</div>
		</>
	);
}

function JobHeader() {
	return <div className="job_header">{/* <PrimaryInfo /> */}</div>;
}

function Description({ job }) {
	return (
		<ExpandableContent
			summary={
				<h4>
					<MdDescription /> Description
				</h4>
			}
			content={
				<div>
					{job.template_text && (
						<div
							dangerouslySetInnerHTML={{
								__html: job.template_text,
							}}
						/>
					)}

					{!job.template_text && job.template_lead_text && (
						<div>
							dangerouslySetInnerHTML=
							{{ __html: job.template_lead_text }}
						</div>
					)}
				</div>
			}
		/>
	);
}

function PseudoFooter({ job }) {
	return (
		<div className="dates">
			<div>
				{/* <strong>publication_date:</strong> */}
				{job.publication_date}
			</div>
			<div className="job_id">{job.job_id}</div>

			<div>
				{/* <strong>end_date</strong>:  */}
				{job.publication_end_date}
			</div>
		</div>
	);
}

// <ExpiredButton job={job} endpoint={apiBaseUrl + expiredEndpoint} />

//     <JobHeader />
//     <ul>
//         <li>publication_end_date: {job.publication_end_date}</li>
//         <li style={{ color: job.is_active ? "green" : "red" }}>
//             {job.is_active ? "IS ACTIVE" : "NOT ACTIVE"}
//         </li>
//         <li>company_logo_file: {job.company_logo_file}</li>
//         {/* <li>slug: {job.slug}</li> */}
//         <li>employment_position_ids: {job.employment_position_ids}</li>
//         <li>employment_grades: {job.employment_grades}</li>
//         <li>contact_person: {job.contact_person}</li>
//         <li>is_paid: {job.is_paid}</li>
//         <li>work_experience: {job.work_experience}</li>
//         <li>language_skills: {job.language_skills}</li>

//         <li>
//             headhunter_application_allowed:
//             {job.headhunter_application_allowed}
//         </li>

function Title({ job }) {
	const isUrlsNotSame = job && job.application_url !== job.external_url;

	return (
		<h3>
			{job && job.title && (
				<div>
					<a href={job.url_en}>{job.title} </a>
					<a href={job.url_api}>| [API]</a>
					{isUrlsNotSame ? (
						<>
							<a href={job.application_url}>
								{" "}
								| [application_url]
							</a>
							<a href={job.external_url}> | [external_url]</a>
						</>
					) : (
						<a href={job.application_url || job.external_url}>
							{" "}
							| [SOURCE]
						</a>
					)}
				</div>
			)}

			{(!job || !job.title || !job.template_profession) && (
				<div>{job && job.template_profession}</div>
			)}
		</h3>
	);
}

function TitleHeader({ job }) {
	return (
		<div className="title">
			<ExpContent
				summary={
					<div>
						<Title job={job} />
						<h5>
							<MdLocationOn /> {job.place}
						</h5>
						<h5>
							<IoMdBusiness /> {job.company_name}
						</h5>
					</div>
				}
				content={
					<>
						<Description job={job} />
					</>
				}
			/>
		</div>
	);
}

function BtnsGroup({ job, onRemove }) {
	return (
		<div className="btns_group">
			<LikeButton job={job} endpoint={apiBaseUrl + likeEndpoint} />
			<DisLikeButton job={job} endpoint={apiBaseUrl + likeEndpoint} />
			<SaveButton job={job} endpoint={apiBaseUrl + saveEndpoint} />
			<ApplyButton job={job} endpoint={apiBaseUrl + applyEndpoint} />
			<CloseButton jobId={job.id} onRemove={onRemove} />
		</div>
	);
}

export default function JobCard({ job, onRemove }) {
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
			<BtnsGroup job={job} onRemove={onRemove} />
		</Card>
	);
}
