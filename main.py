from modules.job_search import search_jobs, is_legitimate_job_site, extract_job_details, is_location_match
from modules.cv_parser import parse_cv
from modules.ai import ai_vet_job, calculate_cv_job_similarity, calculate_similarity
from modules.utils import setup_logging, log_ssl_error
import logging

def main():
    setup_logging()
    use_cv = input("Do you want to use a CV to refine your search? (yes/no): ").lower().strip() == 'yes'
    cv_data = None
    cv_text = ""

    if use_cv:
        cv_path = input("Enter the path to your CV (PDF or DOCX): ")
        try:
            cv_data, cv_text = parse_cv(cv_path)
            print("Extracted skills:", ", ".join(cv_data['skills']))
            print("Education:")
            for edu in cv_data['education']:
                print(f"- {edu}")
            print("Experience highlights:")
            for exp in cv_data['experience'][:3]:
                print(f"- {exp}")
        except Exception as e:
            print(f"Error parsing CV: {e}")
            use_cv = False

    job_title = input("Enter the job title you're looking for: ")
    location = input("Enter your preferred location (e.g., Nairobi, Kenya): ")

    if use_cv:
        query = f"{job_title} {' '.join(cv_data['keywords'][:5])}"
    else:
        query = job_title

    results = search_jobs(query, location)

    priority_results = []
    other_results = []

    for result in results:
        try:
            if is_legitimate_job_site(result['link']):
                salary, job_location = extract_job_details(result['snippet'])

                if is_location_match(job_location, location):
                    relevance_score = ai_vet_job(result['snippet'], query, cv_text)
                    if use_cv:
                        similarity_score = calculate_cv_job_similarity(cv_data, result['snippet'])
                    else:
                        similarity_score = calculate_similarity(query, result['snippet'])

                    job_data = {
                        'title': result['title'],
                        'link': result['link'],
                        'snippet': result['snippet'],
                        'salary': salary,
                        'location': job_location,
                        'relevance_score': relevance_score,
                        'similarity_score': similarity_score
                    }

                    if any(priority_domain in result['link'] for priority_domain in PRIORITY_DOMAINS):
                        priority_results.append(job_data)
                    else:
                        other_results.append(job_data)
        except requests.exceptions.SSLError as e:
            log_ssl_error(result['link'], str(e))
            print(f"Skipping {result['link']} due to SSL certificate issues.")
        except Exception as e:
            print(f"Error processing {result['link']}: {e}")

    priority_results.sort(key=lambda x: (x['relevance_score'], x['similarity_score']), reverse=True)
    other_results.sort(key=lambda x: (x['relevance_score'], x['similarity_score']), reverse=True)

    legitimate_results = priority_results + other_results

    print(f"\nFound {len(legitimate_results)} legitimate job listings in {location}, prioritized and sorted by relevance:\n")
    for i, job in enumerate(legitimate_results, 1):
        print(f"{i}. {job['title']}")
        print(f"   URL: {job['link']}")
        print(f"   Salary: {job['salary']}")
        print(f"   Location: {job['location']}")
        print(f"   Description: {job['snippet'][:100]}...")
        print(f"   Relevance Score: {job['relevance_score']:.2f}")
        print(f"   Similarity Score: {job['similarity_score']:.2f}")
        if use_cv:
            matching_skills = set(cv_data['skills']).intersection(set(re.findall(r'\b\w+\b', job['snippet'].lower())))
            print(f"   Matching Skills: {', '.join(matching_skills)}")
        print()


if __name__ == "__main__":
    main()
