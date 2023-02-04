from jinja2 import Environment, FileSystemLoader
from datetime import date
import streamlit as st # pip install streamlit
import pandas as pd # pip install pandas

#To run the app, use a terminal: streamlit run .\app.py
#Inspiration til denne app er fundet i videoen: https://www.youtube.com/watch?v=IolyDeV0wmo.
#Jinja guide er fundet på https://realpython.com/primer-on-jinja-templating/
whole_content = ""

# Create date variables
today = date.today()
date = today.strftime("%d.%m.%Y")

# Use Jinja to generate common templates
common_environment = Environment(loader=FileSystemLoader("templates/"))
template_bedømmelse = common_environment.get_template("bedømmelse.txt") # Karakter, dato, lærere
template_info = common_environment.get_template("info.txt") # Elev, Overemne, Underemne, Problemformulering

students = {}

# Setup config - to configure title of webpage
st.set_page_config(page_title='Projekttalelser')

if __name__ == "__main__":

    st.title('Projektudtalelser')
    class_size = st.slider('Hvor mange elever', 0, 40, 0)

    for i in range(class_size):
        students[f"name_{i}"] = f"Elev {i+1}"

    overemne = st.text_input('Overemne', 'Det moderne samfund')

    LA1, LA2 = st.columns(2)
    with LA1:
        teacher1 = st.text_input(
            "Lærer 1",
            "KK",
            key="teacher1",
        )
    with LA2:
        teacher2 = st.text_input(
            "Lærer 2",
            "AH",
            key="teacher2",
        )


    if class_size > 0:
        st.markdown('---')

        #df = pd.read_excel(uploaded_file, engine='openpyxl')

        st.markdown('Nedenfor er et datasæt, som du kan bruge til at kontrollere dit uploaded data')

        st.subheader('Downloads:')

        for student in students:

            _name = students[student]

            # Create subheader with stueden's name
            st.subheader(_name)

            # Create input text for student name
            navn = st.text_input('Navn', f'{_name}')

            underemne = st.text_input('Underemne', 'The most awesome underemne ever!', key=f"{navn}_underemne")
            problemformulering = st.text_input('Problemformulering', 'Problem...', key=f"{navn}_problem")
            gruppe_checkbox = st.checkbox(f'{navn} har arbejdet i gruppe')

            # Create columns with student's grade for the 4 areas
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                arb_grade = st.selectbox("Arbejdsprocessen", ('-3','00','02','4', '7', '10', '12'), key=f"{navn}_arb")
            with col2:
                fag_grade = st.selectbox("Fagligtindhold", ('-3','00','02','4', '7', '10', '12'), key=f"{navn}_fag")
            with col3:
                pro_grade = st.selectbox("Produktet", ('-3','00','02','4', '7', '10', '12'), key=f"{navn}_pro")
            with col4:
                frem_grade = st.selectbox("Fremlæggelsen", ('-3','00','02','4', '7', '10', '12'), key=f"{navn}_frem")

            # Create selectbox for the student's grade
            grade = st.selectbox("Samlet karakter", ('-3','00','02','4', '7', '10', '12'), key=f"{navn}_grade")


            # Brug Jinja til at generere skabeloner 
            if gruppe_checkbox == True:
                environment = Environment(loader=FileSystemLoader("templates/gruppe/"))
            
            else:
                environment = Environment(loader=FileSystemLoader("templates/single/"))
            content = ""
            # genererer filnavn på baggrund af den studerendes navn


            content = template_info.render(
                name = navn,
                delemne = underemne,
                overemne = overemne,
                problemformulering = problemformulering,
            ) + "\n\n"


            template_fagligtindhold = environment.get_template(f"fagligtindhold{fag_grade}.txt")
            content = content + template_fagligtindhold.render() + "\n\n"

            template_arbejdsprocessen = environment.get_template(f"arbejdsprocessen{arb_grade}.txt")
            content = content + template_arbejdsprocessen.render() + "\n\n"

            template_produkt = environment.get_template(f"produkt{pro_grade}.txt")
            content = content + template_produkt.render() + "\n\n"

            template_fremlæggelse = environment.get_template(f"fremlæggelse{frem_grade}.txt")
            content = content + template_fremlæggelse.render() + "\n"

            

            content = content + template_bedømmelse.render(
                date = date,
                grade = grade,
                lærer1 = teacher1,
                lærer2 = teacher2,
            )



            #df_student = pd.read_csv(StringIO(content))
            #generate_student_link(content, name=navn)

            st.markdown(content)
            st.download_button(f'Download {navn}', content, file_name=f"projektudtalelse_{navn}_{date}.txt")
            st.markdown('-'*17)
            whole_content += content + "\r\n" + '-'*80 + "\n\n\n"
    st.download_button('Download alle udtalelser', whole_content)

