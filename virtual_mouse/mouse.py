import mediapipe as mp
import cv2
import numpy as np
from mediapipe.framework.formats import landmark_pb2
import time
from math import sqrt
import win32api
import pyautogui
 
 
 
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
click=0
sn=0

def get_label(index, hand, results):
    output = None
    for idx, classification in enumerate(results.multi_handedness):
        if classification.classification[0].index == index:
            
            # Process results
            global label
            label = classification.classification[0].label
            
            text = '{} '.format(label)
            
            # Extract Coordinates
            coords = tuple(np.multiply(
                np.array((hand.landmark[mp_hands.HandLandmark.WRIST].x, hand.landmark[mp_hands.HandLandmark.WRIST].y)),
            [640,480]).astype(int))
            
            output = text, coords
            
    return output
 
video = cv2.VideoCapture(0,cv2.CAP_DSHOW)
 
with mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.8) as hands: 
    while video.isOpened():
        _, frame = video.read()
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
         
        image = cv2.flip(image, 1)
 
        imageHeight, imageWidth, _ = image.shape
 
        results = hands.process(image)
   
 
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
  
        if results.multi_hand_landmarks:
            for num, hand in enumerate(results.multi_hand_landmarks):
                mp_drawing.draw_landmarks(image, hand, mp_hands.HAND_CONNECTIONS, 
                                        mp_drawing.DrawingSpec(color=(250, 44, 250), thickness=2, circle_radius=2),
                                        mp_drawing.DrawingSpec(color=(250, 44, 250), thickness=2, circle_radius=2)
                                         )
                # Render left or right detection
                if get_label(num, hand, results):
                    text, coord = get_label(num, hand, results)
                    cv2.putText(image, text, coord, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
 
        if results.multi_hand_landmarks != None:
          for handLandmarks in results.multi_hand_landmarks:
            for point in mp_hands.HandLandmark:
 
    
                normalizedLandmark = handLandmarks.landmark[point]
                pixelCoordinatesLandmark = mp_drawing._normalized_to_pixel_coordinates(normalizedLandmark.x, normalizedLandmark.y, imageWidth, imageHeight)
    
                point=str(point)
                

                
            
                if point=='HandLandmark.INDEX_FINGER_TIP':
                 try:
                    indexfingertip_x=pixelCoordinatesLandmark[0]
                    indexfingertip_y=pixelCoordinatesLandmark[1]
                    if label=="Right":
                        try:
                          win32api.SetCursorPos((indexfingertip_x*4,indexfingertip_y*5))
                        except:
                            pass
 
                 except:
                    pass
 
                elif point=='HandLandmark.THUMB_TIP':
                 try:
                    thumbfingertip_x=pixelCoordinatesLandmark[0]
                    thumbfingertip_y=pixelCoordinatesLandmark[1]
                    

                 except:
                    pass
                elif point =='HandLandmark.MIDDLE_FINGER_TIP':
                 try:
                    middlefingertip_x = pixelCoordinatesLandmark[0]
                    middlefingertip_y = pixelCoordinatesLandmark[1]


                 except:
                    pass

                elif point =='HandLandmark.PINKY_TIP':
                 try:
                    littlefingertip_x = pixelCoordinatesLandmark[0]
                    littlefingertip_y = pixelCoordinatesLandmark[1]


                 except:
                    pass

                elif point =='HandLandmark.RING_FINGER_TIP':
                 try:
                    ringfingertip_x = pixelCoordinatesLandmark[0]
                    ringfingertip_y = pixelCoordinatesLandmark[1]


                 except:
                    pass
                elif point =='HandLandmark.RING_FINGER_PIP':
                 try:
                    ringfingerpip_x = pixelCoordinatesLandmark[0]
                    ringfingerpip_y = pixelCoordinatesLandmark[1]


                 except:
                    pass
                elif point =='HandLandmark.PINKY_FINGER_MCP':
                 try:
                    pinkyfingermcp_x = pixelCoordinatesLandmark[0]
                    pinkyfingermcp_y = pixelCoordinatesLandmark[1]


                 except:
                    pass

                elif point =='HandLandmark.WRIST':
                 try:
                    wrist_x = pixelCoordinatesLandmark[0]
                    wrist_y = pixelCoordinatesLandmark[1]


                 except:
                    pass

                

                try:
                    Distance_x= sqrt((indexfingertip_x-thumbfingertip_x)**2 + (indexfingertip_x-thumbfingertip_x)**2)
                    Distance_y= sqrt((indexfingertip_y-thumbfingertip_y)**2 + (indexfingertip_y-thumbfingertip_y)**2)
                    if Distance_x<35 or Distance_x<-35:
                        if Distance_y<35 or Distance_y<-35:
                            click=click+1
                            if click%35==0:
                                if label=="Right":
                                  print("left click")
                                  pyautogui.click()
                                if label=="Left":
                                   print("copy")
                                   pyautogui.hotkey('ctrl', 'c')


                except:
                    pass 
                    
                                           
 
                

                try:
                   
                    Distance_x = sqrt(
                        ( thumbfingertip_x - middlefingertip_x) ** 2 + (thumbfingertip_x - middlefingertip_x) ** 2)
                    Distance_y = sqrt(
                        (thumbfingertip_y - middlefingertip_y) ** 2 + (thumbfingertip_y - middlefingertip_y) ** 2)
                    if Distance_x < 35 or Distance_x < -35:
                        if Distance_y < 35 or Distance_y < -35:
                            click = click + 1
                            if click % 40 == 0:
                                if label=="Right":
                                   print("right click")
                                   pyautogui.click(button='right')
                                if label=="Left":
                                   print("paste")
                                   pyautogui.hotkey('ctrl', 'v')

                except:
                    pass

                try:
                    
                    Distance_x = sqrt(
                        ( thumbfingertip_x - littlefingertip_x) ** 2 + (thumbfingertip_x - littlefingertip_x) ** 2)
                    Distance_y = sqrt(
                        (thumbfingertip_y - littlefingertip_y) ** 2 + (thumbfingertip_y - littlefingertip_y) ** 2)
                    if Distance_x < 35 or Distance_x < -35:
                        if Distance_y < 35 or Distance_y < -35:
                            click = click + 1
                            if click % 15 == 0:
                                if label=="Right":
                                    print("screenshot taken")
                                    myScreenshot = pyautogui.screenshot()
                                    sn+=1
                                    myScreenshot.save(f'C:\innovative project\screenshots\{sn}.png')
                                if label=="Left":
                                    print("Dragging")
                                    pyautogui.dragTo(100, 200, button='left')  
                                

                except:
                    pass

                try:
                   
                    Distance_x = sqrt(
                        ( thumbfingertip_x - ringfingertip_x) ** 2 + (thumbfingertip_x - ringfingertip_x) ** 2)
                    Distance_y = sqrt(
                        (thumbfingertip_y - ringfingertip_y) ** 2 + (thumbfingertip_y - ringfingertip_y) ** 2)
                    if Distance_x < 35 or Distance_x < -35:
                        if Distance_y < 35 or Distance_y < -35:
                            click = click + 1
                            if click % 7 == 0:
                                if label=="Right":
                                    print("scrolling up")
                                    pyautogui.scroll(-10)
                                if label=="Left":
                                    print("scrolling down")
                                    pyautogui.scroll(10)

                                
                                

                except:
                    pass

                # try:
                   
                #     Distance_x = sqrt(
                #         ( thumbfingertip_x - ringfingerpip_x) ** 2 + (thumbfingertip_x - ringfingerpip_x) ** 2)
                #     Distance_y = sqrt(
                #         (thumbfingertip_y - ringfingerpip_y) ** 2 + (thumbfingertip_y - ringfingerpip_y) ** 2)
                #     if Distance_x < 35 or Distance_x < -35:
                #         if Distance_y < 35 or Distance_y < -35:
                #             click = click + 1
                #             if click % 10 == 0:
                #                 print("scrolling down")
                #                 pyautogui.scroll(10)

                # except:
                #     pass

                # try:
                   
                #     Distance_x = sqrt(
                #         ( thumbfingertip_x - pinkyfingermcp_x) ** 2 + (thumbfingertip_x - pinkyfingermcp_x) ** 2)
                #     Distance_y = sqrt(
                #         (thumbfingertip_y - pinkyfingermcp_y) ** 2 + (thumbfingertip_y - pinkyfingermcp_y) ** 2)
                #     if Distance_x < 35 or Distance_x < -35:
                #         if Distance_y < 35 or Distance_y < -35:
                #             click = click + 1
                #             if click % 30 == 0:
                #                 print("copy")
                #                 pyautogui.hotkey('ctrl', 'c')

                # except:
                #     pass
                
                # try:
                   
                #     Distance_x = sqrt(
                #         ( thumbfingertip_x - wrist_x) ** 2 + (thumbfingertip_x - wrist_x) ** 2)
                #     Distance_y = sqrt(
                #         (thumbfingertip_y - wrist_y) ** 2 + (thumbfingertip_y - wrist_y) ** 2)
                #     if Distance_x < 35 or Distance_x < -35:
                #         if Distance_y < 35 or Distance_y < -35:
                #             click = click + 1
                #             if click % 30 == 0:
                #                 print("paste")
                #                 pyautogui.hotkey('ctrl', 'v')

                # except:
                #     pass
 
                
 
        cv2.imshow('Hand Tracking', image)
 
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
 
video.release()