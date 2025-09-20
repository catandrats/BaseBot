import os.path
import os
import subprocess
import sys
from robot.api.deco import library, keyword
@library
class BaseBotATPLibrary(object):
    
    def __init__(self):
        self._status = ''
    @keyword
    def open_basebot(self):
        subprocess.Popen('BaseBot.exe')
    @keyword
    def wait_for(self, seconds):
        command = 'TIMEOUT /T ' + str(seconds)
        os.system(command)
    @keyword
    def echo_this(self, comment):
        os.system('echo '+str(comment))
    @keyword
    def check_for_process(self, process):
        output = subprocess.check_output(['tasklist'])
        string_of_interest = output.decode('utf-8')
        self.process_found = 0
        if process in string_of_interest:
            self.process_found = 1
    @keyword
    def fetch_process_status(self):
        return str(self.process_found)
    @keyword
    def kill_process(self, process):
        os.system('taskkill /IM '+process+' /F')
    @keyword
    def delete_question(self, question):
        datapath = os.getenv('APPDATA')
        BaseBot_question_folder = datapath + '\\BaseBot\\' + question
        files = os.listdir(BaseBot_question_folder)
        for file in files:
            file2remove = BaseBot_question_folder + '\\'+ str(file)
            os.remove(file2remove)
        os.rmdir(BaseBot_question_folder)
            