import { Box, Button, ListItem, ListItemText, Paper } from '@mui/material';
import ClusterDataRow from './ClusterDataRow';
import { gql, useQuery } from "@apollo/client";
import * as XLSX from 'xlsx';
import "../../loading-animation.css";
import "./ClusterDataTableStyles.css"

const GET_CLUSTER_DATASET = gql`
  query getClusterdATASET($clusterName: String!,$project:String) {
    clusteredDataset(name: $clusterName,pname:$project) {
		x y labeldata cluster 
    }
  }
`;
const GET_CLUSTER_LABEL_NAME = gql`
  query getClusterLabelName($clusterName: String!,$project:String) {
    config(name: $clusterName,pname:$project) {
		label 
    }
  }
`;
const exportToExcel = (data: any) => {
	const worksheet = XLSX.utils.json_to_sheet(data);
	const workbook = XLSX.utils.book_new();
	XLSX.utils.book_append_sheet(workbook, worksheet, 'Sheet1');
	XLSX.writeFile(workbook, 'clusteredDataset.xlsx');
  }
///////////////////////////////////////////////////////////////
//            CSS
///////////////////////////////////////////////////////////////

const ClusterDataTable = (props:any) => {
	///////////////////////////////////
	///  Inner Handlers
	///////////////////////////////////
	  
	let {clusterName, project}=props;
  
	const handelDownload = () => {
	  exportToExcel(data.clusteredDataset);
	}
  
	const getLeftText = (row: any) => {
	  return "(" + row[0] + ", " + row[1] + ")";
	}
	
	const getMidText = (row: any) => {
	  return row[2].toString();
	}
	
	const getRightText = (row: any) => {
	  return row[3].toString();
	}

	const LoadingAnimation = (text:any) => {
		return (
			<div style={{ display: "flex", flexDirection: "column", alignItems: "center" }}>
				<div style={{ backgroundColor: "#c9d9d2", width: "300px", height: "300px", marginBottom: "10px", marginTop: "15px", display: "flex", justifyContent: "center" }}>
					<span style={{ fontSize: "24px", alignSelf: "center", textAlign: "center", display: "flex", alignItems: "center" }}>
					<div className="loading-animation">
						<div className="spinner"></div>
						<p>{text}</p>
					</div>
						
					</span>
				</div>
			</div>
		);
	  };
	const { loading, error, data } = useQuery(GET_CLUSTER_DATASET, {
	  variables: { clusterName, project },
	});
	
	const { data: labeldata, loading: labelloading, error: labelerror } = useQuery(GET_CLUSTER_LABEL_NAME, {
	  variables: { clusterName, project },
	});
	if (loading) {
		 return LoadingAnimation("Clustered Dataset Loading");
	  }
	  
	  if (error) {
		return <div>"error"</div>
	  }
	if (labelloading) {
		return LoadingAnimation("Clustered Dataset Loading");
	}
	
	if (labelerror) {
	  return <div>"error"</div>
	}
	  
	const label= labeldata.config.label;
	  
	
	  
	const dataset: Array<[number, number, number, number]> = [];
	
	data.clusteredDataset.forEach((item:any) => {
	  const { x, y,labeldata, cluster } = item;
	  dataset.push([x, y, labeldata, cluster]);
	});
	
	////////////////////////////////////////////////////
	//                HTML
	//////////////////////////////////////////////////
	
	return (
	  <div>
		<Box className="table">
		  <ListItem className="title">
			<ListItemText disableTypography primary={"Data"} />
		  </ListItem>
		  
		  <div className="title">
			<ClusterDataRow leftText={'X Cord(um), Y Cord(um)'} midText={label} rightText={'Cluster'} />
		  </div>
		  
		  <Paper className='paperStyle'>
			<div className="outlined">
			  {dataset.map((row, index) => (
				<ClusterDataRow leftText={getLeftText(row)} midText={getMidText(row)} rightText={getRightText(row)} />
			  ))}
			</div>
		  </Paper>
		  
		  <Button variant="contained" size="large" className="viewButton" onClick={() => { handelDownload() }}>
			Download Clustered Dataset
		  </Button>
		</Box>
	  </div>
	);
  }; 

export default ClusterDataTable;