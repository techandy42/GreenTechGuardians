import os
from dotenv import load_dotenv
import pinecone
from openai import OpenAI
import streamlit as st
import pandas as pd
from individual_report_app import report
from data_visualization_app import scatter_results_3d
from chatbot_module import Conversation
from search_query_tags_module import get_search_query_tags
import cohere
from data_extraction_module import extract_data_from_csv_file, get_last_index

load_dotenv()

client = OpenAI(
  api_key=os.environ['OPENAI_API_KEY']
)

co = cohere.Client(os.environ['COHERE_API_KEY'])

def get_embeddings(texts):
    response = client.embeddings.create(input=texts, model="text-embedding-ada-002")
    return [embedding.embedding for embedding in response.data]

def get_reranked_item(rerank_result, docs):
    doc = docs[rerank_result.index]
    doc['relevance_score'] = rerank_result.relevance_score
    return doc

def search_index(query, index, df, top_k=10):
    # Get search query tags
    search_query_tags_response = get_search_query_tags(query)
    search_query_tags = search_query_tags_response.tags

    # Do similarity search
    query_embedding = get_embeddings([query])[0]
    similarity_search_results = index.query(queries=[query_embedding], top_k=top_k)
    ids = [int(match['id']) for match in similarity_search_results['results'][0]['matches']]
    similarity_search_df =  df[df['id'].isin(ids)]
    similarity_search_df['text'] = similarity_search_df['product'] + ' ' + similarity_search_df['summary'] + ' ' + similarity_search_df['categories'].apply(lambda x: ' '.join(x))
    similarity_search_docs = similarity_search_df.to_dict(orient='records')
    
    print('top-k retrieved:', [doc['id'] for doc in similarity_search_docs])

    rerank_results = co.rerank(query=query, documents=similarity_search_docs, top_n=3, model='rerank-english-v2.0')
    relevant_rerank_results = [rerank_result for rerank_result in rerank_results if rerank_result.relevance_score > 0.3]
    # Take the best result if no relevant results
    if len(relevant_rerank_results) == 0:
        relevant_rerank_results = rerank_results[:1]
    rerank_docs = [get_reranked_item(rerank_result, similarity_search_docs) for rerank_result in relevant_rerank_results]
    rerank_df = pd.DataFrame(rerank_docs)
    
    print('top-n reranked:', [doc['id'] for doc in rerank_docs])

    return rerank_df, search_query_tags

df = pd.read_json('outputs/extracted_data_training_dataset.jsonl', lines=True)

print("=" * 10 + " Data Loaded " + "=" * 10)

pinecone.init(api_key=os.environ.get("PINECONE_API_KEY"), environment='us-west4-gcp-free')

index_name = 'greentechguardians'
index = pinecone.Index(index_name)

print("=" * 10 + " Pinecone Index Loaded " + "=" * 10)

if 'view_state' not in st.session_state:
    st.session_state.view_state = 'search'  # Possible values: 'search', 'report' 

if 'selected_prompt' not in st.session_state:
    st.session_state.selected_prompt = None

if 'conversation' not in st.session_state:
    st.session_state.conversation = None

if 'user_uploaded' not in st.session_state:
    st.session_state.user_uploaded = False

if 'uploaded_file' not in st.session_state:
    st.session_state.uploaded_file = None

if 'new_index' not in st.session_state:
    new_index_name = 'greentechguardiansplus'
    EMBEDDING_DIMENSION = 1536
    if new_index_name not in pinecone.list_indexes():
        pinecone.create_index(new_index_name, dimension=EMBEDDING_DIMENSION)
    st.session_state.new_index = pinecone.Index(new_index_name)

if 'selected_question' not in st.session_state:
    st.session_state.selected_question = None

if 'uploaded_df' not in st.session_state:
    st.session_state.uploaded_df = None

def view_report(item_id):
    # Function to view report and change state
    st.session_state.view_state = 'report'
    st.session_state.selected_item_id = item_id
    st.experimental_rerun()

def chat(item_id):
    st.session_state.view_state = 'chat'
    st.session_state.selected_item_id = item_id
    st.experimental_rerun()

def go_back_to_search():
    # Function to go back to the search view
    st.session_state.view_state = 'search'
    st.session_state.selected_prompt = None
    st.experimental_rerun()

