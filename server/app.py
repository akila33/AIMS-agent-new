import sys
import os
sys.path.insert(0, '')
import agent as ai
import servicedescription as sd

from flask import Flask, jsonify, request
from flask_restful import Api, Resource, reqparse
from core.ApiHandler import ApiHandlerFunction
from core.CsvDataHandler import DataHandlerFunction

# Registration libraries
from rdflib import Graph, Literal, RDF, URIRef
from rdflib.namespace import FOAF, XSD
from rdflib.namespace import NamespaceManager
from rdflib import BNode

app = Flask(__name__)
api = Api(app)


class RootApi(Resource):
    '''
    curl -X GET http://localhost:3000/v1/hello --header "Content-Type: application/json"
    curl -X POST http://localhost:3000/v1/hello --header "Content-Type: application/json" --data '{"RequestType":"Hello"}'
    '''

    # Members API Route
    @app.route("/members", methods=["POST"])
    def members():
        try:
            ai.reset_knowledge()
            ai.output_memery = {}
            ai.servicelist = []

            # Retrieve form data (JSON)
            form_data = request.json

            # Extract form fields as parameters
            task_name = form_data.get("taskName")
            path = form_data.get("path")
            desired_output = form_data.get("output")
            problem_domain = form_data.get("domain")
            ai_task_category = form_data.get("category")

            # Call the OperatingTask function with form parameters
            result = ai.OperatingTask(task_name,path,[desired_output],problem_domain,'',ai_task_category)

            return jsonify({"members": [str(result)]})

        except Exception as e:
            return jsonify({"error": str(e)}), 500 

    # New Pipeline Service for Mortality data
    @app.route("/services", methods=['GET', 'POST'])
    def services():
        try:
            # Retrieve form data
            form_data = request.json  # Assuming the data is sent as JSON

            # Extract form fields as parameters
            namespace = form_data.get("namespace")
            serviceName = form_data.get("serviceName")
            description = form_data.get("description")
            requirements = form_data.get("requirements")
            input = form_data.get("input")
            output = form_data.get("output")
            category = form_data.get("category")

            requirements = [requirements]
            dpend = sd.create_dependencies(requirements)
            output_s = sd.Create_input_spec([output])
            description = description

            # Call greateMSGraph function to register the new service
            result = sd.greateMSGraph(namespace, serviceName, description, 'CsvDatHandler', dpend, requirements, 0, 0, 'py', '', output_s, 'https://www.derby.ac.uk/staff/hongqing-yu/', 'https://en.wikipedia.org/wiki/Free-software_license', category)

            return jsonify({"services": [str(result)]})

        except Exception as e:
            return jsonify({"error": str(e)}), 500 

    def get(self):
        return {'resultStatus': 'SUCCESS', 'message': 'Hello from RootApi'}

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('RequestType', type=str)
        args = parser.parse_args()

        message = "RequestType: {}".format(args['RequestType'])
        final_result = {'status': 'SUCCESS', 'message': message}
        return final_result


api.add_resource(ApiHandlerFunction, '/v1/bye')
api.add_resource(DataHandlerFunction, '/v1/datareader')
api.add_resource(RootApi, '/v1/hello')

if __name__ == '__main__':
    app.run(host="localhost", port=3000, debug=True)
