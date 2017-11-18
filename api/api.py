#!/usr/bin/env python
"""Main module of the data quality framework API."""
from flask import Blueprint, Flask, request
from flask_cors import CORS
from flask_restplus import Api, fields, Resource
from batch_method import BatchMethod
from event_method import EventMethod
import utils
import socket

app = Flask(__name__)
CORS(app)

# Create blue print to indicate api base url
blueprint = Blueprint('api', __name__, url_prefix='/dataquality/api')
api = Api(
    blueprint,
    title='Data Quality Framework API',
    version='v1',
    description='RESTful API for the Data Quality Framework. Base URL: http://{}:5000/dataquality/api'.format(socket.gethostname()),
    doc='/doc')
app.register_blueprint(blueprint)

# List of namespaces used by the endpoints below
nsBatch = api.namespace('Batch', path='/v1')
nsDataSource = api.namespace('DataSource', path='/v1')
nsEvent = api.namespace('Event', path='/v1')
nsIndicator = api.namespace('Indicator', path='/v1')
nsSession = api.namespace('Session', path='/v1')
nsStatus = api.namespace('Status', path='/v1')


# BatchOwner
@nsBatch.route('/batchowners')
class BatchOwner(Resource):
    """Class for Batch Owner API endpoints."""
    mdBatchOwner = api.model(
        'BatchOwner',
        {'id': fields.Integer(required=False, description='Batch owner Id'),
            'name': fields.String(required=False, description='Batch owner name')})

    @nsBatch.expect(api.models['BatchOwner'], validate=True)
    def post(self):
        """
        Create Batch Owner.

        Use this method to create a Batch Owner.
        """
        return utils.create('BatchOwner', request.json)

    def get(self):
        """
        Get list of Batch Owners.

        Use this method to get the list of Batch Owners.
        """
        return utils.read('BatchOwner')

    @nsBatch.expect(api.models['BatchOwner'], validate=True)
    def put(self):
        """
        Update Batch Owner.

        Use this method to update a Batch Owner.
        """
        return utils.update('BatchOwner', request.json)

    @nsBatch.expect(api.models['BatchOwner'], validate=True)
    def delete(self):
        """
        Delete Batch Owner.

        Use this method to delete a Batch Owner.
        """
        return utils.read('BatchOwner', request.json)


# Batch execution
@nsBatch.route('/batchowners/<int:batch_owner_id>/execute')
@nsBatch.param('batch_owner_id', 'Batch Owner Id')
class BatchExecution(Resource):
    """Class for Batch Execution endpoints."""

    @nsBatch.expect(api.models['Batch'], validate=True)
    def post(self, batch_owner_id):
        """
        Execute a Batch.

        Use this method to execute a Batch of Indicators for the corresponding Batch Owner.
        """
        return BatchApi.execute(batch_owner_id)


# Batch
@nsBatch.route('/batchowners/<int:batch_owner_id>/batches')
@nsBatch.param('batch_owner_id', 'Batch Owner Id')
class Batch(Resource):
    """Class for Batch endpoints."""
    mdBatchExecute = api.model(
        'Batch',
        {'id': fields.Integer(required=False, description='Data source Id'),
            'batchOwnerId': fields.Integer(required=False, description='Batch owner Id'),
            'statusId': fields.Integer(required=False, description='Status Id')})

    def get(self, batch_owner_id):
        """
        Get list of Batches.

        Use this method to get the list of Batches for the corresponding Batch Owner.
        """
        parameters = {'batchOwnerId': batch_owner_id}
        return utils.read('Batch', parameters)


# Data source
@nsDataSource.route('/datasources')
class DataSource(Resource):
    """Class for Data Source API endpoints."""
    mdDataSource = api.model(
        'DataSource',
        {'id': fields.Integer(required=False, description='Data source Id'),
            'name': fields.String(required=False, description='Data source name'),
            'dataSourceTypeId': fields.Integer(required=False, description='Data source type Id'),
            'connectionString': fields.String(required=False, description='ODBC Connection sring'),
            'login': fields.String(required=False, description='Login'),
            'password': fields.String(required=False, description='Password')})

    @nsDataSource.expect(api.models['DataSource'], validate=True)
    def post(self):
        """
        Create Data Source.

        Use this method to create a Data Source.
        """
        return utils.create('DataSource', request.json)

    def get(self):
        """
        Get list of Data Sources.

        Use this method to get the list of Data Sources.
        """
        return utils.read('DataSource')

    @nsDataSource.expect(api.models['DataSource'], validate=True)
    def put(self):
        """
        Update Data Source.

        Use this method to update a Data Source.
        """
        return utils.update('DataSource', request.json)

    @nsDataSource.expect(api.models['DataSource'], validate=True)
    def delete(self):
        """
        Delete Data Source.

        Use this method to delete a Data Source.
        """
        return utils.delete('DataSource', request.json)


