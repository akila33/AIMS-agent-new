from flask import Flask, request
from flask_restful import Api, Resource
import pandas as pd
import io

app = Flask(__name__)
api = Api(app)

class DataHandlerFunction(Resource):
    def post(self):
        try:
            uploaded_file = request.files['file']
            if uploaded_file:
                result_status, result_data = CSVReaderToJson(uploaded_file)
                return {'resultStatus': result_status, 'resultData': result_data}
            else:
                return {'resultStatus': 'FAILURE', 'resultData': [{'message': 'No file uploaded.'}]}

        except Exception as e:
            return {'resultStatus': 'FAILURE', 'resultData': [{'message': str(e)}]}

def CSVReaderToJson(uploaded_file):
    result_status = 'FAILURE'
    result_data = []

    try:
        csv_data = pd.read_csv(uploaded_file)
        row_count = csv_data.shape[0]
        column_count = csv_data.shape[1]
        column_names = csv_data.columns.tolist()

        final_row_data = []
        for index, rows in csv_data.iterrows():
            final_row_data.append(rows.to_dict())

        json_result = {'rows': row_count, 'cols': column_count, 'columns': column_names, 'rowData': final_row_data}
        result_data.append(json_result)
        result_status = 'SUCCESS'
    except Exception as e:
        result_data.append({'message': 'Unable to process the request.', 'error': str(e)})

    return result_status, result_data

api.add_resource(DataHandlerFunction, '/v1/datareader')

if __name__ == '__main__':
    app.run(debug=True)
