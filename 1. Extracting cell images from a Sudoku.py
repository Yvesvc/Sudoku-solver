#import the necesarry libraries
import cv2
import numpy as np
import copy

#Individual functions:
'''
#Read Sudoku image 
#And convert image to grayscale, convert to either black or white based on treshold, blur the image (for easier edge detection) and detect the edges 

#Input: path of image e.g. 'C:\\Users\user\Documents\image\image1.png'
#Returns cannied image and gray image
'''
def preprocess_image(file_path):
    image = cv2.imread(file_path)
    image_gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    treshold, image_binary = cv2.threshold(image_gray,220,255,cv2.THRESH_BINARY)
    kernel = np.ones((5,5),np.float32)/25
    image_blurred = cv2.filter2D(image_binary,-1,kernel)
    image_canny = cv2.Canny(image_blurred,50,100,apertureSize=3)
    return image_canny,image_gray

'''
#Detects lines and translates each HoughLine onto original image and saves the coordinates
#Credits to user2986898 on https://stackoverflow.com/questions/48954246/find-sudoku-grid-using-opencv-and-python

#Input: cannied image and gray image
#Output: image with HoughLines and coordinates of the HoughLines
'''
def add_HoughLines(image_canny,image_gray):
    HoughLines = cv2.HoughLines(image_canny,1,np.pi/180,150)

    if HoughLines.all() == None:
        return 'No lines were found'

    else:
        lines = []
        image_gray_with_lines = copy.deepcopy(image_gray)
        for line in HoughLines:
            rho,theta = line[0]
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a*rho
            y0 = b*rho
            x1 = int(x0 + 1000*(-b))
            y1 = int(y0 + 1000*(a))
            x2 = int(x0 - 1000*(-b))
            y2 = int(y0 - 1000*(a))
            cv2.line(image_gray_with_lines,(x1,y1),(x2,y2),(0,0,255),2)

            lines.append([x1,y1])
    return image_gray_with_lines, lines

'''
#Based on the HoughLines, get all the cells coordinates in the Sudoku

#Input: lines
#Output: cells coordinates
'''
def get_cells_coordinates(lines):
    #get the horizontal lines
    #get the vertical lines
    lines_horizontal = []
    lines_vertical = []
    for line in lines:
        if line[0] < -900:
            lines_horizontal.append(line[1])
        else:
            lines_vertical.append(line[0])

    #sort horizontal lines form low to high
    lines_horizontal.sort()

    #sort vertical lines from left to right
    lines_vertical.sort()
    
    #remove duplicate horizontal lines by finding two lines that are very close to eachother and remove the first line
    distance_lines_horizontal = []
    for i in range(len(lines_horizontal)):
        if i ==0:
            distance_lines_horizontal.append(lines_horizontal[i])
        else:
            distance_lines_horizontal.append(lines_horizontal[i] -lines_horizontal[i-1])
    distance_lines_horizontal.sort()
    distance_lines_horizontal_correct = distance_lines_horizontal[-1]

    lines_horizontal_no_duplicates = []
    for i in range(len(lines_horizontal)):
        if i ==0 and lines_horizontal[i] > distance_lines_horizontal_correct/2:
            lines_horizontal_no_duplicates.append(lines_horizontal[i])
        elif i!=0 and lines_horizontal[i] - lines_horizontal[i-1] > distance_lines_horizontal_correct/2:
            lines_horizontal_no_duplicates.append(lines_horizontal[i])
            
    #remove duplicate vertical lines by finding two lines that are very close to eachother and remove the first line
    distance_lines_vertical = []
    for i in range(len(lines_vertical)):
        if i ==0:
            distance_lines_vertical.append(lines_vertical[i])
        else:
            distance_lines_vertical.append(lines_vertical[i] -lines_vertical[i-1])
    distance_lines_vertical.sort()
    distance_lines_vertical_correct = distance_lines_vertical[-1]

    lines_vertical_no_duplicates = []
    for i in range(len(lines_vertical)):
        if i ==0 and lines_vertical[i] > distance_lines_vertical_correct/2:
            lines_vertical_no_duplicates.append(lines_vertical[i])
        elif i!=0 and lines_vertical[i] - lines_vertical[i-1] > distance_lines_vertical_correct/2:
            lines_vertical_no_duplicates.append(lines_vertical[i])
            
     #get all the cell coordinates (a cell is the area where 2 horizontal and 2 vertical lines meet
    cells_coordinates = []
    for horizontal in range(len(lines_horizontal_no_duplicates)):
        for vertical in range(len(lines_vertical_no_duplicates)):
            if horizontal == 0 and vertical ==0:
                cells_coordinates.append([':'+str(lines_horizontal_no_duplicates[horizontal]),':'+str(lines_vertical_no_duplicates[vertical])])
            elif horizontal ==0 and vertical != 0:
                cells_coordinates.append([':'+str(lines_horizontal_no_duplicates[horizontal]),str(lines_vertical_no_duplicates[vertical-1])+ ':' +str(lines_vertical_no_duplicates[vertical])])
            elif horizontal != 0 and vertical == 0:
                cells_coordinates.append([str(lines_horizontal_no_duplicates[horizontal-1])+':'+str(lines_horizontal_no_duplicates[horizontal]), ':'+str(lines_vertical_no_duplicates[vertical])])
            elif horizontal != 0 and vertical != 0:
                cells_coordinates.append([str(lines_horizontal_no_duplicates[horizontal-1])+ ':' + str(lines_horizontal_no_duplicates[horizontal]), str(lines_vertical_no_duplicates[vertical-1])+ ':'+ str(lines_vertical_no_duplicates[vertical])])   
    
    return cells_coordinates

