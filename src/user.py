class User:
    def __init__(self):
        pass
        
    def ask_job_keyword(self):
        list_jobs = []
        while True:
            jobs = input('Enter the job tittle you are looking for, type "done" once completed.')
            if jobs.lower() == 'done':
                break
            list_jobs.append(jobs)
        print(f"Your keyword list is: {', '.join(list_jobs)}")
        return list_jobs
    
    def verify_jobs():
        user_response = input('are you happy with the keywords? (Y/N)')
        if user_response.upper() == 'Y':
            return True
        return False  
    
    def convert_to_right(job_list):
        final_list = []
        for s in job_list:
            words = [word.strip() for word in s.split()]  # Split the job title into individual words and remove whitespaces
            final_list.extend(words)  # Add individual words to the final list
        final_title = '%2C%20'.join(final_list)
        return final_title   
    
    def link(final_title):
        link = f"https://www.linkedin.com/jobs/search/?currentJobId=3805534201&geoId=101174742&keywords={final_title}&location=Canada"
        return link  