import "./App.css";
import NavBar from './components/index';
import {  Routes , Route } from 'react-router-dom';
import About from './pages/About';
import OpenProject from "./pages/ProjectsTab/OpenProject";
import UserManual from "./pages/UserManual";
import ViewProject from "./pages/ProjectsTab/ViewProject";


function App() {

  return (
    <div className="App">
      
    <NavBar />
    <Routes>
          <Route path='/OpenProject' element={<OpenProject />} />
          <Route path='/About' element={<About />} />
          <Route path='/Project/:name/*' element={<ViewProject />} />
          <Route path='/UserManual' element={<UserManual />} />
    </Routes>

    </div>
  );
}

export default App;