def go_back_to_report(item_id):
    # Function to go back to the report view
    st.session_state.view_state = 'report'
    st.session_state.selected_item_id = item_id
    st.session_state.conversation = None
    st.session_state.selected_question = None
    st.experimental_rerun()

def select_prompt(option):
    st.session_state.selected_prompt = option

def select_question(option):
    st.session_state.selected_question = option

# Main App

custom_style = """
    <style>
    .bubble-tag {
        display: inline-block;
        background-color: #1F77B4;
        border-radius: 15px;
        padding: 5px 10px;
        margin: 2px;
        font-size: 14px;
        color: white;
    }
    button[kind="primary"]  {
        display: inline-block;
        padding: 0.6em 1.2em;
        margin: 0.3em;
        border: 2px solid #1E88E5; /* Blue border */
        border-radius: 10px; /* Rounded borders */
        background-color: white; /* White background */
        color: black; /* Black text */
        font-size: 14px;
        outline: none;
        cursor: pointer;
        transition: background-color 0.3s, box-shadow 0.3s;
    }
    button[kind="primary"]:hover, button[kind="primary"]:focus {
        background-color: #E3F2FD; /* Light blue background on hover/focus */
        box-shadow: 0 2px 4px 0 rgba(0,0,0,0.2);
    }
    </style>
"""

if st.session_state.view_state == 'search':

    st.session_state.uploaded_file = st.file_uploader("Upload my own CSV dataset to search from")
    print(st.session_state.uploaded_file)
    print(st.session_state.user_uploaded)
    if st.session_state.uploaded_file is not None and st.session_state.user_uploaded == False:
        try:
            uploaded_df = pd.read_csv(st.session_state.uploaded_file, encoding="latin-1")
            items = extract_data_from_csv_file(uploaded_df, "user_uploaded_extraction.jsonl")
            print(items)
            st.session_state.uploaded_df = pd.DataFrame(items)
            print(st.session_state.uploaded_df)
            st.session_state.uploaded_df['combined_text'] = st.session_state.uploaded_df.apply(lambda x: f"{x['product']} {x['summary']} {' '.join(x['categories'])}", axis=1)
            embeddings = get_embeddings(st.session_state.uploaded_df['combined_text'].tolist())
            print("=" * 10 + " OpenAI Embeddings Created " + "=" * 10)
            to_upload = [(str(id), embedding) for id, embedding in zip(st.session_state.uploaded_df['id'], embeddings)]
            st.session_state.new_index.upsert(vectors=to_upload)
            
            # st.write(df)
            st.session_state.user_uploaded = True
            # get uploaded ids
            # data extract
        except:
            st.write("Invalid File Format")
    elif st.session_state.uploaded_file is None:
        st.session_state.user_uploaded = False

    # Create two columns. Adjust the ratios as needed.
    col1, col2 = st.columns([1, 3]) 

    # Column 1: Display the image
    with col1:
        st.image("./assets/green_tech_guardians.jpg", width=100)  # Adjust width as needed

    # Column 2: Display the title
    with col2:
        st.title("GreenTechGuardians Business Search Engine")

    # Display the text input
    prompt = "Enter your search query for our general database:"
    if st.session_state.user_uploaded:
        prompt = "Enter your search query for your uploaded dataset:"
    query = st.text_input(prompt)

    # Display prompt option buttons
    st.write("Example searches:")
    prompt_options = ["water bottle recycling", "fossil fuel replacement", "forest protection"]
    cols = st.columns(len(prompt_options))  # Create columns for the buttons
    for i, option in enumerate(prompt_options):
        cols[i].button(option, key=option, on_click=select_prompt, args=(option,))

    # Modify the conditional to check for query or selected prompt
    if query != '' or st.session_state.selected_prompt is not None:
        if query != '':
            st.session_state.selected_prompt = None
        
        if st.session_state.selected_prompt is not None:
            query = st.session_state.selected_prompt
        
        if st.session_state.user_uploaded or st.session_state.uploaded_file is not None:
            print("using new index")
            print(pinecone.describe_index('greentechguardiansplus'))
            print(st.session_state.uploaded_df)
            results_df, tags = search_index(query, st.session_state.new_index, st.session_state.uploaded_df)
            print(results_df)
        else:
            results_df, tags = search_index(query, index, df)
        st.markdown(custom_style, unsafe_allow_html=True)
        tag_string = ''.join([f'<span class="bubble-tag">#{tag}</span>' for tag in tags])
        st.markdown(f"{tag_string}", unsafe_allow_html=True)

        for i, row in results_df.iterrows():
            button_label = f"Product: {row['product']}\nSummary: {row['summary']}\nCategories: {', '.join(row['categories'])}\nRelevance Score: {row['relevance_score']}"

            # Use the index as a unique key for each button
            if st.button(button_label, key=i, type="primary"):
                print("viewing report ...")
                view_report(row['id'])

        x_data = results_df['embedded_value'].tolist()
        y_data = results_df['processing_level'].tolist()
        z_data = results_df['access_level'].tolist()
        # scatter_results_3d(x_data, y_data, z_data, query)

