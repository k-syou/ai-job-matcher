from app.settings import BASE_PROMPT

def build_prompt(job_posting: dict, user_info: dict) -> str:
    return BASE_PROMPT.format(
        job_posting=job_posting,
        skills=user_info['skills'],
        experience_years=user_info['experience_years'],
        entry_label="예" if user_info['is_entry_level'] else "아니오",
        salary=user_info['salary'],
        location=user_info['location'],
        benefits=user_info['benefits'],
        target_position=user_info['target_position'],
        certifications=user_info['certifications'],
        languages=user_info['languages']
    )