import streamlit as st
from PIL import Image
import time
from io import StringIO
import openai
import graphviz
from pyjarowinkler import distance

st.set_page_config(page_title="Morpheus",
                   page_icon="morpheus_tab_logo_.png",
                   layout="wide")
with st.container():
  cola, colb, colc = st.columns([0.09, 3.5, 1])
  with cola:
    image1 = Image.open('Fractal-Logo-WithBL.png')
    st.image(image1, width=120)
  with colc:
    image1 = Image.open('morpheus_logo_.png')
    st.image(image1, width=150)
  st.write("")
  st.markdown(
    "<h1 style='text-align: center; color: white;font-size: 35px;padding: 0.5% 0.5% 0.5% 0.5%;background-color: #2158B4 ;'>Code Rationalization</h1>",
    unsafe_allow_html=True)

st.title("")
st.markdown("""
<style>
/*sidebar*/
.css-163ttbj
{
    background-color:#f7efdb
}
.css-184tjsw p
{
font-weight:600;
}
/*progress bar*/
.stProgress > div > div > div > div { 
    background-image: linear-gradient(to right, #ebc395 , #e9b271); 
    }
/*button*/
div.stButton > button {
    background-color: #f6e6bc;
    color:black;
    }
div.stButton > button:hover {
    background-color: #f7efdb;
    color:black;
    }
div.stButton > button:focus {
    background-color:#f6e6bc;
    color:black;
    }
div.stButton > button:active {
    background-color: #f6e6bc;
    color:black;
    }
</style>""",
            unsafe_allow_html=True)

code = st.selectbox("Choose an option to compare", ["Sas", "PySpark", "BQ"])
tab1, tab2 = st.tabs(["Comparison", "Results"])
sascode1 = ''
sascode2 = ''
sas_analysis_json1 = ''
sas_analysis_json2 = ''
sas_digraph_out1 = ''
sas_digraph_out2 = ''
with tab1:
  if code == "Sas":
    # File uploaders
    sas_file1 = st.file_uploader("Choose file", key="file1")
    if sas_file1:
      sas_stringio1 = StringIO(sas_file1.getvalue().decode("utf-8"))
      sascode1 = sas_stringio1.read()
      st.code(sascode1, language="sas")

    sas_file2 = st.file_uploader("Choose file", key="file2")
    if sas_file2:
      sas_stringio2 = StringIO(sas_file2.getvalue().decode("utf-8"))
      sascode2 = sas_stringio2.read()
      st.code(sascode2, language="sas")

    # button to compare
    cmpr = st.button("Compare")
    if cmpr:
      if sas_file1 and sas_file2:
        # comparison code here
        st.write("")
        prgs_text = st.empty()
        prgs = st.empty()

        #  FOR FIRST SAS CODE
        prgs_text.markdown(
          "<h6 style='font-size: 15px;'>Analyzing First SAS Code</h6>",
          unsafe_allow_html=True)
        prgs.progress(0)

        sas_code_analysis1 = openai.ChatCompletion.create(
          model="gpt-3.5-turbo",  # this is "ChatGPT" $0.002 per 1k tokens
          messages=[{
            "role": "system",
            "content": sascode1
          }, {
            "role":
            "user",
            "content":
            "provide the input_count, join_count, aggregation_count, jointype, joinkeys, aggergation function, aggregation column, group by in a json format. This json should be 0 level nesting. Provide json output only "
          }])
        sas_analysis_reply_content1 = sas_code_analysis1.choices[
          0].message.content
        sas_analysis_json1 = "[ \n" + sas_analysis_reply_content1 + "\n]"
        st.write("Analyzing First SAS Code - Done")
        ## Find out Dependencies in SAS code
        prgs_text.markdown(
          "<h6 style='font-size: 15px;'>Getting first SAS code dataset dependencies</h6>",
          unsafe_allow_html=True)
        prgs.progress(25)

        sas_code_dependency1 = openai.ChatCompletion.create(
          model="gpt-3.5-turbo",  # this is "ChatGPT" $0.002 per 1k tokens
          messages=[{
            "role": "system",
            "content": sascode1
          }, {
            "role":
            "user",
            "content":
            "provide  datasets and operations dependency in a  GraphViz's Dot language with digraph and rankdir=TB with dataset nodes as rectangle and operation nodes as circle with no style and no fill color"
          }])
        sas_reply_content1 = sas_code_dependency1.choices[0].message.content
        sas_digraph_start1 = sas_reply_content1.index("{")
        sas_digraph_end1 = sas_reply_content1.index("}")
        sas_digraph_interim1 = sas_reply_content1[sas_digraph_start1 -
                                                  1:sas_digraph_end1 + 1]
        sas_digraph_out1 = " digraph " + sas_digraph_interim1
        ##sas_digraph_stringio = StringIO(sas_digraph_out.getvalue().decode("utf-8"))
        ##sas_digraph_final = spark_digraph_stringio.read()
        st.write("Getting first SAS code dataset dependencies - Done")
        #  FOR SECOND SAS CODE
        prgs_text.markdown(
          "<h6 style='font-size: 15px;'>Analyzing second SAS code</h6>",
          unsafe_allow_html=True)
        prgs.progress(50)
        # st.write ("Analyzing Second SAS Code - STARTED")
        sas_code_analysis2 = openai.ChatCompletion.create(
          model="gpt-3.5-turbo",  # this is "ChatGPT" $0.002 per 1k tokens
          messages=[{
            "role": "system",
            "content": sascode2
          }, {
            "role":
            "user",
            "content":
            "provide the input_count, join_count, aggregation_count, jointype, joinkeys, aggergation function, aggregation column, group by in a json format. This json should be 0 level nesting. Provide json output only "
          }])
        sas_analysis_reply_content2 = sas_code_analysis2.choices[
          0].message.content
        sas_analysis_json2 = "[ \n" + sas_analysis_reply_content2 + "\n]"
        st.write("Analyzing second SAS code - Done")
        ## Find out Dependencies in SAS code
        prgs_text.markdown(
          "<h6 style='font-size: 15px;'>Getting second SAS code dataset dependencies</h6>",
          unsafe_allow_html=True)
        prgs.progress(75)

        sas_code_dependency2 = openai.ChatCompletion.create(
          model="gpt-3.5-turbo",  # this is "ChatGPT" $0.002 per 1k tokens
          messages=[{
            "role": "system",
            "content": sascode2
          }, {
            "role":
            "user",
            "content":
            "provide  datasets and operations dependency in a  GraphViz's Dot language with digraph and rankdir=TB with dataset nodes as rectangle and operation nodes as circle with no style and no fill color"
          }])
        sas_reply_content2 = sas_code_dependency2.choices[0].message.content
        sas_digraph_start2 = sas_reply_content2.index("{")
        sas_digraph_end2 = sas_reply_content2.index("}")
        sas_digraph_interim2 = sas_reply_content2[sas_digraph_start2 -
                                                  1:sas_digraph_end2 + 1]
        sas_digraph_out2 = "  \n digraph " + sas_digraph_interim2
        ##sas_digraph_stringio = StringIO(sas_digraph_out.getvalue().decode("utf-8"))
        ##sas_digraph_final = spark_digraph_stringio.read()
        st.write("Getting second SAS code dataset dependencies - Done")
        prgs_text.markdown(
          "<h6 style='font-size: 15px;'>Comparison Done!</h6>",
          unsafe_allow_html=True)
        prgs.progress(100)

      else:
        st.error("Please Upload both files")
  else:
    image1 = Image.open('wip.png')
    st.image(image1, width=350)
