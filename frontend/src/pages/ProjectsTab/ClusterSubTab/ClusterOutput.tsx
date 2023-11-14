import { useState , memo } from 'react';
import { gql, useQuery,useMutation  } from "@apollo/client";
import "../../loading-animation.css";
//////////////////////////////////////////////



const GET_KMEANS_OUTPUT = gql`
  query getKMeansOutput( $numClusters: String!, $randomState: String!, $datasetName:String!, $clusterDataOn:String!, $project:String) {
    clusteringMethod(name:"KMeans"){
  ...on KMeans{
    cluster(numClusters:$numClusters randomState:$randomState datasetName:$datasetName clusterDataOn:$clusterDataOn project:$project){
      error
      rawData
      clusteredData
      clustersFractions
    }
  }
}
  }
`;

const GET_FUZZYCMEANS_OUTPUT = gql`
  query getFuzzycmeansOutput( $numClusters: String!, $fuzzifier: String!, $datasetName:String!, $clusterDataOn:String!, $project:String) {
    clusteringMethod(name:"Fuzzycmeans"){
  ...on Fuzzycmeans{
    cluster(numClusters:$numClusters fuzzifier:$fuzzifier datasetName:$datasetName clusterDataOn:$clusterDataOn project:$project){
      error
      rawData
      clusteredData
      clustersFractions
    }
  }
}
  }
`;

const GET_GAUSSIANMIXTUREMODEL_OUTPUT = gql`
  query getGaussianmixturemodelOutput( $numClusters: String!, $datasetName:String!, $clusterDataOn:String!, $project:String) {
    clusteringMethod(name:"GaussianMixtureModel"){
  ...on GaussianMixtureModel{
    cluster(numClusters:$numClusters datasetName:$datasetName clusterDataOn:$clusterDataOn project:$project){
      error
      rawData
      clusteredData
      clustersFractions
    }
  }
}
  }
`;


const GET_Birch_OUTPUT = gql`
  query getBirchOutput( $numClusters: String!,$threshold: String! ,$branchingFactor: String!,$datasetName:String!, $clusterDataOn:String!, $project:String) {
    clusteringMethod(name:"Birch"){
  ...on Birch{
    cluster(numClusters:$numClusters threshold:$threshold branching_factor:$branchingFactor datasetName:$datasetName clusterDataOn:$clusterDataOn project:$project){
      error
      rawData
      clusteredData
      clustersFractions
    }
  }
}
  }
`;
const GET_Agglomerative_OUTPUT = gql`
  query getAgglomerativeOutput( $numClusters: String!,$linkage:String! $datasetName:String!, $clusterDataOn:String!, $project:String) {
    clusteringMethod(name:"Agglomerative"){
  ...on Agglomerative{
    cluster(numClusters:$numClusters linkage:$linkage datasetName:$datasetName clusterDataOn:$clusterDataOn project:$project){
      error
      rawData
      clusteredData
      clustersFractions
    }
  }
}
  }
`;

const GET_DBSCAN_OUTPUT = gql`
  query getDBSCANOutput( $eps: String!,$minSamples:String! $algorithm: String! $datasetName:String!, $clusterDataOn:String!, $project:String) {
    clusteringMethod(name:"DBSCAN"){
  ...on DBSCAN{
    cluster(eps:$eps minSamples:$minSamples algorithm:$algorithm datasetName:$datasetName clusterDataOn:$clusterDataOn project:$project){
      error
      rawData
      clusteredData
      clustersFractions
    }
  }
}
  }
`;

const GET_Deconvolution_OUTPUT = gql`
  query getDeconvolutionOutput( $mVal: String!,$maxIter:String! $limit: String!  $datasetName:String!, $clusterDataOn:String!, $project:String) {
    clusteringMethod(name:"Deconvolution"){
  ...on Deconvolution{
    cluster(mVal:$mVal maxIter:$maxIter limit:$limit  datasetName:$datasetName clusterDataOn:$clusterDataOn project:$project){
      error
      rawData
      clusteredData
      clustersFractions
    }
  }
}
  }
`;

