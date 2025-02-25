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

@app.route('/', methods=['GET'])
def default():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>LeetCode Extension API</title>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');
            
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Poppins', sans-serif;
                background: linear-gradient(135deg, #1e3c72, #2a5298);
                height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                text-align: center;
            }
            
            .container {
                background: rgba(255, 255, 255, 0.15);
                padding: 40px;
                border-radius: 12px;
                backdrop-filter: blur(10px);
                box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
                max-width: 500px;
                color: white;
            }
            
            h1 {
                font-size: 28px;
                font-weight: 600;
                margin-bottom: 15px;
            }
            
            p {
                font-size: 16px;
                color: #dcdcdc;
            }
            
            .button {
                display: inline-block;
                margin-top: 20px;
                padding: 12px 24px;
                font-size: 16px;
                color: white;
                background: #ff7b00;
                border: none;
                border-radius: 8px;
                text-decoration: none;
                font-weight: bold;
                transition: 0.3s ease;
            }
            
            .button:hover {
                background: #ff5500;
                transform: scale(1.05);
            }

            .emoji {
                font-size: 28px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="emoji">🚀</div>
            <h1>Welcome to LeetCode Extension API!</h1>
            <p>Analyze time complexity and improve your code instantly! 🧠💡</p>
            <a href="https://github.com/yashh1994/Time-Complexity-Extension" class="button">Get the Extension</a>
        </div>
    </body>
    </html>
    '''


if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000)) 
    app.run(host='0.0.0.0', port=port, debug=True)

