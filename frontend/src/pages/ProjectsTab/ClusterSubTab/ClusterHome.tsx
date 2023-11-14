
import ClusterCreate from './ClusterCreate';
import ClusterTable from './ClusterTable';

import styles from "./ClusterHomeStyles.module.css";

///////////////////////////////////////////////////////////////
//            CSS
///////////////////////////////////////////////////////////////

const ClusterHome = () => {
	///////////////////////////////////
	///  Inner Handlerss
	///////////////////////////////////
	let url = window.location.href;
	let start = url.lastIndexOf('Project/');
    let snippedUrl = url.substring(start+8);
    let end = snippedUrl.indexOf(':-');
	let project =snippedUrl.substring(0, end)

	////////////////////////////////////////////////////
	//                HTML
	/////////////////////////////////////////////////
	return (
		<div >
			<div className={styles.leftSide} > 
                <ClusterCreate project={project} />
		    </div>
		    <div className={styles.rightSide} > 
			    <ClusterTable project={project}/>
		    </div>
		</div>
	);
};

export default ClusterHome;