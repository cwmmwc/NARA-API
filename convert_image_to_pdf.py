import pip._vendor.requests as requests
from PIL import Image
import os
from os import listdir
from os.path import isfile, join
import re
import glob

supplied_naId = input("What is the National Archives ID you want to retrieve?\n")
supplied_api_key = input("What is your National Archives API key?\n")
supplied_document_title = input("What would you like to name your PDF? Do not include a .pdf suffix.\n")

pdf_path = "/Users/ben/Desktop/Code/McMillen-PDF-Project/" + supplied_document_title + ".pdf"
my_path = "/Users/ben/Desktop/Code/McMillen-PDF-Project/images/"

# naId = National Archives ID of object
# API key = National Archives API key. 
# Requestable here: https://www.archives.gov/research/catalog/help/api

def convert_national_archives_img(naId, api_key):

    naId = str(naId)
    api_key = str(api_key)

    api_url = "https://catalog.archives.gov/api/v2/records/search"
    api_call_headers = {"x-api-key": api_key, "Content-Type": "application/json"}
    api_call_parameters = {"limit":1, "q":naId, "action":"export"}

    response = requests.get(api_url, headers = api_call_headers, params = api_call_parameters).json()

    response_list = response["body"]["hits"]["hits"][0]["_source"]["record"]["digitalObjects"]

    print("Successfully completed API query.")
    pages = range(0,len(response_list))

    url_list = list()

    for page in pages:
        url_list.append(response_list[page]["objectUrl"])

    page_num = 1
    for url in url_list:
        data = requests.get(url).content

        f = open(my_path + "page-" + str(page_num) + ".jpg","wb") 

        f.write(data) 
        f.close() 

        page_num = page_num + 1

    print("Saved all images to temporary directory.")
    # filepath for folder containing images

    # create list of image file links
    my_image_files = [f for f in listdir(my_path) if isfile(join(my_path, f)) and "jpg" in f]

    page_numbers = list()

    for file in my_image_files:
        page_num = int(re.findall(r'\b\d+\b', file)[0])
        page_numbers.append(page_num)

    sorted_files = [x for _, x in sorted(zip(page_numbers, my_image_files))]


    # create list of actual images using the image file links
    images = [
        Image.open(my_path + f)
        for f in sorted_files
    ]

    # specify path to write PDF to

    # save the images to the PDF 
    images[0].save(
        pdf_path, "PDF" ,resolution=100.0, save_all=True, append_images=images[1:]
    )

    print("Finished writing PDF.")

    def remove_images():
        files_to_rm = glob.glob(my_path + '*')
        for f in files_to_rm:
            os.remove(f)

    remove_images()
    print("Removed temporary images from images folder.")

convert_national_archives_img(naId = supplied_naId,
                              api_key = supplied_api_key)