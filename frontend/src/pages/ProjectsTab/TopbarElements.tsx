
import { NavLink as Link } from 'react-router-dom';
import styled from 'styled-components';


export const Nav = styled.nav`
background: #D9E9E2;
height: 60px;
display: flex;
justify-content: flex-start;
padding: 0.2rem calc((100vw - 1000px) / 2);
z-index: 12;
/* Third Nav */
/* justify-content: flex-start; */
`;

export const NavLink = styled(Link)`
color: black;
display: flex;
align-items: center;
text-decoration: none;
padding: 0 1rem;
height: 100%;
cursor: pointer;
&.active {
	color: #000000;
}
`;



export const NavMenu = styled.div`
display: flex;
align-items: center;
height: 100%;
/* Second Nav */
margin-left: 26%; 
/* Third Nav */
/* width: 100vw;
white-space: nowrap; */
@media screen and (max-width: 768px) {
	display: none;
}
`;



