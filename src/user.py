class User:
    @staticmethod
    def ask_job_keyword():
        list_jobs = []
        while True:
            jobs = input('Enter the job title you are looking for, type "done" once completed: ')
            if jobs.lower() == 'done':
                break
            list_jobs.append(jobs)
        print(f"Your keyword list is: {', '.join(list_jobs)}")
        return list_jobs
    
    @staticmethod
    def verify_jobs():
        user_response = input('Are you happy with the keywords? (Y/N): ')
        return user_response.upper() == 'Y'
    
    @staticmethod
    def convert_to_right(job_list):
        final_list = []
        for s in job_list:
            words = [word.strip() for word in s.split()]  # Split the job title into individual words and remove whitespaces
            final_list.extend(words)  # Add individual words to the final list
        final_title = '%2C%20'.join(final_list)
        return final_title   
    
    @staticmethod
    def link(final_title):
        link = f"https://in.linkedin.com/jobs/search?keywords={final_title}&location=Canada&locationId=&geoId=101174742&f_TPR=r604800&position=1&pageNum=0"
        return link 

if __name__ == "__main__":
    job_list = User.ask_job_keyword()
    if User.verify_jobs():
        final_title = User.convert_to_right(job_list)
        print(User.link(final_title))
    else:
        print('Please enter the job keywords again.')
