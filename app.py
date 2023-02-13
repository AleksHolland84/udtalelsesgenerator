from jinja2 import Environment, FileSystemLoader, BaseLoader
from datetime import date
import streamlit as st # pip install streamlit
from streamlit_extras.buy_me_a_coffee import button as coffee_button # import streamlit extras
from streamlit_extras.no_default_selectbox import selectbox # import no default selectbox 
import pandas as pd # pip install pandas
import json

#To run the app, use a terminal: streamlit run .\app.py
#Jinja guide er fundet på https://realpython.com/primer-on-jinja-templating/

# Version number to show ppl on app
version = "2.0"



with open("templates.json", encoding="utf-8") as templates:
    template_data = json.load(templates)
grades = ('-3','00','02','4', '7', '10', '12')

# Create date variables
download_date = date.today().strftime("%d.%m.%Y")

# Use Jinja to generate common templates
common_environment = Environment(loader=FileSystemLoader("templates/"))
template_bedømmelse = common_environment.get_template("bedømmelse.txt") # Karakter, dato, lærere
template_info = common_environment.get_template("info.txt") # Elev, Overemne, Underemne, Problemformulering


# Get all default values for input boxes.
from session import *
set_session("session", "template_session")   # Get

def template_returner(grades: tuple = ('-3','00','02','4', '7', '10', '12'), template: str = "", template_selecter: str = "", key="") -> list:
    return_list = []
    for _grade in grades:
        st.caption(f"Anbefalet til karakteren {_grade}:")
        for line in template_selecter[template][_grade]:
            add_frem_line = st.checkbox(line, key=f"_{key}_{_grade}_{line}")
            if add_frem_line:
                return_list.append(line)
    user_input = st.text_area(f'Tilføj dine egne linjer her', key=f"_{key}_user_input")
    if user_input:
        return_list.append(user_input.capitalize())
    return return_list


