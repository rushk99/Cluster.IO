import React from 'react';
import Box from '@mui/material/Box';
import { gql, useMutation } from "@apollo/client";
 import "./ProjectCreationStyles.css"


const ADD_DATA = gql`
  mutation AddData ($name:String!){
    createProject(name: $name)
	{
		name
	}
  }
`;

const ProjectCreation = () => {
	///////////////////////////////////
	///  Inner Handlers
	///////////////////////////////////
	//const [open, setOpen] = React.useState(true);
	const [name, setName] = React.useState('');
	const [addData, { data, loading, error }] = useMutation(ADD_DATA);
	const [err, setErr] = React.useState('');



	const handleNameChange = (e:any) => {
		const value = e.target.value;
		
		if (value.includes(' ') || value.includes('/')) {
		  setErr('Project name cannot contain spaces or forward slashes "/"');
		}
		 else {
		  setErr('');
		}
		setName(value);
	  };
	  const isNameValid = !(name.includes(' ') || name.includes('/'));
	////////////////////////////////////////////////////
	//                HTML
	/////////////////////////////////////////////////
	return (
		<div>
		  <Box className="window">
			<h1 className="title">Create New Project</h1>
			<form
			  className="form"
			  onSubmit={(e: any) => {
				e.preventDefault();
				addData({
				  variables: { name: name},
				});
			  }}
			>
			  <label className="label" htmlFor="name">
				Name:
			  </label>
			  <input className="input" type="text" id="name" value={name} onChange={handleNameChange} />
			  
        		{err && <div style={{ color: 'red' }}>{err}</div>}
<button className="button" type="submit" disabled={!isNameValid}>
Create
</button>
</form>
</Box>

  </div>
);
};


export default ProjectCreation;

