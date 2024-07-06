import streamlit as st
from PIL import Image
from PIL.ExifTags import TAGS
import pandas as pd

def get_exif_data(image_path):
    image = Image.open(image_path)
    exif_data = image._getexif()

    if exif_data is not None:
        extracted_exif = {}
        for tag, value in exif_data.items():
            tag_name = TAGS.get(tag, tag)
            extracted_exif[tag_name] = value
        return extracted_exif
    else:
        return None

# Main Streamlit app
def main():
    st.title('Registration of animals')

    # Upload multiple image files
    uploaded_images = st.file_uploader("Upload multiple images", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

    exif_data_list = []
    file_names = []

    for uploaded_image in uploaded_images or []:
        if uploaded_image is not None:
            image = Image.open(uploaded_image)
            st.image(image, caption="Uploaded Image", use_column_width=True)

            # Get file name and EXIF data
            file_names.append(uploaded_image.name)
            exif_data = get_exif_data(uploaded_image)
            exif_data_list.append(exif_data['DateTime'])


    # Save to DataFrame and CSV
    if exif_data_list:
        data = {'img_name': file_names, 'date_registration': exif_data_list}
        df = pd.DataFrame(data)
        st.subheader('Registrations:')
        st.dataframe(df)

        st.subheader('Download CSV File:')
        csv = df.to_csv(index=False)
        st.download_button(label="Download CSV", data=csv, file_name='exif_data.csv', mime='text/csv')

# Run the app
if __name__ == '__main__':
    main()
