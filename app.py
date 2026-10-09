import json
from flask import Flask, request, jsonify

# het definieren van het bestand voor Flask
app = Flask(__name__)

def load_data():
    with open('data.json', 'r') as file:
        return json.load(file)

# Schrijft data terug naar Data.json
def save_data(data):
    with open('data.json', 'w') as file:
        json.dump(data, file, indent=2)

@app.route('/shifts/<shift_id>/eligible-employees', methods=['GET'])
def get_eligible_employees(shift_id):
    data = load_data()

    # 1. Zoek op shift
    shift = next((s for s in data['shifts'] if s['id'] == shift_id), None)
    if not shift:
        return jsonify({"error": "Shift niet gevonden"}), 404

    eligible_employees = []
    required_skill = shift.get('requiredSkill')
    new_start = shift['start']
    new_end = shift['end']

    # 2. Controleer elke medewerker in de lijst
    for emp in data['employees']:
        # CHECK 1: heeft de medewerker de skill?
        if required_skill and required_skill not in emp.get('skills', []):
            continue  # Sla deze medewerker over

        # CHECK 2: Heeft de medewerker tijdsoverlap?
        has_overlap = False
        for s in data['shifts']:
            if s.get('assignedEmployeeId') == emp['id']:
                if s['start'] < new_end and s['end'] > new_start:
                    has_overlap = True
                    break

        if has_overlap:
            continue  # Sla deze medewerker over

        # Als alle checks goed zijn, is de medewerker geschikt!
        eligible_employees.append({
            "id": emp['id'],
            "name": emp['name'],
            "skills": emp['skills']
        })

    # 3. Geef de lijst van geschikte medewerkers terug
    return jsonify({"eligible_employees": eligible_employees}), 200

@app.route('/shifts/<shift_id>/assign', methods=['POST'])
def assign_shift_api(shift_id):
    # 1. Lees het berichtje (JSON) dat binnenkomt
    body = request.get_json()
    employee_id = body.get('employee_id')

    # 2. Laad de data
    data = load_data()

    # 3. Zoek de shift en werknemer
    shift = next((s for s in data['shifts'] if s['id'] == shift_id), None)
    employee = next((e for e in data['employees'] if e['id'] == employee_id), None)

    #shift bestaat niet
    if not shift:
        return jsonify({"error": "Shift niet gevonden"}), 404
    #employee bestaat niet
    if not employee:
        return jsonify({"error": "Werknemer niet gevonden"}), 404

    # CHECK 1: heeft de werknemer de skill?
    required_skill = shift['requiredSkill']
    if required_skill not in employee['skills']:
        return jsonify({"error": f"{employee['name']} mist skill '{required_skill}'"}), 400

    # CHECK 2: is de werknemer beschikbaar tijdens deze shift?
    new_start = shift['start']
    new_end = shift['end']

    for s in data['shifts']:
        # Kijk alleen naar shifts die al aan deze persoon zijn gegeven
        if s.get('assignedEmployeeId') == employee_id:
            # Overlap als: (Start A < Eind B) EN (Eind A > Start B)
            if s['start'] < new_end and s['end'] > new_start:
                return jsonify({"error": f"{employee['name']} werkt al op dat moment"}), 409

    # succes flow:
    shift['assignedEmployeeId'] = employee_id
    save_data(data) # Sla het op in data.json!

    return jsonify({
        "message": "Succesvol toegewezen!",
        "shift_id": shift_id,
        "assigned_to": employee['name']
    }), 200

# Start de server op jouw computer
if __name__ == '__main__':
    app.run(port=5000, debug=True)