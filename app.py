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

def assign_employee_to_shift(shift_id, employee_id, data):
    # importeert de shift en werknemer lijsten
    shift = next((s for s in data['shifts'] if s['id'] == shift_id), None)
    employee = next((e for e in data['employees'] if e['id'] == employee_id), None)

    #shift bestaat niet
    if not shift:
        return False, "Shift niet gevonden"
    #employee bestaat niet
    if not employee:
        return False, "Werknemer niet gevonden"

    # CHECK 1: heeft de werknemer de skill?
    required_skill = shift['requiredSkill']
    if required_skill not in employee['skills']:
        return False, f"{employee['name']} mist de skill '{required_skill}'"

    # CHECK 2: is de werknemer beschikbaar tijdens deze shift?
    new_start = shift['start']
    new_end = shift['end']

    for s in data['shifts']:
        # Kijk alleen naar shifts die al aan deze persoon zijn gegeven
        if s.get('assignedEmployeeId') == employee_id:
            # Overlap als: (Start A < Eind B) EN (Eind A > Start B)
            if s['start'] < new_end and s['end'] > new_start:
                return False, f"{employee['name']} werkt al op dat tijdstip (shift {s['id']})"

    # succes flow:
    shift['assignedEmployeeId'] = employee_id
    return True, f"{employee['name']} is toegewezen aan shift {shift_id}!"


# 3. Testen in de terminal
if __name__ == '__main__':
    data = load_data()

    # Test 1: Anna heeft overlap
    _, msg1 = assign_employee_to_shift('s2', 'e1', data)
    print(msg1)

    # Test 2: Bram mist de skill
    _, msg2 = assign_employee_to_shift('s2', 'e2', data)
    print(msg2)

    # Test 3: Daan heeft alles goed
    _, msg3 = assign_employee_to_shift('s2', 'e3', data)
    print(msg3)