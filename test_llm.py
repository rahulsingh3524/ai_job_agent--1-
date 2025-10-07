from utils.llm_client import query_ollama, parse_llm_response

# Test cases with different variations
test_cases = [
    {
        'name': 'Direct cold email request',
        'message': 'Send cold emails to recruiters for full-stack developer roles. I am Rahul, a B.Tech CSE graduate with 1 year of experience in React.js, Node.js, Express.js, and MongoDB.'
    },
    {
        'name': 'Contact recruiters variation',
        'message': 'Contact recruiters about my MERN stack experience. I have 1 year of experience as a full-stack developer.'
    },
    {
        'name': 'Email recruiters variation',
        'message': 'Email recruiters for React developer positions. I am a B.Tech graduate with Node.js and MongoDB experience.'
    },
    {
        'name': 'Find jobs request (should use crawl_jobs)',
        'message': 'Find React developer jobs in India'
    },
    {
        'name': 'Get recruiter emails (should use find_recruiter_emails)',
        'message': 'Get recruiter emails for Google and Microsoft'
    }
]

print("Testing multiple scenarios...\n")

for test in test_cases:
    print(f"\n=== Testing: {test['name']} ===")
    print(f"Input: {test['message']}")
    response = query_ollama([{'role': 'user', 'content': test['message']}])
    parsed = parse_llm_response(response)
    print(f"Response: {parsed}\n")
    print("-" * 80) 