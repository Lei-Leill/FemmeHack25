from flask import Flask, request, jsonify
import re

app = Flask(__name__)

# Simple function to calculate match score based on keyword overlap
def calculate_match(resume, job_desc):
    resume_words = set(re.findall(r'\w+', resume.lower()))
    job_desc_words = set(re.findall(r'\w+', job_desc.lower()))
    
    common_words = resume_words.intersection(job_desc_words)
    match_score = len(common_words) / len(job_desc_words) * 100  # A simple match percentage
    return match_score

@app.route('/submit', methods=['POST'])
def submit_data():
    data = request.get_json()  # Get JSON data from front-end
    resume = data['resume']
    job_desc = data['job_desc']
    
    score = calculate_match(resume, job_desc)
    
    return jsonify({'match_score': score})

if __name__ == '__main__':
    app.run(debug=True)
