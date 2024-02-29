from crawler_oxy import OxyDownloader
from sei import Sei_Selenium
import logging
import json

def main():
    txt = input("Nome do arquivo txt:").strip()
    process_downloader = OxyDownloader('ajorgefalcao@gmail.com', 'falcon')
    process_downloader.download_and_extract_process(txt)

    with open('json.json', 'r') as arquivo_json:
        content = json.load(arquivo_json)

    try:
        with Sei_Selenium() as client:
            client.start(content, txt)
    except Exception as e:
        logging.critical(f"idTarefa=1: {e}", exc_info=True)

if __name__ == "__main__":
    main()