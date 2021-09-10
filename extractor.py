import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = webdriver.ChromeOptions()
path_to_save = '/home/pedro/Desktop/master/MPMG/document_extration/downloaded_documents'
prefs = {"download.default_directory": path_to_save,
         "safebrowsing.enabled": "false",
         "download.prompt_for_download": False,
         "download.directory_upgrade": True}
options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(executable_path='/home/pedro/Desktop/master/chromedriver', options=options)
driver.get('https://geoobras.tce.mg.gov.br/cidadao/')

element = driver.find_element_by_xpath('//select[@id="ctl00_ContentPlaceHolderConteudo_municipioRadComboBox1"]')
municipios = element.find_elements_by_tag_name("option")

for i in range(1, len(municipios)):
    option = municipios[i]
    mun_str = option.get_attribute("text")
    print("Iniciando Municipio: %s" % option.get_attribute("text"))
    option.click()

    button = driver.find_element_by_xpath('//input[@id="ctl00_ContentPlaceHolderConteudo_consultaImageButton"]').click()

    links_obras = driver.find_elements_by_xpath("//table[@id='ctl00_ContentPlaceHolderConteudo_resultadoASPxGridView_DXMainTable']//a[@href]")
    for j in range(len(links_obras)):
        if j == 0:
            links = links_obras
        if j % 2 == 0:
            continue
        obra = links[j]
        obra.click()
        documents = driver.find_elements_by_xpath("//a[@id='ctl00_documentosLinkButton']")
        documents[0].click()

        contratos = driver.find_elements_by_xpath("//input[@id='ctl00_ContentPlaceHolderConteudo_tipoSelecaoArquivos_1']")[0]

        action = webdriver.common.action_chains.ActionChains(driver)
        action.move_to_element_with_offset(contratos, 5, 5)
        action.click()
        action.perform()

        table = driver.find_elements_by_xpath("//table[@id='ctl00_ContentPlaceHolderConteudo_resultadoASPxGridView_DXMainTable']/tbody/tr")

        for k in range(len(table)-1):
            id = 'ctl00_ContentPlaceHolderConteudo_resultadoASPxGridView_cell' + str(k) + '_4_baixarLinkButton'
            print('iD', id)
            pdf = driver.find_element_by_xpath("//a[@id='" + id + "']").click()
            driver.back()

        driver.back()
        driver.back()
        driver.back()

        links = driver.find_elements_by_xpath("//table[@id='ctl00_ContentPlaceHolderConteudo_resultadoASPxGridView_DXMainTable']//a[@href]")

    driver.get('https://geoobras.tce.mg.gov.br/cidadao/')
    element = driver.find_element_by_xpath('//select[@id="ctl00_ContentPlaceHolderConteudo_municipioRadComboBox1"]')
    municipios = element.find_elements_by_tag_name("option")
