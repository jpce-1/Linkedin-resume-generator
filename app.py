import os
from flask import Flask, render_template, request, send_file, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'outputs'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    if 'linkedin_zip' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['linkedin_zip']

    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not file.filename.endswith('.zip'):
        return jsonify({'error': 'Please upload a ZIP file'}), 400

    zip_path = os.path.join(app.config['UPLOAD_FOLDER'], 'linkedin_data.zip')
    file.save(zip_path)

    from parser import parse_linkedin_zip
    from resume_generator import generate_resumes
    from pdf_generator import create_pdf

    profile_data = parse_linkedin_zip(zip_path)
    # resumes = generate_resumes(profile_data)
    from resume_generator import generate_resumes_test
    resumes = generate_resumes_test(profile_data)

    pdf_paths = []
    for i, resume in enumerate(resumes, 1):
        pdf_path = os.path.join(app.config['OUTPUT_FOLDER'], f'resume_variant_{i}.pdf')
        create_pdf(resume, pdf_path)
        pdf_paths.append(f'resume_variant_{i}.pdf')

    return render_template('results.html', resumes=resumes, pdf_paths=pdf_paths)

@app.route('/download/<int:variant>')
def download(variant):
    pdf_path = os.path.join(app.config['OUTPUT_FOLDER'], f'resume_variant_{variant}.pdf')
    return send_file(pdf_path, as_attachment=True, download_name=f'resume_variant_{variant}.pdf')

if __name__ == '__main__':
    app.run(debug=True)