const GET_KMedoids_OUTPUT = gql`
  query getKMedoidsOutput( $numClusters: String!, $init:String! $randomState: String!, $datasetName:String!, $clusterDataOn:String!, $project:String) {
    clusteringMethod(name:"KMedoids"){
  ...on KMedoids{
    cluster(numClusters:$numClusters init:$init randomState:$randomState datasetName:$datasetName clusterDataOn:$clusterDataOn project:$project){
      error
      rawData
      clusteredData
      clustersFractions
    }
  }
}
  }
`;

const GET_OPTICS_OUTPUT = gql`
  query getOPTICSOutput( $max_eps: String!,$minSamples:String! $algorithm: String! $datasetName:String!, $clusterDataOn:String!, $project:String) {
    clusteringMethod(name:"OPTICS"){
  ...on OPTICS{
    cluster(maxEps:$max_eps minSamples:$minSamples algorithm:$algorithm datasetName:$datasetName clusterDataOn:$clusterDataOn project:$project){
      error
      rawData
      clusteredData
      clustersFractions
    }
  }
}
  }
`;

const GET_Spectral_OUTPUT = gql`
  query getSpectralOutput( $numClusters: String!,$assignLabels: String!, $affinity:String! $randomState: String!, $datasetName:String!, $clusterDataOn:String!, $project:String) {
    clusteringMethod(name:"Spectral"){
  ...on Spectral{
    cluster(numClusters:$numClusters assignLabels:$assignLabels affinity:$affinity randomState:$randomState datasetName:$datasetName clusterDataOn:$clusterDataOn project:$project){
      error
      rawData
      clusteredData
      clustersFractions
    }
  }
}
  }
`;
const ADD_CONFIG = gql`
  mutation AddConfig ($name:String!, $parameters:String!, $datasetName:String!,$label:String!, $project:String){
    uploadConfig(name:$name, parameters:$parameters, datasetName:$datasetName,label:$label, project:$project)
	{
		name
    parameters{name value}
    datasetName 
    rawData
    clusteredData
    clustersFractions
	}
  }
`;
function RenderOutput(props: any) {
  let { clustering,configData,clusterDataOn, project} = props.data;
  const datasetName=configData.datasetName
  let configDataString = JSON.stringify(configData);
  const [configName, setConfigName] = useState('');
  const rawDataUrl = clustering.clusteringMethod.cluster.rawData;
  const clusteredDataUrl = clustering.clusteringMethod.cluster.clusteredData;
  const clustersFractionsUrl = clustering.clusteringMethod.cluster.clustersFractions;
  const [addConfig, { data, loading, error }] = useMutation(ADD_CONFIG);
  const [err, setErr] = useState('');
  const downloadImage = (url: string, imageName: string) => {
    const link = document.createElement("a");
    link.download = imageName;
    link.href = url;
    link.click();
  };

  const ImageWithDownloadButton = ({
    imageUrl,
    imageName,
  }: {
    imageUrl: string;
    imageName: string;
  }) => {
    const imageSrc = `data:image/png;base64,${imageUrl}`;
  
    return (
      <div style={{ alignItems: "center" , marginBottom:20}}>
        <img src={imageSrc} alt={imageName} style={{ height: "170%", width: "170%", border: "1px solid black" }} />
        <button style={{ width: "120%", marginLeft:60}} onClick={() => downloadImage(imageSrc, imageName)}>
          Download {imageName}
        </button>
      </div>
    );
  };
  const handleNameChange = (e:any) => {
		const value = e.target.value;
		
		if (value.includes(' ') || value.includes('/')) {
		  setErr('Config name cannot contain spaces or forward slashes "/"');
		}
		 else {
		  setErr('');
		}
		setConfigName(value);
	  };
	  const isNameValid = !(configName.includes(' ') || configName.includes('/'));

  return (
    <div >
      <br />
      <div >
        <ImageWithDownloadButton
          imageUrl={rawDataUrl}
          imageName="raw-data.png"
        />
      </div>
      <div >
        <ImageWithDownloadButton
          imageUrl={clusteredDataUrl}
          imageName="clustered-data.png"
        />
      </div>
      <div  >
        <ImageWithDownloadButton
          imageUrl={clustersFractionsUrl}
          imageName="clusters-fractions.png"
        />
      </div>
      <br />
      <label htmlFor="config-name">Enter configuration name: </label>

      <input  type="text" id="config-name" name="config-name" onChange={handleNameChange} /><br /><br />
							
				{err && <div style={{ color: 'red' }}>{err}</div>}

      <button disabled={!isNameValid} onClick={(e:any) => {
          e.preventDefault();
          addConfig({variables:{name:configName,  parameters:configDataString, datasetName:datasetName,label:clusterDataOn, project:project}});
          setTimeout(() => window.location.reload(), 200);
        }}>Save configuration</button>
    </div>
  );

}


