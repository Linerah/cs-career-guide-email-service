import base64
import io

from flask_cors import CORS, cross_origin
from flask_mail import Mail, Message
from flask import Flask, request

app = Flask(__name__)
CORS(app)
app.config['MAIL_SERVER'] = 'smtp.office365.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'cscareerguide@outlook.com'
app.config['MAIL_PASSWORD'] = 'CS12345@'

mail = Mail(app)


@app.route("/research", methods=['POST', 'GET'])
@cross_origin()
def research():
    if request.method == "POST":
        research_title = request.json['research_title']
        professor_email = request.json['professor_email']
        professor_name = request.json['professor_name']
        student_email = request.json['student_email']
        student_name = request.json['student_name']
        resume = request.json.get('resume')
        pdf_file = io.BytesIO(base64.b64decode(resume))

        # Email sent to professor
        msg_professor = Message('Research Submission - Student Interest',
                                sender='cscareerguide@outlook.com', recipients=[professor_email])
        msg_professor.body = f'Hi {professor_name}, \n' \
                             f'\n' \
                             f'Hope you are doing well,\n' \
                             f'{student_name} has shown interest in joining your {research_title} ' \
                             f'research. Attached is their ' \
                             f'resume! \n' \
                             f'\n' \
                             f'Have a great day! \n' \
                             f'CS Career Guide Team'
        msg_professor.attach(filename='resume.pdf', content_type='application/pdf', data=pdf_file.getvalue())
        mail.send(msg_professor)

        # Email sent to student
        msg_student = Message('Research Submission - Confirmation Email',
                              sender='cscareerguide@outlook.com', recipients=[student_email])
        msg_student.body = f'Hi {student_name}, \n' \
                           f'\n' \
                           f'Hope you are doing well,\n' \
                           f'This is a confirmation for your interest in {research_title} ' \
                           f'research. Attached is the resume ' \
                           f'you sent! \n' \
                           f'\n' \
                           f'Have a great day! \n' \
                           f'CS Career Guide Team'
        msg_student.attach(filename='resume.pdf', content_type='application/pdf', data=pdf_file.getvalue())
        mail.send(msg_student)
        return "Both emails sent!"
    return 'The endpoint exists!'