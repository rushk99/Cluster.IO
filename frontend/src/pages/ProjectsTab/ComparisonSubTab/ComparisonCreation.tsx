import { Box, Button } from '@mui/material';
import AddIcon from '@mui/icons-material/Add';

import "./ComparisonCreationStyles.css";

///////////////////////////////////////////////////////////////
//            CSS
///////////////////////////////////////////////////////////////


const ComparisonCreation = () => {
	///////////////////////////////////
	///  Inner Handlers
	///////////////////////////////////

	//Expands main tabs(shows file name)
	
	const handleCreationClick = () => {
		console.log("works");
	};
    


	////////////////////////////////////////////////////
	//                HTML
	/////////////////////////////////////////////////
	return (
		<div>
			<Box borderRadius="30px" className="window">
				<h1 className="text">Create New Comparison</h1>
				<Button variant="contained" size="large" endIcon={<AddIcon />} 
				className="createButton" onClick={() => { handleCreationClick() }}>
					New
				</Button>
			</Box>
		</div>
	);
};

export default ComparisonCreation;