# Data source type
@nsDataSource.route('/datasourcetypes')
class DataSourceType(Resource):
    """Class for Data Source Type API endpoints."""
    mdDataSourceType = api.model(
        'DataSourceType',
        {'id': fields.Integer(required=False, description='Data source type Id'),
            'name': fields.String(required=False, description='Data source type name')})

    @nsDataSource.expect(api.models['DataSourceType'], validate=True)
    def post(self):
        """
        Create Data Source Type.

        Use this method to create a Data Source Type.
        """
        return utils.create('DataSourceType', request.json)

    def get(self):
        """
        Get list of Data Source Types.

        Use this method to get the list of Data Source Types.
        """
        return utils.read('DataSourceType')

    @nsDataSource.expect(api.models['DataSourceType'], validate=True)
    def put(self):
        """
        Update Data Source Type.

        Use this method to update a Data Source Type.
        """
        return utils.update('DataSourceType', request.json)

    @nsDataSource.expect(api.models['DataSourceType'], validate=True)
    def delete(self):
        """
        Delete Data Source Type.

        Use this method to delete a Data Source Type.
        """
        return utils.delete('DataSourceType', request.json)


# Event
@nsEvent.route('/events')
@nsEvent.param('batch_owner_id', 'Batch Owner Id')
class Event(Resource):
    """Class for Event endpoints."""
    mdEvent = api.model(
        'Event',
        {'event': fields.String(required=True, description='Event to log for the indicator', example='Start, Stop, Error')})

    @nsEvent.expect(api.models['Event'], validate=True)
    def post(self, batch_owner_id):
        """
        Log Event.

        Use this method to log an event for the Session of an Indicator.
        """
        parameters = request.json
        return EventApi.log(parameters['indicator_id'], parameters['batch_owner_id'], parameters['event'])


# Event type
@nsEvent.route('/eventtypes')
class EventType(Resource):
    """Class for Event Type API endpoints."""
    mdEventType = api.model(
        'EventType',
        {'id': fields.Integer(required=False, description='Event type type Id'),
            'name': fields.String(required=False, description='Event type name')})

    @nsEvent.expect(api.models['EventType'], validate=True)
    def post(self):
        """
        Create Event Type.

        Use this method to create an Event Type.
        """
        return utils.create('EventType', request.json)

    def get(self):
        """
        Get list of Event Types.

        Use this method to get the list of Event Types.
        """
        return utils.read('EventType')

    @nsEvent.expect(api.models['EventType'], validate=True)
    def put(self):
        """
        Update Event Type.

        Use this method to update an Event Type.
        """
        return utils.update('EventType', request.json)

    @nsEvent.expect(api.models['EventType'], validate=True)
    def delete(self):
        """
        Delete Event Type.

        Use this method to delete an Event Type.
        """
        return utils.delete('EventType', request.json)


# Indicator
@nsIndicator.route('/indicators')
class Indicator(Resource):
    """Class for Indicator API endpoints."""
    mdIndicator = api.model(
        'Indicator',
        {'id': fields.Integer(required=False, description='Indicator Id'),
            'name': fields.String(required=False, description='Indicator name'),
            'description': fields.String(required=False, description='Indicator description'),
            'indicatorTypeId': fields.Integer(required=False, description='Indicator type Id'),
            'batchOwnerId': fields.Integer(required=False, description='Batch owner Id'),
            'executionOrder': fields.Integer(required=False, description='Execution order'),
            'active': fields.Integer(required=False, description='Active flag: 1 or 0')})

    @nsIndicator.expect(api.models['Indicator'], validate=True)
    def post(self):
        """
        Create Indicator.

        Use this method to create an Indicator.
        """
        return utils.create('Indicator', request.json)

    def get(self):
        """
        Get list of Indicator.

        Use this method to get the list of Indicators.
        """
        return utils.read('Indicator')

    @nsIndicator.expect(api.models['Indicator'], validate=True)
    def put(self):
        """
        Update Indicator.

        Use this method to update an Indicator.
        """
        return utils.update('Indicator', request.json)

    @nsIndicator.expect(api.models['Indicator'], validate=True)
    def delete(self):
        """
        Delete Indicator.

        Use this method to delete an Indicator.
        """
        return utils.delete('Indicator', request.json)


