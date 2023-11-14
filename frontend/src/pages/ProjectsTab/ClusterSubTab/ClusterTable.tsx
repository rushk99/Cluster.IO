import React from 'react';
import { Box, Button, ListItem, ListItemText } from '@mui/material';
import CheckBoxOutlineBlankIcon from '@mui/icons-material/CheckBoxOutlineBlank';
import CheckBoxIcon from '@mui/icons-material/CheckBox';
import ListItemButton from "@mui/material/ListItemButton"; 
import {useNavigate}  from "react-router-dom";
import { gql, useQuery, useMutation } from "@apollo/client";

import styles from "./ClusterTableStyles.module.css";
let clusterSelected = [false, false,false,false, false, false, false, false, false, false, false, false];
let numSelected = 0;
let selectedFileName: string="";
let selectedFileNames: string[] = [];
let displayButton = true;
const DELETE_CONFIG = gql`
  mutation DeleteConfig ($name:String!, $datasetName:String!, $project:String!){
    deleteConfig(name: $name, datasetName:$datasetName, project:$project)
  }
`;
const GET_CONFIG = gql`
	query getclusters($project: String!) {
  configs(name: $project) {
	  name 
  }
}
  `;

const GET_DATA = gql`
query getclusters($project: String!) {
  configs(name: $project) {
	  name 
  }
}
`;

function getClusterSelected() {
	return clusterSelected;
}





///////////////////////////////////////////////////////////////
//            CSS
///////////////////////////////////////////////////////////////


const ClusterTable = (props:any) => {
	///////////////////////////////////
	///  Inner Handlers
	///////////////////////////////////
	const { project } = props;
	let url = window.location.href;
	let start = url.lastIndexOf(':-');
    let snippedUrl = url.substring(start+2);
    let end = snippedUrl.indexOf('/');
	let datasetName =snippedUrl.substring(0, end)
	
	const init = () => {
		const pathname = window.location.pathname;
		if(pathname.indexOf('/Cluster') == -1){
			displayButton = false;
		}else{
			displayButton = true;
		}
	};

	let history = useNavigate();
	const [open, setOpen] = React.useState(true);
	init();


	//Expands main tabs(shows file name)


	const selectCluster = (text: string, index: number) => {
		clusterSelected[index] = !clusterSelected[index];
		if (clusterSelected[index]){
			numSelected = numSelected + 1;
			selectedFileName=text;
			selectedFileNames.push(text);
		}else{
			numSelected = numSelected -1;
			selectedFileNames = selectedFileNames.filter(name => name !== text);
		}
		setOpen(!open);
	};

	const viewCluster = (text: String) => {
		const pathname = window.location.pathname;
		let url=pathname.substring(0, pathname.lastIndexOf('/')+1) + text + "/view";
		window.location.href = url;
	};

	const compareClusters = () => {
		const selectedFileNamesQueryParam = encodeURIComponent(JSON.stringify(selectedFileNames));
		const pathname = window.location.pathname;
		let url = pathname.substring(0, pathname.lastIndexOf('/Cluster')) + "/Comparison/New?selectedFileNames=" + selectedFileNamesQueryParam;
		window.location.href = url;
	  };
    
	const [deleteConfig, { data, loading, error }] = useMutation(DELETE_CONFIG);
	const getConfig = useQuery(GET_CONFIG, {
        variables: { project },
    });
	if (getConfig.loading){
		return <div>loading...</div>
	}
	if (getConfig.error){
		return <div>error...</div>
	}
	////////////////////////////////////////////////////
	//                HTML
	//onClick={() => { selectCluster(text, index) }}
	/////////////////////////////////////////////////
		return (
  <div>
    <Box className={styles.table}>
      <ListItem key="title" className={styles.title}>
        <ListItemText disableTypography primary={"Existing Cluster Configurations"} />
      </ListItem>
      {getConfig.data.configs.map((config:any, index:any) => (
        <div key={config.name}>
          <ListItemButton
            className={styles.clusterName}
            
            onClick={() => {
              selectCluster(config.name, index);
            }}
          >
            <ListItemText primary={config.name} />
            {getClusterSelected()[index] ? <CheckBoxIcon /> : <CheckBoxOutlineBlankIcon />}
          </ListItemButton>
        </div>
      ))}
      {displayButton ?<div>
        <div style={{ display: 'flex', justifyContent: 'space-between' }}>
          <Button variant="contained" disabled={numSelected < 2} size="large" className={styles.compareButton} onClick={() => { compareClusters(); }}>
            Compare Clusters
          </Button>
          <Button variant="contained" disabled={numSelected !== 1} size="large" className={styles.compareButton} onClick={(e) => {
            e.preventDefault();
            deleteConfig({ variables: { name: selectedFileName, datasetName: datasetName, project: project } });
          }}>
            Delete Cluster
          </Button>
		  
        </div><div className={styles.compareButton2}><Button variant="contained" disabled={numSelected !== 1} size="large"  onClick={() => {
              viewCluster(selectedFileName);
            }}>
            View Cluster
          </Button> </div></div>: <br></br>}
    </Box>
  </div>
);
};

export default ClusterTable;
