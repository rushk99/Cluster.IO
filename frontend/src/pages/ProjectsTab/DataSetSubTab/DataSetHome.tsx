import DataSetUpload from './DataSetUpload';
import DataSetTable from './DataSetTable';


import styles from "./DatasetHomeStyles.module.css"


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
		<div className={styles.container}>
		  <div className={styles.leftSide}> 
			<DataSetUpload />
		  </div>
		  <div className={styles.rightSide}> 
			<DataSetTable />
		  </div>
		</div>
	  );
};

export default DataSetHome;