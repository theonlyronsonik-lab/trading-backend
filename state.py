import json
import os

STATE_FILE = "signal_state.json"


def load_state():
    if not os.path.exists(STATE_FILE):
        return {}
    with open(STATE_FILE, "r") as f:
        return json.load(f)


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def is_new_structure(symbol, structure):
    state = load_state()

    if symbol not in state:
        return True

    return state[symbol] != structure


def update_structure(symbol, structure):
    state = load_state()
    state[symbol] = structure
    save_state(state)
