import Header from './Header';

import {
Nav,
NavLink,
Bars,
NavMenu,
} from './NavBarElements';

const Navbar = () => {

return (
	<Nav>
		<Bars />
        <Header/>
		<NavMenu>


		<NavLink  to='/About' style={({ isActive }) => ({
            fontSize: '24px',
            fontWeight: isActive ? "bold" : "",
            color: isActive ? "white" : "",
          })} >

			ABOUT
		</NavLink>

        <NavLink to='/OpenProject' style={({ isActive }) => ({
            fontSize: '24px',
            fontWeight: isActive ? "bold" : "",
            color: isActive ? "white" : "",
          })} >

			PROJECTS
		</NavLink>
		<NavLink to='/UserManual' style={({ isActive }) => ({
            fontSize: '24px',
            fontWeight: isActive ? "bold" : "",
            color: isActive ? "white" : "",
          })}>
			USER MANUAL
		</NavLink>
		</NavMenu>
	</Nav>
	
);
};

export default Navbar;


