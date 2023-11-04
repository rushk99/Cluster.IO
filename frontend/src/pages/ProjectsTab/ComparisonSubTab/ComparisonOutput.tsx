
import { Box, Button, ListItem, ListItemText,FormControl, InputLabel, MenuItem, Select } from '@mui/material';
import { gql, useQuery } from "@apollo/client";

import "../../loading-animation.css";


import "./ComparisonOutputStyles.css";

const GET_CLUSTER_COMPARISON = gql`
  query getClustercOMPARISON($fileNamesString: String!,$method:String , $project:String) {
    clusterComparisons(list: $fileNamesString,metric:$method,pname:$project) {
		clustername metric score 
    }
  }
`;
const GET_CLUSTERED_DATA_URL = gql`
  query getClusteredDataURL( $clustername: String!) {
    config(name:$clustername){
      clusteredData
    
}
  }
`;
function ImageFromConfigName(props: any) {
    let  clustername  = props.name;
        
    
    
    const { loading, error, data } = useQuery(GET_CLUSTERED_DATA_URL, {
        variables: { clustername },
    });
    
    
    
    if (loading) {
        return <div>loading...</div>
    }
    if (error){
        return <div>error...</div>
    
    }
    const imageUrl=`data:image/png;base64,${data.config.clusteredData}`;
    
    
    return <div><img src={imageUrl} alt="clustered-data.png" /></div>}


    const LoadingAnimation = (text:any) => {
        return (
            <div style={{ display: "flex", flexDirection: "column", alignItems: "center" }}>
                <div style={{ backgroundColor: "#c9d9d2", width: "500px", height: "500px", marginBottom: "10px", marginTop: "15px", display: "flex", justifyContent: "center" }}>
                    <span style={{ fontSize: "24px", alignSelf: "center", textAlign: "center", display: "flex", alignItems: "center" }}>
                    <div className="loading-animation">
                        <div className="spinner"></div>
                        <p>{text}</p>
                    </div>
                        
                    </span>
                </div>
            </div>
        );
      };

function ComparisonOutput(props: any) {
    let { fileNamesString,method ,project} = props.data;
        
    
    const { loading, error, data } = useQuery(GET_CLUSTER_COMPARISON, {
        variables: { fileNamesString,method ,project},
    });
      
    if (loading) {
        return <div><Box  className="table">
            {LoadingAnimation("Loading Comparison Results")}
            
        </Box></div>
    }
    if (error){
        return <div>error...</div>
    }
    
    return <div><Box  className="table">
        <ListItem key="title" className="title">
            <ListItemText style ={{fontSize:34}} disableTypography primary={"Comparison Results"} />
        </ListItem>
            {data.clusterComparisons.map((clusterComparison:any, index:any) => (
                <div  >
                    
                    <ListItem 
                    key={clusterComparison.clustername} className="clusterName" >
                        <ListItemText    primary={`${index + 1}) ${clusterComparison.clustername}`} />
                        
                    </ListItem>
                    {/* <ListItem  
                    key={clusterComparison.clustername} className={classes.clusterName} >
                        <ImageFromConfigName
                        name={clusterComparison.clustername}
                    />
                        
                    </ListItem> */}
                    <ListItem key={`${clusterComparison.metric}-${clusterComparison.score}`} className="clusterName">
  <ListItemText  primary={< h1 style={{ fontSize:20}}>{clusterComparison.metric}:- </h1>} secondary={<strong style={{color: 'black' ,fontSize:20}}>{Number(clusterComparison.score).toFixed(2)}</strong>} />
</ListItem>

                    <hr className="hr" />
                </ div>
            ))}
</Box></div>
    }



export default ComparisonOutput;