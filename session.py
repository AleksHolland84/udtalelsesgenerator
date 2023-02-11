import streamlit as st
import json

with open("templates.json", encoding="utf-8") as templates:
    session_data = json.load(templates)


# Sets the session keys, defined in the templates.json file, to the values defined in the file.
def set_session(*sessions):
    for session in sessions: 
        session_items = session_data[session]
        for key, value in session_items.items():
            if key not in st.session_state:
                print("Key not set", key)
                print(f"Setting session: {key}:{value}")
                st.session_state[key] = value
            else:
                print(f"Session key found: {key}: {st.session_state[key]}")
                pass

# This function is not used, but os ment to reset (remove) all values from the session part.
# Defined in the templates.json file
def reset_session():
    session_items = session_data["session"]
    for key, value in session_items.items():
        if key  in st.session_state:
            st.session_state[key] = ""

# This function is triggeret when the button "Ny elevudtalelse" is pressed.
# It resets (removes) all data from the template session par.
# Defined in the templates.json file.
def reset_template_session():
    session_items = session_data["template_session"]
    for key, value in session_items.items():
        if key in st.session_state:
            st.session_state[key] = value
            # This part below could be remoed...
            if isinstance(st.session_state[key], str): 
                st.session_state[key] = ""
            elif isinstance(st.session_state[key], bool):
                st.session_state[key] = False

    # Reset checked checkboxes for 
    uncheck_checkboxes("single_templates", "group_templates")

def uncheck_checkboxes(*templates):
    for template in templates:
        print(f"Unchecking {template}")
        areas = {
                "arbejdsprocessen": "_arb", 
                "fagligtindhold": "_fag", 
                "produktet": "_pro", 
                "fremlæggelsen": "_frem"
                }
        for area, _key in areas.items():
            single_templates = session_data.get(template)[area]
            for grade, lines in single_templates.items():
                for line in lines:
                    key = f"{_key}_{grade}_{line}"
                    if key in st.session_state:
                        if isinstance(st.session_state[key], bool):
                            st.session_state[key] = False   
    

def debug_session():
    for key in st.session_state:
        print(key, st.session_state[key])

    