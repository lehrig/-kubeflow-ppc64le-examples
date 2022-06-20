#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import streamlit as st
import requests

st.set_page_config(layout="wide")

left_column, right_column = st.columns(2)


def answer():
    # store question and answer to be displayed later (under text input)
    st.session_state.question = st.session_state.user_input
    st.session_state.answer = requests.post(
            "http://localhost:5000/", 
            json={
                "question": st.session_state.question,
                "backend": backend
            }).json()

    # reset question field
    st.session_state.user_input = ""


with st.sidebar:
    # st.image("https://upload.wikimedia.org/wikipedia/en/2/21/Kubeflow-logo.png", width=200)
    # TODO check if they work? Ping or dummy request?
    backend = st.selectbox("Backend server to use:",
            ["TorchServe", "TFServing", "Triton Inference Server"])



with left_column:
    st.title("Kubeflow on Power")
    st.header("Question Answering")

    # create user text input for question
    st.text_input("", key="user_input", on_change=answer)
    st.button("Submit", on_click=answer)

    # display results (only when answer exists, so after the first run)
    if "answer" in st.session_state:
        st.write(st.session_state.question)
        st.write(st.session_state.answer["answer"])

if st.checkbox("Show logs"):
    st.json(st.session_state.answer)


# Examples column
with right_column:
    examples = [
        "Where did Neil Armstrong study?",
        "When was Nelson Mandela born?",
    ]

    def set_question(example_id):
        st.session_state.user_input = examples[example_id]


    for example_id, example in enumerate(examples):
        st.button(example, on_click=set_question, args=(example_id,))