if __name__ == "__main__":
    # Setup config - to configure title of webpage
    st.set_page_config(page_title='Projekttalelser', page_icon="📝",)

    st.title('Projektudtalelser')
    st.caption(f"version {version}")

    st.markdown('''Dette er en simpel udtalelsesgenerator, der generer elevudtalelser på baggrund af bedømmelsen på de 4 områder. 
                    Udfyld **_Overemne_**, **_Lærer 1_**, **_Lærer 2_** og ændre **_Dato_** hvis ønsket. Gå derefter videre til den enkelte elevudtalelse.
                    Udfold de 4 bedømmelsesområder; Arbejdsprocessen, Fagligtindhold, Produktet og Fremlæggelsen og :ballot_box_with_check:
                    de ønskede sætninger. Under hver bedømmelsesområde har du også mulighed for, at tilføje din egen sætning til sidst. Disse tilføjes
                    som den sidste sætning under hver bedømmelsesområde.
                    ''')

    class_size = 1

    overemne = st.text_input('Overemne', 
                        key="_overemne")

    LA1, LA2 = st.columns(2)
    with LA1:
        teacher1 = st.text_input(
            "Lærer 1",
            key="_teacher1",
        )
    with LA2:
        teacher2 = st.text_input(
            "Lærer 2",
            key="_teacher2",
        )

    date_stamp, location_stamp = st.columns(2)
    with date_stamp:
        date = st.date_input ("Dato", date(2023, 5, 2))
        date = date.strftime("%d.%m.%Y")
    with location_stamp:
        location = st.text_input("By", key="_location").capitalize()
        
    if class_size > 0:
        st.markdown('---')

        st.markdown('''Nedenfor kan du se datafeltet for elevudtalelsen.
        Udtalelsen bliver genereret ud fra de valgte sætninge under **Arbejdsprocessen**, **Fagligtindhold**, 
        **Produktet** og **Fremlæggelsen** og genereres løbende imens du bruger appen''')

        #st.subheader('Downloads:')
        st.subheader("Elevudtalelse")


        # Create input text for student name
        navn = st.text_input('Navn', key="_name")
        navn = ' '.join(elem.capitalize() for elem in navn.split())

        underemne = st.text_input('Underemne', key=f"_underemne")
        problemformulering = st.text_area('Problemformulering', key=f"_problem")
        gruppe_checkbox = st.checkbox(f'{"Eleven"} har arbejdet i gruppe', key="_gruppe_checkbox")

        if gruppe_checkbox == True:
            template_selecter = template_data["group_templates"]
        else:
            template_selecter = template_data["single_templates"]
            
        with st.expander("Arbejdssprocessen"):
            arbejdsprocessen = template_returner(template="arbejdsprocessen", template_selecter=template_selecter, key="_arb")


        with st.expander("Fagligtindhold"):
            fagligtindhold = template_returner(template="fagligtindhold", template_selecter=template_selecter, key="_fag")


        with st.expander("Produktet"):
            produkt = template_returner(template="produktet", template_selecter=template_selecter, key="_pro")

        with st.expander("Fremlæggelsen"):
            fremlæggelsen = template_returner(template="fremlæggelsen", template_selecter=template_selecter, key="_frem")


        # Create selectbox for the student's grade
        karakter = selectbox("Samlet karakter", ('-3','00','02','4', '7', '10', '12'), key=f"_grade")

                        
        # Content creation
        content = ""
        content = template_info.render(
            name = navn,
            delemne = underemne,
            overemne = overemne,
            problemformulering = problemformulering,
        ) + "\n\n"

        if gruppe_checkbox == True:
            gruppe_string = template_data["gruppe_checkbox"]["true"]
            template_gruppe = Environment(loader=BaseLoader()).from_string(f'{navn} {gruppe_string}')
            content = content + template_gruppe.render(
                elev = navn,
            )+ "\n\n"

        arbejdsprocessen_text = " ".join(arbejdsprocessen)
        template_arbejdsprocessen = Environment(loader=BaseLoader()).from_string("ARBEJDSPROCES: " + arbejdsprocessen_text)
        content = content + template_arbejdsprocessen.render() + "\n\n"
            
        fagligtindhold_text = " ".join(fagligtindhold)
        template_fagligtindhold = Environment(loader=BaseLoader()).from_string("FAGLIGT INDHOLD: " + fagligtindhold_text)
        content = content + template_fagligtindhold.render() + "\n\n"

        produkt_text = " ".join(produkt)
        template_produkt = Environment(loader=BaseLoader()).from_string("PRODUKT: " + produkt_text)
        content = content + template_produkt.render() + "\n\n"

        fremlæggelsen_text = " ".join(fremlæggelsen)
        template_fremlæggelse = Environment(loader=BaseLoader()).from_string("FREMLÆGGELSE: " + fremlæggelsen_text)
        content = content + template_fremlæggelse.render() + "\n\n"

        content = content + template_bedømmelse.render(
            date = date,
            grade = karakter,
            lærer1 = teacher1,
            lærer2 = teacher2,
            by = location,
        )

        # Display content to web app
        content_container = st.container()
        content_container.subheader("Generet elevudtalelse:")
        content_container.markdown(content)

        down_button, rest_button = st.columns([11,4], gap="large")
        with down_button:
            st.download_button(f'Download udtalelse', content, file_name=f"projektudtalelse_{navn}_{download_date}.txt", help=f"Downloader projektudtalelse for {navn}")
        
        with rest_button:
            st.button("Ny elevuudtalelse", on_click=reset_template_session, type="primary",help="Fjerner alt input under 'Elevudtalelse'. Overemne, lærernavne, dato og by slettes ikke,")
            
        st.markdown('-'*17)
            


    coffee, mail = st.columns([11,2 ])
    with coffee:
        #coffee_button(username="fake-username", floating=True, width=221)
        st.caption(f"Developer: A.Holland")

    with mail:
        #st.markdown('<a style="color:#9fa19f; text-decoration: none" href="mailto:hello@streamlit.io">Kontakt mig</a>', unsafe_allow_html=True)
        from streamlit_extras.mention import mention
        GOOGLE = "https://upload.wikimedia.org/wikipedia/commons/4/4e/Gmail_Icon.png"
        mention(
            label="A.Holland",
            icon="github",
            url="https://github.com/AleksHolland84",
        )

       