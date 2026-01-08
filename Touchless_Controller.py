import cv2
import mediapipe as mp
import pyautogui
import time
import math
import numpy as np 

# --- HELPER FUNCTION ---
def map_range(x, in_min, in_max, out_min, out_max):
    val = (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
    return max(0, min(val, out_max))

# --- CONFIGURATION ---
FRAME_REDUCTION = 190   
SMOOTHING = 5           # Higher = Smoother Mouse
CLICK_COOLDOWN = 0.5    
SCROLL_COOLDOWN = 0.05  # Speed limit for scrolling

# Zones
SCROLL_ZONE_TOP = 0.1   # Top 10%
SCROLL_ZONE_BOTTOM = 0.9 # Bottom 10%

# Scroll Speed Settings
MAX_SPEED = 5
MIN_SPEED = 1

# Colors
COLOR_MOUSE = (255, 179, 186)   
COLOR_CLICK = (186, 255, 201)   
COLOR_NEUTRAL = (250, 200, 200) 

pyautogui.PAUSE = 0
pyautogui.FAILSAFE = False 
wScr, hScr = pyautogui.size()

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

window_name = "Touchless Controller"
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
cv2.setWindowProperty(window_name, cv2.WND_PROP_TOPMOST, 1)
cv2.resizeWindow(window_name, 500, 280)

# Variables
plocX, plocY = 0, 0 
clocX, clocY = 0, 0 
last_click_time = 0
last_scroll_time = 0

print("Controller Active. Middle = Mouse. Edges = Scroll. Pinch = Click.")

while True:
    success, img = cap.read()
    if not success: break

    img = cv2.flip(img, 1)
    h, w, c = img.shape
    
    # Draw the Virtual Mousepad Box (White)
    cv2.rectangle(img, (FRAME_REDUCTION, FRAME_REDUCTION), 
                  (w - FRAME_REDUCTION, h - FRAME_REDUCTION), 
                  (255, 255, 255), 2)
    
    # Draw Scroll Limits (Lavender)
    cv2.line(img, (0, int(h * SCROLL_ZONE_TOP)), (w, int(h * SCROLL_ZONE_TOP)), COLOR_NEUTRAL, 2)
    cv2.line(img, (0, int(h * SCROLL_ZONE_BOTTOM)), (w, int(h * SCROLL_ZONE_BOTTOM)), COLOR_NEUTRAL, 2)

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            index_tip = hand_landmarks.landmark[8]
            thumb_tip = hand_landmarks.landmark[4]
            
            x1 = int(index_tip.x * w)
            y1 = int(index_tip.y * h)
            
            current_time = time.time()

            # --- 1. SCROLL CHECK (TOP EDGE) ---
            if index_tip.y < SCROLL_ZONE_TOP:
                if current_time - last_scroll_time > SCROLL_COOLDOWN:
                    # Calculate Speed based on how high your finger is
                    depth = (SCROLL_ZONE_TOP - index_tip.y) / SCROLL_ZONE_TOP
                    speed = int(MIN_SPEED + (depth * (MAX_SPEED - MIN_SPEED)))
                    
                    cv2.putText(img, f"UP x{speed}", (50, 50), cv2.FONT_HERSHEY_DUPLEX, 1, (200,255,200), 2)
                    for _ in range(speed): pyautogui.press('up')
                    last_scroll_time = current_time
            
            # --- 2. SCROLL CHECK (BOTTOM EDGE) ---
            elif index_tip.y > SCROLL_ZONE_BOTTOM:
                if current_time - last_scroll_time > SCROLL_COOLDOWN:
                    # Calculate Speed based on how low your finger is
                    depth = (index_tip.y - SCROLL_ZONE_BOTTOM) / (1.0 - SCROLL_ZONE_BOTTOM)
                    speed = int(MIN_SPEED + (depth * (MAX_SPEED - MIN_SPEED)))
                    
                    cv2.putText(img, f"DOWN x{speed}", (50, 50), cv2.FONT_HERSHEY_DUPLEX, 1, (200,200,255), 2)
                    for _ in range(speed): pyautogui.press('down')
                    last_scroll_time = current_time
                
            else:
                # --- 3. MOUSE MOVE (MIDDLE ZONE) ---
                # Only move mouse if we are NOT in the scroll zones
                # Map coordinates
                x3 = map_range(x1, FRAME_REDUCTION, w - FRAME_REDUCTION, 0, wScr)
                y3 = map_range(y1, FRAME_REDUCTION, h - FRAME_REDUCTION, 0, hScr)
                
                # Smooth it
                clocX = plocX + (x3 - plocX) / SMOOTHING
                clocY = plocY + (y3 - plocY) / SMOOTHING
                
                try:
                    pyautogui.moveTo(clocX, clocY)
                except:
                    pass
                plocX, plocY = clocX, clocY
                
                cv2.circle(img, (x1, y1), 10, COLOR_MOUSE, cv2.FILLED)

            # --- 4. CLICK CHECK (PINCH) ---
            ix, iy = int(index_tip.x * w), int(index_tip.y * h)
            tx, ty = int(thumb_tip.x * w), int(thumb_tip.y * h)
            dist = math.hypot(ix - tx, iy - ty)
            
            if dist < 30 and (current_time - last_click_time > CLICK_COOLDOWN):
                cv2.circle(img, (ix, iy), 15, COLOR_CLICK, cv2.FILLED)
                cv2.putText(img, "CLICK", (ix, iy-20), cv2.FONT_HERSHEY_DUPLEX, 1, COLOR_CLICK, 2)
                pyautogui.click()
                last_click_time = current_time

    cv2.imshow(window_name, img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()