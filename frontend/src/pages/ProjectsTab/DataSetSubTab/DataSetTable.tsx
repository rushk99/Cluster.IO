import React from 'react';
import {
  Box,
  Button,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  ListItem,
  ListItemText,
} from '@mui/material';
import { gql, useQuery, useMutation } from "@apollo/client";
import styles from "./DatasetTableStyles.module.css"
import ListItemButton from "@mui/material/ListItemButton"; 
let selectedFile = -1;
let selectedFileName: String="";

const DELETE_DATA = gql`
  mutation DeleteData ($name:String!, $project:String){
    deleteDataset(name: $name, project:$project)
  }
`;

const GET_DATA = gql`
query getDatasets($project: String!) {
  datasets(name: $project) {
	  name 
  }
}
`;



///////////////////////////////////////////////////////////////
//            CSS
///////////////////////////////////////////////////////////////


const DataSetTable = () => {
	///////////////////////////////////
	///  Inner Handlers
	///////////////////////////////////
	let url = window.location.href;
	let start = url.lastIndexOf('Project/');
    let snippedUrl = url.substring(start+8);
    let end = snippedUrl.indexOf('/');
	let project =snippedUrl.substring(0, end)
	const [open, setOpen] = React.useState(true);
	const getData = useQuery(GET_DATA, {
        variables: { project },
    });
	const [deleteData, { data, loading, error }] = useMutation(DELETE_DATA);
	if (getData.loading){
		return <div>loading...</div>
	}
	if (getData.error){
		return <div>error...</div>
	}
	
	const selectDataSet = (text: String, index: number) => {
		selectedFile = index;
		selectedFileName=text;
		setOpen(!open);
	};

	const clusterData = () => {
		console.log("cluster");
	}
    


	////////////////////////////////////////////////////
	//                HTML
	/////////////////////////////////////////////////
	return (
    <Box className={styles.window}>
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
        <TableContainer className={styles.table}>
            <ListItemText style={{ fontSize: 35 }} disableTypography primary={"Existing Data Sets"} />
          <Table>
            <TableBody>
              {getData.data.datasets.map((dataset:any, index:any) => (
                <TableRow
                  key={dataset.name}
                  selected={selectedFile === index}
                  onClick={() => {
                    selectDataSet(dataset.name, index);
                  }}
                >
                  <TableCell>{dataset.name}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
        <div style={{ display: 'flex', justifyContent: 'space-between' }}>
          <a href={selectedFile === -1 ? 'javascript:void(0)' : `/Project/${project}:-${selectedFileName}/Cluster/Home`} style={{ pointerEvents: selectedFile === -1 ? 'none' : 'auto' }}>
            <Button sx={{ float: 'right', marginRight: '15px', marginLeft: '15px', fontSize: '13px' }} variant="contained" disabled={selectedFile === -1} size="large" onClick={() => { clusterData(); }}>
              Perform Cluster
            </Button>
          </a>
          <Button sx={{ float: 'right', marginRight: '15px', marginLeft: '15px', fontSize: '13px' }} variant="contained" disabled={selectedFile === -1} size="large" onClick={(e) => { deleteData({ variables: { name: selectedFileName, project: project } }); }}>
            Delete Dataset
          </Button>
        </div>
      </div>
    </Box>
  );
};

export default DataSetTable;