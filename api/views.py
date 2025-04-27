from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from google import genai
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pandas as pd
import json
from .agents import FinancialAlphaCrew

# Fuction to generate bot response
def generator(history):
    client = genai.Client(api_key="AIzaSyC09vgOIf0feqQ2omtUaraUbzYZu9vUtHI")
    response = client.models.generate_content(
        model="gemini-1.5-pro", 
        contents=f"You are Jarvis, an assistant. Answer based on below history. \n\n Session History:\n {history}",
    )
    return response.text

# Verify if the given input is valid financial idea, if not suggest an idea
def idea_verfication_tool(idea):
    client = genai.Client(api_key="AIzaSyC09vgOIf0feqQ2omtUaraUbzYZu9vUtHI")
    response = client.models.generate_content(
        model="gemini-1.5-pro", 
        contents=f"If following query looks like a financial idea for alpha making, Respond -> 1. If not responed -> 0.  \n\n Query:\n {idea}",
    )
    return response.text

# Create alpha using idea, datafields and operators
def get_alpha(idea, rd, ro):
    client = genai.Client(api_key="AIzaSyC09vgOIf0feqQ2omtUaraUbzYZu9vUtHI")
    response = client.models.generate_content(
        model="gemini-1.5-pro", 
        contents=f"Create an alpha using given idea. You can use below datafields and operators if necessary to create alpha for worldquant brain. Dont give python code just give worldquant brain style alpha.\n\n Idea:\n {idea} \n\n Datafields:\n {rd} \n\n operators:\n {ro}",
    )
    return response.text

# using idea get relevant operators and datafields to generate alpha
def get_operators_and_datafields(idea):
    model = SentenceTransformer('all-MiniLM-L6-v2')  # lightweight and fast
    query = model.encode([idea], convert_to_numpy=True)

    index_datafields = faiss.read_index("static/knowledge/vd_matrix.idx")
    index_operators = faiss.read_index("static/knowledge/vd_operators.idx")

    # d1 and d2 are distance lists and location is location in corresponding csv files in static/knowledge
    d1, location_datafields = index_datafields.search(query, 7)
    d2, location_operators = index_operators.search(query, 4)

    datafields = pd.read_csv('static/knowledge/datafields_matrix.csv')
    operators = pd.read_csv('static/knowledge/operators.csv')
    
    required_datafields = datafields.loc[location_datafields[0]][['id','description']].to_string(index=False)
    required_operators = operators.loc[location_operators[0]][['name','definition','description']].to_string(index=False)
    
    return required_datafields, required_operators
    
def memory_list_to_string(memory):
    history = ""
    for di in memory:
        if di['role'] == 'user':
            history = f"{history} \nuser: {di['content']}"
        else:
            history = f"{history} \nassistant: {di['content']}"
    return history

@csrf_exempt
def chat_response(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_message = data.get("message", "")
            memory = data.get("memory","")
            history = memory_list_to_string(memory)
            print("history:", history)
            #response_message = generator(history)
            # print("user:", user_message)
            # print("bot:", response_message)
            #-----------------------------------------------------------
            rd, ro = get_operators_and_datafields(user_message)
            # response_message = get_alpha(user_message, rd, ro)
            financial_alpha_crew = FinancialAlphaCrew()
            response_message = str(financial_alpha_crew.handle_query(user_message))
            #-----------------------------------------------------------
            return JsonResponse({"response": response_message})
        except Exception as e:
            return JsonResponse({"response": e})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    if request.method == "GET":
        return JsonResponse({"success": "OK"}, status=200)
    
    return JsonResponse({"error": "Invalid request method"}, status=405)
