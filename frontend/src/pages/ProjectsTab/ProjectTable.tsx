import React from 'react';
import { Box, Button, ListItem, ListItemText } from '@mui/material';
import { gql, useQuery, useMutation } from "@apollo/client";

import "./ProjectTableStyles.css"

let selectedProject = -1;
let selectedProjectName: String="";


const DELETE_DATA = gql`
  mutation DeleteData ($name:String!){
    deleteProject(name: $name)
  }
`;
const GET_DATA = gql`
	{
	projects{
	  name
	}
  }
  `;

///////////////////////////////////////////////////////////////
//            CSS
///////////////////////////////////////////////////////////////


const ProjectTable = () => {
	///////////////////////////////////
	///  Inner Handlers
	///////////////////////////////////
	
	const [open, setOpen] = React.useState(true);

	const [deleteData, { data, loading, error }] = useMutation(DELETE_DATA);


	//Expands main tabs(shows file name)
	
	const selectProject = (text: String, index: number) => {
		selectedProject = index;
		console.log("selectedComparison");
		setOpen(!open);
	};

    const viewProject = () => {
		console.log("cluster");
	}

	const getData = useQuery(GET_DATA);
	if (getData.loading){
		return <div>loading...</div>
	}
	if (getData.error){
		return <div>error...</div>
	}
	const selectDataSet = (text: String, index: number) => {
		selectedProject = index;
		selectedProjectName=text;
		setOpen(!open);
	};
	////////////////////////////////////////////////////
	//                HTML
	/////////////////////////////////////////////////
	return (
		<Box className="window">
		<div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
  <Box className="table">
    <ListItem className="title">
      <ListItemText style={{ fontSize: 40 }} disableTypography primary={"Existing Projects"} />
    </ListItem>
    {getData.data.projects.map((dataset:any ,index:any ) => (
			  <div >
				<ListItem  button selected={selectedProject==index} 
				key={dataset.name} className="filename" onClick={() => { selectDataSet(dataset.name, index) }}>
				  <ListItemText classes={{ primary: "listItemTextLarge" }} primary={dataset.name}  />
				</ListItem>
			  </ div>
			))}
  </Box>
  <div style={{ display: 'flex', justifyContent: 'space-between' }}>
    <a href={"/Project/"+selectedProjectName+"/DataSet/Home"}>
      <Button variant="contained" disabled={selectedProject==-1} size="large" className="viewButton"
        onClick={() => { viewProject() }}>
        View Project
      </Button>
    </a>
	<Button variant="contained" disabled={selectedProject==-1} size="large" className="viewButton" onClick={(e:any) => { deleteData({variables:{name:selectedProjectName}}); }}>
			  Delete Project
	</Button>
  </div>
</div></Box>
	);
};

export default ProjectTable;