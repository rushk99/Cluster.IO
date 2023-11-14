
import Paper from '@mui/material/Paper';
import Grid from '@mui/material/Grid';
import Button from '@mui/material/Button';

import styles from './AboutStyles.module.css';


export default function About() {

  return (
    <div className={styles.root}>
		
   
	
<Grid>
        <Grid item xs={12}>
          <Paper className={styles.paper}>

		
		  <h1>About Us</h1>


		  <h5>This research is based on an interdisciplinary effort between the Cote Research Group and Data Science Professor Rodica Neamtu's research group. 
			We use advanced data science techniques to shed light on new insights into materials science and advanced manufacturing. 
			These techniques have provided eye-opening observations that would have been overlooked without this perspective.</h5>
			  
			  <Button type="submit"
            
            variant="contained"
            color="inherit"
			href="https://sites.google.com/view/datadrivenmaterialsscience/team?authuser=0">
			    LEARN MORE ABOUT THE TEAM
				</Button> 
			  </Paper>

			  
        </Grid>
        
      </Grid>
	
    </div>
  );
}