const LoadingAnimation = (text:any) => {
  return (
    <div className="loading-animation">
      <div className="spinner"></div>
      <p>{text}</p>
    </div>
  );
};

function RenderLoading(){
  return (
    <div style={{ display: "flex", flexDirection: "column", alignItems: "center" }}>
        <div style={{ backgroundColor: "#c9d9d2", width: "300px", height: "900px", marginBottom: "10px", marginTop: "15px", display: "flex", justifyContent: "center" }}>
            <span style={{ fontSize: "24px", alignSelf: "center", textAlign: "center", display: "flex", alignItems: "center" }}>
                <span>{LoadingAnimation("Performing Clustering")} </span>
            </span>
        </div>
    </div>
)



}


function RenderKMeans(props:any){

    let configData= props.data;
    const numClusters=configData.numClusters;
    const randomState=configData.randomState;
    const datasetName=configData.datasetName;
    const clusterDataOn=configData.clusterDataOn;
    const project=configData.project;
    console.log("testing renderkmeans");
    console.log(props.data);
    const { loading, error, data } = useQuery(GET_KMEANS_OUTPUT, {
        variables: { numClusters,randomState ,datasetName ,clusterDataOn , project},
      });
    let clustering =data;
    if (loading) {
      return <RenderLoading/>
    
    }
    if (error) {
        return <div>Error</div>
    }
    
    return <RenderOutput  data={{ clustering, configData,clusterDataOn,project}} />

}



function RenderFuzzycmeans(props:any){

  let configData= props.data;
  const numClusters=configData.numClusters;
  const fuzzifier=configData.fuzzifier;
  const datasetName=configData.datasetName;
  const clusterDataOn=configData.clusterDataOn;
  const project=configData.project;
  const { loading, error, data } = useQuery(GET_FUZZYCMEANS_OUTPUT, {
      variables: { numClusters,fuzzifier ,datasetName ,clusterDataOn , project},
    });
  let clustering =data;
  if (loading) {
    return <RenderLoading/>
  
  }
  if (error) {
      return <div>Error</div>
  }
  
  return <RenderOutput  data={{ clustering, configData,clusterDataOn,project}} />

}

function RenderGaussianmixturemodel(props:any){

  let configData= props.data;
  const numClusters=configData.numClusters;
  const datasetName=configData.datasetName;
  const clusterDataOn=configData.clusterDataOn;
  const project=configData.project;
  const { loading, error, data } = useQuery(GET_GAUSSIANMIXTUREMODEL_OUTPUT, {
      variables: { numClusters,datasetName ,clusterDataOn , project},
    });
  let clustering =data;
  if (loading) {
    return <RenderLoading/>
  
  }
  if (error) {
      return <div>Error</div>
  }
  
  return <RenderOutput  data={{ clustering, configData,clusterDataOn,project}} />

}


