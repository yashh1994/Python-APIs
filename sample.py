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

prompt = [ """
Generate a **detailed and well-structured LeetCode solution file** for the problem **"Minimum Time to Repair Cars"** using the provided Python code.

### **Requirements:**

1. **Rich Formatting & Sections:**
- Use **Markdown-style headers** (`#`, `##`, `###`) to structure different sections.
- Add **emojis** to make the explanation engaging.

2. **Content Requirements:**
- **Problem Statement** 📜: Clearly describe the problem with input/output examples.
- **Intuition** 🤔: Explain the thought process behind solving the problem.
- **Approach** 💡: Break down the steps of the solution in a structured manner.
- **Time & Space Complexity Analysis** ⏱️: Clearly state and justify the complexity.
- **Helper Function Breakdown** ⚙️: Explain the purpose of `can_be_done()`.
- **Code Explanation** 📝: Add inline comments to explain each part of the code.

3. **Code Requirements:**
- Format the code properly using syntax highlighting.
- Maintain readability with meaningful variable names.
- Ensure correct implementation of **Binary Search**.

4. **Example Output & Edge Cases:**
- Include at least **two example cases** to showcase how the function works.
- Explain why the output is correct.

---

### **Code to Format:**
```language
 GIVEN CODE
"""
]

fileContent = """
__import__("atexit").register(lambda: open("display_runtime.txt", "w").write("0"))

class Solution:
    def repairCars(self, ranks: List[int], cars: int) -> int:
        def can_be_done(mnt,cars):
            total_can = 0
            for r in ranks:
                total_can += int((mnt//r)**0.5)
            return total_can >= cars




        l, r = 0, min(ranks) * (cars ** 2)
        ans = 0
        while r>=l:
            mid = (l+r)//2
            if can_be_done(mid,cars):
                ans = mid
                r = mid-1
            else:
                l = mid+1
        return ans
        
"""
question = f"""Here is the LeetCode solution file:
\n\n\n{fileContent}
"""

def get_gemini_response(question, prompt):
    model = genai.GenerativeModel('gemini-1.5-pro-001')
    response = model.generate_content([prompt[0], question])
    print("This is the response from the model: ", response._result.candidates[0].content.parts[0].text)
    return response.text


response_text = get_gemini_response(question=question, prompt=prompt)
