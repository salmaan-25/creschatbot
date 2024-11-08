# from sklearn.feature_extraction.text import CountVectorizer
# import numpy as np
# import sys
# import json
# import re

# # Define input-output pairs
# responses = {
#     "hi": "Hello!",
#     "cse syllabus": "You can find the CSE syllabus here: <a href='https://crescent.education/university/schools/school-of-computer-information-and-mathematical-sciences/department-of-computer-science-and-engineering/programmes-approved-2/' target='_blank'>CSE Syllabus Link</a>",
#     "Lost and found": "You can find the Lost and found in crescent college here: <a href='https://crescentlostandfound.netlify.app' target='_blank'>LOST AND FOUND LINK</a>",
#     " student affairs Dean Details" : "You can find the Studentaffairs Dean Details here: <a href='https://crescent.education/student-affairs/about-student-affairs/' target='_blank'>Student Affairs Dean</a>",
#     "who are you":"am a chat bot",
#     "admission process": "You can find the details about the admission process here: <a href='https://crescent.education/admissions/' target='_blank'>Admission Process</a>",
#     "library hours": "<a href='https://library.crescent.education/' target='_blank'>Library details</a>",
#     "Feedback": " You can find more details here: <a href='https://crescent.education/feedback/' target='_blank'>Feedback</a>",
#     "sports facilities": "Crescent College offers various sports facilities including football, basketball, badminton, and more. For a complete list, visit: <a href='https://crescent.education/estate/facilities/sports/' target='_blank'>Sports Facilities</a>",
#     "hostel details": "You can learn more about hostel accommodations and fees here: <a href='https://crescent.education/estate/facilities/hostel-facilities/' target='_blank'>Hostel Information</a>",
#     "exam schedule": "The exam schedule is updated regularly. You can check the latest schedule here: <a href='https://crescent.education/schedule-of-exams1/' target='_blank'>Exam Schedule</a>",
#     "bye": "Goodbye!"
# }

# # Predefined inputs for vectorization
# input_questions = list(responses.keys())

# # Create the CountVectorizer instance and fit it on the input questions
# count_vectorizer = CountVectorizer()
# count_vectorizer.fit(input_questions)

# def get_response(user_input):
#     user_vector = count_vectorizer.transform([user_input])
#     similarities = np.dot(user_vector.toarray(), count_vectorizer.transform(input_questions).T.toarray())
#     best_match_index = np.argmax(similarities)
    
#     if similarities[0][best_match_index] > 0:
#         response = responses[input_questions[best_match_index]]
#         # Check if the response contains a URL and format it as an HTML anchor tag
#         return response
#     else:
#         return "I'm sorry, I don't understand that."

# if __name__ == "__main__":
#     # Read input from command line
#     user_input = sys.argv[1]
#     response = get_response(user_input)
#     print(json.dumps({"response": response}))

import sys
import requests
from bs4 import BeautifulSoup
import json
import re

def scrape_url(user_input):
    # Target URL of the Crescent website
    target_url = "https://hindustanuniv.ac.in/"
    
    try:
        # Send a GET request to the website
        response = requests.get(target_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all anchor tags <a> on the page
        links = soup.find_all('a', href=True)

        # Filter links that contain the user_input (case-insensitive)
        matching_links = []
        for link in links:
            if re.search(user_input, link.get_text(), re.IGNORECASE):
                matching_links.append(link['href'])
        
        # If we find matching links, return them
        if matching_links:
            return {"response": matching_links}
        else:
            return {"response": "No matching links found for your query."}
    
    except Exception as e:
        return {"response": f"Error occurred while scraping: {str(e)}"}

if __name__ == "__main__":
    # Read user input from the command line
    user_input = sys.argv[1]  # The keyword entered by the user
    response = scrape_url(user_input)  # Get the scraped URLs based on the user input
    print(json.dumps(response))  # Print the response as a JSON object

