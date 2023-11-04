import Header from './Header';

import {
Nav,
NavLink,
Bars,
NavMenu,
NavBtn,
NavBtnLink,
} from './NavBarElements';

const Navbar = () => {
	const isAbout = () => {
		return window.location.pathname.indexOf('/About') != -1;
	};

	const isOpenProject = () => {
		return window.location.pathname.indexOf('/OpenProject') != -1 || window.location.pathname.indexOf('/Project') != -1;
	};

	const isSettings = () => {
		return window.location.pathname.indexOf('/Settings') != -1;
	};

	const isManual = () => {
		return window.location.pathname.indexOf('/UserManual') != -1;
	};

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



        {/* activeStyle */}
			PROJECTS
		</NavLink>
		<NavLink to='/UserManual' style={({ isActive }) => ({
            fontSize: '24px',
            fontWeight: isActive ? "bold" : "",
            color: isActive ? "white" : "",
          })}>
        {/* activeStyle */}
			USER MANUAL
		</NavLink>
		{/* Second Nav */}
		{/*<NavBtnLink to='/Login'>Sign In</NavBtnLink> */}
		</NavMenu>
	</Nav>
	
);
};

export default Navbar;


