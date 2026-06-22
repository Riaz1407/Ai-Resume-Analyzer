from flask import Flask, render_template, request
from pypdf import PdfReader
import google.generativeai as genai
import os
import json

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):

    os.makedirs(UPLOAD_FOLDER)

genai.configure(

    api_key=os.getenv(

        "my api key"

    )

)

model = genai.GenerativeModel(

    "gemini-2.5-flash"

)


def extract_text(path):

    reader = PdfReader(path)

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:

            text += page_text


    return text




def analyze_resume(

    resume_text,

    job_description

):


    prompt=f"""

You are an ATS Resume Expert.


Analyze the resume against the job description.


Return ONLY VALID JSON.


Format:


{{
"ats_score":85,

"job_match":80,

"summary":"",

"strengths":["",""],

"weaknesses":["",""],

"missing_skills":["",""],

"suggestions":["",""],

"cover_letter":"",

"interview_questions":["","",""],

"roadmap":[

"", "", ""

]

}}




Resume:


{resume_text}




Job Description:


{job_description}


"""



    response=model.generate_content(

        prompt

    )



    result=response.text



    result=result.replace(

        "```json",

        ""

    )



    result=result.replace(

        "```",

        ""

    )



    return json.loads(

        result

    )





@app.route("/")

def home():

    return render_template(

        "index.html"

    )





@app.route(

    "/analyze",

    methods=["POST"]

)

def analyze():

    file=request.files[

        "resume"

    ]


    job_description=request.form[

        "job_description"

    ]



    path=os.path.join(

        app.config["UPLOAD_FOLDER"],

        file.filename

    )



    file.save(

        path

    )



    resume_text=extract_text(

        path

    )



    result=analyze_resume(

        resume_text,

        job_description

    )



    return render_template(

        "index.html",

        result=result

    )





if __name__=="__main__":

    app.run(

        debug=True

    )