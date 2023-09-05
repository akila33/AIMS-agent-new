import React, { Component } from 'react';
import {
  Card,
  CardBody,
  CardHeader,
  Col,
  Row,
} from 'reactstrap';
import JsonTable from 'ts-react-json-table';

class CsvDataReader extends Component {
  constructor(props) {
    super(props);

    this.state = {
      selectedFile: null,
      csvDataObject: null,
    };
  }

  handleFileInputChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      this.setState({ selectedFile });
    }
  };

  handleFormSubmit = (e) => {
    e.preventDefault();

    if (!this.state.selectedFile) {
      alert('Please select a file before submitting.');
      return;
    }

    const formData = new FormData();
    formData.append('file', this.state.selectedFile);

    const requestOptions = {
      method: 'POST',
      body: formData,
    };

    fetch(`/v1/datareader`, requestOptions)
      .then((response) => response.json())
      .then((data) => {
        this.setState({
          csvDataObject: data,
        });
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  };

  renderCsvDataResults = () => {
    if (this.state.csvDataObject && this.state.csvDataObject.resultStatus && this.state.csvDataObject.resultData) {
      const apiStatus = this.state.csvDataObject.resultStatus;
      const apiData = this.state.csvDataObject.resultData;

      if (apiStatus === 'SUCCESS' && apiData.length === 1) {
        const csvData = apiData[0];

        return (
          <div>
            <span className="text-success">
              Rows: <span className="text-primary"><b>{csvData.rows}</b></span>
            </span>
            <br />
            <span className="text-success">
              Columns: <span className="text-primary"><b>{csvData.cols}</b></span>
            </span>
            <br />
            <span className="text-success">
              Column Names: <span className="text-primary"><b>{this.renderColumnNames(csvData.columns)}</b></span>
            </span>
            <hr />
            <Card>
              <CardHeader>All Rows</CardHeader>
              <CardBody className="mb-1" style={{ height: '600px', overflowY: 'auto' }}>
                <JsonTable rows={csvData.rowData} columns={csvData.columns} />
              </CardBody>
            </Card>
          </div>
        );
      } else {
        return (
          <div>
            <span className="text-danger">{apiData[0].message}</span>
          </div>
        );
      }
    }
  };

  renderColumnNames = (columnList) => {
    return columnList.map((item, index) => (
      <span key={index} className="mr-1 text-default">
        {index + 1}: {item}
      </span>
    ));
  };

  loading = () => <div className="animated fadeIn pt-1 text-center">Loading...</div>;

  render() {
    return (
      <div className="animated fadeIn">
        <Row>
          <Col md={12}>
            <h3>Dynamic Data Handler</h3>
            <hr />
            <div className="rightPanel">
              <form name="members" onSubmit={this.handleFormSubmit}>
                <div className="row">
                  <label htmlFor="file" className="col-sm-2 col-form-label">
                    Select a file:
                  </label>
                  <div className="col-sm-6 mb-2">
                    <input
                      type="file"
                      id="file"
                      name="file"
                      className="form-control"
                      onChange={this.handleFileInputChange}
                    />
                  </div>
                  <div className="col-sm-4"></div>
                </div>
                {/* <br />
                <button type="submit" className="btn btn-primary">
                  Submit
                </button> */}
              </form>
            </div>
            
            {this.state.csvDataObject && this.state.csvDataObject.resultStatus ? (
              this.renderCsvDataResults()
            ) : (
              <div className="text-center">
                <button className="btn btn-primary" onClick={this.handleFormSubmit}>
                  Submit
                </button>
              </div>
            )}
          </Col>
        </Row>
      </div>
    );
  }
}

export default CsvDataReader;
