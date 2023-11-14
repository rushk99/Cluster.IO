import React from 'react';
import {  Button} from '@mui/material';
import ArrowBack from '@mui/icons-material/ArrowBack';
import ArrowForward from '@mui/icons-material/ArrowForward';
import { gql, useQuery } from "@apollo/client";


import "../../loading-animation.css";


const GET_CLUSTER_OUTPUT = gql`
  query getClusterOutput($clusterName: String!, $project:String) {
    config(name: $clusterName,pname:$project) {
		rawData clusteredData clustersFractions 
    }
  }
`;




///////////////////////////////////////////////////////////////
//            CSS
///////////////////////////////////////////////////////////////

const LoadingAnimation = (text:any) => {
    return (
        <div style={{ display: "flex", flexDirection: "column", alignItems: "center" }}>
            <div style={{ backgroundColor: "#c9d9d2", width: "300px", height: "300px", marginBottom: "10px", marginTop: "15px", display: "flex", justifyContent: "center" }}>
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
const downloadImage = (src: string, filename: string) => {
    const anchor = document.createElement('a');
    anchor.href = src;
    anchor.download = filename;
    document.body.appendChild(anchor);
    anchor.click();
    document.body.removeChild(anchor);
  };
  const ClusterGraphs = (props: any) => {
    let { clusterName, project } = props;
    const [imageIndex, setImageIndex] = React.useState(0);
    const imageLabels = ["Raw Data", "Clustered Data", "Clusters Fractions"];
    const { loading, error, data } = useQuery(GET_CLUSTER_OUTPUT, {
        variables: { clusterName ,project },
    });

    if (loading) {
        return LoadingAnimation("Cluster Graphs Loading");
    }

    if (error) {
        return <div>"error"</div>
    }

    const imageSources = [
        `data:image/png;base64,${data.config.rawData}`,
        `data:image/png;base64,${data.config.clusteredData}`,
        `data:image/png;base64,${data.config.clustersFractions}`
    ];

    const handleImageBack = () => {
        setImageIndex((imageIndex + 2) % 3);
    };

    const handleImageForward = () => {
        setImageIndex((imageIndex + 1) % 3);
    };

    const handleDownloadImage = (index: number) => {
        downloadImage(imageSources[index], `${clusterName}_${imageLabels[index]}.png`);
    };

    return (
        <div>
            <img src={imageSources[imageIndex]} className="image" alt={imageLabels[imageIndex]} />
            <br />
            <Button className="arrowButton" onClick={handleImageBack}>
                <ArrowBack fontSize="large" />
            </Button>
            <Button className="arrowButton" onClick={handleImageForward}>
                <ArrowForward fontSize="large" />
            </Button><br />
            <Button className="downloadButton" variant="contained" color="primary" onClick={() => handleDownloadImage(imageIndex)}>
                Download {imageLabels[imageIndex]}
            </Button>
        </div>
    );
};

export default ClusterGraphs;