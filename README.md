# AI_Travel_Assistant
A conversational travel planning assistant powered by LLaMA 3, 
built with Streamlit and Ollama.

## Overview
This app generates personalised multi-day travel itineraries 
through a step-by-step chat interface. Users provide their 
destination, interests, budget, and exclusions — and the assistant 
produces a custom travel plan using a locally hosted LLaMA 3 model.

## Features
- Conversational multi-step chat interface
- Personalised itinerary generation using LLaMA 3
- Supports budget and exclusion preferences
- Built with Streamlit for interactive UI

## Tech Stack
- Python
- Streamlit
- LLaMA 3 (via Ollama)
- REST API

## How to Run
1. Install Ollama and pull LLaMA 3:
   ollama pull llama3
2. Install dependencies:
   pip install streamlit requests
3. Run the app:
   streamlit run travel_assistant.py

## Author
Gouthami Chelluri
