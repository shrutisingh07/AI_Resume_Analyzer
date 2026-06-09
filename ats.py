from skills import skills_list

def extract_skills(text):

    text = text.lower()

    found_skills = []

    for skill in skills_list:
        if skill in text:
            found_skills.append(skill)

    return found_skills


def calculate_ats(resume_skills, job_skills):

    matched = len(
        set(resume_skills).intersection(
            set(job_skills)
        )
    )

    if len(job_skills) == 0:
        return 0

    score = (matched / len(job_skills)) * 100

    return round(score, 2)