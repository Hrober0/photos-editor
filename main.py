import pathlib
from typing import List, Tuple
from flask import Flask, redirect, render_template, request, Response
import scripts.progres_counter as progres
import scripts.images_manager as imgManager
import scripts.unsplash_api as unsplash
import scripts.pillow_api as pillow

# Declaration of all const paths using by app
IMAGE_EXTENSION = '.jpg'
CURRENT_PATH = str(pathlib.Path(__file__).parent.resolve()) + '/'

IMAGES_FOLDER_SATIC = 'uploads/'
IMAGES_FOLDER_PATH = f'{CURRENT_PATH}static/{IMAGES_FOLDER_SATIC}'

EDIT_FILE_STATIC = 'tmp/edit' + IMAGE_EXTENSION
EDIT_FILE_PATH = f'{CURRENT_PATH}static/{EDIT_FILE_STATIC}'

COLLAGE_FILE_STATIC = 'tmp/collage' + IMAGE_EXTENSION
COLLAGE_FILE_PATH = f'{CURRENT_PATH}static/{COLLAGE_FILE_STATIC}'


# Declaration of all const values used for display web
IMAGES_IN_ROW = 4


# Init flask app
app = Flask(__name__)
app.config['UPLOAD_PATH'] = IMAGES_FOLDER_PATH


# Init modules using by app
task_progres = progres.ProgresCounter(0, 100)
images_manager = imgManager.ImagesManager(IMAGES_FOLDER_PATH, IMAGE_EXTENSION)
photo_editor = pillow.PhotoEditor(EDIT_FILE_PATH)


# Local methods
def _format_images_to_galery() -> List[List[pathlib.Path]]:
    """Returns images paths from images directory framed in rows"""
    images = images_manager.get_images_from_directory(task_progres)
    images_rows = []
    index = len(images) - 1
    while index >= 0:
        row = []
        for i in range(IMAGES_IN_ROW):
            row.append(images[index])
            index -= 1
            if index < 0:
                break
        images_rows.append(row)
    return images_rows


def _format_images_to_display() -> List[List[Tuple[str, str, int]]]:
    """Returns images data needed to display on page.
    Datas are frmaed in rows.
    Each data is a tuple build of:
        (str) web path
        (str) image formated name
        (int) image index
        """
    images_rows = _format_images_to_galery()
    formated_images_rows = []
    for row in images_rows:
        formated_row = []
        formated_images_rows.append(formated_row)
        for image in row:
            web_path = IMAGES_FOLDER_SATIC + image.name
            formated_row.append((
                web_path,
                images_manager.format_image_name(image.name),
                images_manager.get_image_index(image.name)
                ))
    return formated_images_rows


def _return_exception(text: str) -> str:
    """Format exception name, print it in console
    and return formated exception text"""
    text = f'[EXPECTION] {text}'
    print(f'\n{text}\n')
    return text


# Web methos - used to provide page actions
@app.route('/', methods=['GET', 'POST'])
def route_main() -> Response:
    """Display main galery page"""
    return render_template(
        'galery.html',
        uploads_rows=_format_images_to_display(),
        resolutions=unsplash.get_resolutions(),
        )


@app.route('/search', methods=['GET', 'POST'])
def route_search_images() -> Response:
    """Request images from unsplash api and save them in images directory"""
    if request.method == 'POST':
        query = request.form['search_photos']
        results_number = int(request.form['results_number'])
        resolution = request.form['resolution']
        try:
            images = unsplash.search_images(
                query, results_number, resolution, task_progres)
        except Exception as e:
            return _return_exception(e)
        images_manager.save_images(images, task_progres)
        return redirect('/')


@app.route('/delete-all', methods=['GET'])
def route_delete_all_images() -> Response:
    """Delete all images from images directory"""
    images_manager.delete_all_images(task_progres)
    return redirect('/')


@app.route('/delete/<image_index>', methods=['GET'])
def route_delete_image(image_index: str) -> Response:
    """Delete single image of given index from images directory"""
    image_index = int(image_index)
    images_manager.delate_image_on_index(image_index, task_progres)
    return redirect('/')


@app.route('/save-as-collage', methods=['GET'])
def route_save_as_collage() -> Response:
    """Save all images fromimages directory as one image"""
    images_rows = _format_images_to_galery()
    try:
        photo_editor.save_images_as_collage(
            images_rows,
            300,
            COLLAGE_FILE_PATH)
    except pillow.EmptyGaleryExpection as e:
        return _return_exception(e)
    photo_editor.set_edit_image(pathlib.Path(COLLAGE_FILE_PATH))
    return render_template(
        'image_edit.html',
        image_name='collage',
        image_path=EDIT_FILE_STATIC
        )


@app.route('/edit-set/<image_index>', methods=['GET'])
def route_edit_set_image(image_index: str) -> Response:
    """Select image to edit and redirect to image edit page"""
    image_index = int(image_index)
    images = images_manager.get_images_from_directory(task_progres)
    image = images[image_index]
    photo_editor.set_edit_image(image)
    return render_template(
        'image_edit.html',
        image_name=images_manager.format_image_name(image.name),
        image_path=EDIT_FILE_STATIC
        )


@app.route('/edit-save/<name>', methods=['GET'])
def route_edit_save_image(name: str) -> Response:
    """Save edited image in images directory"""
    try:
        image_bytes = photo_editor.get_edit_image_bytes()
    except Exception as e:
        return _return_exception(e)
    images_manager.save_image(name, image_bytes, False)
    return redirect('/')


@app.route('/edit-apply/<method>', methods=['GET'])
def route_edit_image(method: str) -> Response:
    """Applay given effect to edited image
    Available effect (name as str):
    - turn-left
    - turn-right
    - flip-vertical
    - flip-horizontal
    - blur
    """
    dir = {
        'turn-left': lambda: photo_editor.edit_rotate(90),
        'turn-right': lambda: photo_editor.edit_rotate(-90),
        'flip-vertical': lambda: photo_editor.edit_flip(False),
        'flip-horizontal': lambda: photo_editor.edit_flip(True),
        'blur': lambda: photo_editor.edit_blur()
    }
    if method not in dir:
        return _return_exception(f'no edit method as {method}!')
    dir[method]()
    image_name = photo_editor.edit_file_name
    image_name = images_manager.format_image_name(image_name)
    return render_template(
        'image_edit.html',
        image_name=image_name,
        image_path=EDIT_FILE_STATIC
        )


@app.route('/move-galery-image/<dir>/<image_index>', methods=['GET'])
def route_move_image_position(dir: str, image_index: str) -> Response:
    """Change image index in images directory.
    Available dirs (str):
    - up
    - down
    - right
    - left
    """
    shifts = {
        'up': IMAGES_IN_ROW,
        'down': -IMAGES_IN_ROW,
        'right': -1,
        'left': 1,
    }
    index = int(image_index)
    if dir not in shifts:
        return _return_exception(f'no galry image move as {dir}!')
    shift = shifts[dir]
    images_manager.move_image_position(index, shift, task_progres)
    return redirect('/')


@app.route('/progres')
def route_get_progres() -> str:
    """Returns current task progress"""
    return str(task_progres.progres)


if __name__ == '__main__':
    app.run(debug=True)
