import React from "react";
import { Link } from "react-router-dom";

function Home() {
  return (
    <div>
      HOME PAGE <br/>
      <Link to="/registration"> GO TO THE REGISTRATION PAGE </Link>
    </div>
  );
}

export default Home;
