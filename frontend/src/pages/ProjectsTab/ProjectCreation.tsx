import React from 'react';
import Box from '@mui/material/Box';
import { gql, useMutation } from "@apollo/client";
import styles from "./ProjectCreationStyles.module.css"


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
		  <Box className={styles.window}>
			<h1 className={styles.title}>Create New Project</h1>
			<form
			  className={styles.form}
			  onSubmit={(e: any) => {
				e.preventDefault();
				addData({
				  variables: { name: name},
				});
				setTimeout(() => window.location.reload(), 200);
			  }}
			>
			  <label className={styles.label} htmlFor="name">
				Name:
			  </label>
			  <input className={styles.input} type="text" id="name" value={name} onChange={handleNameChange} />
			  
        		{err && <div style={{ color: 'red' }}>{err}</div>}
<button className={styles.button} type="submit" disabled={!isNameValid}>
Create
</button>
</form>
</Box>

  </div>
);
};


export default ProjectCreation;

