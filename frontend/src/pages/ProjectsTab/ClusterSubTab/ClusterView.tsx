

import ClusterGraphs from'./ClusterGraphs';
import ClusterDataTable from'./ClusterDataTable';

import styles from "./ClusterViewStyles.module.css";


///////////////////////////////////////////////////////////////
//            CSS
///////////////////////////////////////////////////////////////


const ClusterView = () => {
	///////////////////////////////////
	///  Inner Handlers
	///////////////////////////////////
	
    
	let url1 = window.location.href;
	let start1 = url1.lastIndexOf('Project/');
    let snippedUrl1 = url1.substring(start1+8);
    let end1 = snippedUrl1.indexOf(':-');
	let project =snippedUrl1.substring(0, end1)
	let url = window.location.href;
    let start = url.lastIndexOf('/Cluster/');
    let snippedUrl = url.substring(start + 9);
    let end = snippedUrl.indexOf('/view');
	let clusterName=decodeURIComponent(snippedUrl.substring(0, end));

	////////////////////////////////////////////////////
	//                HTML
	/////////////////////////////////////////////////
	return (
		<div className={styles.container}>
		  <div className={styles.clusterView}>
			<div className={styles.leftSide}>
			  <ClusterGraphs clusterName={clusterName} project={project} />
			</div>
			<div className={styles.rightSide}>
			  <ClusterDataTable clusterName={clusterName} project={project} />
			</div>
		  </div>
		</div>
	  );
	  
};

export default ClusterView;