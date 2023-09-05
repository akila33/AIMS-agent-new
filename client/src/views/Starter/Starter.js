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
        services: [],
      };
    }

    handleLinkClick = () => {
      alert('Service registered Successfully!');
    };

    handleFormSubmit = (e) => {
      e.preventDefault();
    
      // Get form data
      const formData = new FormData(e.target);
    
      // Convert form data to a plain object
      const formDataObject = {};
      formData.forEach((value, key) => {
        formDataObject[key] = value;
      });
    
      // Send a POST request to the Flask server
      fetch("/services", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formDataObject),
      })
        .then((response) => response.json())
        .then((data) => {
          console.log(data.services);
          this.setState({ services: data.services });
          // Handle the response from the Flask server as needed
        })
        .catch((error) => {
          console.error("Error submitting form:", error);
        });
    };

    renderServiceForm = () => {
      return (
        <div className="rightPanel">
    
        <form name="services" onSubmit={this.handleFormSubmit}>
    
        <div className="title">
          {/* <h5>Service Registration</h5> */}
            
          </div>
          <div className='content'>
            <div className="row">
              <label className="col-sm-2 col-form-label">Namespace</label>
              <div className="col-sm-3 mb-2">
                <input type="text" name="namespace" className="form-control" placeholder="http://aimicroservice.derby.ac.uk" />
              </div>
    
              <div className="col-sm-4">
              </div>
            </div>
    
            <div className="row">
              <label className="col-sm-2 col-form-label">Service name</label><br/><br/>
              <div className="col-sm-6 mb-2">
                <input type="text" name="serviceName" className="form-control" placeholder='csvjsonmodel'></input>
              </div>
              <div className="col-sm-4">
              </div>
            </div>
            <div className="row">
              <label className="col-sm-2 col-form-label">Description</label>
              <div className="col-sm-6 mb-2">
                <input type="text" name="description" className="form-control" placeholder="Service to parse CSV data as json objects to the React frontend" />
              </div>
              <div className="col-sm-4">
              </div>
            </div>
            <div className="row">
              <label className="col-sm-2 col-form-label">Requirements</label>
              <div className="col-sm-6 mb-2">
                <input type="text" name="requirements" className="form-control" placeholder="flask_restful" />
              </div>
              <div className="col-sm-4">
              </div>
            </div>
            <div className="row">
              <label className="col-sm-2 col-form-label">Input Spec</label>
              <div className="col-sm-6 mb-2">
                <input type="text" name="input" className="form-control" placeholder="datafile.pandas" />
              </div>
              <div className="col-sm-4">
              </div>
            </div>
            <div className="row">
              <label className="col-sm-2 col-form-label">Output Spec</label>
              <div className="col-sm-6 mb-2">
                <input type="text" name="output" className="form-control" placeholder="model.csv_json_datahandler" />
              </div>
              <div className="col-sm-4">
              </div>
            </div>
            <div className="row">
              <label className="col-sm-2 col-form-label">Service Category</label>
              <div className="col-sm-6 mb-2">
                <input type="text" name="category" className="form-control" placeholder="data_engineering" />
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
                <button type="submit" className="btn btn-primary" onClick={this.handleLinkClick}>
                  Register Service
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
              <h3>Service Registration</h3>
              <hr/>
              {this.renderServiceForm()}
            </Col>
          </Row>
        </div>
    );
  }
}

export default Starter;
