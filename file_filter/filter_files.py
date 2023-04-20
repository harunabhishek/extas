#!/usr/bin/env python3

# Filters the files from folders and also delete files with particular type within a folder and subfolders.

import os
from os.path import isdir, isfile, join
# import shutil

class DirectoryManager:
    def __init__(self):
        self.user_path = ""
        self.mode = ""
        self.filetype = ""
        self.check_remove = ""
        self.remover_mode = ""
        self.remove_dir = ""
        self.remove_file = ""
        self.check_crawl = ""
        self.user_requirements()

    def user_requirements(self):
        # Asks for requires parameters and mode of choice
        print("enter the path, enter nothing for default path(current working directory) ")
        while True:
            # verifies user path 
            self.user_path = input("")
            if self.user_path:
                if not os.path.exists(self.user_path):
                    print("path doesn't exist, try again")
                    continue
                else:
                    break
            else:
                self.user_path = os.getcwd()
                break

        print("select mode\n1)seprate all files\n2)seprate files with extension\n3)remove file and directories")
        while True:
            # Asks for mode to choose
            self.mode = input("")
            if self.mode == "1":
                self.check_remove = input("do you want to remove seprated files from the parent directory, enter[y/n]")
                print("seprated files will be stored in that particular directory named /*seprated_files")
                break
            elif self.mode == "2":
                self.filetype = input("enter the filetype, i.e txt, jpg ")
                self.check_remove = input("do you want to remove " + self.filetype + " from parent directory, enter[y/n]")
                print("seprated files will be stored in that particular directory named /*_" + self.filetype + "-files")
                break
            elif self.mode == "3":
                print("1)remove directories\n2)remove files")
                self.remover_mode = input("")
                if self.remover_mode == "1":
                    self.remove_dir = input("directory name ")
                elif self.remover_mode == "2":
                    self.remove_file = input("filetype ")
                break
            else:
                print("Invalid mode, try again")
                continue
        self.check_crawl = input("Do you want to apply to subdirectories as well [y/n]")
        print("\nChossen Options:")
        print(self.user_path, self.mode, self.filetype, self.check_remove, self.remover_mode, self.remove_dir, self.remove_file)
        assure = input("\nAre you sure you want to continue [y/n]")
        if not assure == "y":
            print("Exitting ..........")
            exit()


    def copy_file(self, source_path, dest_path):
        # Copy files from sourde to destination
        with open(source_path, "rb") as source_file:
            with open(dest_path, "wb") as destination_file:
                destination_file.write(source_file.read())


    def remove_directories(self, path):
        # Removes a directory
        dirs_files_list = os.listdir(path)

        for dir_file in dirs_files_list:
            dir_file_path = join(path, dir_file)

            if isfile(dir_file_path):
                os.remove(dir_file_path)
            elif isdir(dir_file_path):
                self.remove_directories(dir_file_path)
                os.rmdir(dir_file_path)


    def crawl_dirs(self, path=None):
        # Crawls the directory within directories and apply operation accordingly
        if path is None:
            path = self.user_path

        dirs_files_list = os.listdir(path)                                                            #gets the all the directories within a directory
        # print(path, dirs_files_list)
        temp_files_list = []
        temp_dirs_list = []
        new_files_path = ""

        for dir_file in dirs_files_list:
            dir_file_path = join(path, dir_file)                                                       #joins the original path and searched directory

            if isfile(dir_file_path):
                temp_files_list.append(dir_file)

                if self.mode == "1":
                    # seprates files from directories                                                                
                    if not new_files_path:
                        new_files_path = join(path, "seprated-files")
                        os.mkdir(new_files_path)
                    self.copy_file(dir_file_path, join(new_files_path, dir_file))
                    if self.check_remove == "y":
                        os.remove(dir_file_path)

                elif self.mode == "2":
                    # seprates files of particular type
                    if dir_file.endswith("." + self.filetype): 
                        if not new_files_path:
                            new_files_path = join(path, self.filetype + "-files")
                            os.mkdir(new_files_path)
                        self.copy_file(dir_file_path, join(new_files_path, dir_file))
                        if self.check_remove == "y":
                            os.remove(dir_file_path)

                elif self.mode == "3":
                    # removes particular files 
                    if self.remover_mode == "2":
                        if dir_file.endswith(self.remove_file):
                        # if self.remove_file in dir_file:
                            os.remove(dir_file_path)

            elif isdir(dir_file_path):
                temp_dirs_list.append(dir_file)

                if self.mode == "3":
                    # removes particular type of directories
                    if self.remover_mode == "1":
                        if dir_file.endswith(self.remove_dir):
                        # if self.remove_dir in dir_file:
                            self.remove_directories(dir_file_path)
                            os.rmdir(dir_file_path)
                            print("Removed" + dir_file_path)
                            continue

                if self.check_crawl == "y":
                    self.crawl_dirs(dir_file_path)                                                      #recursively call itself to appy to subdirectories as well
        if self.mode == "1" or self.mode == "2" and new_files_path != "":
            print("seprated in ", path)
        # print(path, temp_dirs_list, temp_files_list)


# main code
try:
    file_manage = DirectoryManager()
    file_manage.crawl_dirs()
except KeyboardInterrupt:
    print("[+] Ctrl + C detected ...........Exitting")


