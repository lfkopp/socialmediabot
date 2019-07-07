def get_credentials(socialmedia):
    with open('credentials.txt', 'r') as file:
        credentials = eval(str(file.read()))
    return credentials[socialmedia]['user'], credentials[socialmedia]['password'] 