function RenderBirch(props:any){

  let configData= props.data;
    const numClusters=configData.numClusters;
    const datasetName=configData.datasetName;
    const clusterDataOn=configData.clusterDataOn;
    const threshold=configData.threshold;
    const branchingFactor=configData.branchingFactor
    const project=configData.project;
    const { loading, error, data } = useQuery(GET_Birch_OUTPUT, {
      variables: { numClusters,threshold ,branchingFactor,datasetName,clusterDataOn , project},
    });
    let clustering =data;
  if (loading) {
    return <RenderLoading/>
  }
  if (error) {
      return <div>Error</div>
  }
  return <RenderOutput  data={{ clustering, configData,clusterDataOn,project}} />
}

function RenderAgglomerative(props:any){


  let configData= props.data;
    const numClusters=configData.numClusters;
    const datasetName=configData.datasetName;
    const linkage=configData.linkage;
    const clusterDataOn=configData.clusterDataOn;
    const project=configData.project;
    const { loading, error, data } = useQuery(GET_Agglomerative_OUTPUT, {
        variables: { numClusters, linkage ,datasetName,clusterDataOn , project},
      });
      let clustering =data;
    if (loading) {
      return <RenderLoading/>
    }
    if (error) {
        return <div>Error</div>
    }
    return <RenderOutput  data={{ clustering, configData,clusterDataOn,project}} />

}

function RenderDBSCAN(props:any){

  let configData= props.data;
  const eps=configData.eps;
  const datasetName=configData.datasetName;
  const minSamples=configData.minSamples;
  const algorithm=configData.algorithm;
  const clusterDataOn=configData.clusterDataOn;
  const project=configData.project;
  const { loading, error, data } = useQuery(GET_DBSCAN_OUTPUT, {
      variables: { eps,minSamples,algorithm ,datasetName,clusterDataOn , project},
    });
    let clustering =data;
  if (loading) {
    return <RenderLoading/>
  }
  if (error) {
      return <div>Error</div>
  }
  return <RenderOutput  data={{ clustering, configData,clusterDataOn,project}} />

}

function RenderDeconvolution(props:any){

  let configData= props.data;
  const mVal=configData.mVal;
  const datasetName=configData.datasetName;
  const maxIter=configData.maxIter;
  const limit=configData.limit;
  const label=configData.label;
  const clusterDataOn=configData.clusterDataOn;
  const project=configData.project;
  
  const { loading, error, data } = useQuery(GET_Deconvolution_OUTPUT, {
      variables: { mVal,maxIter,limit,label ,datasetName,clusterDataOn , project},
    });
    let clustering =data;
  if (loading) {
    return <RenderLoading/>
  }
  if (error) {
      return <div>Error</div>
  }
  return <RenderOutput  data={{ clustering, configData,clusterDataOn,project}} />

}

function RenderKMedoids(props:any){

  let configData= props.data;
  const numClusters=configData.numClusters;
  const datasetName=configData.datasetName;
  const init=configData.init;
  const randomState=configData.randomState;
  const clusterDataOn=configData.clusterDataOn;
  const project=configData.project;
  const { loading, error, data } = useQuery(GET_KMedoids_OUTPUT, {
      variables: { numClusters,init,randomState ,datasetName,clusterDataOn , project},
    });

    let clustering =data;
  if (loading) {
    return <RenderLoading/>
  }
  if (error) {
      return <div>Error</div>
  }
  return <RenderOutput  data={{ clustering, configData,clusterDataOn,project}} />

}
function RenderOPTICS(props:any){

  let configData= props.data;
  const max_eps=configData.max_eps;
  const datasetName=configData.datasetName;
  const minSamples=configData.minSamples;
  const algorithm=configData.algorithm;
  const clusterDataOn=configData.clusterDataOn;
  const project=configData.project;
  const { loading, error, data } = useQuery(GET_OPTICS_OUTPUT, {
      variables: { max_eps,minSamples,algorithm ,datasetName,clusterDataOn , project},
    });
    let clustering =data;
  if (loading) {
    return <RenderLoading/>
  }
  if (error) {
      return <div>Error</div>
  }
  return <RenderOutput  data={{ clustering, configData,clusterDataOn,project}} />

}
function RenderSpectral(props:any){

  let configData= props.data;
  const numClusters=configData.numClusters;
  const datasetName=configData.datasetName;
  const assignLabels=configData.assignLabels;
  const affinity=configData.affinity;
  const randomState=configData.randomState;
  const clusterDataOn=configData.clusterDataOn;
  const project=configData.project;
  const { loading, error, data } = useQuery(GET_Spectral_OUTPUT, {
      variables: { numClusters,assignLabels,affinity,randomState ,datasetName,clusterDataOn , project},
    });
    let clustering =data;
  if (loading) {
    return <RenderLoading/>
  }
  if (error) {
      return <div>Error</div>
  }
  return <RenderOutput  data={{ clustering, configData,clusterDataOn,project}} />

}

