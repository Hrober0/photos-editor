import pathlib
from typing import List, Tuple
from scripts.progres_counter import ProgresCounter


class ImagesManager:
    """class is used to manipulate images in a directory"""

    def __init__(
            self,
            images_path: str,
            images_extension: str
            ) -> None:
        """Sets basic class values.

        Args:
            images_path: folder where images are store
            images_extension: extension of images that will be using
        """

        self._images_path = images_path
        self._images_extension = images_extension
        self._FILE_PREFIX_SEPARATOR = '[#]'

    def get_images_from_directory(
            self,
            task_progres: ProgresCounter
            ) -> List[pathlib.Path]:
        """Load images from the images directory.
        It also formats all images names by adding prefix witf image index
        to keep proper order.

        Args:
            task_progres: class to track task progress

        Returns:
            list of all images from the images directory
        """

        task_progres.set_new_task('loading images', 5)

        # get all images from directory
        path = pathlib.Path(self._images_path)
        images = list(path.glob('*'+self._images_extension))
        images.sort(key=lambda img: img.name)
        task_progres.complate_subtask()

        # select unordered images
        ordered_images = []
        unordered_images = []
        for image in images:
            if self.get_image_index(image.name) >= 0:
                ordered_images.append(image)
            else:
                unordered_images.append(image)
        task_progres.complate_subtask()

        # reorder ordered images
        index = 0
        ordered_images.sort(key=lambda img: self.get_image_index(img.name))
        for index in range(len(ordered_images)):
            image = ordered_images[index]
            name = self._trim_image_index(image.name)
            name = self._add_image_index(name, index)
            ordered_images[index] = self._rename_image(image, name)
        task_progres.complate_subtask()

        # name unordered images
        for image in unordered_images:
            index = len(ordered_images)
            new_name = self._add_image_index(image.name, index)
            image = self._rename_image(image, new_name)
            ordered_images.append(image)
        task_progres.complate_subtask()

        # sort images
        task_progres.complate_task()
        return ordered_images

    def save_images(
            self,
            images: List[Tuple[str, bytes]],
            task_progres: ProgresCounter
            ) -> None:
        """Save given images in the images directory

        Args:
            images: list of images to save,
            tuple contains name of image and image data as bytes
            task_progres: class to track task progress
        """

        task_progres.set_new_task('saving images', len(images))
        for image in images:
            self.save_image(image[0], image[1], True)
            task_progres.complate_subtask()
        task_progres.complate_task()

    def save_image(
            self,
            image_name: str,
            image: bytes,
            create_new: bool
            ) -> None:
        """save image in images directory.

        Args:
            image_name: image with file will be save
            image: bytes of image
            create_new: if it is true and image of this name already
            exist in directory then file will be creqted with unique sufix
        """

        generic_path = self._images_path+image_name+'{}'+self._images_extension
        if create_new:
            # if an other image with the same name already exist
            # add a suffix to image
            dupicates = 0
            while True:
                path = generic_path.format('' if dupicates == 0 else dupicates)
                if not pathlib.Path(path).is_file():
                    break
                dupicates += 1
        else:
            path = generic_path.format('')
        with open(path, 'wb') as image_file:
            image_file.write(image)

    def delete_all_images(
            self,
            task_progres: ProgresCounter
            ) -> None:
        """delete all images files from images directory

        Args:
            task_progres: class to track task progress
        """

        images = self.get_images_from_directory(task_progres)
        task_progres.set_new_task('deleteing images', len(images))
        for f in images:
            f.unlink()
            task_progres.complate_subtask()
        images = None
        task_progres.complate_task()

    def delate_image_on_index(
            self,
            index: int,
            task_progres: ProgresCounter
            ) -> None:
        """delete image file of given index from images directory

        Args:
            index: index in list of images from images directory
            task_progres: class to track task progress
        """

        images = self.get_images_from_directory(task_progres)
        task_progres.set_new_task(f'deleteing image {index}', 1)
        image = images[index]
        image.unlink()
        task_progres.complate_task()

    def format_image_name(self, image_name: str) -> str:
        """remove image extension and order prefix from name

        Args:
            image: image name

        Returns:
            formated name
        """

        name = image_name.rstrip(self._images_extension)
        name = self._trim_image_index(name)
        return name

    def move_image_position(
            self,
            index: int,
            shift: int,
            task_progres: ProgresCounter
            ) -> None:
        """Image position move by swap images poaition of given index
        with other image. Image file of given index and other image
        will be renamed, because position are defined by files sufix.

        Args:
            index: index of image to move
            shift: number of indexs to change
            task_progres: class to track task progress
        """

        images = self.get_images_from_directory(task_progres)
        task_progres.set_new_task(f'move images {index} shift: {shift}', 2)

        # calculate index of image to swap place with
        target_index = index + shift
        target_index = self._clamp(target_index, 0, len(images)-1)
        if index != target_index:
            f_image = images[index]
            s_image = images[target_index]
            # rename first image to temp name to avoid conflicts
            f_image = self._rename_image(f_image, '_tmp' + f_image.name)
            # rename second image to change index
            name = self._trim_image_index(s_image.name)
            name = self._add_image_index(name, index)
            self._rename_image(s_image, name)
            # rename first image to change index
            name = self._trim_image_index(f_image.name)
            name = self._add_image_index(name, target_index)
            self._rename_image(f_image, name)
            task_progres.complate_subtask()
        task_progres.complate_task()

    def get_image_index(self, name: str) -> int:
        """read image index from image name

        Args:
            name: image name

        Returns:
            if name contains correct sufix returns image index as int
            else return -1
        """

        if self._FILE_PREFIX_SEPARATOR not in name:
            return -1
        spearatr_index = name.find(self._FILE_PREFIX_SEPARATOR)
        indexstr = name[:spearatr_index]
        try:
            return int(indexstr)
        except (Exception):
            return -1

    def _rename_image(self, image: pathlib.Path, name: str) -> pathlib.Path:
        """Change name of  image file

        Args:
            image: path to image with extension
            name: name to set

        Returns:
            path of renamed image
        """

        full = f'{image.parent}/{name}'
        return image.rename(full)

    def _trim_image_index(self, name: str) -> str:
        """remove suffix that allows to read image index from its name

        Args:
            name: image name

        Returns:
            image name without sufix
        """

        if self._FILE_PREFIX_SEPARATOR in name:
            spearatr_index = name.find(self._FILE_PREFIX_SEPARATOR)
            spearatr_index += len(self._FILE_PREFIX_SEPARATOR)
            name = name[spearatr_index:]
        return name

    def _add_image_index(self, name: str, index: int) -> str:
        """add suffix that allows to read image index to its name

        Args:
            name: image name
            index: number as index

        Returns:
            name with index sufix
        """
        return f'{index}{self._FILE_PREFIX_SEPARATOR}{name}'

    def _clamp(self, val: int, min: int, max: int) -> int:
        """keep value bettwen minimum and maximum values"""
        return min if val < min else max if val > max else val
