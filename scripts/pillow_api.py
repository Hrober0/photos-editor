import pathlib
from typing import Tuple
from PIL import Image, ImageFilter


class NoEditFileExpection(Exception):
    """Exception raises when image file to edit not exist"""
    def __init__(self) -> None:
        super().__init__("No edit file")


class EmptyGaleryExpection(Exception):
    """Exception raised when iterating through empty list images"""
    def __init__(self) -> None:
        super().__init__("galery is empty")


class PhotoEditor:
    """Class is use to applay effect on images.
    Images is store as a file in given path"""

    def __init__(self, edit_file_path: str) -> None:
        """Sets basic values.

        Args:
            edit_file_path: path with the file name and file extension
            on which the image manipulations will be performed
        """
        self._edit_file_path = edit_file_path
        self._edit_file_name = 'none'

    def set_edit_image(self, image: pathlib.Path):
        """Set images as image to apply efectson.
        Image of given path will be copy to editor directory.
        Also sets _edit_file_name as image name without

        Args:
            image: path of image to copy
        """

        with image.open('rb') as f:
            image_bytes = f.read()
        with open(self._edit_file_path, 'wb') as f:
            f.write(image_bytes)
        self._edit_file_name = image.stem

    def get_edit_image_bytes(self) -> bytes:
        """Returns bytes of images at edit path.

        Raises:
            NoEditFileExpection: image file to edit not exist

        Returns:
            bytes of edited images
        """

        try:
            with pathlib.Path(self._edit_file_path).open('rb') as f:
                image_bytes = f.read()
        except Exception:
            raise NoEditFileExpection()
        return image_bytes

    @property
    def edit_file_name(self) -> str:
        return self._edit_file_name

    def _get_edit_image(self) -> Image:
        """Read edit image file as pillow image."""
        try:
            img = Image.open(self._edit_file_path)
        except Exception:
            raise NoEditFileExpection()
        return img

    def _save_edit_image(self, image: Image) -> None:
        """Save pillow image as file in edit path."""
        image.save(self._edit_file_path)

    def edit_rotate(self, angle: int) -> None:
        """Applay rotation of given angle on edited file
        angle < 0 rotate in left"""
        image = self._get_edit_image()
        image = image.rotate(angle, expand=True)
        self._save_edit_image(image)

    def edit_flip(self, horizontal: bool) -> None:
        """Applay reversal in horizontal or vertical axies on edited file"""
        image = self._get_edit_image()
        if horizontal:
            image = image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        else:
            image = image.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
        self._save_edit_image(image)

    def edit_blur(self) -> None:
        """Applay blur on edited file"""
        image = self._get_edit_image()
        image = image.filter(ImageFilter.BLUR)
        self._save_edit_image(image)

    def save_images_as_collage(
            self,
            images_rows: pathlib.Path,
            single_image_height: int,
            save_path: str
            ) -> None:
        """Create one image with all images from the given list,
        keeps images order in rows and columns.

        Args:
            images_rows: list of rows with images
            single_image_height: number of pixeles with each row will be save
            save_path: path with file name and extension
            where file will be save

        Raises:
            EmptyGaleryExpection: when image_rows list is empty
        """

        if images_rows is None or len(images_rows) == 0:
            raise EmptyGaleryExpection()

        # calculate total size
        total_height = single_image_height * len(images_rows)
        row_widths = []
        for row in images_rows:
            row_width = 0
            for img_path in row:
                img = Image.open(img_path)
                new_size = self._format_img_size(img.size, single_image_height)
                row_width += new_size[0]
            row_widths.append(row_width)
        total_width = max(row_widths)

        # crete main image
        bg_color = (51, 62, 73)
        main_image = Image.new('RGB', (total_width, total_height), bg_color)

        # paste single image
        paste_y = 0
        for row_index, row in enumerate(images_rows):
            paste_x = int((total_width - row_widths[row_index]) / 2)
            for img_path in row:
                img = Image.open(img_path)
                size = self._format_img_size(img.size, single_image_height)
                img = img.resize(size)
                main_image.paste(img, (paste_x, paste_y))
                paste_x += size[0]
            paste_y += single_image_height

        # save
        main_image.save(save_path, 'JPEG')

    def _format_img_size(
            self,
            size: Tuple[int, int],
            target_height: int
            ) -> Tuple[int, int]:
        """resize tuple with (width, hight) to target_height
        keeps width to height ratio"""

        scale_factor = target_height / size[1]
        width = int(size[0] * scale_factor)
        return (width, target_height)