function ClusterOutput(props:any){
    let url = window.location.href;
	let start = url.lastIndexOf(':-');
    let snippedUrl = url.substring(start+2);
    let end = snippedUrl.indexOf('/');
	let datasetName =snippedUrl.substring(0, end)
    let formData=props.fdata;
    let clusterName=props.cname;
    let project=props.project;
    let clusterDataOn = formData.selectedClusterDataOn;
    
    
    if (clusterName==="KMeans") {
        let numClusters=formData.num_clusters;
        let randomState=formData.random_state;
        console.log("testing clusteroutput");
        console.log(formData);
        return <RenderKMeans  data={{ numClusters,randomState,datasetName,clusterDataOn,project}} />
    }
    else if (clusterName==="Fuzzycmeans") {
      let numClusters=formData.num_clusters;
      let fuzzifier=formData.fuzzifier;
      return <RenderFuzzycmeans  data={{ numClusters,fuzzifier,datasetName,clusterDataOn,project}} />
  }
  else if (clusterName==="GaussianMixtureModel") {
    let numClusters=formData.num_clusters;
    return <RenderGaussianmixturemodel  data={{ numClusters,datasetName,clusterDataOn,project}} />
}
    else if (clusterName==="Birch") {
        let numClusters=formData.num_clusters;
        let threshold=formData.threshold;
        let branchingFactor=formData.branching_factor;
        return <RenderBirch  data={{ numClusters,threshold,branchingFactor,datasetName,clusterDataOn,project}} />
    }
    else if (clusterName==="Agglomerative") {
      let numClusters=formData.num_clusters;
      let linkage=formData.linkage;
      return <RenderAgglomerative  data={{ numClusters,linkage,datasetName,clusterDataOn,project}} />
  }
  
  else if (clusterName==="DBSCAN") {
    let eps=formData.eps;
    let minSamples=formData.min_samples;
    let algorithm=formData.algorithm;
    return <RenderDBSCAN  data={{ eps,minSamples,algorithm ,datasetName,clusterDataOn,project}} />
}
else if (clusterName==="Deconvolution") {
  
  
  let mVal=formData.m_val;
  let maxIter=formData.max_iter;
  let limit=formData.limit;
  return <RenderDeconvolution  data={{ mVal,maxIter,limit ,datasetName,clusterDataOn,project}} />
}
  else if (clusterName==="KMedoids") {
    let numClusters=formData.num_clusters;
    let randomState=formData.random_state;
    let init=formData.init;
    return <RenderKMedoids  data={{ numClusters,init,randomState,datasetName,clusterDataOn,project}} />
}
else if (clusterName==="OPTICS") {
  let max_eps=formData.max_eps;
    let minSamples=formData.min_samples;
    let algorithm=formData.algorithm;
    return <RenderOPTICS  data={{ max_eps,minSamples,algorithm ,datasetName,clusterDataOn,project}} />
}
else if (clusterName==="Spectral") {
  let numClusters=formData.num_clusters;
  let randomState=formData.random_state;
  let affinity=formData.affinity;
  let assignLabels=formData.assign_labels;
  return <RenderSpectral  data={{ numClusters, assignLabels, affinity,randomState,datasetName,clusterDataOn,project}} />
}
    else{
        return(
            <div>
                yet to be added
            </div>
        )
    }
    

}

ClusterOutput.defaultProps = {
	data: {num_clusters: '0', random_state: '0'}
  };

export default memo(ClusterOutput);