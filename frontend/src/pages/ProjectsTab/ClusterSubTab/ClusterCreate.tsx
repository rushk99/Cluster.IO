import { useState } from 'react';
import { Box } from '@mui/material';
import { gql, useQuery } from "@apollo/client";
import ClusterConfig from './ClusterConfig';

///////////////////////////////////////////////////////////////
//            CSS
///////////////////////////////////////////////////////////////

import styles from "./ClusterCreateStyles.module.css";

const GET_CLUSTER = gql`
	query{clusteringMethods{name}}
  `;


const ClusterCreate = (props:any) => {
	///////////////////////////////////
	///  Inner Handlers
	///////////////////////////////////
	const { project } = props;
  	const [selectedOption, setSelectedOption] = useState("");
	//Expands main tabs(shows file name)
	const getCluster = useQuery(GET_CLUSTER);
	const [showDiv2, setShowDiv2] = useState(false);
	if (getCluster.loading){
		return <div>loading...</div>
	}
	if (getCluster.error){
		return <div>error...</div>
	}
	


	////////////////////////////////////////////////////
	//                HTML
	/////////////////////////////////////////////////
	return (
		<div>
		  <Box display="flex" flexWrap="wrap" className={styles.window}>
			<div>
			  <h1 className={styles.title}>Create a New Cluster Configuration</h1>
			  <div className={styles.dropDown}>
				<select value={selectedOption} className={styles.select} onChange={(e) => { setSelectedOption(e.target.value);
																				setShowDiv2(true); }}>
				  <option value="" disabled>--Select a Clustering Algorithm--</option>
				  {getCluster.data.clusteringMethods.map((cluster:any) => (
					<option key={cluster.name} value={cluster.name} className={styles.selectOption}>
					  {cluster.name}
					</option>
				  ))}
				</select>
			  </div>
			</div>
		  </Box>
		  {showDiv2&&(<div>
			<ClusterConfig clusterName={selectedOption} project={project}/>
		  </div>)}
		</div>
	  );
};

export default ClusterCreate;