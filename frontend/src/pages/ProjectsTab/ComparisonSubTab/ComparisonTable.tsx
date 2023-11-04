import React  from 'react';
import { Box, ListItem, ListItemText,ListItemButton  } from '@mui/material';

import "./ComparisonTableStyles.css";
const comparisonNames = ["PVC", "AVB", "K Mean V K Nice"];
let selectedComparison = -1;

//TODO atach to backend
function getComparisonNames() {
	return comparisonNames;
}




///////////////////////////////////////////////////////////////
//            CSS
///////////////////////////////////////////////////////////////


const ComparisonTable = () => {
	///////////////////////////////////
	///  Inner Handlers
	///////////////////////////////////
	
	const [open, setOpen] = React.useState(true);
	


	//Expands main tabs(shows file name)
	
	const selectComparison = (text: String, index: number) => {
		selectedComparison = index;
		setOpen(!open);
	};

    


	////////////////////////////////////////////////////
	//                HTML
	/////////////////////////////////////////////////
	return (
		<div>
			<Box className="table">
				<ListItem className="title">
					<ListItemText disableTypography primary={"Existing Comparisons"} />
				</ListItem>
					{getComparisonNames().map((text, index) => (
						<div>
							<ListItemButton
  selected={selectedComparison === index}
  key={text}
  className="comparisonName"
  onClick={() => selectComparison(text, index)}
>
  <ListItemText primary={text} />
</ListItemButton>
						</ div>
					))}
			</Box>
		</div>
	);
};

export default ComparisonTable;