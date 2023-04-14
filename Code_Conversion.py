import streamlit as st
from PIL import Image
import time
from io import StringIO
import openai
import graphviz 
from pyjarowinkler import distance

st.set_page_config(page_title="Morpheus", page_icon="morpheus_tab_logo_.png", layout="wide")
openai.api_key = open("key.txt","r").read().strip('\n')

with st.container():
    cola,colb,colc=st.columns([0.09,3.5,1])
    with cola:
        image1 = Image.open('Fractal-Logo-WithBL.png')
        st.image(image1,width=120)
    with colc:
        image1 = Image.open('morpheus_logo_.png')
        st.image(image1,width=150)
    st.write("")
    st.markdown("<h1 style='text-align: center; color: white;font-size: 35px;padding: 0.5% 0.5% 0.5% 0.5%;background-color: #2158B4 ;'>Code Conversion</h1>", unsafe_allow_html=True)

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
</style>""", unsafe_allow_html=True)


code=st.selectbox("Choose an option to convert",["Sas to PySpark","Sas to BQ","IBM SPL to PySpark"])

tab1,tab2=st.tabs(["Conversion","Results"])
sparkcode=''
sas_analysis_json=''
spark_analysis_json=''
sas_digraph_final=''
spark_digraph_final=''
sas_digraph_out=''
spark_digraph_out=''
sas_explainability_reply_content=''
spark_explainability_reply_content=''
with tab1:
    if code=="Sas to PySpark":
        # Expander to upload Sas code 
        with st.expander("Upload Sas Code"):
            #File uploader
            sasfile=st.file_uploader("Choose file")
            if sasfile:
                sas_stringio = StringIO(sasfile.getvalue().decode("utf-8"))
                sascode = sas_stringio.read()
                st.code(sascode,language="sas")
            #Button to Covert
            cnvrt=st.button("Convert")

            if cnvrt:
                if sasfile:
                    # coversion code here
                    st.write("")
                    prgs_text=st.empty()
                    prgs=st.empty()

                    ## Analyze SAS code operators
                    prgs_text.markdown("<h6 style='font-size: 15px;'>Analyzing SAS Code</h6>", unsafe_allow_html=True)
                    prgs.progress(0)
                    
                    sas_code_analysis = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo", # this is "ChatGPT" $0.002 per 1k tokens
                        #messages=[{"role": "system", "content": sascode},{"role": "user", "content": "provide the input_count, join_count, aggregation_count, jointype, joinkeys, aggergation function, aggregation column, group by in a json format. This json should be 0 level nesting. Provide json output only "} ]
                        messages=[{"role": "system", "content": sascode},{"role": "user", "content": "Provide no. of inputs, transformations  , joins , aggregations, sorting & outputs and operation details of inputs, transformations, joins, aggregations, sorting & outputs  in json format with keys as input_count, transformation_count, join_count, agg_count, sort_count, output_count, input_details, transformation_details , join_details, agg_details, sort_details, output_details respectively.This json should be 0 level nesting. Provide json output only "} ]
                            )
                    sas_analysis_reply_content = sas_code_analysis.choices[0].message.content
                    sas_analysis_json = "[ \n"+sas_analysis_reply_content+"\n]"
                    st.write ("SAS Code Analysis - Done")

                    ##  SAS code Explainability
                    prgs_text.markdown("<h6 style='font-size: 15px;'>SAS code Explainability</h6>", unsafe_allow_html=True)
                    prgs.progress(15)
                    
                    sas_code_explainability = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo", # this is "ChatGPT" $0.002 per 1k tokens
                        #messages=[{"role": "system", "content": sascode},{"role": "user", "content": "provide the input_count, join_count, aggregation_count, jointype, joinkeys, aggergation function, aggregation column, group by in a json format. This json should be 0 level nesting. Provide json output only "} ]
                        messages=[{"role": "system", "content": sascode},{"role": "user", "content": "Explain the details of SAS code steps in business terms with step names ."} ]
                            )
                    sas_explainability_reply_content = sas_code_explainability.choices[0].message.content
                    #sas_analysis_json = "[ \n"+sas_analysis_reply_content+"\n]"
                    st.write ("SAS Code Explainability - Done")
                    
                    ## Find out Dependencies in SAS code
                    prgs_text.markdown("<h6 style='font-size: 15px;'>Getting SAS code dataset dependencies</h6>", unsafe_allow_html=True)
                    prgs.progress(30)
                    
                    sas_code_dependency= openai.ChatCompletion.create(
                        model="gpt-3.5-turbo", # this is "ChatGPT" $0.002 per 1k tokens
                        #messages=[{"role": "system", "content": sascode},{"role": "user", "content": "provide  datasets and operations dependency in a  GraphViz's Dot language with digraph and rankdir=TB with dataset nodes as rectangle and operation nodes as circle with no style and no fill color and no subgraph"} ]
                        messages=[{"role": "system", "content": sascode},{"role": "user", "content": "provide  datasets and operations dependency in a  GraphViz's Dot language with digraph and rankdir=TB with dataset nodes as rectangle and operation nodes as circle with no style and no fill color and no subgraph in output digraph "} ]
                            )
                    sas_reply_content = sas_code_dependency.choices[0].message.content
                    sas_digraph_start = sas_reply_content.index("{")
                    sas_digraph_end= sas_reply_content.index("}")
                    sas_digraph_interim = sas_reply_content[sas_digraph_start-1 : sas_digraph_end+1]
                    sas_digraph_out = " \n digraph " + sas_digraph_interim 
                    ##sas_digraph_stringio = StringIO(sas_digraph_out.getvalue().decode("utf-8"))
                    ##sas_digraph_final = spark_digraph_stringio.read()
                    st.write ("Getting SAS code Dependencies - Done")

                    ## Convert SAS to Pyspark Json
                    prgs_text.markdown("<h6 style='font-size: 15px;'>Converting SAS Code to Pyspark</h6>", unsafe_allow_html=True)
                    prgs.progress(45)
                    
                    spark_completion = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo", # this is "ChatGPT" $0.002 per 1k tokens
                        messages=[{"role": "system", "content": sascode},{"role": "user", "content": "Convert SAS program to Pyspark with dataframes and keep the code in between pyspark-start and pyspark-end "} ]
                            )
                    spark_int_code = spark_completion.choices[0].message.content
                    spark_pattern_start = spark_int_code.index("pyspark-start")
                    spark_pattern_stop = spark_int_code.index("pyspark-end")

                    sparkcode = spark_int_code[spark_pattern_start+14 : spark_pattern_stop]
                    
                    st.write ("Converting SAS Code to Pyspark - Done")
                    ## Analyze Spark code operators
                    prgs_text.markdown("<h6 style='font-size: 15px;'>Analyzing PYSpark Code</h6>", unsafe_allow_html=True)
                    prgs.progress(60)
                    
                    spark_code_analysis = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo", # this is "ChatGPT" $0.002 per 1k tokens
                        #messages=[{"role": "system", "content": spark_int_code},{"role": "user", "content": "provide the input_count, join_count, aggregation_count, jointype, joinkeys, aggergation function, aggregation column, group by in a json format. This json should be 0 level nesting. Provide json output only  "} ]
                        messages=[{"role": "system", "content": spark_int_code},{"role": "user", "content": "Provide no. of inputs, transformations  , joins , aggregations, sorting & outputs and operation details of inputs, transformations, joins, aggregations, sorting & outputs  in json format with keys as input_count, transformation_count, join_count, agg_count, sort_count, output_count, input_details, transformation_details , join_details, agg_details, sort_details, output_details respectively. This json should be 0 level nesting. Provide json output only  "} ]
                            )
                    spark_analysis_reply_content = spark_code_analysis.choices[0].message.content
                    spark_analysis_json = "[ \n"+spark_analysis_reply_content+"\n]"
                    
                    st.write ("Analyzing PYSpark Code - Done")

                    ##  Spark code Explainability
                    prgs_text.markdown("<h6 style='font-size: 15px;'>SAS code Explainability</h6>", unsafe_allow_html=True)
                    prgs.progress(75)
                    
                    spark_code_explainability = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo", # this is "ChatGPT" $0.002 per 1k tokens
                        #messages=[{"role": "system", "content": sascode},{"role": "user", "content": "provide the input_count, join_count, aggregation_count, jointype, joinkeys, aggergation function, aggregation column, group by in a json format. This json should be 0 level nesting. Provide json output only "} ]
                        messages=[{"role": "system", "content": spark_int_code},{"role": "user", "content": "Explain the details of pySpark code steps in business terms and with step names ."} ]
                            )
                    spark_explainability_reply_content = spark_code_explainability.choices[0].message.content
                    #sas_analysis_json = "[ \n"+sas_analysis_reply_content+"\n]"
                    st.write ("PySpark Code Explainability - Done")
                    
                    ##Find out dependencies in Spark code
                    prgs_text.markdown("<h6 style='font-size: 15px;'>Getting Spark Dataframe dependencies</h6>", unsafe_allow_html=True)
                    prgs.progress(90)

                    spark_code_dependency = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo", # this is "ChatGPT" $0.002 per 1k tokens
                        #messages=[{"role": "system", "content": spark_int_code},{"role": "user", "content": "provide  datframes and operations dependency in a  GraphViz's Dot language with digraph and rankdir=TB with dataframe nodes as rectangle and operation nodes as circle with no style and no fill color "} ]
                        messages=[{"role": "system", "content": spark_int_code},{"role": "user", "content": "provide  datasets and operations dependency in a  GraphViz's Dot language with digraph and rankdir=TB with dataset nodes as rectangle and operation nodes as circle with no style and no fill color and no subgraph in output digraph "} ]
                            )
                    spark_reply_content = spark_code_dependency.choices[0].message.content
                    spark_digraph_start = spark_reply_content.index("{")
                    spark_digraph_end= spark_reply_content.index("}")
                    spark_digraph_interim = spark_reply_content[spark_digraph_start-1 : spark_digraph_end+1]
                    spark_digraph_out = " \n digraph " + spark_digraph_interim 
                    ##spark_digraph_stringio = StringIO(spark_digraph_out.getvalue().decode("utf-8"))
                    ##spark_digraph_final = spark_digraph_stringio.read()
                    st.write ("Getting Spark Dataframe dependencies - Done")
                    prgs_text.markdown("<h1 style='font-size: 15px;color:black'>Converted Successfully!</h1>", unsafe_allow_html=True)
                    prgs.progress(100)

                    
                else:
                    st.error("Please upload code")

        # Expander to display converted Pyspark code            
        with st.expander("Converted Spark Code"):
            st.code(sparkcode,language="python")
     
    else:
        image1 = Image.open('wip.png')
        st.image(image1,width=350)

with tab2:
    if code=="Sas to PySpark":
        #index logic here
        if sas_analysis_json != '' and spark_analysis_json != '' :
            conversion_index= int(round(distance.get_jaro_distance(str(sas_analysis_json), str(spark_analysis_json),winkler=True, scaling=0.1)*100))
        else:
            conversion_index=0
        progress_text="Conversion Index"
        
        # Progress bar to show conersion index
        c1,c2=st.columns([2,1])
        my_bar = c1.progress(0, text=progress_text)

        # small animation to progress bar
        for percent_complete in range(conversion_index):
            time.sleep(0.01)
            my_bar.progress(percent_complete + 1, text=progress_text)
        c2.header(str(conversion_index)+'%')

        # Expander to show graph and table
        with st.expander("Code Analysis Comparison"):
            col1, col2 = st.columns(2)
            with col1:
                st.write("SAS Code Analysis")
                if sas_analysis_json != '':
                    st.json(sas_analysis_json)
                else:
                    st.write('Please load Valid Json')
            with col2:
                st.write("Spark Code Analysis")
                if spark_analysis_json != '':
                    st.json(spark_analysis_json)
                else:
                    st.write('Please load Valid Json')
                

        # Expander to show graph and table
        with st.expander("Dependency Comparison Details"):
            col3, col4 = st.columns(2)
            with col3:
                st.write("SAS Code Dataset Dependecy Chart")
                st.graphviz_chart(sas_digraph_out)
                st.write(sas_digraph_out)
            with col4:
                st.write("Spark Code Dataframe Dependecy Chart")
                st.graphviz_chart(spark_digraph_out)
                st.write(spark_digraph_out)
        
        # Expander to show Code Explainability
        with st.expander("Code Explainability"):
            #image1 = Image.open('wip.png')
            #st.image(image1,width=350)
            col5, col6 = st.columns(2)
            with col5:
                st.write("SAS Code Explainability")
                
                st.write(sas_explainability_reply_content)
            with col6:
                st.write("SAS Code Explainability")
                
                st.write(spark_explainability_reply_content)
            
    else:
        image1 = Image.open('wip.png')
        st.image(image1,width=350)