import speech_recognition as sr
import pyttsx3 as pt
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder
import xgboost as xgb


def split_data(df):
    X = df.drop(['RiskLevel'], axis=1)
    y = df.RiskLevel
    return X, y


def preprocess_scaling(x):
    x = sc.fit_transform(x)
    return x


def scale_predict(x):
    x = sc.transform(x)
    return x


listener = sr.Recognizer()
speak = pt.init()
key_val = {'SystolicBP': 0,
           'DiastolicBP': 0,
           'Age': 0,
           'BS': 0.0,
           'BodyTemp': 0.0,
           'HeartRate': 0}


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
    df = pd.read_csv('Maternal Health Risk Data Set.csv')
    sc = StandardScaler()
    le = LabelEncoder()
    X, y = split_data(df)
    X.BodyTemp = (X.BodyTemp - 32) * 5 / 9  # converting to celcius
    y = le.fit_transform(y)
    X = preprocess_scaling(X)
    xgb_clf = xgb.XGBClassifier(n_estimator=66, learning_rate=0.09, max_depth=9, random_state=7)
    xgb_clf = xgb_clf.fit(X, y)
    print("Logs: --------------------------------------------------------------------------------")
    print(("Hi, I will be assisting you with the filling of the data, please speak the values for the variables as I "
           "say them"))
    talk("Hi, I will be assisting you with the filling of the data, please speak the values for the variables as I "
         "say them")
    to_get = {'SystolicBP': 'upper blood pressure or systolic blood pressure',
              'DiastolicBP': 'lower blood pressure or diastolic blood pressure',
              'Age': 'age in years',
              'BS': 'blood glucose level or blood sugar level',
              'BodyTemp': 'body temperature in Celsius',
              'HeartRate': 'heart rate'}
    for key, value in to_get.items():
        get_value(key, value)
        print("---------------------------------------------------------------------------------")
    talk("Thank you for sharing the patient's data with me")


    age = key_val['Age']
    systolicBp = key_val['SystolicBP']
    diastolicBp = key_val['DiastolicBP']
    bloodSugar = key_val['BS']
    bodyTemp = key_val['BodyTemp']
    heartRate = key_val['HeartRate']
    pred = [[age], [systolicBp], [diastolicBp], [bloodSugar], [bodyTemp], [heartRate]]
    pred = np.array(pred)
    pred = np.reshape(pred, (1, 6))
    pred = scale_predict(pred)

    ans = xgb_clf.predict(pred)
    if ans == [0]:
        print('Mother is at Low Risk')
        talk('Mother is at Low Risk')
        key_val['RiskLevel'] = ans[0]
    elif ans == [1]:
        print('Mother is at Medium Risk')
        talk('Mother is at Medium Risk')
        key_val['RiskLevel'] = ans[0]
    else:
        print('Mother is at High Risk')
        talk('Mother is at High Risk')
        key_val['RiskLevel'] = ans[0]

    df.append(key_val, ignore_index=True)
    df = df.to_csv('Maternal Health Risk Data Set.csv', index=False)
    talk("Thank you!")
    print("---------------------------------------------------------------------------------")