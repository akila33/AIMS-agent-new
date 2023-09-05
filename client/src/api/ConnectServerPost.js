function  PostRestRequest(apiUrl, postBodyData, postResultObj) {
    var data = JSON.stringify(postBodyData)
    return fetch(apiUrl, {
         mode: 'cors',
         method: 'POST',
         body: data,
         json: true,
         headers: new Headers({
             'Content-Type': 'application/json',
             Accept: "application/json"
         })
       },
     )
     .then(checkStatus)
     .then(parseJSON)
     .then(postResultObj);
} 

function checkStatus(response) {
  if (response.status >= 200 && response.status < 300) {
    return response;
  }
  const error = new Error(`HTTP Error ${response.statusText}`);
  error.status = response.statusText;
  error.response = response;
  console.log(error);
  throw error;
}

function parseJSON(response) {
  return response.json();
}

const PostRestObject = { PostRestRequest };
export default PostRestObject;