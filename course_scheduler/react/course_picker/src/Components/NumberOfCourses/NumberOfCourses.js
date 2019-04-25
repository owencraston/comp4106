import React, { Component } from "react";
import { InputNumber } from 'antd';

class NumberOfCoursesPicker extends Component {
  render() {
    return (
        <InputNumber min={1} max={10} defaultValue={3}/>
    );
  }
}

export default NumberOfCoursesPicker;
