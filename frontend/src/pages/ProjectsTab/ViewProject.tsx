import ProjectTopbar from './ProjectTopbar';
import {  Routes , Route } from 'react-router-dom';
import DataSetHome from './DataSetSubTab/DataSetHome';
import ClusterHome from './ClusterSubTab/ClusterHome';
import ComparisonHome from './ComparisonSubTab/ComparisonHome';
import ClusterView from './ClusterSubTab/ClusterView';
import NewComparisonCreation from './ComparisonSubTab/NewComparisonTab'



function getProjectName():String{
	let url = window.location.href;
	let start = url.lastIndexOf('Project/');
	let snippedUrl = url.substring(start+8);
	let end = snippedUrl.indexOf('/');

	return snippedUrl.substring(0, end);
}


function getClusterName():String{
	let url = window.location.href;
	let start = url.lastIndexOf('/Cluster/');
	if(start==-1){
		return "not a cluster tab";
	}
	let snippedUrl = url.substring(start+9);
	let end = snippedUrl.indexOf('/view');
	return decodeURIComponent(snippedUrl.substring(0, end));
}



const ViewProject = () => {
	const topbarStyle = {
    height: 60,
    cursor: "pointer", // Add cursor style to make it look clickable
  };
	return (
		<div>
			<div style={topbarStyle} onClick={()=>{getProjectName()}} >
				<ProjectTopbar projName={ getProjectName()} />
			</div>
			<div >
				<Routes>
					<Route path={'/DataSet/Home/'} element={<DataSetHome />}/>
					<Route path={'/Cluster/Home/'} element={<ClusterHome />} />
					<Route path={'/Comparison/Home/'} element={<ComparisonHome />} />
					<Route path={'/Comparison/New/'} element={<NewComparisonCreation />}/>
					<Route path={'/Cluster/'+getClusterName()+'/view'} element={<ClusterView />} />
				</Routes>
			</div>
		</div>
	);
};


export default ViewProject;
