import streamlit as st
import pandas as pd
from tempfile import NamedTemporaryFile
import os
from PIL import Image
import sys
import subprocess
import getpass

username = getpass.getuser() # os.getlogin()
desktop = 'C:\\Users\\' + username + '\\Desktop\\' 
print('Username: {}'.format(username))

def resize_images(set_images_df, height, width):
    if set_images_df is not None:
        for image_s in set_images_df:    
            file = image_s.read()    
            file_details = {'filename': image_s.name, 'filetype': image_s.type, 'imageSize': image_s.size}
            # , 'imageWidth': image_s.width, 'imageHeight': image_s.height}
            #with NamedTemporaryFile(dir='.', suffix='.png') as f:
            #    f.write(image_s.getbuffer())
            # Open image
            image = Image.open(image_s) # desktop + '\\' +  image_s.name)
            # Get the current file size
            image_size = file_details['imageSize'] # os.stat(desktop + '\\' +  image_s.name).st_size # os.path.getsize(image_s.name) 
            image_width = image.width # file_details['imageWidth']
            image_height = image.height # file_details['imageHeight']
            if image_width > width or image_height > height:
                # Calculate new image size
                new_width = width
                new_height = height
                # Resize image
                image_n = image.resize((new_width, new_height))
                # Save the refactored image to the specified folder
                save_dir = desktop + 'Resized_Images\\' # os.path.join('Resized_Images\\')
                os.makedirs(save_dir, exist_ok=True)
                print(save_dir)
                image_n.save(save_dir + image_s.name[:-4] + '_resized.jpg')
                st.text("Resizing Completed!")      
            else:
                print('Image is already with desired size!')
                st.text("Image has already the desired size!")
                image_n = image
            st.image(image_n)                
    return 

# Logo image
image = Image.open('resize-image.png')
new_image = image.resize((700, 400))
st.image(new_image)
# st.image('resize-image.png', width=700, img_height=150)
# Text
st.title("Image Reduction Program")


# Insert image
set_images  = st.file_uploader("Insert image", type=[".jpg", ".png"], accept_multiple_files=True)
# Set the desired image height and width
col3, buff, buff2 = st.columns([1,3,1])
with col3:
    img_height = st.number_input("Image Height: ", value=100, )
col4, buff, buff2 = st.columns([1,3,1])
with col4:
    img_width = st.number_input("Image Width: ", value=150)

# Button to resize
btn = st.button("Resize", disabled=False) # on_click=resize_images(set_images, MAX_FILE_SIZE), 
if btn:
    resize_images(set_images, img_height, img_width)