# Indicator parameter
@nsIndicator.route('/indicators/<int:indicator_id>/parameters')
@nsIndicator.param('indicator_id', 'Indicator Id')
class IndicatorParameter(Resource):
    """Class for Indicator Parameter API endpoints."""
    mdIndicatorParameter = api.model(
        'IndicatorParameter',
        {'id': fields.Integer(required=False, description='Indicator parameter Id'),
            'name': fields.String(required=False, description='Indicator parameter name'),
            'value': fields.String(required=False, description='Indicator parameter value')})

    @nsIndicator.expect(api.models['IndicatorParameter'], validate=True)
    def post(self, indicator_id):
        """
        Create Indicator Parameter.

        Use this method to create an Indicator Parameter.
        """
        parameters = request.json
        parameters['indicatorId'] = indicator_id
        return utils.create('IndicatorParameter', parameters)

    def get(self, indicator_id):
        """
        Get list of Indicator Parameter.

        Use this method to get the list of Indicator Parameters.
        """
        parameters = {}
        parameters['indicatorId'] = indicator_id
        return utils.read('IndicatorParameter', parameters)

    @nsIndicator.expect(api.models['IndicatorParameter'], validate=True)
    def put(self, indicator_id):
        """
        Update Indicator Parameter.

        Use this method to update an Indicator Parameter.
        """
        parameters = request.json
        parameters['indicatorId'] = indicator_id
        return utils.update('IndicatorParameter', parameters)

    @nsIndicator.expect(api.models['IndicatorParameter'], validate=True)
    def delete(self, indicator_id):
        """
        Delete Indicator Parameter.

        Use this method to delete an Indicator Parameter.
        """
        parameters = request.json
        parameters['indicatorId'] = indicator_id
        return utils.delete('IndicatorParameter', parameters)


# Indicator result
@nsIndicator.route('/indicators/<int:indicator_id>/results')
@nsIndicator.param('indicator_id', 'Indicator Id')
class IndicatorResult(Resource):
    """Class for Indicator Result API endpoints."""
    mdIndicatorResult = api.model(
        'IndicatorResult',
        {'id': fields.Integer(required=False, description='Indicator result Id'),
            'sessionId': fields.Integer(required=False, description='Session Id'),
            'alertOperator': fields.String(required=False, description='Alert operator'),
            'alertThreshold': fields.String(required=False, description='Alert threshold'),
            'nbRecords': fields.Integer(required=False, description='Number of records in indicator result'),
            'nbRecordsAlert': fields.Integer(required=False, description='Number of records triggering an alert in indicator result'),
            'nbRecordsNoAlert': fields.Integer(required=False, description='Number of records not triggering an alert in indicator result')})

    def get(self, indicator_id):
        """
        Get list of Indicator Result.

        Use this method to get the list of Indicator Result.
        """
        parameters = {}
        parameters['indicatorId'] = indicator_id
        return utils.read('IndicatorResult', parameters)


# Indicator type
@nsIndicator.route('/indicatortypes')
class IndicatorType(Resource):
    """Class for Indicator Type API endpoints."""
    mdIndicatorType = api.model(
        'IndicatorType',
        {'id': fields.Integer(required=False, description='Indicator type Id'),
            'name': fields.String(required=False, description='Indicator type name'),
            'module': fields.String(required=False, description='Indicator type module name'),
            'function': fields.String(required=False, description='Indicator type function name')})

    @nsIndicator.expect(api.models['IndicatorType'], validate=True)
    def post(self):
        """
        Create Indicator Type.

        Use this method to create an Indicator Type.
        """
        return utils.create('IndicatorType', request.json)

    def get(self):
        """
        Get list of Indicator Types.

        Use this method to get the list of Indicator Types.
        """
        return utils.read('IndicatorType')

    @nsIndicator.expect(api.models['IndicatorType'], validate=True)
    def put(self):
        """
        Update Indicator Type.

        Use this method to update an Indicator Type.
        """
        return utils.update('IndicatorType', request.json)

    @nsIndicator.expect(api.models['IndicatorType'], validate=True)
    def delete(self):
        """
        Delete Indicator Type.

        Use this method to delete an Indicator Type.
        """
        return utils.delete('IndicatorType', request.json)


# Status
@nsStatus.route('/status')
class Status(Resource):
    """Class for Status API endpoints."""
    mdStatus = api.model(
        'Status',
        {'id': fields.Integer(required=False, description='Status Id'),
            'name': fields.String(required=False, description='Status name')})

    @nsStatus.expect(api.models['Status'], validate=True)
    def post(self):
        """
        Create Status.

        Use this method to create a Status.
        """
        return utils.create('Status', request.json)

    def get(self):
        """
        Get list of Status.

        Use this method to get the list of Status.
        """
        return utils.read('Status')

    @nsStatus.expect(api.models['Status'], validate=True)
    def put(self):
        """
        Update Status.

        Use this method to update a Status.
        """
        return utils.update('Status', request.json)

    @nsStatus.expect(api.models['Status'], validate=True)
    def delete(self):
        """
        Delete Status.

        Use this method to delete a Status.
        """
        return utils.delete('Status', request.json)


if __name__ == '__main__':
    host_name = socket.gethostname()
    app.run(host=host_name, threaded=True)  # debug=True
