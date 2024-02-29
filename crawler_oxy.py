import requests
import zipfile
import os
import logging 
import shutil

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class OxyDownloader:
    def __init__(self, email, password):
        self.session = requests.session()
        self.clean_folder()
        self.login(email, password)

    def login(self, email:str, password:str):
        try:
            data = {'email': email, 'passwd': password}
            self.session.post('https://falcaorios.oxygenjus.adv.br/login', data=data, timeout=100)
            logging.info("Login na Oxy Realizado com sucesso")
        except:
            raise ValueError("Erro devido a problemas de tempo de resposta do servidor da Oxy")

    def download_process_zip(self, filename:str, process_id:str):
        url_down = f"https://falcaorios.oxygenjus.adv.br/juridico/autos/download/{process_id}/true"

        response = self.session.get(url_down)
        with open(filename, 'wb') as file:
            file.write(response.content)

    def extract_zip(self, zip_filename:str, extract_folder:str):
        with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
            zip_ref.extractall(extract_folder)

    def download_and_extract_process(self, process_ids_file):
        with open(process_ids_file, 'r') as arquivo:
            for linha in arquivo:
                process_id = linha.strip()
                name_doc = process_id.split("/")[0]
                extract_folder = f"documentos/{name_doc}"
                zip_filename = f'documentos/arquivo.zip'

                self.download_process_zip(zip_filename, process_id)
                os.makedirs(extract_folder, exist_ok=True)
                self.extract_zip(zip_filename, extract_folder)
                os.remove(zip_filename)

                logging.info(f'Conteúdo extraído para a pasta: {extract_folder}')


    def clean_folder(self):
        if not os.path.exists("documentos"):
            logging.info(f"A pasta documentos não existe.")
            return
        try:
            shutil.rmtree("documentos")
            os.makedirs("documentos")
        except Exception as e:
            raise ValueError(f"Erro ao excluir o arquivo documentos: {e}")
    
        logging.info(f"A pasta documentos foi limpa com sucesso.")




