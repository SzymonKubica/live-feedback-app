import React, {useState, useEffect, Fragment}from 'react';

import { 
  BrowserRouter as Router,
  Routes,
  Route,
} from "react-router-dom"  


import { HomeView } from './components/HomeView';
import { StudentView } from './components/StudentView';
import { TeacherView } from './components/TeacherView';
import { SnapshotView } from './components/SnapshotView';


function App() {
  const [state, setState] = useState("")
 
  useEffect(() => {
    fetch("/test").then(res => res.json()).then(data=> {
      setState(data.test)
    })
  },[])

  return (
      <Router>
          <Fragment> 
          <Routes>
            <Route path="" element={<HomeView />}/>
            <Route path="student" element={<StudentView />}/>
            <Route path="teacher" element={<TeacherView />}/>
            <Route path="teacher/snapshots" element={<SnapshotView />}/>

          </Routes>
          </Fragment>
      </Router>

  );
}

export default App;
