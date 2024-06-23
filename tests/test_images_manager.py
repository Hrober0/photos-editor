from scripts.images_manager import ImagesManager
from scripts.progres_counter import ProgresCounter
from pathlib import Path


IMAGES_PATH = str(Path(__file__).parent.resolve())+'/test_management/'
IMAGE_EXTENSION = '.jpg'


def _cler_test_folder():
    path = Path(IMAGES_PATH)
    images = list(path.glob('*' + IMAGE_EXTENSION))
    for f in images:
        f.unlink()


def _create_path(name):
    return IMAGES_PATH + name + IMAGE_EXTENSION


def _create_bytes():
    return bytes('test', 'UTF-8')


def test_save_image():
    _cler_test_folder()
    im = ImagesManager(IMAGES_PATH, IMAGE_EXTENSION)
    im.save_image('t', _create_bytes(), False)
    path = Path(IMAGES_PATH)
    assert len(list(path.glob('*' + IMAGE_EXTENSION))) == 1
    with Path(_create_path('t')).open('rb') as f:
        byt = f.read()
    assert byt == _create_bytes()


def test_save_image_dupicated_name():
    _cler_test_folder()
    im = ImagesManager(IMAGES_PATH, IMAGE_EXTENSION)
    im.save_image('t', _create_bytes(), False)
    assert len(list(Path(IMAGES_PATH).glob('*' + IMAGE_EXTENSION))) == 1
    im.save_image('t', _create_bytes(), False)
    assert len(list(Path(IMAGES_PATH).glob('*' + IMAGE_EXTENSION))) == 1


def test_save_image_dupicated_name_create_new():
    _cler_test_folder()
    im = ImagesManager(IMAGES_PATH, IMAGE_EXTENSION)
    im.save_image('t', _create_bytes(), True)
    path = Path(IMAGES_PATH)
    assert len(list(path.glob('*' + IMAGE_EXTENSION))) == 1
    im.save_image('t', _create_bytes(), True)
    assert len(list(path.glob('*' + IMAGE_EXTENSION))) == 2


def test_save_images():
    _cler_test_folder()
    images = [
        ('a', _create_bytes()),
        ('d', _create_bytes()),
        ('c', _create_bytes())
    ]
    im = ImagesManager(IMAGES_PATH, IMAGE_EXTENSION)
    im.save_images(images, ProgresCounter(0, 100))
    assert len(list(Path(IMAGES_PATH).glob('*' + IMAGE_EXTENSION))) == 3


# test  get_images_from_directory and get_image_index
def test_get_images():
    test_input_list = [
        ('0[#]d', _create_bytes()),
        ('0[#]d', _create_bytes()),
        ('[#]d', _create_bytes()),
        ('a', _create_bytes()),
        ('a', _create_bytes()),
        ('a', _create_bytes()),
        ('a[#]a', _create_bytes()),
        ('[#]d', _create_bytes()),
        ('1[#]d2', _create_bytes()),
        ('10[#]d3', _create_bytes()),
        ('[#]b', _create_bytes()),
        ('[#]a', _create_bytes())
        ]
    test_output_list = [
        '0[#]d.jpg',
        '1[#]d1.jpg',
        '2[#]d2.jpg',
        '3[#]d3.jpg',
        '4[#][#]a.jpg',
        '5[#][#]b.jpg',
        '6[#][#]d.jpg',
        '7[#][#]d1.jpg',
        '8[#]a.jpg',
        '9[#]a1.jpg',
        '10[#]a2.jpg',
        '11[#]a[#]a.jpg'
        ]
    _cler_test_folder()
    im = ImagesManager(IMAGES_PATH, IMAGE_EXTENSION)
    im.save_images(test_input_list, ProgresCounter(0, 100))
    images_o = im.get_images_from_directory(ProgresCounter(0, 100))
    assert len(images_o) == len(test_output_list)
    for o, t in zip(images_o, test_output_list):
        assert o.name == t
    images_o = im.get_images_from_directory(ProgresCounter(0, 100))
    assert len(images_o) == len(test_output_list)
    for o, t in zip(images_o, test_output_list):
        assert o.name == t


