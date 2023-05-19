from flask import Flask, request, jsonify

app = Flask(__name__)

# Sample event data
events = [
    {
        "id": 1,
        "uid": 18,
        "name": "Event 1",
        "tagline": "Tagline for Event 1",
        "schedule": "2023-05-20T10:00:00Z",
        "description": "Description for Event 1",
        "moderator": "John Doe",
        "category": "Category 1",
        "sub_category": "Subcategory 1",
        "rigor_rank": 5,
        "attendees": []
    }
    # Add more events here...
]


# GET /api/v3/app/events?id=:event_id
@app.route('/api/v3/app/events', methods=['GET'])
def get_event_by_id():
    event_id = request.args.get('id')
    event = next((e for e in events if e['id'] == int(event_id)), None)

    if event:
        return jsonify(event)
    else:
        return jsonify({'error': 'Event not found'}), 404


# GET /api/v3/app/events?type=latest&limit=5&page=1
@app.route('/api/v3/app/events', methods=['GET'])
def get_latest_events():
    event_type = request.args.get('type')
    limit = int(request.args.get('limit', 5))
    page = int(request.args.get('page', 1))

    # Filter events by type (if needed)
    # filtered_events = [e for e in events if e['type'] == event_type]

    # Paginate results
    start_index = (page - 1) * limit
    end_index = page * limit
    paginated_events = events[start_index:end_index]

    return jsonify(paginated_events)


# POST /api/v3/app/events
@app.route('/api/v3/app/events', methods=['POST'])
def create_event():
    event_data = request.json
    new_event_id = len(events) + 1
    new_event = {
        "id": new_event_id,
        **event_data,
        "attendees": []
    }

    events.append(new_event)
    return jsonify({"id": new_event_id})


# PUT /api/v3/app/events/:id
@app.route('/api/v3/app/events/<int:event_id>', methods=['PUT'])
def update_event(event_id):
    event_data = request.json

    event_index = next((i for i, e in enumerate(events) if e['id'] == event_id), None)
    if event_index is not None:
        events[event_index] = {"id": event_id, **event_data}
        return jsonify({"message": "Event updated successfully"})
    else:
        return jsonify({'error': 'Event not found'}), 404


# DELETE /api/v3/app/events/:id
@app.route('/api/v3/app/events/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    event_index = next((i for i, e in enumerate(events) if e['id'] == event_id), None)
    if event_index is not None:
        events.pop(event_index)
        return jsonify({"message": "Event deleted successfully"})
    else:
        return jsonify({'error': 'Event not found'}), 404


if __name__ == '__main__':
    app.run()
