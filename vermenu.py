import customtkinter
import os
from PIL import Image
import json
from CTkScrollableDropdown import *
import minecraft_launcher_lib
import subprocess
import requests
import psutil,threading




class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_images")
        self.logo_ico = os.path.join(image_path, "logo.ico")
        self.version= "1.20.6"
        self.memory_select =0
        self.iconbitmap(self.logo_ico)
        self.title("CatLauncher")
        self.geometry("800x450")
        self.resizable(False, False)
        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)


        # load images with light and dark mode image
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "logo.png")), size=(26, 26))
        self.image_icon_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "image_icon_light.png")), size=(20, 20))
        self.home_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "minecraft_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "minecraft_light.png")), size=(20, 20))
        self.anvil_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "forge_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "forge_light.png")), size=(30, 25))
        self.add_user_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "custom_dark.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "custom_light.png")), size=(20, 20))
        self.settings_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "gear_dark.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "gear_light.png")), size=(20, 20))

        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(5, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="  CatLauncher", image=self.logo_image,
                                                             compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Vanila",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=self.home_image, anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.frame_2_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Forge",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.anvil_image, anchor="w", command=self.frame_2_button_event)
        self.frame_2_button.grid(row=2, column=0, sticky="ew")
        self.frame_4_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Settings",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.settings_image, anchor="w", command=self.frame_4_button_event)
        self.frame_4_button.grid(row=4, column=0, sticky="ew")

        self.frame_3_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Custom Modpacks",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.add_user_image, anchor="w", command=self.frame_3_button_event)
        self.frame_3_button.grid(row=3, column=0, sticky="ew")

        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame, values=["Dark","Light","System"],
                                                                command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")

        # create home frame
        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)
        self.empty = customtkinter.CTkLabel(self.home_frame,text="")
        self.empty.grid(row=4, column=0, padx=10, pady=140, sticky="ws")
        self.entry_minecraft_directory = customtkinter.CTkEntry(self.home_frame,placeholder_text=".CatLauncher",width=120,height=25,border_width=2,corner_radius=10)
        self.entry_minecraft_directory.grid(row=3, column=0, padx=10, pady=10, sticky="ws")
        self.entry_name = customtkinter.CTkEntry(self.home_frame,placeholder_text="Ник",width=120,height=25,border_width=2,corner_radius=10)
        self.entry_name.grid(row=5, column=0, padx=10, pady=2.5, sticky="ws")
        self.button_play = customtkinter.CTkButton(self.home_frame,width=120,height=32,border_width=0,corner_radius=8,text="Play",command=self.play_minecraft)
        self.button_play.grid(row=6, column=2, padx=10, pady=10, sticky="ws")
        self.versions = []
        with open(f"{os.path.realpath(__file__)[:-11]}\\version_manifest.json", 'r', encoding="utf-8") as fin:
            data = json.load(fin)
            tmp_id =""
            for section,dat in data.items():
                if section != "latest":
                    for dataset in dat:
                        for loop_one,loop_two in dataset.items():
                            if loop_one == "type":
                                if loop_two != "snapshot":
                                    self.versions.append(tmp_id)
                            if loop_one == "id":
                                tmp_id = loop_two
        self.menu_version_selection = customtkinter.CTkOptionMenu(self.home_frame,values=self.versions,command=self.selection_version)
        self.menu_version_selection.grid(row=6, column=0, padx=10, pady=10, sticky="ws")
        CTkScrollableDropdown(self.menu_version_selection,values=self.versions,command=self.selection_version)
        self.progressbar1 = customtkinter.CTkProgressBar(self.home_frame, orientation="horizontal")
        self.progressbar1.grid(row=6,column=1, padx=0, pady=0)
        self.progressbar1.set(0)
        

        # create second frame
        self.second_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.second_frame.grid_columnconfigure(0, weight=1)
        self.empty = customtkinter.CTkLabel(self.second_frame,text="")
        self.empty.grid(row=4, column=0, padx=10, pady=140, sticky="ws")
        self.entry_minecraft_directory2 = customtkinter.CTkEntry(self.second_frame,placeholder_text=".CatLauncher",width=120,height=25,border_width=2,corner_radius=10)
        self.entry_minecraft_directory2.grid(row=3, column=0, padx=10, pady=10, sticky="ws")
        self.entry_name2 = customtkinter.CTkEntry(self.second_frame,placeholder_text="Ник",width=120,height=25,border_width=2,corner_radius=10)
        self.entry_name2.grid(row=5, column=0, padx=10, pady=2.5, sticky="ws")
        self.button_play2 = customtkinter.CTkButton(self.second_frame,width=120,height=32,border_width=0,corner_radius=8,text="Play",command=self.play_minecraft2)
        self.button_play2.grid(row=6, column=2, padx=10, pady=10, sticky="ws")
        self.versions = []
        with open(f"{os.path.realpath(__file__)[:-11]}\\version_manifest.json", 'r', encoding="utf-8") as fin:
            data = json.load(fin)
            tmp_id =""
            self.forge_versions = []
            for section,dat in data.items():
                if section != "latest":
                    for dataset in dat:
                        for loop_one,loop_two in dataset.items():
                            if loop_one == "type":
                                if loop_two != "snapshot":
                                    forge_version =minecraft_launcher_lib.forge.find_forge_version(tmp_id)
                                    if forge_version is not None:
                                        self.forge_versions.append(forge_version)
                            if loop_one == "id":
                                tmp_id = loop_two
        self.menu_version_selection2 = customtkinter.CTkOptionMenu(self.second_frame,values=self.forge_versions,command=self.selection_version)
        self.menu_version_selection2.grid(row=6, column=0, padx=10, pady=10, sticky="ws")
        CTkScrollableDropdown(self.menu_version_selection2,values=self.forge_versions,command=self.selection_version)
        self.progressbar2 = customtkinter.CTkProgressBar(self.second_frame, orientation="horizontal")
        self.progressbar2.grid(row=6,column=1, padx=0, pady=0)
        self.progressbar2.set(0)

        # create third frame
        self.third_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.third_frame.grid_columnconfigure(0, weight=1)
        self.empty = customtkinter.CTkLabel(self.third_frame,text="")
        self.empty.grid(row=4, column=0, padx=10, pady=140, sticky="ws")
        self.entry_minecraft_directory3 = customtkinter.CTkEntry(self.third_frame,placeholder_text=".CatLauncher",width=120,height=25,border_width=2,corner_radius=10)
        self.entry_minecraft_directory3.grid(row=3, column=0, padx=10, pady=10, sticky="ws")
        self.entry_name3 = customtkinter.CTkEntry(self.third_frame,placeholder_text="Ник",width=120,height=25,border_width=2,corner_radius=10)
        self.entry_name3.grid(row=5, column=0, padx=10, pady=2.5, sticky="ws")
        self.button_play3 = customtkinter.CTkButton(self.third_frame,width=120,height=32,border_width=0,corner_radius=8,text="Play",command=self.play_minecraft3)
        self.button_play3.grid(row=6, column=2, padx=10, pady=10, sticky="ws")
        self.progressbar3 = customtkinter.CTkProgressBar(self.third_frame, orientation="horizontal")
        self.progressbar3.grid(row=6,column=1, padx=0, pady=0)
        self.versions = []
        self.max_value = [0]
        self.current_max = 0
        self.callback = {
            "setProgress": lambda value: self.printProgressBar(value, self.max_value[0]),
            "setMax": lambda value: self.maximum(self.max_value, value)
        }
        with open(f"{os.path.realpath(__file__)[:-11]}\\save.txt","r",encoding="utf-8") as f:
            mine_dir=f.readline()
            self.minecraft_directory = mine_dir
            mine_dir=mine_dir.rstrip("\n")
            self.entry_minecraft_directory.insert(0,mine_dir)
            self.entry_minecraft_directory2.insert(0,mine_dir)
            self.entry_minecraft_directory3.insert(0,mine_dir)
            if self.minecraft_directory == " ":
                self.minecraft_directory = ".CatLauncher"
            name= f.readline()
            name=name.rstrip("\n")
            self.entry_name.insert(0,name)
            self.entry_name2.insert(0,name)
            self.entry_name3.insert(0,name)
            self.memory_select = f.readline()
        try:
            self.modpacks = [name for name in os.listdir(f"{self.entry_minecraft_directory3.get()}\\customs") if os.path.isdir(os.path.join(f"{self.entry_minecraft_directory3.get()}\\customs", name))]
            for modpack in self.modpacks:
                self.modpack_version = [name for name in os.listdir(f"{self.entry_minecraft_directory3.get()}\\customs\\{modpack}") if os.path.isdir(os.path.join(f"{self.entry_minecraft_directory3.get()}\\customs\\{modpack}", name))]
        except:
            print("Not found customs!")
            self.modpacks = []
        self.menu_version_selection3 = customtkinter.CTkOptionMenu(self.third_frame,values=self.modpacks,command=self.selection_version)
        self.menu_version_selection3.grid(row=6, column=0, padx=10, pady=10, sticky="ws")
        CTkScrollableDropdown(self.menu_version_selection3,values=self.modpacks,command=self.selection_version)
        
        
        
        self.settings_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.settings_frame.grid_columnconfigure(0, weight=1)
        self.memory_slider = customtkinter.CTkSlider(self.settings_frame, from_=0, to=(psutil.virtual_memory().total//1024)//1024//1024, command=self.slider_event)
        self.memory_slider.grid(row=6, column=0, padx=10, pady=10, sticky="ws")
        self.memory_label = customtkinter.CTkLabel(self.settings_frame,text="Memory: 4G")
        self.memory_label.grid(row=6, column=0, padx=210, pady=15, sticky="ws")
        
         
        # select default frame
        self.select_frame_by_name("home")
        self.progressbar3.set(0)
        self.percent = 0
        if self.memory_select ==0 or self.memory_select == "":
            self.memory_select= 4
            self.memory_slider.set(4)
        else:
            self.memory_label.configure(text=f"Memory: {self.memory_select}G")
            self.memory_slider.set(int(self.memory_select))
            print(self.memory_select)

    def maximum(self,max_value, value):
        max_value[0] = value
    def printProgressBar(self,iteration, total, decimals=1):
        self.percent = iteration / float(total)
        self.progressbar1.set(self.percent)
        self.progressbar2.set(self.percent)
        self.progressbar3.set(self.percent)
        if self.percent >= 1:
            self.progressbar1.set(0)
            self.progressbar2.set(0)
            self.progressbar3.set(0)
    def slider_event(self,value):
        print(value)
        self.memory_label.configure(text=f"Memory: {round(value)}G")
        self.memory_select = round(value)
            
   
    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.frame_2_button.configure(fg_color=("gray75", "gray25") if name == "frame_2" else "transparent")
        self.frame_3_button.configure(fg_color=("gray75", "gray25") if name == "frame_3" else "transparent")
        self.frame_4_button.configure(fg_color=("gray75", "gray25") if name == "frame_4" else "transparent")

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "frame_2":
            self.second_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.second_frame.grid_forget()
        if name == "frame_3":
            self.third_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.third_frame.grid_forget()
        if name == "frame_4":
            self.settings_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.settings_frame.grid_forget()

    def home_button_event(self):
        self.select_frame_by_name("home")
        self.version= "1.20.6"
        self.menu_version_selection.set("1.20.6")
    def frame_2_button_event(self):
        self.select_frame_by_name("frame_2")
        self.version= "1.20.6-50.0.31"
        self.menu_version_selection2.set("1.20.6-50.0.31")

    def frame_3_button_event(self):
        self.select_frame_by_name("frame_3")
        self.menu_version_selection3.set(self.modpacks[0])
        self.version = self.modpacks[0]
    def frame_4_button_event(self):
        self.select_frame_by_name("frame_4")
    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)
    def selection_version(self,new_version):
        self.version = new_version
        self.menu_version_selection.set(new_version)
        self.menu_version_selection2.set(new_version)
        self.menu_version_selection3.set(new_version)
    def play_minecraft(self):
        try:
            minecraft=threading.Thread(target=self.async_play_minecraft)
            minecraft.start()
            print("successfully")
            return
        except RuntimeError:
            return 
    def async_play_minecraft(self):
        try:
            url = f'https://api.mojang.com/users/profiles/minecraft/{self.entry_name.get()}?'
            response = requests.get(url)
            uuid = response.json()['id']
            url = f'http://skinsystem.ely.by/textures/{self.entry_name.get()}'
            response = requests.get(url)
            skin = response.json()['SKIN']["url"]
            try:
                alias = response.json()["SKIN"]["metadata"]
            except:
                alias = "STEVE"
            options={
                "username" : self.entry_name.get(),
                "uuid": uuid,
                "token": "",
                "launcherName": "CatLauncher",
                "launcherVersion": "0.5",
                "jvmArguments":[f"-Xmx{self.memory_select}G","-Xms2G"],
                "skins" : [{
                    "id" : "6a6e65e5-76dd-4c3c-a625-162924514568",
                    "state" : "ACTIVE",
                    "url" : skin,
                    "variant" : "CLASSIC"
                }]
            }
        except:
            url = f'http://skinsystem.ely.by/textures/{self.entry_name.get()}'
            response = requests.get(url)
            skin = response.json()['SKIN']["url"]
            try:
                alias = response.json()["SKIN"]["metadata"]
            except:
                alias = "STEVE"
            print(alias)
            url_id = f"https://authserver.ely.by/api/users/profiles/minecraft/{self.entry_name.get()}"
            response_id = requests.get(url_id)
            uuid = response_id.json()["id"]
            options={
                "username" : self.entry_name.get(),
                "uuid": uuid,
                "token": "",
                "launcherName": "CatLauncher",
                "launcherVersion": "0.5",
                "jvmArguments":[f"-Xmx{self.memory_select}G","-Xms2G"],
                "skins" : [{
                    "id" : "6a6e65e5-76dd-4c3c-a625-162924514568",
                    "state" : "ACTIVE",
                    "url" : skin,
                    "variant" : "CLASSIC",
                    "alias" : alias
                }]
            }
        with open(f"{os.path.realpath(__file__)[:-11]}\\save.txt","w+",encoding="utf-8") as f:
            f.write(f"{self.entry_minecraft_directory.get()}\n{self.entry_name.get()}")
        self.minecraft_directory = f"{self.entry_minecraft_directory.get()}//vanila//{self.version}"
        minecraft_launcher_lib.install.install_minecraft_version(self.version,self.minecraft_directory,callback=self.callback)
        print(options)
        print("test")
        subprocess.call(minecraft_launcher_lib.command.get_minecraft_command(version=self.version,minecraft_directory=self.minecraft_directory,options=options))
    def play_minecraft2(self):
        try:
            minecraft=threading.Thread(target=self.async_play_minecraft2)
            minecraft.start()
            print("successfully")
            return
        except RuntimeError:
            return 
    def async_play_minecraft2(self):
        try:
            url = f'https://api.mojang.com/users/profiles/minecraft/{self.entry_name2.get()}?'
            response = requests.get(url)
            uuid = response.json()['id']
            url = f'http://skinsystem.ely.by/textures/{self.entry_name2.get()}'
            response = requests.get(url)
            skin = response.json()['SKIN']["url"]
            try:
                alias = response.json()["SKIN"]["metadata"]
            except:
                alias = "STEVE"
            options={
                "username" : self.entry_name2.get(),
                "uuid": uuid,
                "token": "",
                "launcherName": "CatLauncher",
                "launcherVersion": "0.5",
                "jvmArguments":[f"-Xmx{self.memory_select}G","-Xms2G"],
                "skins" : [{
                    "id" : "6a6e65e5-76dd-4c3c-a625-162924514568",
                    "state" : "ACTIVE",
                    "url" : skin,
                    "variant" : "CLASSIC"
                }]
            }
        except:
            url = f'http://skinsystem.ely.by/textures/{self.entry_name2.get()}'
            response = requests.get(url)
            skin = response.json()['SKIN']["url"]
            try:
                alias = response.json()["SKIN"]["metadata"]
            except:
                alias = "STEVE"
            print(alias)
            url_id = f"https://authserver.ely.by/api/users/profiles/minecraft/{self.entry_name2.get()}"
            response_id = requests.get(url_id)
            uuid = response_id.json()["id"]
            options={
                "username" : self.entry_name2.get(),
                "uuid": uuid,
                "token": "",
                "launcherName": "CatLauncher",
                "launcherVersion": "0.5",
                "jvmArguments":[f"-Xmx{self.memory_select}G","-Xms2G"],
                "skins" : [{
                    "id" : "6a6e65e5-76dd-4c3c-a625-162924514568",
                    "state" : "ACTIVE",
                    "url" : skin,
                    "variant" : "CLASSIC",
                    "alias" : alias
                }]
            }
        with open(f"{os.path.realpath(__file__)[:-11]}\\save.txt","w+",encoding="utf-8") as f:
            f.write(f"{self.entry_minecraft_directory.get()}\n{self.entry_name2.get()}")
        self.minecraft_directory = f"{self.entry_minecraft_directory2.get()}//forge//{self.version}"
        print(self.minecraft_directory)
        minecraft_launcher_lib.forge.install_forge_version(self.version, self.minecraft_directory,callback=self.callback)
        subprocess.call(minecraft_launcher_lib.command.get_minecraft_command(version=minecraft_launcher_lib.forge.forge_to_installed_version(self.version),minecraft_directory=self.minecraft_directory,options=options))
    def play_minecraft3(self):
        try:
            minecraft=threading.Thread(target=self.async_play_minecraft3)
            minecraft.start()
            print("successfully")
            return
        except RuntimeError:
            return 
    def async_play_minecraft3(self):
        try:
            url = f'https://api.mojang.com/users/profiles/minecraft/{self.entry_name3.get()}?'
            response = requests.get(url)
            uuid = response.json()['id']
            url = f'http://skinsystem.ely.by/textures/{self.entry_name3.get()}'
            response = requests.get(url)
            skin = response.json()['SKIN']["url"]
            try:
                alias = response.json()["SKIN"]["metadata"]
            except:
                alias = "STEVE"
            options={
                "username" : self.entry_name3.get(),
                "uuid": uuid,
                "token": "",
                "launcherName": "CatLauncher",
                "launcherVersion": "0.5",
                "jvmArguments":[f"-Xmx{self.memory_select}G","-Xms2G"],
                "skins" : [{
                    "id" : "6a6e65e5-76dd-4c3c-a625-162924514568",
                    "state" : "ACTIVE",
                    "url" : skin,
                    "variant" : "CLASSIC"
                }]
            }
        except:
            url = f'http://skinsystem.ely.by/textures/{self.entry_name3.get()}'
            response = requests.get(url)
            skin = response.json()['SKIN']["url"]
            try:
                alias = response.json()["SKIN"]["metadata"]
            except:
                alias = "STEVE"
            print(alias)
            url_id = f"https://authserver.ely.by/api/users/profiles/minecraft/{self.entry_name3.get()}"
            response_id = requests.get(url_id)
            uuid = response_id.json()["id"]
            options={
                "username" : self.entry_name3.get(),
                "uuid": uuid,
                "token": "",
                "launcherName": "CatLauncher",
                "launcherVersion": "0.5",
                "jvmArguments":[f"-Xmx{self.memory_select}G","-Xms2G"],
                "skins" : [{
                    "id" : "6a6e65e5-76dd-4c3c-a625-162924514568",
                    "state" : "ACTIVE",
                    "url" : skin,
                    "variant" : "CLASSIC",
                    "alias" : alias
                }]
            }
        with open(f"{os.path.realpath(__file__)[:-11]}\\save.txt","w+",encoding="utf-8") as f:
            f.write(f"{self.entry_minecraft_directory.get()}\n{self.entry_name3.get()}\n{self.memory_select}")
        print([name for name in os.listdir(f"{self.entry_minecraft_directory3.get()}\\customs\\{self.version}") if os.path.isdir(os.path.join(f"{self.entry_minecraft_directory3.get()}\\customs\\{self.version}"))])
        if [name for name in os.listdir(f"{self.entry_minecraft_directory3.get()}\\customs\\{self.version}") if os.path.isdir(os.path.join(f"{self.entry_minecraft_directory3.get()}\\customs\\{self.version}"))] == ["forge"]:
            custom_ver = [name for name in os.listdir(f"{self.entry_minecraft_directory3.get()}\\customs\\{self.version}\\forge") if os.path.isdir(os.path.join(f"{self.entry_minecraft_directory3.get()}\\customs\\{self.version}\\forge", name))]
            self.minecraft_directory = f"{self.entry_minecraft_directory2.get()}\\custom\\{self.version}\\forge\\{custom_ver[0]}"
            print(self.minecraft_directory)
            print(custom_ver[0])
            minecraft_launcher_lib.forge.install_forge_version(custom_ver[0], self.minecraft_directory,callback=self.callback)
            subprocess.call(minecraft_launcher_lib.command.get_minecraft_command(version=minecraft_launcher_lib.forge.forge_to_installed_version(custom_ver[0]),minecraft_directory=self.minecraft_directory,options=options))
        elif [name for name in os.listdir(f"{self.entry_minecraft_directory3.get()}\\customs\\{self.version}") if os.path.isdir(os.path.join(f"{self.entry_minecraft_directory3.get()}\\customs\\{self.version}"))] == ["vanila"]:
            custom_ver = [name for name in os.listdir(f"{self.entry_minecraft_directory3.get()}\\customs\\{self.version}\\vanila") if os.path.isdir(os.path.join(f"{self.entry_minecraft_directory3.get()}\\customs\\{self.version}\\vanila", name))]
            self.minecraft_directory = f"{self.entry_minecraft_directory2.get()}\\custom\\{self.version}\\vanila\\{custom_ver[0]}"
            print(custom_ver[0])
            minecraft_launcher_lib.install.install_minecraft_version(custom_ver[0],self.minecraft_directory,callback=self.callback)
            subprocess.call(minecraft_launcher_lib.command.get_minecraft_command(version=custom_ver[0],minecraft_directory=self.minecraft_directory,options=options))


        
if __name__ == "__main__":
    app = App()
    app.mainloop()
