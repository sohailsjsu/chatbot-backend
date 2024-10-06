from flask import Flask, request, jsonify
import openai
import json

# Initialize Flask app
app = Flask(__name__)

# Set your OpenAI API key
openai.api_key = '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'

# JSON data of the resume (from previous step)
resume_data = {
    "name": "Sohail Shaik",
    "contact": {
        "location": "Bayarea, CA, 95126",
        "phone": "+14086395368",
        "email": "sohail.shaik@gmail.com",
        "linkedin": "https://www.linkedin.com/in/sohailshaik23/",
        "github": "http://github.com/sohail-coder"
    },
    "education": {
        "institution": "San Jose State University",
        "degree": "Master of Science, Computer Science",
        "graduation_date": "May 2025",
        "coursework": [
            "Machine Learning",
            "Database Systems Principles",
            "Distributed Computing",
            "Design Analysis of Algorithms"
        ]
    },
    "work_experience": [
        {
            "company": "Zemoso Labs",
            "location": "Hyderabad, India",
            "role": "Associate Software Engineer",
            "duration": "Jun 2022 - Jul 2023",
            "responsibilities": [
                "Developed high-performance and maintainable code by refactoring a monolithic application into microservices using Java Spring Boot, enhancing scalability and reducing deployment time.",
                "Implemented CI/CD pipelines using Jenkins and integrated with AWS EC2, reducing deployment time by 45%.",
                "Implemented comprehensive unit and integration tests using JUnit and React Testing Library, achieving high test coverage and ensuring code reliability.",
                "Built microservices using Java Spring Boot, developed deep learning models in Python, and created interactive dashboards with React and Chart.js.",
                "Solved complex problems by integrating GraphQL to improve data retrieval performance, reducing over-fetching issues and optimizing system efficiency.",
                "Collaborated in Agile teams, actively participating in daily standups, providing feedback, and contributing to feature implementation."
            ]
        }
    ],
    "projects": [
        {
            "title": "Large Language Model (LLM) Integrated PDF Viewer App",
            "description": [
                "Implemented seamless Google sign-in for secure Google Drive access, designed the app to remember the last read page of each PDF, synchronizing this information across devices to ensure users can resume reading from where they left off.",
                "Incorporated a LLM to provide sentence meanings within the PDF, alongside an inbuilt dictionary for word definitions, developed a feature enabling users to add audio comments to specific sections of the PDF."
            ]
        }
    ],
    "skills": {
        "languages": ["Java", "Python", "C/C++", "SQL", "JavaScript", "HTML/CSS", "Typescript", "GraphQL", "Groovy", "Kotlin"],
        "frameworks": ["React.js", "Node.js", "Spring Boot", "JUnit", "Material-UI", "REST API", "Agile", "Kanban", "Jira", "SwiftUI"],
        "cloud_databases": ["AWS", "GCP", "Azure", "Digital Ocean", "MySQL", "PostgreSQL", "MongoDB", "HBase"],
        "devops": ["Docker", "Linux", "CI/CD", "Jenkins", "Kubernetes", "Git", "Terraform", "Prometheus", "NGINX"],
        "concepts": [
            "Object-Oriented Design", "Clean Code", "Data Structures", "Building Scalable Infrastructure"
        ]
    }
}

# Convert JSON resume to a string for the prompt
resume_text = json.dumps(resume_data, indent=4)

@app.route('/')
def home():
    return "Welcome to the Resume Chatbot! Use /chatbot to ask questions."

# API endpoint to handle chat requests
@app.route('/chatbot', methods=['POST'])
def chatbot():
    try:
        # Get user input (question) from frontend
        data = request.get_json()
        question = data.get('question', '')
        
        # Build the prompt with the resume data and user question
        messages = [
            {"role": "system", "content": "You are a helpful assistant that answers questions based on the following resume data."},
            {"role": "system", "content": resume_text},
            {"role": "user", "content": question}
        ]
        
        # Query the OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7,
            max_tokens=150,
            n=1,
            stop=None
        )
        
        # Extract the answer from the API response
        answer = response.choices[0].message['content'].strip()
        return jsonify({'answer': answer})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
