import time
from selenium.webdriver.common.by import By

class Login():

    def login(self, login, password):
        self.switch_to_screen("Login")
        self.URL_BASE = 'https://seibahia.ba.gov.br/sei/'
        self.URL_LOGIN = self.URL_BASE + "/controlador_externo.php?acao=usuario_externo_logar&id_orgao_acesso_externo=0"

        self.DRIVER.get(self.URL_LOGIN)
        self.find_locator("usernameInput").send_keys(login)
        self.find_locator("passwordInput").send_keys(password)
        self.find_locator("enterButton").click()
        self.URL_HOME = self.DRIVER.current_url
        self.switch_to_screen("SignDocs")
        return self
