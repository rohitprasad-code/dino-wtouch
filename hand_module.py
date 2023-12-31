import cv2
import mediapipe as mp
import numpy as np
import web_module as web
import key_module as keyboard
import pynput.keyboard as kb

thumb_tip = 4
index_tip = 8
middle_tip = 12
ring_tip = 16
pinky_tip = 20

threshold = 0.1

def is_pinch(landmarks, index_tip, thumb_tip, threshold=0.04):
    index_x, index_y = landmarks[index_tip*3], landmarks[index_tip*3+1]
    thumb_x, thumb_y = landmarks[thumb_tip*3], landmarks[thumb_tip*3+1]
    
    distance = np.sqrt((index_x - thumb_x)**2 + (index_y - thumb_y)**2)
    
    return distance < threshold

def extract_landmarks(hand_landmarks):
    landmarks = []
    for point in hand_landmarks.landmark:
        landmarks.extend([point.x, point.y, point.z]) 
    return np.array(landmarks)

def live_hand():
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands()
    
    web.open_web()
    
    cap = cv2.VideoCapture(0)  
    
    isPressed = False

    while True:
        _, frame = cap.read()

        frameRGB = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        
        mp_drawing = mp.solutions.drawing_utils
        
        if frameRGB.multi_hand_landmarks:
            for hand_landmarks in frameRGB.multi_hand_landmarks:
                landmarks = extract_landmarks(hand_landmarks)
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                
                if is_pinch(landmarks, index_tip, thumb_tip, threshold):
                    print("Pinch detected!")
                    cv2.putText(frame, 'Pinch', (25, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    if not isPressed:
                        keyboard.press_key(kb.Key.space)
                        isPressed = True
                else:
                    print("No pinch.")
                    cv2.putText(frame, 'No Pinch', (25, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    if isPressed:
                        keyboard.release_key(kb.Key.space)
                        isPressed = False
                
        cv2.imshow('Hand Tracking', frame)
        
        if cv2.waitKey(1) == ord('q'):
            break
        
    cap.release()
    cv2.destroyAllWindows()
    
live_hand()
