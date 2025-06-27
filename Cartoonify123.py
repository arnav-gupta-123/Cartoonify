import numpy as np
import cv2
import matplotlib.pyplot as plt
import PySimpleGUI as sg
import os
import io
from PIL import Image, ImageTk  

working_directory = os.getcwd()

answer = ""
name = ""

def cartoon_window():
  global answer
  global name
  layout = [[sg.Image(name,expand_x=True, expand_y=True)]]
  window = sg.Window("Cartoon Image", layout, margins=(10, 10),resizable=True).Finalize()
  window.Maximize()
  
  while True:
      event, values = window.read()

      if event in (None, 'Exit'):
        break
     
  window.close()

def ink_window():
  global answer
  global name
  layout = [[sg.Image(name,expand_x=True, expand_y=True)]]
  window = sg.Window("Ink Sketch", layout, margins=(10, 10),resizable=True).Finalize()
  window.Maximize()
  
  while True:
      event, values = window.read()
      if event in (None, 'Exit'):
        break

      
  window.close()

def pencil_window():
  global answer
  global name
  layout = [[sg.Image(name,expand_x=True, expand_y=True)]]
  window = sg.Window("Pencil Sketch", layout, margins=(10, 10),resizable=True).Finalize()
  window.Maximize()
  
  while True:
      event, values = window.read()
      if event in (None, 'Exit'):
        break
      
  window.close()

def image_window():
  global name
  global answer

  layout = [[sg.Text("Press Load Image to check if you have the correct image to Cartoonify.")],[sg.Image(key="-IMAGE-")],[sg.Button("Load Image")],[sg.Text("Then, choose an Option:")],[sg.Button("Cartoon")],[sg.Button("Ink Sketch")],[sg.Button("Colored Pencil")]]

  window = sg.Window("Original Image", layout, margins=(10, 10),resizable=True).Finalize()
  window.Maximize()
  
  while True:
      event, values = window.read()

      if event == "Load Image":
        image = Image.open(answer)
        image.thumbnail((400, 400))
        bio = io.BytesIO()
        image.save(bio, format="PNG")
        window["-IMAGE-"].update(data=bio.getvalue())
  
      if event == "Cartoon":
        ImagePathway = answer
        color = cv2.imread(ImagePathway)
        greyscale = cv2.cvtColor(color, cv2.COLOR_BGR2GRAY)
        blurred = cv2.blur(greyscale, (8,8))
        edges = cv2.adaptiveThreshold(blurred, 200, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 15, 5)
        reshapingimage = color.reshape((-1,3))
        reshapingimage = np.float32(reshapingimage)
        criteria =(cv2.TERM_CRITERIA_EPS+cv2.TERM_CRITERIA_MAX_ITER,10,1.0)
        K = 100
        compactness,label,center = cv2.kmeans(reshapingimage,K,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)
        center = np.uint8(center)
        a = center[label.flatten()]
        b = a.reshape(color.shape)
        cartoon_image = cv2.bitwise_and(b,b,mask=edges)
        name = "Cartoon_Image.png"
        cv2.imwrite(name, cartoon_image)
        cartoon_window()

      if event == "Ink Sketch":
        ImagePathway = answer
        color = cv2.imread(ImagePathway)
        greyscale = cv2.cvtColor(color, cv2.COLOR_BGR2GRAY)
        #blurred = cv2.blur(greyscale, (8,8))
        edges = cv2.adaptiveThreshold(greyscale, 200, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 15, 5)
        name = "Ink_Image.png"
        cv2.imwrite(name, edges)
        ink_window()

      if event == "Colored Pencil":
        ImagePathway = answer
        color = cv2.imread(ImagePathway)
        a, b = cv2.pencilSketch(color, sigma_s=100, sigma_r=0.02, shade_factor=0.1) 
        #b = cv2.cvtColor(b, cv2.COLOR_BGR2RGB)
        name = "Colored_Pencil_Image.png"
        cv2.imwrite(name, b)
        pencil_window()
        
      if event in (None, 'Exit'):
        break
        
  window.close()

def directions():
  global name
  global answer
  layout = [[sg.Text("1) Select an Image. It must be a PNG or JPG file and for best results, it should be in good quality")], [sg.Text("2) Click Load Image to check if you have the correct image file.")], [sg.Text("3) Choose either Cartoon, Ink Sketch, or Colored Pencil. ")], [sg.Text("4) Wait a couple minutes for the image to load. The final image will be displayed on the screen and will also be saved in your directory.")]]

  window = sg.Window("Instructions", layout, margins=(10, 10),resizable=True).Finalize()
  window.Maximize()
  
  while True:
      event, values = window.read()
      if event in (None, 'Exit'):
        break

def main_window():
  global answer 
  
  layout = [  
            [sg.Text("Choose an image file (PNG or JPEG):")],
            [sg.InputText(key="-FILE_PATH-"), 
            sg.FileBrowse(initial_folder=working_directory)],
            [sg.Button('Submit'), sg.Exit(), sg.Button("Instructions")]
        ]
  window = sg.Window("Cartoonify", layout, margins=(10, 10),resizable=True).Finalize()
  window.Maximize()
  
  while True:
      event, values = window.read()
  
      if event == "Submit":
        answer = values["-FILE_PATH-"]
        image_window()
        
      if event in (sg.WIN_CLOSED, 'Exit'):
        break

      if event == "Instructions":
        directions()

  window.close()

if __name__ == "__main__":
  main_window()