with tab2:
  if code == "Sas":
    #index logic here
    if sas_analysis_json1 != '' and sas_analysis_json2 != '':
      comparision_index = int(
        round(
          distance.get_jaro_distance(str(sas_analysis_json1),
                                     str(sas_analysis_json2),
                                     winkler=True,
                                     scaling=0.1) * 100))
    else:
      comparision_index = 0

    progress_text = "Comparison Index"

    # Progress bar to show conersion index
    c1, c2 = st.columns([2, 1])
    my_bar = c1.progress(0, text=progress_text)

    # small animation to progress bar
    for percent_complete in range(comparision_index):
      time.sleep(0.01)
      my_bar.progress(percent_complete + 1, text=progress_text)
    c2.header(str(comparision_index) + '%')

    st.title("")

    # Expander to display Tabular details
    with st.expander("Comaprision Details"):
      st.write("SAS Code details Comparison")
      col1, col2 = st.columns(2)
      with col1:
        st.write("First SAS code details")
        if sas_analysis_json1 != '':
          st.json(sas_analysis_json1)
        else:
          st.write('Please load Valid Json')
      with col2:
        st.write("Second SAS code details")
        if sas_analysis_json2 != '':
          st.json(sas_analysis_json2)
        else:
          st.write('Please load Valid Json')
      st.write(
        "====================================================================")
      st.write("")
      st.write("SAS Code Dependency Comparison")
      col3, col4 = st.columns(2)
      with col3:
        st.write("First SAS code Dependency Diagram")
        #st.write(sas_digraph_out1)
        #print(sas_digraph_out1)
        st.graphviz_chart(sas_digraph_out1)
        st.write(sas_digraph_out1)
      with col4:
        st.write("Second SAS code Dependency Diagram")
        #st.write(sas_digraph_out2)
        #print(sas_digraph_out2)
        st.graphviz_chart(sas_digraph_out2)
        st.write(sas_digraph_out2)
        #st.graphviz_chart(' digraph { node[shape=ellipse]; orders -> orders_customers [label="join"]; customers -> orders_customers [label="join"]; orders_customers -> customer_sales [label=" aggregation"]; }')

    # Expander to show Test cases
    with st.expander("Test Cases"):
      image1 = Image.open('wip.png')
      st.image(image1, width=350)
  else:
    image1 = Image.open('wip.png')
    st.image(image1, width=350)
