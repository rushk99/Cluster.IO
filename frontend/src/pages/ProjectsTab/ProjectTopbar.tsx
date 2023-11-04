import ArrowRightAltIcon from '@mui/icons-material/ArrowRightAlt';

import {
Nav,
NavLink,
NavMenu
} from './TopbarElements';

const ProjectTopbar = (props: { projName: String } ) => {

  return (
    <Nav>
      <h1 style={{ fontSize: '24px', marginTop: "10px", width: "500px", textAlign: "left" }}>{props.projName}</h1>
      <NavMenu style={{ marginLeft: "0px" }}>
        <NavLink
          to={'/Project/' + props.projName + '/DataSet/Home'}
          style={({ isActive }) => ({
            fontSize: '24px',
            fontWeight: isActive ? "bold" : "",
            color: isActive ? "black" : "",
          })}
        >
          Data Sets/Upload
        </NavLink>
        <ArrowRightAltIcon />
        <NavLink
          to={'/Project/' + props.projName + '/Cluster/Home'}
          style={({ isActive }) => ({
            fontSize: '24px',
            fontWeight: isActive ? "bold" : "",
            color: isActive ? "black" : "",
          })}
        >
          Cluster Configurations
        </NavLink>
        <ArrowRightAltIcon />
        <NavLink
          to={'/Project/' + props.projName + '/Comparison/Home'}
          style={({ isActive }) => ({
            fontSize: '24px',
            fontWeight: isActive ? "bold" : "",
            color: isActive ? "black" : "",
          })}
        >
          Comparisons
        </NavLink>
      </NavMenu>
    </Nav>
  );
};

export default ProjectTopbar;







