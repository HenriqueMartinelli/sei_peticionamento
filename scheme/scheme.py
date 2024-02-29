# Dictionary with the description of the site screens,
# each screen has an indication of screen iframe, available actions and elements for interaction
SITE_SCHEME = {
    "Login": {
        "elements": {
            "usernameInput": "//input[@id='txtEmail']",
            "passwordInput": "//input[@id='pwdSenha']",
            "enterButton": "//button[@id='sbmLogin']"
        }
    },

    "Protocol": {
        "actions": ["get_pratical_exam_categories", "set_pratical_exam_category", "solve_captcha"],
        "elements": {
            "inputUpload1": "//*[@id=\"fileArquivoPrincipal\"]",
            "inputUpload2": "//*[@id=\"fileArquivoEssencial\"]",
            "formTexto": "//*[@id=\"txtEspecificacao\"]",
            "NomeDoc1": "//*[@id=\"complementoPrincipal\"]",
            "NomeDoc2": "//*[@id=\"complementoEssencial\"]",
            "btncomprovante": "//*[@id=\"formBotoesAcao:btnSalvarComprovante\"]",
            "NatoBtn1": "//label[@for=\"rdNato1_1\"]",
            "NatoBtn2": "//label[@for=\"rdNato2_1\"]",
            "DigitalizadoBtn1": "//label[@for=\"rdDigitalizado1_2\"]",
            "DigitalizadoBtn2": "//label[@for=\"rdDigitalizado2_2\"]",
            "tipoDocumentoEssencial": "//select[@id=\"TipoConferenciaEssencial\"]",
            "selCargo": "//select[@id=\"selCargo\"]",
            "AddDoc1": "//*[@id=\"camposDigitalizadoPrincipalBotao\"]/input",
            "AddDoc2": "//*[@id=\"camposDigitalizadoEssencial\"]/div/div/input",
            "btnSigner": "//*[@id=\"Peticionar\"]",
            "inputPassw": "//*[@id=\"pwdsenhaSEI\"]",
            "signer": "//*[@value=\"Assinar\"]",
        }
    },

    "SignerFrame": {
        "actions": ["get_pratical_exam_categories", "set_pratical_exam_category", "solve_captcha"],
        "elements": {
            "selCargo": "//select[@id=\"selCargo\"]",
            "inputPassw": "//*[@id=\"pwdsenhaSEI\"]",
            "signer": "//*[@value=\"Assinar\"]",
            "trProtocol": "//tr[@class=\"infraTrAcessada\"]/td[2]",
        }
    },
            "inputPassw": "//*[@id=\"pwdsenhaSEI\"]",
            "signer": "//*[@value=\"Assinar\"]",
    "SignDocs": {
        "actions": ["get_pratical_exam_categories", "set_pratical_exam_category", "solve_captcha"],
        "elements": {
            "btncomprovante": "//*[@id=\"formBotoesAcao:btnSalvarComprovante\"]",
            "screenDocs": "//*[@id=\"infraMenu\"]/li[4]/a",
            "btnScreen": "//*[@id=\"submenu3\"]/li[1]/a",
            "Assunto": "//*[@data-desc=\"'consignataria: inscricao/ contratacao/ requerimento'\"]",
            "btnSigner": "//*[@id=\"btn-assinador\"]"
        }
    },
    "IncidentalProtocol": {
        "actions": ["get_pratical_exam_categories", "set_pratical_exam_category", "solve_captcha"],
        "elements": {
            "confirmPage": "//*[@id=\"divDocumentoPrincipal\"]",
            "checkBoxs": "//*[@id=\"expTb:tb\"]",
            "btnSigner": "//*[@id=\"btn-assinador\"]",
            "confirmSigner": "//*[@id=\"dvMsg\"]/dl/dt[1]/span"
        }
    }
}
