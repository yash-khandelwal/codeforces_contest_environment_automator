from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from gtts import gTTS
import PySimpleGUI as sg
import playsound
import os
import time

contest_link = ""
# GUI
sg.theme('DarkAmber')  # Add a touch of color
# All the stuff inside your window.
layout = [[sg.Text('Please Enter the link of contest')],
          [sg.Text('Link'), sg.InputText()],
          [sg.Button('Ok'), sg.Button('Cancel')]]

# Create the Window
window = sg.Window('Window Title', layout)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel':  # if user closes window or clicks cancel
        exit()
        break
    else:
        contest_link = values[0]
        print('You entered ', values[0])
        break

window.close()


def speak(txt):
    language = 'en'
    voice = gTTS(text=txt, lang=language, slow=False)
    voice.save("voice.mp3")
    # os.system("start speak.mp3")
    playsound.playsound("voice.mp3")


driver_path = "<YOUR CHROME DRIVERS PATH>"

driver = webdriver.Chrome(driver_path)

driver.get(contest_link)
contest = driver.title
contest = contest[12:-13]
print(contest)

problem_list = []
PATH = r'<FOLDER PATH IN WHICH YOU WANT TO SETUP ENVIRONMENT>'

text = ""
try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "problems"))
    )
    print(element.text)
    problems = element.find_elements_by_class_name("id")
    for problem in problems:
        tmp = problem.find_element_by_tag_name("a")
        problem_list.append(tmp.text)
        # print(problem_list[-1])
    print(problem_list)

    text = "this " + contest + " have " + str(len(problem_list)) + " problems to solve"
    contest_path = os.path.join(PATH, contest)
    try:
        os.mkdir(contest_path)
        message = "successfully created contest directory"

    except:
        message = "couldn't create directory"
        speak(message)

    text += " " + message
    for problem in problem_list:
        problem_dir = os.path.join(contest_path, problem)
        os.mkdir(problem_dir)
        message = ""
        text += " "
        f = open(problem_dir + "\\" + problem + "solution.cpp", "w+")
        f.close()
        try:
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.LINK_TEXT, problem))
            )
            message = problem + ", "
            element.click()

            driver.implicitly_wait(5)

            test_input = driver.find_elements_by_class_name("input")

            test_output = driver.find_elements_by_class_name("output")
            input_file_name = "input"
            output_file_name = "output"

            i = 0
            for t_input in test_input:
                f_in = open(problem_dir + "\\" + input_file_name + str(i) + ".txt", "w+")
                w = t_input.find_element_by_tag_name("pre")
                print(t_input.text)
                print("-------------------------------------------------------original below ------------------------------------------------")
                print(w.text)
                content = w.text
                f_in.write(content)
                f_in.close()
                i += 1
            i = 0
            for t_output in test_output:
                f_out = open(problem_dir + "\\" + output_file_name + str(i) + ".txt",  "w+")
                w = t_output.find_element_by_tag_name("pre")
                print(t_output.text)
                print("-------------------------------------------------------original below ------------------------------------------------")
                print(w.text)
                content = w.text
                f_out.write(content)
                f_out.close()
                i += 1
            driver.back()
        except:
            message = " not " + str(problem)


        finally:
            text += " "
            text = text + str(message)
except:
    message = "error occured"
finally:
    driver.quit()
    speak(text)
