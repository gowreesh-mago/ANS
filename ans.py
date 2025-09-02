import json
import pprint
import requests
from glob import glob
from datetime import datetime


class ANS:
    def __init__(self, config_path):
        with open(config_path, 'r') as file:
            self.config = json.load(file)
        self.api_key = self.config.get('api_key', None)
        self.assignment_id = self.config.get('assignment_id', None)
        self.course_id = self.config.get('course_id', None)
        self.student_ids = []
        self.submission_ids = []
        self.canvas_student_ids = []
        self.canvas2ans = {}
    def get_canvas_student_ids(self, extracted_path):
        folders = glob(f"{extracted_path}/*")
        for folder in folders:
            student_id = folder.split('_')[-2]
            self.canvas_student_ids.append(student_id)
        print(f"Extracted Canvas student IDs: {self.canvas_student_ids}")

    def get_student_ids(self):
        if not self.api_key or not self.course_id:
            raise ValueError("API key or course ID is not set.")
        print(f"Fetching users for course {self.assignment_id}")
        url = f"https://ans.app/api/v2/courses/{self.course_id}"
        response = requests.get(url, headers={"Authorization": f"Token {self.api_key}"})
        results = response.json()
        learners = results.get('learners', [])
        for learner in learners:
            ans_id = learner.get('user_id')
            canvas_id = learner.get('student_number')
            self.student_ids.append(ans_id)
            if ans_id and canvas_id:
                self.canvas2ans[canvas_id] = ans_id

    def post_comment_on_submissions(self, submission_id, comment):
        if not self.api_key:
            raise ValueError("API key is not set.")
        print(f"Posting comment to submission {submission_id}: {comment}")
        url = f"https://ans.app/api/v2/comments/"
        try:
            requests.post(url, json={
            "commentable_id": submission_id,
            "commentable_type": "Submission",
            "content": comment
            }, headers={"Authorization": f"Token {self.api_key}"})
        except Exception as e:
            print(f"Failed to post comment: {e}")
        
    def get_submissions(self):
        if not self.api_key or not self.assignment_id:
            raise ValueError("API key or assignment ID is not set.")
        print(f"Fetching submissions for assignment {self.assignment_id}")
        url = f"https://ans.app/api/v2/assignments/{self.assignment_id}/results"
        response = requests.get(url, headers={"Authorization": f"Token {self.api_key}"})
        results = response.json()
        pprint.pprint(results)
        for result in results:
            student_id = result.get('user_id')
            submission_id = result.get('id')
            if student_id:
                self.student_ids.append(student_id)
            if submission_id:
                self.submission_ids.append(submission_id)
    def post_comments(self):
        if not self.submission_ids:
            print("No submissions found to comment on")
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_filename = f"./comment_log_{timestamp}.txt"
        
        with open(log_filename, 'w') as log_file:
            for submission_id in self.submission_ids:
                try:
                    comment = f"Automated feedback for submission {submission_id}"
                    self.post_comment_on_submissions(submission_id, comment)
                    log_entry = f"[{datetime.now()}] Successfully posted comment for submission {submission_id}\n"
                    log_file.write(log_entry)
                    print(log_entry.strip())
                    
                except Exception as e:
                    error_entry = f"[{datetime.now()}] Error posting comment for submission {submission_id}: {str(e)}\n"
                    log_file.write(error_entry)
                    print(error_entry.strip())
if __name__ == "__main__":
    ans = ANS('/Users/gowreeshmago/Desktop/CODE/autograde_ans/config.json')
    ans.get_ans_student_ids()