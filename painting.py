import cv2, pyautogui, numpy as np, keyboard, time

pyautogui.PAUSE = 0.003

dirPath = 'C:/Users/Daniel Rosenhamer/Desktop/ColoringProgram/'
colPath = 'C:/Users/Daniel Rosenhamer/Desktop/ColoringProgram/Columns/'

def filter_data(Coords, filter_type):
    add = True
    newCoords = []
    previousCoord = None
    for point in Coords:
        if previousCoord is None:
            if filter_type == "numbers":
                _, y = point
                if y < 1300:
                    newCoords.append(point)
                    previousCoord = point
                    continue
            else:
                newCoords.append(point)
                previousCoord = point
                continue
        
        for newPoint in newCoords:
            if abs(point[0] - newPoint[0]) <= 5 and abs(point[1] - newPoint[1]) <= 5:
                add = False
                
        if add:
            if filter_type == "numbers":
                _, y = point
                if y < 1300:
                    newCoords.append(point)
                    previousCoord = point
            else:
                newCoords.append(point)
                previousCoord = point
            
        add = True
                
    return sorted(newCoords)

def change_color(i):
    x = 215
    pyautogui.moveTo([x + (110*i), 1370])
    pyautogui.click()

def paint_screen(path, colorNum):
    # Load the image you want to search for
    template = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

    # Get the screen dimensions
    screen = pyautogui.screenshot()
    screen = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2GRAY)
    screen_width, screen_height = screen.shape[::-1]

    # Perform template matching
    res = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
    threshold = .85  # Adjust this threshold as needed
    locations = np.where(res >= threshold)

    index = 0

    Coords = []

    # Check if any matches were found
    if locations[0].size > 0:
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
        # print("Number not found")
        
    Coords = sorted(Coords, key=lambda x: x[1])
    newCoords = filter_data(Coords, "numbers")
    
    if len(newCoords) > 0:
        change_color(colorNum)

    for point in newCoords:
        if keyboard.is_pressed('esc'):
                exit()
        x, y = point
        pyautogui.moveTo(x, y)
        pyautogui.click()
        
colors = [[215, 1370], [325, 1370], [435, 1370], [545, 1370], [655, 1370], [765, 1370], [875, 1370], [985, 1370], [1095, 1370]]

# def change_color(i):
#     x = 215
#     pyautogui.moveTo([x + (110*i), 1370])
#     pyautogui.click()

border_color = (241, 213, 164)

def is_finished():
    if pyautogui.pixel(215, 1370) != border_color:
        return False
    return True

def run(numOfColors):
    for i in range(numOfColors):
        if not is_finished():
            if keyboard.is_pressed('esc'):
                    exit()
            if keyboard.is_pressed(' '):
                    break
            # if numOfColors - 21 < 1:
            #     change_color(i)
            # else:
                # TODO implement drag_change_color()
                # print("drag change")
            paint_screen(dirPath + str(i + 1) + ".png", i)
    
def pan_up():
    if not is_finished():
        print("pan up")
        pyautogui.moveTo(15, 0)
        pyautogui.dragTo(15, 1270, button="right")
        pyautogui.mouseUp(button="right")
    
def pan_down():
    if not is_finished():
        print("pan down")
        pyautogui.moveTo(15, 1270)
        pyautogui.dragTo(15, 0, button="right")
        pyautogui.mouseUp(button="right")
        pyautogui.moveTo(15, 1270)
    
def pan_right():
    if not is_finished():
        print("pan right")
        pyautogui.moveTo(1480, 15)
        pyautogui.dragTo(0, 15, button="right")
        pyautogui.mouseUp(button="right")
        pyautogui.moveTo(1050, 15)
        pyautogui.dragTo(0, 15, button="right")
        pyautogui.mouseUp(button="right")
    
def pan_left():
    if not is_finished():
        print("pan left")
        pyautogui.moveTo(0, 15)
        pyautogui.dragTo(1480, 15, button="right")
        pyautogui.mouseUp(button="right")
        pyautogui.moveTo(0, 15)
        pyautogui.dragTo(1050, 15, button="right")
        pyautogui.mouseUp(button="right")
        
def pan_up_half(): 
    pyautogui.moveTo(15, 0)
    pyautogui.dragTo(15, 570, button="right")
    
def pan_down_half():
    pyautogui.moveTo(15, 650)
    pyautogui.dragTo(15, 0, button="right")
    
def pan_right_half():
    pyautogui.moveTo(1260, 15)
    pyautogui.dragTo(0, 15, button="right")
    
def pan_left_half():
    pyautogui.moveTo(0, 15)
    pyautogui.dragTo(1260, 15, button="right")
    
def check_border(constant, position, start, end):
    i = start
    while i < end:
        if position == 0:
            if pyautogui.pixel(constant, i) != border_color:
                return False
        elif position == 1:
            if pyautogui.pixel(i, constant) != border_color:
                return False
        i += 100
    return True

def paint(numOfColors):
    run(numOfColors)
    run(numOfColors)

def find_dimensions():
    count = 0
    # Pan up all the way
    while(True and not is_finished()):
        count += 1
        if count > 1000:
            print("infinite up")
            break
        pan_up()
        if(check_border(715, 1, 35, 2400)):
            break
      
    pan_down_half()
    
    # Find height by panning down
    height = 1
    while(True and not is_finished()):
        count += 1
        if count > 1000:
            print("infinite down")
            break
        pan_down()
        if(check_border(720, 1, 35, 2400)):
            break
        else:
            height += 1
    
    pan_up_half()
        
    # Pan left all the way
    while(True and not is_finished()):
        count += 1
        if count > 1000:
            print("infinite left")
            break
        pan_left()
        if(check_border(1270, 0, 35, 1275)):
            break
        
    pan_right_half()
    
    # Find width by panning right
    width = 1
    while(True and not is_finished()):
        count += 1
        if count > 1000:
            print("infinite right")
            break
        pan_right()
        if(check_border(1280, 0, 35, 1200)):
            break
        else:
            width += 1
            
    pan_left_half()
        
    return width + 1, (height + 1) if height < 2 else height

def paintImage(numOfColors):
    width, height = find_dimensions()
    paint(numOfColors)
    
    # Paint every section of the image
    isPanDown = False
    for i in range(width):
        for j in range(height):
            if not isPanDown:
                pan_up()
            else:
                pan_down()
            paint(numOfColors)
        pan_left()
        if isPanDown:
            pan_up_half()
        else:
            pan_down_half()
        paint(numOfColors)
        isPanDown = not isPanDown