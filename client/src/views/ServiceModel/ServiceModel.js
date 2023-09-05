import React, { Component, lazy, Suspense } from 'react';
import {
  Card,
  CardBody,
  CardFooter,
  CardHeader,
  CardTitle,
  Col,
  Row,
} from 'reactstrap';
import GetRestObject from '../../api/ConnectServerGet';
import PostRestObject from '../../api/ConnectServerPost';
import { Link } from "react-router-dom";

class Starter extends Component {
    constructor(props) {
      super(props);
  
      this.state = {
        members: '',
      };
    }

    handleFormSubmit = (e) => {
      e.preventDefault();

      // Get form data
      const formData = new FormData(e.target);

      // Extract the file name from the path
      const pathInput = document.getElementById("path");
      const filePath = pathInput.value;
      const fileName = filePath.split("\\").pop();

      // Convert form data to a plain object
      const formDataObject = {};
      formData.forEach((value, key) => {
        if (key === "path") {
          formDataObject[key] = fileName;
        } else {
          formDataObject[key] = value;
        }
      });

      // Send a POST request to the Flask server
      fetch("/members", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formDataObject),
      })
        .then((response) => response.json())
        .then((data) => {
          console.log(data.members);
          this.setState({ members: data.members });
          // Handle the response from the Flask server as needed
        })
        .catch((error) => {
          console.error("Error submitting form:", error);
        });
    };

    renderServiceForm = () => {
      return (
        <div className="rightPanel">
    
        <form name="members" onSubmit={this.handleFormSubmit}>
    
    <div className="title">
          {/* <h5>ML Model Selecter</h5> */}
            
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
                <input type="text" name="domain" className="form-control" id="domain" placeholder="medical" />
              </div>
              <div className="col-sm-4">
              </div>
            </div>
            <div className="row">
              <label htmlFor="staticEmail1" className="col-sm-2 col-form-label">AI Task Category</label><br/><br/>
              <div className="col-sm-6 mb-2">
                <select className="custom-select" name="category" id="inlineFormCustomSelect" >
                  <option value="MLmodel_classification">MLmodel_classification</option>
                  <option value="Image_classification">Image_classification</option>
                  <option value="ML_featuretest">ML_featuretest</option>
                  <option value="ETL_transform">ETL_transform</option>
                </select>
              </div>
              <div className="col-sm-4">
              </div>
            </div>
    
            <div className="row">
              <div className="col-sm-5 mb-2">
              </div>
              <div className="col-sm-4">
                {/* <button type="button" className="registerbtn" 
            onClick={() => {
              // setGoToContact(true);
            }}
                >
                  {" "}
                  Register
                </button> */}
                <br/><br/><br/><br/>
                <button type="submit" className="btn btn-primary">
                  Submit
                </button>

              </div>
              <div className="col-sm-3"></div>
            </div>
          </div> 
        </form>
         
    
        </div>    
    
      );      
    }

    loading = () => <div className="animated fadeIn pt-1 text-center">Loading...</div>
  
    render() {
  
      return (
        <div className="animated fadeIn">
          <Row>
            <Col md={12}>
              <h3>ML Model Selecter</h3>
              <hr/>
              {this.renderServiceForm()}
              {/* Display the server response */}
              <div className="output-container">
                <h4>ML Model Output:</h4>
                <pre style={{ whiteSpace: 'pre-line' }}>{JSON.stringify(this.state.members, null, 2)}</pre>
              </div>
            </Col>
          </Row>
        </div>
    );
  }
}

export default Starter;
