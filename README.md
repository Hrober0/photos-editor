# Photo editor
A user-friendly application for creating and managing personalized photo galleries through an intuitive visual interface.

![image](https://github.com/user-attachments/assets/2a5f578d-cc32-403c-9453-1ee54c3bd48f)


## Utilities
- Get unique photos from the web, searched by phots description
- Display photos on one page
- Maniplate photos positions
- Adding and removing photos from the gallery
- Applies various effects on photos such as:
    - rotation
    - flip
    - blur
- Save prepared photos as one file

## Used frameworks and APIs
- flask
    - display the application as a web page
    - file organization

- pillow
    - image edition

- unsplash
    - receive images of the given query

## Configuration
(Linux command line)
* pip install pillow
* pip install flask
* export FLASK_APP=main.py
* export FLASK_ENV=development

## Project structure
- main.py       - script controls page display and handles page actions,
                -  contain app configuration data,
                -  app should be run by
                -  it is user interface so it needn't be tested

- README.md     - project description

- scripts
    - images_manager.py   - used to manipulate images in an images directory
    - pillow_api.py       - use to apply effect on images
    - unsplash_api.py     - used to request images
    - progres_counter.py  - clas to track long task progress and raport task status in console

- tests - directory with tests
    - test_images         - directory for test images
    - test_management     - directory for test images_manager
    - test_images_manager.py  - tests for images_manager
    - test_pillow_api.py      - tests for pillow_api
    - test_unsplash_api.py    - tests for unsplash_api 
    - progres_counter.py      - tests for progres_counter

- static
    - app_images    -  directory with images for web app
    - stylesheets   - directory with styles files for web app
        - base.css          - base styles
        - galery.css        - styles for main page with gallery
        - image_edit.css    - styles for edit page
    - tmp           - directory for temporary files like edit.jpg or collage.jp
    - uploads       - directory with images displayed on the page (in code called images directory)

- templates - directory for HTML files
    - base.html         - basse page structure with progress bar
    - galery.html       - main page with photo gallery and options
    - image edit.html   - edit page with photo edit options and photo preview
