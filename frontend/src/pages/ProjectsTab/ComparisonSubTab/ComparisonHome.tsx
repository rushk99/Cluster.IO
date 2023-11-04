
import ComparisonCreation from './ComparisonCreation';
import ComparisonTable from './ComparisonTable';
import "./ComparisonHomeStyles.css";
///////////////////////////////////////////////////////////////
//            CSS
///////////////////////////////////////////////////////////////

const ComparisonHome = () => {
	

	////////////////////////////////////////////////////
	//                HTML
	/////////////////////////////////////////////////
	return (
		<div>
			<div className="leftSide" > 
                <ComparisonCreation />
		    </div>
		    <div className="rightSide" > 
			    <ComparisonTable />
		    </div>
		</div>
	);
};

export default ComparisonHome;