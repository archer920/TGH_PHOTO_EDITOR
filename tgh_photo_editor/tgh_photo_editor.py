#!/usr/local/bin/python3

import os
import shutil
import subprocess
import tkinter
from enum import Enum, unique
from pathlib import Path
from tkinter import simpledialog
from tkinter.filedialog import askdirectory

from PIL import Image  # PIL Image: also in tkinter


@unique
class ImageTypes(Enum):
    GOLD = '-Gold.'
    SILVER = '-Silver.'
    BRONZE = '-Bronze.'


class GringoImage:
    def __init__(self, path: str) -> None:
        self.im = None
        self.path = path

    def open(self) -> None:
        self.im = Image.open(self.path)

    def is_square(self) -> bool:
        return self.im.size[0] == self.im.size[1]

    def scale_image(self, width: int = 400) -> None:
        required_width = width
        factor = required_width / self.im.size[0]

        w = int(self.im.size[0] * factor)
        h = int(self.im.size[1] * factor)
        self.im = self.im.resize((w, h))

    def square_image(self) -> None:
        self.open()

        if self.is_square():
            self.scale_image(200)
            self.save_image()
        else:
            cmd = ['open', self.path, '-a', 'Gimp.app']
            subprocess.run(cmd)

    def save_image(self) -> None:
        self.im.save(self.path)


def destination_file_name(source_file_name: str, topic: str) -> str:
    f_extension = source_file_name.split('.')[-1]
    f_name = source_file_name.split('.')[0]
    destination_name = f_name.replace(' ', '-') + topic + '.' + f_extension
    return destination_name


def square_file_name(source_file_name: str, topic: str, image_type: ImageTypes) -> str:
    extension = source_file_name.split('.')[1]
    source_file_name = source_file_name.split('.')[0]
    f_name = source_file_name.replace(' ', '-') + topic + '{}' + extension
    return f_name.format(image_type.value)


def scale_image(image_path: str) -> None:
    i = GringoImage(image_path)
    i.open()
    i.scale_image()
    i.save_image()


def handle_square_image(source_path: str, source_file: str,
                        destination_dir: str, topic_name: str, image_type: ImageTypes) -> str:
    destination_path: str = os.path.join(os.path.sep, destination_dir,
                                         square_file_name(source_file, topic_name, image_type))
    shutil.copyfile(source_path, destination_path)
    return destination_path


def main() -> None:
    tkinter.Tk()
    topic_name = simpledialog.askstring('Picture Editor', 'Enter topic name')
    topic_name = '-Best-' + topic_name.replace(' ', '-')

    input_dir = askdirectory(initialdir=Path.home())
    destination_dir: str = input_dir + '_edited'

    os.mkdir(destination_dir)

    editors_choice = False
    top3 = False
    best_value = False

    square_images = []

    for root, dirs, files in os.walk(input_dir):
        for f in files:
            if f == '.DS_Store':
                continue

            source_path = os.path.join(os.path.sep, root, f)
            destination_path = os.path.join(os.path.sep, destination_dir, destination_file_name(f, topic_name))

            shutil.copyfile(source_path, destination_path)
            scale_image(destination_path)

            if not editors_choice:
                is_editors_choice = simpledialog.askstring('Picture Editor', 'Is {} the Gold'.format(f))
                if is_editors_choice.lower() == 'y':
                    square_images.append(
                        handle_square_image(source_path, f, destination_dir, topic_name, ImageTypes.GOLD))
                    editors_choice = True
                    continue

            if not top3:
                is_top3 = simpledialog.askstring('Picture Editor', 'Is {} the Silver?'.format(f))
                if is_top3.lower() == 'y':
                    square_images.append(
                        handle_square_image(source_path, f, destination_dir, topic_name, ImageTypes.SILVER))
                    top3 = True
                    continue

            if not best_value:
                is_bv = simpledialog.askstring('Picture Editor', 'Is {} the Bronze?'.format(f))
                if is_bv.lower() == 'y':
                    square_images.append(
                        handle_square_image(source_path, f, destination_dir, topic_name, ImageTypes.BRONZE))
                    best_value = True
                    continue

    for i in square_images:
        gi = GringoImage(i)
        gi.square_image()


if __name__ == '__main__':
    main()
