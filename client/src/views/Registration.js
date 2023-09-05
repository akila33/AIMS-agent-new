import React from "react";
import { Navigate } from "react-router-dom";
import './../style.css';
// import { Routes, Route } from 'react-router-dom';

function About() {

  const [goToContact, setGoToContact] = React.useState(false);

  if (goToContact) {
    return <Navigate to="/output" />;
  }

  return (
    <div className="rightPanel">

    <form name="members" action="/members" method="post">

<div className="title">
        AI Service Registration
      </div>
      <div className='content'>
        <div className="row">
          <label className="col-sm-2 col-form-label">Task Name</label>
          <div className="col-sm-3 mb-2">
            <input type="text" name="taskName" className="form-control" placeholder="Task 1" />
          </div>

          <div className="col-sm-4">
          </div>
        </div>
        <div className="row">
          <label htmlFor="email" className="col-sm-2 col-form-label">Select a file: </label><br/><br/>
          <div className="col-sm-6 mb-2">
            <input type="file" id="path" name="path" className="form-control"></input>
          </div>
          <div className="col-sm-4">
          </div>
        </div><br/>
        <div className="row">
          <label htmlFor="telephone" className="col-sm-2 col-form-label">Desired Output</label>
          <div className="col-sm-6 mb-2">
            <input type="text" name="output" className="form-control" id="output" placeholder="['pipeline']" />
          </div>
          <div className="col-sm-4">
          </div>
        </div>
        <div className="row">
          <label htmlFor="staticEmail1" className="col-sm-2 col-form-label">Problem Domain</label>
          <div className="col-sm-6 mb-2">
            <input type="text" name="output" className="form-control" id="output" placeholder="medical" />
          </div>
          <div className="col-sm-4">
          </div>
        </div>
        <div className="row">
          <label htmlFor="staticEmail1" className="col-sm-2 col-form-label">AI Task Category</label><br/><br/>
          <div className="col-sm-6 mb-2">
            <select className="custom-select" name="category" id="inlineFormCustomSelect" >
              <option value="US">MLmodel_classification</option>
              <option value="IN">Image_classification</option>
              <option value="US">ML_featuretest</option>
              <option value="IN">ETL_transform</option>
            </select>
          </div>
          <div className="col-sm-4">
          </div>
        </div>

        <div className="row">
          <div className="col-sm-5 mb-2">
          </div>
          <div className="col-sm-4">
            <button type="button" className="registerbtn" 
        onClick={() => {
          setGoToContact(true);
        }}
            >
              {" "}
              Register
            </button>
          </div>
          <div className="col-sm-3"></div>
        </div>
      </div> 
    </form>
     

    </div>    

  );
}

export default About;
