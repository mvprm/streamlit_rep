import streamlit as st
import pandas as pd
from tempfile import NamedTemporaryFile
import os
from PIL import Image
import sys
import subprocess
import getpass
import base64
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import io

username = getpass.getuser() # os.getlogin()
desktop = 'C:\\Users\\' + username + '\\Desktop\\' 
print('Username: {}'.format(username))

def resize_images(set_images_df, max_size): # height, width):
    transformed_images = []
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
            if image_width > max_size: # > width or image_height > height:
                # Calculate new image size
                new_size = (max_size / image_size) ** 0.5
                new_width, new_height = int(new_size * image.size[0]), int(new_size * image.size[1])
                # new_width = width
                # new_height = height
                # Resize image
                image_n = image.resize((new_width, new_height))
                # Save the refactored image to the specified folder
                save_dir = desktop + 'Resized_Images\\' # os.path.join('Resized_Images\\')
                os.makedirs(save_dir, exist_ok=True)
                print(save_dir)
                image_n.save(save_dir + image_s.name[:-4] + '_resized.jpg')
                      
            else:
                print('Image is already with desired size!')
                st.text("Image has already the desired size!")
                image_n = image
            st.image(image_n)   
            transformed_images.append(image_n)
    st.text("Resizing Completed!")             
    return transformed_images

# Define function to download the image
def download_image(image):
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    href = f'<a download="result.jpg" href="data:file/jpg;base64,{img_str}">Download result</a>'
    return href

# Define function to send email
def send_email(images, recipient_email):
    # Set up email parameters
    sender_email = "migas22.meneses@gmail.com" # st.text_input("Sender email address:", value="migas_meneses@hotmail.com" )
    sender_password = "nuhfslbmnuziuymw" # st.text_input("Your email password:", type="password", value="P1gn2t3ll1!22" )
    recipient_email = recipient_email # st.text_input("Your email address:", value=recipient_email) # st.text_input("Recipient email address:")
    subject = "Fotografias Dermatologia Resized" # st.text_input("Subject:")
    body = "Versão minimizada das fotografias." # st.text_area("Message:")
    # Create message object
    msg = MIMEMultipart()
    msg["From"] = recipient_email
    msg["To"] = recipient_email
    msg["Subject"] = subject
    for i, image in enumerate(images):
        buffered = io.BytesIO()
        image.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        img = MIMEImage(base64.b64decode(img_str), name=f"result_{i+1}.jpg")
        msg.attach(img)
    # Add text to message
    text = MIMEText(body)
    msg.attach(text)

    print(sender_email)
    print(recipient_email)
    # Send email
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()        
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()
        st.success("Email sent!")
    except Exception as e:
        st.error(f"Error: {e}")

# Logo image
image = Image.open('resize-image.png')
new_image = image.resize((700, 400))
st.image(new_image)
# st.image('resize-image.png', width=700, img_height=150)
# Text
st.title("Image Reduction Program")


# Insert image
set_images  = st.file_uploader("Insert image", type=[".jpg", ".png"], accept_multiple_files=True)
# # Set the desired image height and width
# col3, buff, buff2 = st.columns([1,3,1])
# with col3:
#     img_height = st.number_input("Image Height: ", value=100, )
# col4, buff, buff2 = st.columns([1,3,1])
# with col4:
#     img_width = st.number_input("Image Width: ", value=150)

slider = st.slider("Maximum image size (MB)", min_value=0.0, max_value=5.0, value=1.0, step=0.5) # 1000000
MAX_FILE_SIZE = slider * 1000000

if "load_state" not in st.session_state:
     st.session_state.load_state = False
     st.session_state.send_email = False
     st.session_state.download_btn = False

output = False
# Button to resize
btn = st.button("Resize", disabled=False) # on_click=resize_images(set_images, MAX_FILE_SIZE), 
if btn or st.session_state.load_state:    
    st.session_state.load_state = True
    transformed_images = resize_images(set_images, slider) # img_height, img_width)
    st.write(f"Number of transformed images: {len(transformed_images)}")
    # st.session_state['images'] = transformed_images
    # Download or send images        
    # st.session_state.get(name="", button_sent=False)
    # output_option = st.radio("Output option:", ("Download results", "Send via email"), disabled=False, on_change=output)
    output = True

    if output:        
        output_option = st.radio("Output option:", ["Download results", "Send via email"], disabled=False)
        if output_option == "Download results":        
            # transformed_images = st.session_state['images']
            download =  st.button("Download results", disabled=False)
            st.session_state.download_btn = False
            if download or st.session_state.download_btn:
                st.session_state.download_btn = True
                for i, transformed_image in enumerate(transformed_images):
                    st.markdown(download_image(transformed_image), unsafe_allow_html=True)
        elif output_option == "Send via email":
            # transformed_images = st.session_state['images']
            recipient_email = st.text_input("Recipient email address:", value="mmeneses@arsnorte.min-saude.pt")
            send = st.button("Send email", disabled=False)
            st.session_state.send_email = False
            if send or st.session_state.send_email:
                # st.text('HERE')
                send_email(transformed_images, recipient_email) 

        

        

