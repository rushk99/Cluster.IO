import React from 'react';
import ProjectCreation from './ProjectCreation';
import ProjectTable from './ProjectTable';

import "./OpenProjectStyles.css"


const OpenProject = () => {
	///////////////////////////////////
	///  Inner Handlers
	///////////////////////////////

	//Expands main tabs(shows file name)
	/*
	const handleExpandTab = (index: number) => {


		tabsEnabled[index] = !tabsEnabled[index];
		setOpen(!open);
	};
    */


	////////////////////////////////////////////////////
	//                HTML
	/////////////////////////////////////////////////
	return (
		<div className="container">
			<div className="leftSide" > 
                <ProjectCreation />
		    </div>
		    <div className="rightSide" > 
			    <ProjectTable />
		    </div>
		</div>
	);
};

export default OpenProject;
