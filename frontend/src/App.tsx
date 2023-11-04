import "./App.css";
import NavBar from './components/index';
import { BrowserRouter as Router, Routes , Route } from 'react-router-dom';
import About from './pages/About';
import OpenProject from "./pages/ProjectsTab/OpenProject";
import Login from "./pages/Login";
import UserManual from "./pages/UserManual";
import ViewProject from "./pages/ProjectsTab/ViewProject";
import NewProject from "./pages/ProjectsTab/NewProject"


function App() {
  return (
   

    <div className="App">
      
    <Router>
    <NavBar />
    <Routes>
    <Route path='/OpenProject' Component={OpenProject} />  
      <Route path='/About' Component={About} />
      <Route path='/Project' Component={ViewProject} />
      <Route path='/Login' Component={Login} />
      <Route path='/UserManual' Component={UserManual} />
      <Route path='/NewProject' Component={NewProject} />
    </Routes>
    </Router>

    </div>
  );
}

export default App;


