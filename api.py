import streamlit as st
import os
import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

app = Flask(__name__)
# Load environment variables from a .env file
load_dotenv('pro.env')
CORS(app)
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

def get_gemini_response(question, prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt[0], question])
    print("This is the response from the model: ", response._result.candidates[0].content.parts[0].text)
    return response.text

@app.route('/analyze', methods=['POST'])
def analyze_code():
    data = request.json
    code = data.get('code', '')

    prompt = [
        """Analyze the following code snippet and provide its time and space complexity in Big O notation.  Present your answer in exactly two lines:

Time Complexity: [Time Complexity in Big O notation, e.g., O(n), O(log n), O(n^2)]
Space Complexity: [Space Complexity in Big O notation, e.g., O(1), O(n), O(n^2)]"""
    ]

    question = f"""
    Analyze the time and space complexity of the following code:
    
    {code}
    
    Provide your analysis in the following format:

    Time Complexity: O(...)
    Space Complexity: O(...)
    """

    response_text = get_gemini_response(question=question, prompt=prompt)
    return jsonify({'analysis': response_text})


@app.route('/improve', methods=['POST'])
def improve_code():
    data = request.json
    fileContent = data.get('code', '')

    prompt = [
        """
    You are an expert LeetCode solution writer and code commentator. Please enhance and complete the provided LeetCode solution file. Your task is to:
        1.  Add Intuition: ...
        2.  Add Approach: ...
        3.  Add Complexity Analysis: ...
        4.  Enhance the Code Section: ...
        5.  Use Emojis and make it actractive: ...
        6.  Explanation of Code and Maintain the Structure: ...
"""
    ]
    question = f"""Here is the LeetCode solution file:
    \n\n\n{fileContent}
    """
    
    response_text = get_gemini_response(question=question, prompt=prompt)
    return jsonify({'improved_code': response_text})


if __name__ == '__main__':
    port = 5000
    app.run(host='0.0.0.0', port=port, debug=True)