elif st.session_state.view_state == 'report':
    # Clear the previous items and show the report
    st.empty()
    if st.button("Go Back To Search"):
        go_back_to_search()  # Go back to search view
    if st.button("Chat with ChatBot"):
        chat(st.session_state.selected_item_id)
    report(st.session_state.selected_item_id)
    current_item = df[df['id']==st.session_state.selected_item_id].iloc[0]
    results_df, tags = search_index(current_item['summary'], index, df)
    st.markdown(custom_style, unsafe_allow_html=True)
    tag_string = ''.join([f'<span class="bubble-tag">#{tag}</span>' for tag in tags])
    st.markdown(f"{tag_string}", unsafe_allow_html=True)

    for i, row in results_df.iterrows():
        button_label = f"Product: {row['product']}\nSummary: {row['summary']}\nCategories: {', '.join(row['categories'])}\nRelevance Score: {row['relevance_score']}"

        # Use the index as a unique key for each button
        if st.button(button_label, key=i, type="primary"):
            view_report(row['id'])

elif st.session_state.view_state == 'chat':
    # Clear the previous items and show the report
    st.empty()
    if st.button("Go Back To Report"):
        go_back_to_report(st.session_state.selected_item_id)

    current_item = df[df['id'] == st.session_state.selected_item_id].iloc[0]
    st.subheader("Ask ChatBot Advisor")

    # Initialize the Conversation object in session state if not already initialized
    if st.session_state.conversation is None:
        background_info = f"""
        The above are conversation history between a user and a chatbot. Reference the conversation history to answer the user's question.

        Use the following information about a circular economy business below to answer the user's question.

        Product Name: {current_item['product']}
        Product Summary: {current_item['summary']}
        Business Problem: {current_item['problem']}
        Business Solution: {current_item['solution']}
        """
        st.session_state.conversation = Conversation(background_info)

    sample_questions_results = st.session_state.conversation.get_sample_questions()
    sample_questions = sample_questions_results.sample_questions

    # User input for the chatbot
    user_question = st.text_input("Your question to the ChatBot:", key="user_question")

    cols = st.columns(len(sample_questions))  # Create columns for the buttons
    for i, option in enumerate(sample_questions):
        cols[i].button(option, key=option, on_click=select_question, args=(option,))

    # Button to submit the question
    if user_question != '' or st.session_state.selected_question is not None:
        if user_question != '':
            st.session_state.selected_question = None
        
        if st.session_state.selected_question is not None:
            user_question = st.session_state.selected_question
            
        st.session_state.conversation.ask_question(user_question)

    custom_style = """
    <style>
    .chatbox_chatbot {
        background-color: #4CAF50;  /* Green background */
        color: white;
        padding: 10px;
        border-radius: 10px;
        margin: 10px 0;
    }

    .chatbox_user {
        background-color: #2196F3;  /* Blue background */
        color: white;
        padding: 10px;
        border-radius: 10px;
        margin: 10px 0;
    }
    </style>
    """

    st.markdown(custom_style, unsafe_allow_html=True)
    chat_history_string = ''.join([f'<div class="{"chatbox_chatbot" if dialog["role"] == "assistant" else "chatbox_user"}">{dialog["content"]}</div>' for dialog in st.session_state.conversation.chat_history])
    st.markdown(f"{chat_history_string}", unsafe_allow_html=True)