def test_move_image_position():
    input = [
        ('0[#]a', _create_bytes()),
        ('1[#]b', _create_bytes()),
        ('2[#]c', _create_bytes()),
    ]
    output = [
        '0[#]a.jpg',
        '1[#]c.jpg',
        '2[#]b.jpg',
    ]
    _cler_test_folder()
    im = ImagesManager(IMAGES_PATH, IMAGE_EXTENSION)
    im.save_images(input, ProgresCounter(0, 100))
    im.move_image_position(1, 1, ProgresCounter(0, 100))
    images_o = im.get_images_from_directory(ProgresCounter(0, 100))
    assert len(images_o) == len(input)
    for o, t in zip(images_o, output):
        assert o.name == t


def test_move_image_position_neg():
    input = [
        ('0[#]a', _create_bytes()),
        ('1[#]b', _create_bytes()),
        ('2[#]c', _create_bytes()),
    ]
    output = [
        '0[#]b.jpg',
        '1[#]a.jpg',
        '2[#]c.jpg',
    ]
    _cler_test_folder()
    im = ImagesManager(IMAGES_PATH, IMAGE_EXTENSION)
    im.save_images(input, ProgresCounter(0, 100))
    im.move_image_position(1, -1, ProgresCounter(0, 100))
    images_o = im.get_images_from_directory(ProgresCounter(0, 100))
    assert len(images_o) == len(input)
    for o, t in zip(images_o, output):
        assert o.name == t


def test_delete_img_index():
    test_input_list = [
        ('0[#]d', _create_bytes()),
        ('0[#]d', _create_bytes()),
        ('[#]d', _create_bytes()),
        ('a', _create_bytes()),
        ('a', _create_bytes()),
        ('a', _create_bytes()),
        ('a[#]a', _create_bytes()),
        ('[#]d', _create_bytes()),
        ('1[#]d2', _create_bytes()),
        ('10[#]d3', _create_bytes()),
        ('[#]b', _create_bytes()),
        ('[#]a', _create_bytes())
        ]
    test_output_list = [
        '0[#]d.jpg',
        '1[#]d1.jpg',
        '2[#]d2.jpg',
        '3[#]d3.jpg',
        '4[#][#]a.jpg',
        '5[#][#]b.jpg',
        '6[#][#]d1.jpg',
        '7[#]a.jpg',
        '8[#]a1.jpg',
        '9[#]a2.jpg',
        '10[#]a[#]a.jpg'
        ]
    _cler_test_folder()
    im = ImagesManager(IMAGES_PATH, IMAGE_EXTENSION)
    im.save_images(test_input_list, ProgresCounter(0, 100))
    im.delate_image_on_index(6, ProgresCounter(0, 100))
    images_o = im.get_images_from_directory(ProgresCounter(0, 100))
    assert len(images_o) == len(test_output_list)
    for o, t in zip(images_o, test_output_list):
        assert o.name == t


def test_delete_all():
    input = [
        ('0[#]a', _create_bytes()),
        ('1[#]b', _create_bytes()),
        ('2[#]c', _create_bytes()),
    ]
    _cler_test_folder()
    im = ImagesManager(IMAGES_PATH, IMAGE_EXTENSION)
    im.save_images(input, ProgresCounter(0, 100))
    im.delete_all_images(ProgresCounter(0, 100))
    images_o = im.get_images_from_directory(ProgresCounter(0, 100))
    assert len(images_o) == 0


def test_format_img_name():
    im = ImagesManager(IMAGES_PATH, IMAGE_EXTENSION)
    assert im.format_image_name('0[#]test.jpg') == 'test'
    assert im.format_image_name('[#]test.jpg') == 'test'
    assert im.format_image_name('[#]0[#]test.jpg') == '0[#]test'
    assert im.format_image_name('a[#]test.jpg') == 'test'
    assert im.format_image_name('0[#]test') == 'test'
    assert im.format_image_name('test') == 'test'
    assert im.format_image_name('test.jpg') == 'test'
    assert im.format_image_name('test.ww.jpg') == 'test.ww'
