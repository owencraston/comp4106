import React from 'react';
import { PageHeader} from "antd";
import { NumberOfCourses } from './Components/NumberOfCourses';


function App() {
  return (
    <div>
      <PageHeader title={"Course Picker"}></PageHeader>
      <NumberOfCourses />
    </div>
  );
}

export default App;
