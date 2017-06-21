from e5 import app, event_stream
from e5.events import Event, ContextFilter

from flask import jsonify, request
from flask_login import login_required

@app.route('/event/<event_id>', methods=['DELETE'])
@login_required
def delete_event(event_id):
    result = event_stream.delete_event(event_id)
    if result.deleted_count > 0:
        return ('', 200)

    return ('', 500)

@app.route('/event', methods=['GET'])
@login_required
def get_events():
    events = event_stream.get_events()
    event_dicts = []
    for event in events:
        event_dicts.append(event.dict)

    return jsonify(event_dicts)

@app.route('/event/<context_type>/<context_id>', methods=['GET'])
@login_required
def get_events_by_context(context_type, context_id):
    context_filter = ContextFilter(context_id, context_type)
    events = event_stream.get_events(context_filters = [context_filter])
    event_dicts = []
    for event in events:
        event_dicts.append(event.dict)

    return jsonify(event_dicts)

@app.route('/event', methods=['POST'])
@login_required
def create_event():
    content = request.json
    event = Event.from_dict(content)
    event_id = event_stream.push(event)
    if event_id is not None:
        #TODO return event_id
        return ('', 200)

    return ('', 500)
