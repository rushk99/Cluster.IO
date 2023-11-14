import { useState } from 'react';
import { gql, useQuery } from "@apollo/client";
import { Box } from '@mui/material';
import ClusterOutput from './ClusterOutput';
///////////////////////////////////////////////////////////////
//            CSS
///////////////////////////////////////////////////////////////

import styles from "./ClusterConfigStyles.module.css";


const GET_CLUSTER_CONFIG = gql`
  query getClusterConfig($clusterName: String!) {
    clusteringMethod(name: $clusterName) {
		name label options {
    	name description type default}
    }
  }
`;

function ClusterConfig(props: any) {
    const { project, clusterName } = props;
    const [formData, setFormData] = useState({});
    let [copyformData, setcopyFormData] = useState({});
    const [showDiv2, setShowDiv2] = useState(false);
    const [selectedClusterDataOn, setselectedClusterDataOn] = useState("Hardness"); 
    const { loading, error, data } = useQuery(GET_CLUSTER_CONFIG, {
        variables: { clusterName },
    });

    if (loading) {
        return <div>loading...</div>;
    }
    if (error) {
        return <div>error...</div>;
    }

    const handleChange = (event: any) => {
        setFormData({ ...formData, [event.target.name]: event.target.value });
    };

    const handleClusterDataChange = (event: any) => {
        setselectedClusterDataOn(event.target.value);
    };

    const handleSubmit = (event: any) => {
        console.log("testing columns");
        
        console.log(formData);
        
        event.preventDefault();
        setcopyFormData({ ...formData, selectedClusterDataOn });
        setShowDiv2(true);
    };

    return (
        <div style={{ display: "flex" }}>
            <div style={{ flex: 1 }}>
                <Box
                    display="flex"
                    flexWrap="wrap"
                    borderRadius="30px"
                    className={styles.window}
                >
                    <form onSubmit={handleSubmit}>
                        {data.clusteringMethod.options.map(
                            (option: any, index: any) => (
                                <div className={styles.config}>
                                    <h3>
                                        {index + 1}) Parameter :-{" "}
                                        {option.name}
                                    </h3>
                                    <h5>
                                        Description :-{" "}
                                        {option.description}
                                    </h5>
                                    <h4>
                                        &emsp;&emsp;&emsp;Type :-{" "}
                                        {option.type}
                                    </h4>
                                    <label>
                                        <h4>
                                            &emsp;&emsp;&emsp;Set Parameter:- <br />
                                            &emsp;&emsp;&emsp;(default value = "
                                            {option.default}")<br />
                                            &emsp;&emsp;&emsp;
                                            <input
                                                type="text"
                                                name={option.name}
                                                placeholder={option.default}
                                                onChange={handleChange}
                                            />
                                        </h4>
                                    </label>
                                </div>
                            )
                        )}
                        <div className={styles.config}>
                            <h3>Select Cluster Data On:</h3>
                            <label>
                                <input
                                    type="radio"
                                    value="Hardness"
                                    checked={selectedClusterDataOn === "Hardness"}
                                    onChange={handleClusterDataChange}
                                />
                                &nbsp;Hardness
                            </label>
                            <br />
                            <label>
                                <input
                                    type="radio"
                                    value="Modulus"
                                    checked={selectedClusterDataOn === "Modulus"}
                                    onChange={handleClusterDataChange}
                                />
                                &nbsp;Modulus
                            </label>
                            <br />
                            <label>
                                <input
                                    type="radio"
                                    value="Hard_Mod"
                                    checked={selectedClusterDataOn === "Hard_Mod"}
                                    onChange={handleClusterDataChange}
                                />
                                &nbsp;Hardness & Modulus
                            </label>
                        </div>
                        <br />
                        <button className={styles.clusterButton} type="submit">
                            Perform Clustering!
                        </button>
                    </form>
                </Box>
            </div>
            {showDiv2 && (
                <div style={{ flex: 1 }}>
                    <div className={styles.clusterOutput}>
                        <ClusterOutput
                            fdata={copyformData}
                            cname={clusterName}
                            project={project}
                        />
                    </div>
                </div>
            )}
        </div>
    );
}
export default ClusterConfig;