import React from 'react';
import { Box, Button, FormControl, InputLabel, MenuItem, Select } from '@mui/material';
import ComparisonOutput from './ComparisonOutput';
import "./ComparisonMethodSelectStyles.css"
let method = "";




///////////////////////////////////////////////////////////////
//            CSS
///////////////////////////////////////////////////////////////


const ComparisonMethodSelect = () => {
	///////////////////////////////////
	///  Inner Handlers
	///////////////////////////////////
	let url = window.location.href;
	let start = url.lastIndexOf('Project/');
    let snippedUrl = url.substring(start+8);
    let end = snippedUrl.indexOf(':-');
	let project =snippedUrl.substring(0, end)
	const [showDiv2, setShowDiv2] = React.useState(false);
	//Expands main tabs(shows file name)
	
	const handleComparisonClick = () => {
		setShowDiv2(true);
	};

    const handleComparisonMethodChange = (event: any) => {
		setShowDiv2(false);
        method = event.target.value;
	};
    
	const query = new URLSearchParams(window.location.search);
	const selectedFileNamesQueryParam = query.get("selectedFileNames");
	const selectedFileNames = JSON.parse(decodeURIComponent(selectedFileNamesQueryParam??""));
	const fileNamesString = selectedFileNames.map((name :any) => `${name}`).join(",");
	
	

	////////////////////////////////////////////////////
	//                HTML
	/////////////////////////////////////////////////
	return (
		<div style={{ display: "flex", justifyContent: "space-between" }}>
			<Box borderRadius="30px" className="window">
				<h1>
					Select Comparison Method for: <br />
					{selectedFileNames.map((fileName: any, index: any) => (
						<span key={fileName}>
							<h6>
								{(index + 1)}. {fileName} <br />
							</h6>
						</span>
					))}
				</h1>
	
				<FormControl className="dropDown">
					<InputLabel id="dropdownLabel">Comparison Method</InputLabel>
					<Select labelId="dropdownLabel" onChange={handleComparisonMethodChange}>
						<MenuItem value={"calinski_harabasz_score"}>Calinski Harabasz Score</MenuItem>
						<MenuItem value={"davies_bouldin_score"}>Davies Bouldin Score</MenuItem>
						<MenuItem value={"silhouette_score"}>Silhouette Score</MenuItem>
					</Select>
				</FormControl>
	
				<br></br>
				<Button
					variant="contained"
					size="large"
					className="createButton"
					onClick={() => {
						handleComparisonClick();
					}}
				>
					Compare
				</Button>
			</Box>
			<div style={{ flexGrow: 1 }}>
				{showDiv2 && (
					<div>
						<ComparisonOutput data={{ fileNamesString, method, project }} />
					</div>
				)}
			</div>
		</div>
	);
	
};

export default ComparisonMethodSelect;