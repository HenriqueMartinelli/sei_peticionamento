import logging, os

from src.init import BaseDriver
from src.login import Login
from src.inicial_protocol import Inicial_Protocol
from src.incidental_protocol import Incidental_Protocol

class Sei_Selenium(BaseDriver, Login, Inicial_Protocol, Incidental_Protocol):
    def __exit__(self, type, value, traceback):
        if self.DRIVER:
            pass
            # self.DRIVER.quit()
        
    def __enter__(self): 
        self.setDriver(self.driver_path, self.chrome_options)
        return self


    def start(self, contents, path_txt):
        self.path_txt = path_txt
        self.login(contents["login"], contents['senha'])
        for content in os.listdir(self.path_docs):
            self.process_folder(content)

    def process_folder(self, content):
        try:
            caminho_pasta = os.path.join(self.path_docs, content)
            nome_pasta = caminho_pasta.split("/")[-1]
            logging.info(f"Consultando a pasta {nome_pasta}")

            if os.path.isdir(caminho_pasta):
                self.process_directory(caminho_pasta)
            else:
                raise ValueError("Erro ao percorrer a pasta pai")
        except Exception as e:
            self.handle_exception(content, e, nome_pasta)

    def process_directory(self, caminho_pasta):
        if self.tipo == 0:
            self.inicial_protocol(caminho_pasta)
        elif self.tipo == 1:
            self.incidental_protocol(caminho_pasta)

    def handle_exception(self, content, e, nome_pasta):
        if len(e.args) > 0:
            self.save_protocol(content=content, error=True, msg=e.args[0])
        else:
            self.save_protocol(content=content, error=True, msg="Erro não mapeado")
        logging.warning(f'ID={nome_pasta}, ERRO EM 1 PROCESSO - ' + str(e))


    def inicial_protocol(self, content):
        self.switch_to_screen("SignDocs")
        self.navigate_to_docs_screen()
        process = self.navigate_to_protocol_screen(content)
        self.save_protocol(content, msg=f"Protocolado -> {process}")
        input()
    
    def incidental_protocol(self, content):
        self.global_variables(content)
        self.switch_to_screen("IncidentalProtocol")
        self.navigate_to_incidental_page()
        self.returnMsg(inputs=content)


    def save_protocol(self, content: str, msg: str, error=False):
        content_id = content.split("/")[-1]
        final_log = f"- Erro:{error} - {msg}"

        with open(self.path_txt, 'r+') as arquivo:
            linhas = arquivo.readlines()
            arquivo.seek(0)
            for linha in linhas:
                if content_id in linha:
                    arquivo.write(linha.strip() + final_log + "\n")
                else:
                    arquivo.write(linha)
            arquivo.truncate()