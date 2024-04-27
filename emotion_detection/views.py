from django.shortcuts import render
from django.http import JsonResponse
from .youtube_scraper import YoutubeBot, search_on_youtube
from tensorflow.keras.models import load_model
from keras.preprocessing.image import img_to_array
import cv2
import numpy as np
import time

face_classifier = cv2.CascadeClassifier('model_files/haarcascade_frontalface_default.xml')
classifier = load_model('model_files/model.h5')
emotion_labels = ['Angry', 'Disgusted', 'Feared', 'Happy', 'Neutral', 'Sad', 'Surprised']

def mood_enhancer(emotion):
    opposite_keywords = {
        'Angry': 'calm',
        'Disgusted': 'uplifting',
        'Feared': 'comforting',
        'Neutral': 'joyful',
        'Sad': 'happy or party',
        'Happy': 'melody',
        'Surprised': 'playful'
    }
    return opposite_keywords.get(emotion, '')

youtube_bot = None

def detect_emotion(request):
    if request.method == 'POST':
        cap = cv2.VideoCapture(0)
        start_time = time.time()
        detected_emotion = None

        while time.time() - start_time < 3:  
            ret, frame = cap.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_classifier.detectMultiScale(gray)

            for (x, y, w, h) in faces:
                roi_gray = gray[y:y + h, x:x + w]
                roi_gray = cv2.resize(roi_gray, (48, 48), interpolation=cv2.INTER_AREA)

                if np.sum([roi_gray]) != 0:
                    roi = roi_gray.astype('float') / 255.0
                    roi = img_to_array(roi)
                    roi = np.expand_dims(roi, axis=0)

                    prediction = classifier.predict(roi)[0]
                    detected_emotion = emotion_labels[prediction.argmax()]
                    break

        cap.release()
        cv2.destroyAllWindows()

        if detected_emotion:
            print("Emotion detected:", detected_emotion)
            request.session['detected_emotion'] = detected_emotion  
            return JsonResponse({'emotion': detected_emotion})
        else:
            print("No faces detected during emotion detection.")
            return JsonResponse({'error': 'No faces detected during emotion detection.'})
    else:
        return render(request, 'detect_emotion.html')

def suggest_song(request):
        global youtube_bot
        if request.method == 'POST':
            singer_name = request.POST.get('singer_name', '')
            detected_emotion = request.session.get('detected_emotion', '')  
            opposite_keyword = mood_enhancer(detected_emotion)
            prompt = f"{singer_name} {opposite_keyword} songs"
            print(prompt)  
            
            if youtube_bot is None:
                youtube_bot = YoutubeBot()
                youtube_bot.open_youtube()
                youtube_bot.search(prompt)  
            else:
                youtube_bot.search(prompt)  
            
            search_on_youtube(prompt)  
            return JsonResponse({'prompt': prompt})  
        else:
            return JsonResponse({'error': 'Invalid request.'})  

