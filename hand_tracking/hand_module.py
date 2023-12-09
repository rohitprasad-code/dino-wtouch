import cv2
import mediapipe as mp
import numpy as np

def extract_landmarks(hand_landmarks):
    landmarks = []
    for point in hand_landmarks.landmark:
        landmarks.extend([point.x, point.y, point.z])
    return np.array(landmarks)

def live_hand():
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands()

    cap = cv2.VideoCapture(0)  

    while True:
        ret, frame = cap.read()

        results = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        
        mp_drawing = mp.solutions.drawing_utils
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                landmarks = extract_landmarks(hand_landmarks)
                print(landmarks)
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                
        cv2.imshow('Hand Tracking', frame)
        
        if cv2.waitKey(1) == ord('q'):
            break
        
    cap.release()
    cv2.destroyAllWindows()
    
live_hand()

