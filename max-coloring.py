import cv2, pyautogui, numpy as np, keyboard, time
from maxPaint import paintImage
import os

pyautogui.PAUSE = 0.003
colPath = 'C:/Users/Daniel Rosenhamer/Desktop/ColoringProgram/Columns/'

def click_tab():
    pyautogui.moveTo(200, 200)
    pyautogui.click()

def zoom_out():
    for i in range(0, 500):
        pyautogui.scroll(500)
    for i in range(0, 5):
        pyautogui.scroll(-500)
    
def print_coords(coords):
    print("Coords:")
    for x,y in coords:
        pyautogui.moveTo(x, y)
        print("Point at (" + str(x) + ", " + str(y) +")")
        time.sleep(2)

def find_image(path, numOfColors):
    # Load the image you want to search for
    template = cv2.imread(path)
    
    target_hsv = cv2.cvtColor(template, cv2.COLOR_BGR2HSV)

    # Get the screen dimensions
    screen = pyautogui.screenshot()
    screen = cv2.cvtColor(np.array(screen), cv2.COLOR_BGR2HSV)

    # Perform template matching
    res = cv2.matchTemplate(screen, target_hsv, cv2.TM_CCOEFF_NORMED)
    threshold = .98  # Adjust this threshold as needed
    locations = np.where(res >= threshold)

    Coords = []

    # Check if any matches were found
    if locations[0].size > 0:
        print("Found book")
        
        for pt in zip(*locations[::-1]):        
            
            if keyboard.is_pressed('esc'):
                break
            
            # Get the coordinates of each match
            x, y = pt
            # Get the center coordinates of each match
            center_x = x + template.shape[1] // 2
            center_y = y + template.shape[0] // 2
            Coords.append([center_x, center_y])
    # else:
    #     print("Drawing not found")
        
    Coords = sorted(Coords, key=lambda x: x[1])
    count = 0
    # print_coords(Coords)
    for point in Coords:
        print(point)
        x,y = point
        if keyboard.is_pressed('esc'):
            exit()
        pyautogui.moveTo(x, y + 55)
        pyautogui.click()
        pyautogui.moveTo(500, 500)
        zoom_out()
        paintImage(numOfColors)
        close_image()
        time.sleep(1)
    
def close_image():
    pyautogui.moveTo(50, 1400)
    pyautogui.click()

def color_book():
    for i in range(1, 91):
        if keyboard.is_pressed('esc'):
                exit()
        currPath = colPath + str(i + 1) + ".png"
        if os.path.exists(currPath):
            find_image(currPath, i + 1)
            time.sleep(.25)
        
def drag_change_color():
    pyautogui.moveTo(215, 1000)
    pyautogui.mouseDown()
    pyautogui.moveTo(100, 1000, .5, pyautogui.easeOutQuad)
    pyautogui.mouseUp()
    pyautogui.moveTo(215, 1000)
        
click_tab()
# zoom_out()
# drag_change_color()
color_book()
# paintImage(16)