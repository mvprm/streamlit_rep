import streamlit as st
import pandas as pd
from tempfile import NamedTemporaryFile
import os
from PIL import Image
import sys
import subprocess

# desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop') 

# from win32com.shell import shell, shellcon
# import pypiwin32 
# desktop = shell.SHGetFolderPath (0, shellcon.CSIDL_DESKTOP, 0, 0)

# if sys.platform == "win32":
#    command = r'reg query "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders" /v "Desktop"'
#    result = subprocess.run(command, stdout=subprocess.PIPE, text = True)
#    desktop = result.stdout.splitlines()[2].split()[2]
#else:
#    desktop = os.path.expanduser("~/Desktop")

username = 'migas' # os.getlogin()
desktop = 'C:\\Users\\' + username + '\\Desktop' 

def resize_images(set_images_df, MAX_FILE_SIZE):
    if set_images_df is not None:
        for image_s in set_images_df:    
            file = image_s.read()    
            file_details = {'filename': image_s.name, 'filetype': image_s.type, 'imageSize': image_s.size}
            #with NamedTemporaryFile(dir='.', suffix='.png') as f:
            #    f.write(image_s.getbuffer())
            # Open image
            image = Image.open(image_s) # desktop + '\\' +  image_s.name)
            # Get the current file size
            image_size = file_details['imageSize'] # os.stat(desktop + '\\' +  image_s.name).st_size # os.path.getsize(image_s.name) 
            if image_size > MAX_FILE_SIZE:
                # Calculate new image size
                new_size = (MAX_FILE_SIZE / image_size) ** 0.5
                new_width, new_height = int(new_size * image.size[0]), int(new_size * image.size[1])
                # Resize image
                image_n = image.resize((new_width, new_height))
                # Save the refactored image to the specified folder
                '''with open(os.path.join('Resized_Images', image_s.name), 'wb') as f:
                    f.write(image_s.getbuffer())'''
                save_dir = os.path.join('Resized_ims/')
                os.makedirs(save_dir, exist_ok=True)
                image_n.save(save_dir + image_s.name[:-4] + '_resized.jpg')
                st.text("Resizing Completed!")      
            else:
                print('Image is already below Max Size!')
                st.text("Image is already reduced")
                image_n = image
            st.image(image_n)                
    return 

# Image.from()


# Text
st.title("Image Reduction Program")

# Insert image
set_images = st.file_uploader("Insert image", type=[".jpg", ".png"], accept_multiple_files=True)
# Set the desired maximum file size in bytes
slider = st.slider("Maximum image size (MB)", min_value=0.0, max_value=5.0, value=1.0, step=0.5) # 1000000
MAX_FILE_SIZE = slider * 1000000

# Button to resize
btn = st.button("Resize", disabled=False) # on_click=resize_images(set_images, MAX_FILE_SIZE), 
if btn:
    resize_images(set_images, MAX_FILE_SIZE)

