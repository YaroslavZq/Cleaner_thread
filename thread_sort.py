import os
from pathlib import Path
import shutil
from threading import Thread
from time import time


IMAGES = ('JPEG', 'PNG', 'JPG', 'SVG')
VIDEO = ('AVI', 'MP4', 'MOV', 'MKV')
DOCS = ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX')
MUSIC = ('MP3', 'OGG', 'WAV', 'AMR')
ARCHIVES = ('ZIP', 'GZ', 'TAR')

ALL = ('JPEG', 'PNG', 'JPG', 'SVG', 'AVI', 'MP4', 'MOV', 'MKV',
       'DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX', 'MP3',
       'OGG', 'WAV', 'AMR', 'ZIP', 'GZ', 'TAR')


def find_images() -> list:
    files = os.listdir(path)
    type_img = (list(
        filter(lambda x: any(
            filter(lambda y: x.lower().endswith(y.lower()),
                   IMAGES)
        ), files)
    ))
    return type_img


def find_video() -> list:
    files = os.listdir(path)
    type_video = (list(
        filter(lambda x: any(
            filter(lambda y: x.lower().endswith(y.lower()),
                   VIDEO)
        ), files)
    ))
    return type_video


def find_docs() -> list:
    files = os.listdir(path)
    type_docs = (list(
        filter(lambda x: any(
            filter(lambda y: x.lower().endswith(y.lower()),
                   DOCS)
        ), files)
    ))
    return type_docs


def find_music() -> list:
    files = os.listdir(path)
    type_mus = (list(
        filter(lambda x: any(
            filter(lambda y: x.lower().endswith(y.lower()),
                   MUSIC)
        ), files)
    ))
    return type_mus


def find_archives() -> list:
    files = os.listdir(path)
    type_arch = (list(
        filter(lambda x: any(
            filter(lambda y: x.lower().endswith(y.lower()),
                   ARCHIVES)
        ), files)
    ))
    return type_arch


def del_empty_dirs(path: str) -> None:
    for dirs in os.listdir(path):
        new_directory = os.path.join(path, dirs)
        if os.path.isdir(new_directory):
            del_empty_dirs(new_directory)
            if not os.listdir(new_directory):
                os.rmdir(new_directory)


def deep_into_dir():
    for el in os.listdir(path):
        address = os.path.join(path, el)
        if os.path.isdir(address):
            files_in_dir = os.listdir(address)
            for file in files_in_dir:
                shutil.move(os.path.join(address, file), path)
                del_empty_dirs(path)
            if not os.path.isdir(path):
                break
            else:
                deep_into_dir()


def transfer_files(folder_name: str, files: list) -> None:
    if folder_name not in path:
        os.chdir(path)
        os.mkdir(folder_name)
    if folder_name == 'archives':
        to_unpack_folder = os.path.join(path, folder_name)
        os.chdir(to_unpack_folder)
        for arch_name in files:
            named = arch_name.split('.')
            name = named[0]
            os.mkdir(name)
            path_to_unpack = os.path.join(to_unpack_folder, name)
            file_for_unpack = os.path.join(path, arch_name)
            try:
                shutil.unpack_archive(file_for_unpack, path_to_unpack)
                os.remove(file_for_unpack)
            except shutil.ReadError:
                error_name = os.path.split(file_for_unpack)
                del_empty_dirs(os.path.join(path, 'archives'))
                print(f'File {error_name[-1]} isn`t archive.')
    if folder_name != 'archives':
        file_destination = os.path.join(path, folder_name)
        get_files = files
        for files in get_files:
            shutil.move(os.path.join(path, files), file_destination)


def relocate():
    t1 = Thread(target=transfer_files, args=('images', find_images()))
    t2 = Thread(target=transfer_files, args=('music', find_music()))
    t3 = Thread(target=transfer_files, args=('video', find_video()))
    t4 = Thread(target=transfer_files, args=('documents', find_docs()))
    t5 = Thread(target=transfer_files, args=('archives', find_archives()))

    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()

    t1.join()
    t2.join()
    t3.join()
    t4.join()
    t5.join()


def main():
    deep_into_dir()
    relocate()


if __name__ == '__main__':
    path = input("Input path to folder:")
    start = time()
    if os.path.exists(path) and Path(path).is_dir():
        main()
    else:
        print('Wrong way to folder')
    print(f"{time()-start}")
