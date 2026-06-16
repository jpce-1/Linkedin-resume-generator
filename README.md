#  LinkedIn Resume Generator

An AI-powered web app that transforms your LinkedIn profile data into 3 professionally written resume styles instantly — powered by Claude AI.

---

##  Features

-  Generates **3 unique resume styles** from your LinkedIn data:
  - **Professional** — Traditional corporate format with formal language
  - **ATS Optimized** — Keyword-rich format designed to pass applicant tracking systems
  - **Creative** — Bold, skills-first format that stands out
-  **Instant PDF download** for each resume variant
-  **Privacy first** — uses LinkedIn's official data export, no scraping
-  Fast generation powered by Claude Haiku AI

---

##  Tech Stack

- **Backend** — Python, Flask
- **AI** — Anthropic Claude API (claude-haiku-4-5)
- **PDF Generation** — ReportLab
- **Frontend** — HTML, CSS (vanilla)

---

##  Installation

**1. Clone the repo**

```bash
git clone https://github.com/jpce-1/linkedin-resume-generator.git
cd linkedin-resume-generator
```

**2. Create and activate virtual environment**

```bash
python -m venv venv
venv\Scripts\activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Add your API key**

Create a `.env` file in the project root:

```
ANTHROPIC_API_KEY=your_key_here
```

**5. Run the app**

```bash
python app.py
```

Open your browser at `http://127.0.0.1:5000`

---

##  How to Get Your LinkedIn Data

1. Go to LinkedIn → **Settings & Privacy**
2. Left sidebar → **Data Privacy**
3. Click **"Download your data"**
4. Tick Profile, Positions, Education, Skills & Certifications
5. Click **Request archive** and wait for LinkedIn's email
6. Download the ZIP and upload it to the app

---

##  Project Structure

```
linkedin-resume-generator/
├── app.py                 # Flask application & routes
├── parser.py              # LinkedIn ZIP/CSV parser
├── resume_generator.py    # Claude AI resume generation
├── pdf_generator.py       # PDF creation with ReportLab
├── templates/
│   ├── index.html         # Upload page
│   └── results.html       # Resume results & download page
├── static/                # CSS & assets
├── uploads/               # Temporary ZIP storage
├── outputs/               # Generated PDF resumes
├── requirements.txt
└── .env                   # API key (not committed to GitHub)
```

---

##  Future Improvements

- [ ] Job description input to tailor resumes to specific roles
- [ ] ATS score checker for each resume variant
- [ ] Cover letter generator
- [ ] Deploy to live URL

---

##  Author

**JP** — [GitHub](https://github.com/jpce-1) · [LinkedIn](www.linkedin.com/in/johnpaul-ehiemere-22563b397) 

---

## 📄 License

MIT License
