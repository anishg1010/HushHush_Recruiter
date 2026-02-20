import requests

# StackOverflow API base URL
BASE_URL = "https://api.stackexchange.com/2.3"

# Get top questions
def get_questions(tag="python", limit=10):
    params = {
        "order": "desc",
        "sort": "activity",
        "tagged": tag,
        "site": "stackoverflow",
        "pagesize": limit
    }
    response = requests.get(f"{BASE_URL}/questions", params=params)
    return response.json()

# Get question details
def get_question_details(question_id):
    params = {
        "site": "stackoverflow"
    }
    response = requests.get(f"{BASE_URL}/questions/{question_id}", params=params)
    return response.json()

# Get answers for a question
def get_answers(question_id):
    params = {
        "order": "desc",
        "sort": "activity",
        "site": "stackoverflow"
    }
    response = requests.get(f"{BASE_URL}/questions/{question_id}/answers", params=params)
    return response.json()

# Search questions
def search_questions(query, limit=10):
    params = {
        "intitle": query,
        "site": "stackoverflow",
        "pagesize": limit
    }
    response = requests.get(f"{BASE_URL}/search/advanced", params=params)
    return response.json()

# Example usage
if __name__ == "__main__":
    questions = get_questions("python", 5)
    for q in questions["items"]:
        print(f"Title: {q['title']}")
        print(f"Score: {q['score']}\n")