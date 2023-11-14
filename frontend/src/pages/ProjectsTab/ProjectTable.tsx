import React from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Table,
  TableHead,
  TableBody,
  TableRow,
  TableCell,
  ListItem,
  Button,
  ListItemText,
} from '@mui/material';
import { gql, useQuery, useMutation } from "@apollo/client";

import styles from  "./ProjectTableStyles.module.css"

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
	const navigate = useNavigate();
	const buttoncss ={
      float: 'right',
      marginRight: '15px',
      marginLeft: '15px',
      marginTop: '10px',
      fontSize: '13px',
    };

    const viewProject = () => {
		navigate(`/Project/${selectedProjectName}/DataSet/Home/`);
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
		<Box className={styles.window}>
      <ListItem>
        <ListItemText style={{ fontSize: 40 }} disableTypography primary={"Existing Projects"} />
      </ListItem>
      <Table>
        <TableHead>
        </TableHead>
        <TableBody>
          {getData.data.projects.map((dataset:any, index:any) => (
            <TableRow
              key={dataset.name}
              selected={selectedProject === index}
              className={styles.filename}
              onClick={() => {
                selectDataSet(dataset.name, index);
              }}
            >
              <TableCell>{dataset.name}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
  <div style={{ display: 'flex', justifyContent: 'space-between' }}>
  <Button
    variant="contained"
    disabled={selectedProject === -1}
    size="large"
    sx={buttoncss}
    onClick={() => {
      viewProject();
    }}
  >
    View Project
  </Button>

  <Button
    variant="contained"
    disabled={selectedProject === -1}
    size="large"
    sx={buttoncss}
    onClick={(e: any) => {
      deleteData({ variables: { name: selectedProjectName } });
    }}
  >
    Delete Project
  </Button>
</div>

</Box>
	);
};

export default ProjectTable;