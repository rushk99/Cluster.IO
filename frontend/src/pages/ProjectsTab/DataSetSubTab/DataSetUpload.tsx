import React from 'react';
import Box from '@mui/material/Box';
import { gql, useMutation } from "@apollo/client";

import "./DatasetUploadStyles.css"


///////////////////////////////////////////////////////////////
//            CSS
///////////////////////////////////////////////////////////////


const ADD_DATA = gql`
  mutation AddData ($name:String!, $file:Upload!, $description:String!, $project:String){
    uploadDataset(name: $name, file:$file, description:$description, project:$project)
	{
		name
		fileName
		description
		url
	}
  }
`;

const DataSetUpload = () => {
	///////////////////////////////////
	///  Inner Handlers
	///////////////////////////////////
	//const [open, setOpen] = React.useState(true);
	let url = window.location.href;
	let start = url.lastIndexOf('Project/');
    let snippedUrl = url.substring(start+8);
    let end = snippedUrl.indexOf('/');
	let project =snippedUrl.substring(0, end)
	const [name, setName] = React.useState('');
  	const [description, setDescription] = React.useState('');
  	const [file, setFile] = React.useState< File | null>(null);
	const [addData, { data, loading, error }] = useMutation(ADD_DATA);
	const [err, setErr] = React.useState('');



	const handleNameChange = (e:any) => {
		const value = e.target.value;
		
		if (value.includes(' ') || value.includes('/')) {
		  setErr('Dataset name cannot contain spaces or forward slashes "/"');
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
			<h1 className="title">Upload New Data Set</h1>
			<form
			  className="form"
			  onSubmit={(e: any) => {
				e.preventDefault();
				addData({
				  variables: { name: name, description: description, file: file , project: project},
				});
			  }}
			>
			  <label className="label" htmlFor="name">
				Name:
			  </label>

				<input className="input" type="text" id="name" value={name} onChange={handleNameChange} />
							
				{err && <div style={{ color: 'red' }}>{err}</div>}



			  <label className="label" htmlFor="description">
				Description:
			  </label>
			  <textarea
				className="input"
				id="description"
				value={description}
				onChange={(e) => setDescription(e.target.value)}
			  />
			  <label className="label" htmlFor="file">
				Choose a file
			  </label>
			  <div>
				<input
				  className="fileInput"
				  type="file"
				  id="file"
				  onChange={(e: any) => {
					setFile(e.target.files[0]);
}}
/>
<label htmlFor="file" className="uploadButton">
Browse...
</label>
</div>
{file && (
<p className="fileName">
File Selected: <strong>{file.name}</strong>
</p>
)}
<button className="button" type="submit" disabled={!isNameValid}>
Upload
</button>
</form>
</Box>

  </div>
);
};


export default DataSetUpload;


