import Box from '@mui/material/Box';  
import ProjectCreation from './ProjectCreation';
import ProjectTable from './ProjectTable';

import styles from "./OpenProjectStyles.module.css";

const OpenProject = () => {
    
    return (
        <Box className={styles.container} display="flex">
            <Box className={styles.leftSide}>
                <ProjectCreation />
            </Box>
            <Box className={styles.rightSide}>
                <ProjectTable />
            </Box>
        </Box>
    );
};

export default OpenProject;
