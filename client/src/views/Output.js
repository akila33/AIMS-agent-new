import React, { useState, useEffect } from "react";
import { render } from "react-dom";
import "./style.css"; // Import CSS file for styling

function Output() {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetch("/members")
      .then((res) => res.json())
      .then((data) => {
        setData(data.members);
        console.log(data.members);
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
      });
  }, []);

  useEffect(() => {
    fetch("/services")
      .then((res) => res.json())
      .then((data) => {
        setData(data.services);
        console.log(data.services);
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
      });
  }, []);
  

  const renderPipeline = (pipeline) => {
    if (typeof pipeline === "object") {
      return (
        <ul>
          {Object.entries(pipeline).map(([key, value]) => (
            <li key={key}>
              <strong>{key}: </strong>
              {renderPipeline(value)}
            </li>
          ))}
        </ul>
      );
    } else {
      return <span>{pipeline}</span>;
    }
  };

  return (
    <div className="output-container">
      {data === null ? (
        <p>Loading...</p>
      ) : (
        renderPipeline(data)
      )}
    </div>
  );
}

export default Output;
