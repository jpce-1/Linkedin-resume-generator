import zipfile
import csv
import io

def parse_linkedin_zip(zip_path):
    profile_data = {
        'profile': {},
        'experience': [],
        'education': [],
        'skills': [],
        'certifications': []
    }

    with zipfile.ZipFile(zip_path, 'r') as z:
        file_list = z.namelist()

        # Parse Profile.csv
        if 'Profile.csv' in file_list:
            with z.open('Profile.csv') as f:
                reader = csv.DictReader(io.TextIOWrapper(f, encoding='utf-8'))
                for row in reader:
                    profile_data['profile'] = {
                        'first_name': row.get('First Name', ''),
                        'last_name': row.get('Last Name', ''),
                        'headline': row.get('Headline', ''),
                        'summary': row.get('Summary', ''),
                        'location': row.get('Geo Location', ''),
                        'email': row.get('Email Address', '')
                    }

        # Parse Positions.csv (work experience)
        if 'Positions.csv' in file_list:
            with z.open('Positions.csv') as f:
                reader = csv.DictReader(io.TextIOWrapper(f, encoding='utf-8'))
                for row in reader:
                    profile_data['experience'].append({
                        'title': row.get('Title', ''),
                        'company': row.get('Company Name', ''),
                        'location': row.get('Location', ''),
                        'started_on': row.get('Started On', ''),
                        'finished_on': row.get('Finished On', 'Present'),
                        'description': row.get('Description', '')
                    })

        # Parse Education.csv
        if 'Education.csv' in file_list:
            with z.open('Education.csv') as f:
                reader = csv.DictReader(io.TextIOWrapper(f, encoding='utf-8'))
                for row in reader:
                    profile_data['education'].append({
                        'school': row.get('School Name', ''),
                        'degree': row.get('Degree Name', ''),
                        'field': row.get('Field Of Study', ''),
                        'started_on': row.get('Start Date', ''),
                        'finished_on': row.get('End Date', '')
                    })

        # Parse Skills.csv
        if 'Skills.csv' in file_list:
            with z.open('Skills.csv') as f:
                reader = csv.DictReader(io.TextIOWrapper(f, encoding='utf-8'))
                for row in reader:
                    skill = row.get('Name', '')
                    if skill:
                        profile_data['skills'].append(skill)

        # Parse Certifications.csv
        if 'Certifications.csv' in file_list:
            with z.open('Certifications.csv') as f:
                reader = csv.DictReader(io.TextIOWrapper(f, encoding='utf-8'))
                for row in reader:
                    profile_data['certifications'].append({
                        'name': row.get('Name', ''),
                        'authority': row.get('Authority', ''),
                        'started_on': row.get('Started On', ''),
                        'finished_on': row.get('Finished On', '')
                    })

    return profile_data