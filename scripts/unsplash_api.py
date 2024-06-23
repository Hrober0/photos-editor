import requests
from typing import List, Tuple
from typing import Dict
from scripts.progres_counter import ProgresCounter


class IncorrectPageResultExpection(Exception):
    def __init__(self) -> None:
        super().__init__('Incorrect page result')


class IncorrectQueryExpection(Exception):
    def __init__(self) -> None:
        super().__init__('Incorrect query')


class IncorrectResolutionExpection(Exception):
    def __init__(self) -> None:
        super().__init__('Incorrect resolution')


class NoImageResolutionExpection(Exception):
    pass


def _get_url(
        query: str,
        images_amount: int,
        page: int
        ) -> str:
    """prepear url to recive image from unsplash.com

    Args:
        query: subject of the image
        images_amount: target number of images to search
        page: number of page with images

    Raises:
        IncorrectQueryExpection:
        - when query is none or empty
        - when images_amount < 0
        - when page < 1

    Returns:
        formated url
    """

    if query is None or query == '' or images_amount < 0 or page < 1:
        raise IncorrectQueryExpection()

    api_url = 'https://unsplash.com/napi/search/photos?'
    api_url += f'query={query}'
    api_url += f'&per_page={images_amount}'
    api_url += f'&page={page}'
    return api_url


def get_resolutions() -> List[str]:
    """
    Returns:
        list of all supported resolutions
    """

    return [
        'small',
        'regular',
        'full',
        'raw'
    ]


def _download_image(
        image: Dict[str, str],
        resolution: str,
        alternative_name: str
        ) -> Tuple[str, bytes]:
    """download image from url and returns image bytes and title

    Args:
        image: unsplash image JSON
        resolution: resolution of image
        alternative_name: title that will be use when image not have own title

    Raises:
        NoImageResolutionExpection: image doesn't contain given resolution

    Returns:
        images tumples (title, data bytes)
    """

    image_title = image['alt_description']
    if image_title is None:
        image_title = image['description']
    if image_title is None:
        image_title = alternative_name
    urls = image['urls']
    if resolution not in urls:
        raise NoImageResolutionExpection()
    image_url = urls[resolution]
    image_result = requests.get(image_url)
    return (image_title, image_result.content)


def search_images(
        query: str,
        images_amount: int,
        resolution: str,
        task_progres: ProgresCounter
        ) -> List[Tuple[str, bytes]]:
    """Request images from unsplash.com and return them as list

    Args:
        query: subject of the image
        images_amount: target number of images to search
        resolution: resolution of image
        task_progres: class to track task progress

    Raises:
        IncorrectQueryExpection: query is none or empty
        IncorrectResolutionExpection: given resolution is not supported
        IncorrectPageResultExpection: result from page is no a json

    Returns:
        list of images tumples (title, data bytes)
    """

    task_progres.set_new_task('seraching for ' + str(query), images_amount)

    if resolution not in get_resolutions():
        raise IncorrectResolutionExpection()

    page_url = _get_url(query, images_amount, 1)
    page_result = requests.get(page_url)

    try:
        json_data = page_result.json()
        images = json_data['results']
    except Exception:
        raise IncorrectPageResultExpection()

    output = []
    for image_json in images:
        try:
            image_data = _download_image(image_json, resolution, query)
        except NoImageResolutionExpection:
            continue
        output.append(image_data)
        images_amount -= 1
        task_progres.complate_subtask()
        if images_amount <= 0:
            break

    task_progres.complate_task()
    return output
