class Email:
    def __init__(self,email,password,to_list,cc_list,operation):
        self.email = email
        self.password = password
        self.to_list = to_list
        self.cc_list = cc_list
        self.operation = operation