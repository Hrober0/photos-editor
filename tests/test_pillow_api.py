from scripts.pillow_api import PhotoEditor
import pathlib
import os
import pytest
import scripts.pillow_api as pillow


IMAGES_PATH = str(pathlib.Path(__file__).parent.resolve()) + '/test_images/'
TEST_FILE_PATH = IMAGES_PATH + 'test_img.jpg'
EDIT_FILE_PATH = IMAGES_PATH + 'edit_img.jpg'


def _clear_edit_file():
    if pathlib.Path(EDIT_FILE_PATH).exists():
        os.remove(EDIT_FILE_PATH)


def _are_images_the_same(editor, second_path):
    with open(second_path, 'rb') as ef:
        test_bytes = ef.read()
    edit_bytes = editor.get_edit_image_bytes()
    assert test_bytes == edit_bytes


def test_set_edit_image_name():
    editor = PhotoEditor(EDIT_FILE_PATH)
    editor.set_edit_image(pathlib.Path(TEST_FILE_PATH))
    assert editor.edit_file_name == 'test_img'


def test_get_edit_image_bytes():
    _clear_edit_file()
    editor = PhotoEditor(EDIT_FILE_PATH)
    editor.set_edit_image(pathlib.Path(TEST_FILE_PATH))
    _are_images_the_same(editor, TEST_FILE_PATH)


def test_get_edit_image_bytes_no_file():
    _clear_edit_file()
    editor = PhotoEditor(EDIT_FILE_PATH)
    with pytest.raises(pillow.NoEditFileExpection):
        editor.get_edit_image_bytes()


def test_edit_blur():
    _clear_edit_file()
    editor = PhotoEditor(EDIT_FILE_PATH)
    editor.set_edit_image(pathlib.Path(TEST_FILE_PATH))
    editor.edit_blur()
    _are_images_the_same(editor, IMAGES_PATH + 'test_img_blur.jpg')


def test_edit_blur_no_file():
    _clear_edit_file()
    editor = PhotoEditor(EDIT_FILE_PATH)
    with pytest.raises(pillow.NoEditFileExpection):
        editor.edit_blur()


def test_edit_flip():
    _clear_edit_file()
    editor = PhotoEditor(EDIT_FILE_PATH)
    editor.set_edit_image(pathlib.Path(TEST_FILE_PATH))
    editor.edit_flip(False)
    _are_images_the_same(editor, IMAGES_PATH + 'test_img_vflip.jpg')


def test_edit_flip_no_file():
    _clear_edit_file()
    editor = PhotoEditor(EDIT_FILE_PATH)
    with pytest.raises(pillow.NoEditFileExpection):
        editor.edit_flip(True)


def test_edit_rotate():
    _clear_edit_file()
    editor = PhotoEditor(EDIT_FILE_PATH)
    editor.set_edit_image(pathlib.Path(TEST_FILE_PATH))
    editor.edit_rotate(90)
    _are_images_the_same(editor, IMAGES_PATH + 'test_img_left.jpg')


def test_edit_roatate_no_file():
    _clear_edit_file()
    editor = PhotoEditor(EDIT_FILE_PATH)
    with pytest.raises(pillow.NoEditFileExpection):
        editor.edit_flip(0)


def test_save_as_collage():
    editor = PhotoEditor(EDIT_FILE_PATH)
    images = [[
        pathlib.Path(IMAGES_PATH + 'test_img_vflip.jpg'),
        pathlib.Path(TEST_FILE_PATH)
    ]]
    editor.save_images_as_collage(images, 300, EDIT_FILE_PATH)
    _are_images_the_same(editor, IMAGES_PATH + 'test_collage.jpg')


def test_save_as_collage_empty():
    editor = PhotoEditor(EDIT_FILE_PATH)
    images = []
    with pytest.raises(pillow.EmptyGaleryExpection):
        editor.save_images_as_collage(images, 300, EDIT_FILE_PATH)
