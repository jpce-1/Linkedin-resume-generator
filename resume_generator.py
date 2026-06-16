import os
from groq import Groq

client = Groq(api_key=os.getenv('GROQ_API_KEY'))

def format_profile_for_prompt(profile_data):
    profile = profile_data['profile']
    experience = profile_data['experience']
    education = profile_data['education']
    skills = profile_data['skills']
    certifications = profile_data['certifications']

    text = f"""
NAME: {profile.get('first_name')} {profile.get('last_name')}
HEADLINE: {profile.get('headline')}
LOCATION: {profile.get('location')}
EMAIL: {profile.get('email')}
SUMMARY: {profile.get('summary')}

WORK EXPERIENCE:
"""
    for job in experience:
        text += f"""
- {job['title']} at {job['company']} ({job['started_on']} - {job['finished_on']})
  Location: {job['location']}
  Description: {job['description']}
"""

    text += "\nEDUCATION:\n"
    for edu in education:
        text += f"- {edu['degree']} in {edu['field']} at {edu['school']} ({edu['started_on']} - {edu['finished_on']})\n"

    text += "\nSKILLS:\n"
    text += ", ".join(skills)

    text += "\n\nCERTIFICATIONS:\n"
    for cert in certifications:
        text += f"- {cert['name']} by {cert['authority']} ({cert['started_on']})\n"

    return text


def generate_single_resume(profile_text, style):
    styles = {
        'professional': """
You are a professional resume writer. Create a traditional, corporate-style resume.
- Use formal language
- Focus on achievements and responsibilities
- Structure: Summary, Experience, Education, Skills, Certifications
- Use strong action verbs like 'Led', 'Managed', 'Delivered'
""",
        'modern': """
You are an ATS optimization expert. Create a modern, ATS-friendly resume.
- Use clean simple language packed with keywords
- Focus on measurable results and numbers where possible
- Structure: Summary, Skills, Experience, Education, Certifications
- Make sure it passes applicant tracking systems
""",
        'creative': """
You are a creative resume writer. Create a skills-focused, punchy resume.
- Use confident, energetic language
- Lead with skills and strengths
- Structure: Personal Brand Statement, Core Skills, Experience, Education, Certifications
- Make it stand out from traditional resumes
"""
    }

    prompt = f"""
Here is the candidate's LinkedIn profile data:

{profile_text}

{styles[style]}

Write the complete resume now. Use clear sections with headers in ALL CAPS.
Do not add any commentary — just the resume content itself.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=1500
    )
    
    resume_text = response.choices[0].message.content
    resume_text = resume_text.replace('**', '')
    return resume_text
    

   


def generate_resumes(profile_data):
    profile_text = format_profile_for_prompt(profile_data)

    resumes = []
    styles = ['professional', 'modern', 'creative']
    style_names = ['Professional', 'ATS Optimized', 'Creative']

    for style, name in zip(styles, style_names):
        print(f"Generating {name} resume...")
        resume_text = generate_single_resume(profile_text, style)
        resumes.append({
            'style': name,
            'content': resume_text
        })

    return resumes