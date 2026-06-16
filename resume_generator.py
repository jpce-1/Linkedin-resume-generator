import os
import anthropic

client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

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

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1500,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.content[0].text


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

def generate_resumes_test(profile_data):
    profile = profile_data['profile']
    name = f"{profile.get('first_name')} {profile.get('last_name')}"

    dummy_resumes = [
        {
            'style': 'Professional',
            'content': f"""
{name}
{profile.get('headline')}
{profile.get('email')} | {profile.get('location')}

SUMMARY
{profile.get('summary')}

EXPERIENCE
Test Company | Software Developer
January 2023 - Present
Developed and maintained web applications using Python and Flask.

EDUCATION
Test University | Computer Science
2019 - 2023

SKILLS
Python, Flask, SQL, HTML, CSS

CERTIFICATIONS
Test Certification | Test Authority
"""
        },
        {
            'style': 'ATS Optimized',
            'content': f"""
{name}
{profile.get('email')} | {profile.get('location')}

PROFESSIONAL SUMMARY
Results-driven professional with expertise in Python development and automation.

CORE SKILLS
Python | Flask | SQL | REST APIs | HTML | CSS | Git

EXPERIENCE
Test Company | Software Developer
January 2023 - Present
Delivered 10+ automation tools reducing manual work by 40%.

EDUCATION
Test University | Computer Science | 2019 - 2023

CERTIFICATIONS
Test Certification | Test Authority
"""
        },
        {
            'style': 'Creative',
            'content': f"""
{name}
{profile.get('headline')}
{profile.get('email')} | {profile.get('location')}

PERSONAL BRAND
Passionate developer who builds tools that make people's lives easier.

CORE SKILLS
Python | Flask | AI Integration | Web Development | Automation

EXPERIENCE
Test Company | Software Developer
January 2023 - Present
Built AI-powered tools used by 100+ users daily.

EDUCATION
Test University | Computer Science | 2019 - 2023

CERTIFICATIONS
Test Certification | Test Authority
"""
        }
    ]

    return dummy_resumes