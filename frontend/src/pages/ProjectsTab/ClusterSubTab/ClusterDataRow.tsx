
import { ListItemText } from '@mui/material';

///////////////////////////////////////////////////////////////
//            CSS
///////////////////////////////////////////////////////////////
import "./ClusterDataRowStyles.css";
  
  const ClusterDataRow = (props: { leftText: String, midText: String, rightText: String }) => {

  
  
	return (
	  <div>
		<ListItemText disableTypography className="leftSide" primary={props.leftText} />
		<ListItemText disableTypography className="midSide" primary={props.midText} />
		<ListItemText disableTypography className="rightSide" primary={props.rightText} />
	  </div>
	);
  };

export default ClusterDataRow;