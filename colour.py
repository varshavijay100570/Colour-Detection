import cv2
import pandas as pd
import pyttsx3

engine = pyttsx3.init()

csv_path = 'C:/Users/Varsha/OneDrive/Desktop/workshop/colour_recognition/colours.csv'


index = ['color', 'color_name', 'hex', 'R', 'G', 'B']
df = pd.read_csv(csv_path, names=index, header=None)

clicked = False
r = g = b = xpos = ypos = 0

def get_color_name(R, G, B):
    minimum = 1000
    cname = ""
    for i in range(len(df)):
        d = abs(R - int(df.loc[i, 'R'])) + abs(G - int(df.loc[i, 'G'])) + abs(B - int(df.loc[i, 'B']))
        if d < minimum:
            minimum = d
            cname = df.loc[i, 'color_name']
    return cname

def draw_function(event, x, y, flags, param):
    global b, g, r, xpos, ypos, clicked
    if event == cv2.EVENT_LBUTTONDBLCLK:
        clicked = True
        xpos, ypos = x, y
        b, g, r = frame[y, x]
        b, g, r = int(b), int(g), int(r)
        # Get the color name
        color_name = get_color_name(r, g, b)
        # Output the color name as audio
        engine.say(f"The color is {color_name}")
        engine.runAndWait()

cv2.namedWindow('Camera')
cv2.setMouseCallback('Camera', draw_function)

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.resize(frame, (800, 800))
    
    if clicked:
        cv2.rectangle(frame, (20, 20), (600, 60), (0, 0, 0), -1)
        text = get_color_name(r, g, b) 
        cv2.putText(frame, text, (50, 50), 2, 0.8, (255, 255, 255), 2, cv2.LINE_AA)
    
    cv2.imshow('Camera', frame)
    
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
