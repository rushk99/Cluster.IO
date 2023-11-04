import React from 'react';
import DataSetUpload from './DataSetUpload';
import DataSetTable from './DataSetTable';


import "./DatasetHomeStyles.css"


///////////////////////////////////////////////////////////////
//            CSS
///////////////////////////////////////////////////////////////


const DataSetHome = () => {
	///////////////////////////////////
	///  Inner Handlers
	///////////////////////////////////

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
		  <div className="leftSide"> 
			<DataSetUpload />
		  </div>
		  <div className="rightSide"> 
			<DataSetTable />
		  </div>
		</div>
	  );
};

export default DataSetHome;