'''
#Return a specific cell in the Sudoku

#Input: gray Sudoku image, cells, cell of interest in the Sudoku
#Output: image of the cell of interest in the Sudoku
'''

def get_cell_image(image, cells_coordinates,cell_number):
    cell = cells_coordinates[cell_number]
    #if first horizontal and first vertical
    if cell[0][0] == ':' and cell[1][0] == ':':
        x_begin = 0
        x_end = int(cell[0].split(':')[1])
        y_begin = 0
        y_end = int(cell[1].split(':')[1])
    #if first horizontal and not-first vertical	
    if cell[0][0] == ':' and cell[1][0] != ':':
        x_begin = 0
        x_end = int(cell[0].split(':')[1])
        y_begin = int(cell[1].split(':')[0])
        y_end = int(cell[1].split(':')[1])
    #if not-first horizontal and first vertical
    if cell[0][0] != ':' and cell[1][0] == ':':
        x_begin = int(cell[0].split(':')[0])
        x_end = int(cell[0].split(':')[1])
        y_begin = 0
        y_end = int(cell[1].split(':')[1])
    #if not-first horizontal and not-first vertical
    if cell[0][0] != ':' and cell[1][0] != ':':
        x_begin = int(cell[0].split(':')[0])
        x_end = int(cell[0].split(':')[1])
        y_begin = int(cell[1].split(':')[0])
        y_end = int(cell[1].split(':')[1])

    cell = image[x_begin:x_end, y_begin:y_end]
    return cell


#Enclosing function
'''
Given a Sudoku image, images of all cells are returned

#Input: Sudoku image
#Output: cells images of the Sudoku stored in a list
'''

def get_sudoku_cells(file_path):
    image_canny, image_gray = preprocess_image(file_path)
    image_gray_with_lines, lines = add_HoughLines(image_canny,image_gray)
    cells_coordinates = get_cells_coordinates(lines)
    sudoku_cells = []
    for cell in range(len(cells_coordinates)):
        sudoku_cells.append(get_cell_image(image_gray, cells_coordinates,cell))
    return sudoku_cells
    