import logging 
import time , os, re
from src.init import BaseDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select


class Inicial_Protocol():
    @BaseDriver.screen_decorator("Protocol")
    def navigate_to_protocol_screen(self, content):
        docs = self.listar_arquivos_recursivamente(content)
        self.add_all_docs_process(docs)
        self.switch_to_screen("SignerFrame")
        return self.signer_process()
    
    @BaseDriver.screen_decorator("SignDocs")
    def navigate_to_docs_screen(self):
        self.find_locator("screenDocs", method="click")
        self.find_locator("btnScreen", method="click")
        self.find_locator("Assunto", method="click")
        return self.switch_to_screen("Protocol")
    
    @BaseDriver.screen_decorator("SignerFrame")
    def signer_process(self):
        self.set_inputs_protocol()
        self.wait_result_protocol()
        return self.verify_protocol()

    def add_all_docs_process(self, docs):
        self.set_principal_docs(docs)
        self.set_essential_docs(docs)
        self.find_locator("btnSigner").click()


    def wait_result_protocol(self):
        if "Senha inválida" in self.DRIVER.page_source:
            raise ValueError("Senha inválida")


    def verify_protocol(self):
        try:
            processo = self.find_locator("trProtocol", retry_count=10)
            numero_processo = processo.text
            logging.info(f"Protocolo confirmado com o numero:{numero_processo}")
            return numero_processo
        except:
            raise ValueError("Erro ao confirmar o protocolo")

    def set_inputs_protocol(self):
        time.sleep(1)
        self.switch_to_frame("//iframe[@name=\"modal-frame\"]")
        self.set_grid_option_value("selCargo", "Representante Legal")
        self.send_keys_and_clear("inputPassw", "2022Ajfr")
        self.find_locator("signer").click()
    
    def set_principal_docs(self, contents):
        itens = [item for item in contents if re.search(r'/1-', item)]
        for item in itens:
            nome_anexo = "REQUERIMENTO"
            self.find_locator("AddDoc1", method="click")
            time.sleep(1)


    def listar_arquivos_recursivamente(self, pasta):
        arquivos = []
        for root, dirs, files in os.walk(pasta):
            for file in files:
                caminho_completo = os.path.join(root, file)
                arquivos.append(caminho_completo)
        return arquivos


    def set_essential_docs(self, contents):
        itens = [item for item in contents if re.search(r'2\.\d+', item)]
        itens.append("3-CONTRATO SOCIAL E DOCS REPRESENTANTE LEGAL.pdf")
        index = 0
        for item in itens:
            index += 1
            nome_anexo = self.find_name_doc(item)
            self.add_in_inputs_essential(nome_anexo, index, item)
            self.DRIVER.execute_script("validarUploadArquivo('2')")
            self.wait_upload()
            if index == 3: index = 0


    def add_in_inputs_essential(self, nome: str, index: int, item: str):
        self.send_keys_and_clear("NomeDoc2", nome)
        self.set_grid_option_script(index)
        self.type_docs("DigitalizadoBtn", 2, 3)
        self.find_locator("inputUpload2").send_keys(item)

    def add_in_inputs_principal(self, nome: str, index: int, item: str):
        self.find_locator("formTexto").send_keys(nome)
        self.find_locator("NomeDoc1").send_keys(nome)
        self.find_locator("inputUpload1").send_keys(item)
        self.type_docs("Nato-digital", 1, None)


    def wait_upload(self):
        attemps, max_attemps = 0, 15
        while attemps < max_attemps:
            iframe = self.find_element("ifrProgressofrmDocumentosEssenciais", by=By.ID)
            iframe_src = iframe.get_attribute("src")
            if not "infra_upload_progresso" in iframe_src:break
            time.sleep(1)


    def send_keys_and_clear(self, locator:str, value:str):
        element = self.find_locator(locator)
        element.clear()
        time.sleep(0.5)
        element.send_keys(value)


    def find_name_doc(self, doc):
        if "PROCURACAO" in doc.upper():
            return "PROCURAÇÃO"
        elif "DOCUMENTOS-PESSOAIS" in doc.upper():
            return "DOCUMENTOS-PESSOAIS"
        elif "CONTRATO SOCIAL"in doc.upper():
            return "CONTRATO SOCIAL"
        raise ValueError(f"Não achou o tipo de documento: {doc}")
        

    def type_docs(self, type, num, index):
        if type == "Nato-digital":
            self.find_locator(f"NatoBtn{num}").click()
        else:
            self.find_locator(f"DigitalizadoBtn{num}").click()
            self.set_grid_option_index(index)
        time.sleep(0.2)

    def set_grid_option_index(self, option_index: int):
        select_element = self.find_locator("tipoDocumentoEssencial")
        select_object = Select(select_element)
        select_object.select_by_index(option_index)

    def set_grid_option_value(self, element,  option_value: str):   
        select_element = self.find_locator(element)
        select_object = Select(select_element)
        select_object.select_by_visible_text(option_value)

    def set_grid_option_script(self, index):  
        time.sleep(0.2)
        script = f"document.getElementById('tipoDocumentoEssencial').selectedIndex = {index}"
        return self.DRIVER.execute_script(script)





