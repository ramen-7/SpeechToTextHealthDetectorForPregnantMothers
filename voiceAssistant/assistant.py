import speech_recognition as sr

import pyttsx3 as pt

listener = sr.Recognizer()
speak = pt.init()
key_val = {'SystolicBP': 0,
           'DiastolicBP': 0,
           'Age': 0,
           'BS': 0.0,
           'BodyTemp': 0.0,
           'HeartRate':0}


def talk(text):
    speak.say(text)
    speak.runAndWait()


def audio_inp():
    with sr.Microphone() as source:
        print("Listening...")
        talk("Listening")
        voice = listener.listen(source)
        print("Processing...")
        voice_inp = ''
        try:
            voice_inp = listener.recognize_google(voice)
        except sr.UnknownValueError:
            talk("Sorry I did not get that")
        except sr.RequestError:
            talk("Sorry, my speech service is down")

        return voice_inp.lower()


def get_value(key, value):
    print(f"Please enter the {value}")
    talk(f"Please enter the {value}")
    value_inp = audio_inp()
    print(f"Checking if {value} entered is {value_inp} correct? [Yes/No]")
    talk(f"{value} entered is {value_inp} correct?")
    yes_or_no = audio_inp()
    print(f"User said {yes_or_no}")
    if str(yes_or_no.lower()) == 'no':
        get_value(key, value)
    elif str(yes_or_no.lower()) == 'yes':
        if key == 'BodyTemp' or key == 'BS':
            key_val[key] = float(value_inp)
        else:
            key_val[key] = int(value_inp)
    else:
        get_value(key, value)
    print(f"Updated Dictionary: ")
    print(key_val)


if __name__ == '__main__':
    print("Logs")
    print(("Hi, I will be assisting you with the filling of the data, please speak the values for the variables as I "
           "say them"))
    talk("Hi, I will be assisting you with the filling of the data, please speak the values for the variables as I "
         "say them")
    to_get = {'SystolicBP': 'upper blood pressure or systolic blood pressure',
              'DiastolicBP': 'lower blood pressure or diastolic blood pressure',
              'Age': 'age',
              'BS': 'blood glucose level or blood sugar level',
              'BodyTemp': 'body temperature in Celsius',
              'HeartRate': 'heart rate'}
    for key, value in to_get.items():
        get_value(key, value)
    talk("Thank you for sharing the patient's data with me")

