# automation/servopa_lances.py
# Módulo completo para automação de lances no Servopa

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

TIMEOUT = 20
SERVOPA_PAINEL_URL = "https://www.consorcioservopa.com.br/vendas/painel"
SERVOPA_LANCES_URL = "https://www.consorcioservopa.com.br/vendas/lances"


def alterar_consorcio(driver, progress_callback=None):
    """
    Clica em 'Alterar Consórcio' para voltar à busca
    
    Args:
        driver: Instância do WebDriver
        progress_callback: Função para atualizar progresso na UI
        
    Returns:
        bool: True se bem-sucedido
    """
    try:
        if progress_callback:
            progress_callback("🔄 Clicando em 'Alterar Consórcio'...")
        
        wait = WebDriverWait(driver, TIMEOUT)
        
        # Procura link "Alterar Consórcio"
        alterar_link = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//a[@href='https://www.consorcioservopa.com.br/vendas/painel' or contains(text(), 'Alterar Consórcio')]")
        ))
        
        alterar_link.click()
        time.sleep(3)  # Aguarda carregamento
        
        if progress_callback:
            progress_callback("✅ Retornado à seleção de consórcio")
        
        return True
        
    except Exception as e:
        if progress_callback:
            progress_callback(f"❌ Erro ao alterar consórcio: {e}")
        return False


def buscar_grupo(driver, grupo_number, progress_callback=None):
    """
    Preenche número do grupo e clica em buscar
    
    Args:
        driver: Instância do WebDriver
        grupo_number: Número do grupo (ex: "1550")
        progress_callback: Função para atualizar progresso na UI
        
    Returns:
        bool: True se bem-sucedido
    """
    try:
        wait = WebDriverWait(driver, TIMEOUT)
        
        if progress_callback:
            progress_callback(f"🔍 Buscando grupo {grupo_number}...")
        
        # Localiza o campo de grupo
        grupo_input = wait.until(EC.presence_of_element_located((By.ID, "grupofrm")))
        
        # Preenche o campo com delay natural
        grupo_input.clear()
        time.sleep(0.5)
        for char in grupo_number:
            grupo_input.send_keys(char)
            time.sleep(0.1)  # Digitação natural
        
        time.sleep(1)
        
        # Localiza e clica no botão Buscar
        buscar_button = wait.until(EC.element_to_be_clickable(
            (By.ID, "btn_representante_cota")
        ))
        
        buscar_button.click()
        time.sleep(4)  # Aguarda busca carregar
        
        if progress_callback:
            progress_callback(f"✅ Grupo {grupo_number} buscado com sucesso")
        
        return True
        
    except Exception as e:
        if progress_callback:
            progress_callback(f"❌ Erro ao buscar grupo: {e}")
        return False


def selecionar_cota(driver, cota_number, progress_callback=None):
    """
    Seleciona a cota específica na tabela de resultados
    
    Args:
        driver: Instância do WebDriver
        cota_number: Número da cota (ex: "1123")
        progress_callback: Função para atualizar progresso na UI
        
    Returns:
        dict: Dados da cota selecionada ou None se falhar
    """
    try:
        wait = WebDriverWait(driver, TIMEOUT)
        
        if progress_callback:
            progress_callback(f"🔍 Procurando cota {cota_number} na tabela...")
        
        # Aguarda tabela carregar
        time.sleep(2)
        
        # Procura todas as linhas da tabela
        rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")
        
        if not rows:
            if progress_callback:
                progress_callback("❌ Nenhuma linha encontrada na tabela")
            return None
        
        if progress_callback:
            progress_callback(f"📊 {len(rows)} linhas encontradas, procurando cota {cota_number}...")
        
        # Procura a linha com a cota específica
        for row in rows:
            try:
                # Pega todas as células da linha
                cells = row.find_elements(By.TAG_NAME, "td")
                
                # A cota está na 5ª coluna (índice 4)
                if len(cells) >= 5:
                    cota_cell = cells[4]  # Coluna "Cota"
                    cota_value = cota_cell.text.strip()
                    
                    if cota_value == cota_number:
                        # Encontrou a cota!
                        nome_cliente = cells[0].text.strip()
                        valor = cells[1].text.strip()
                        grupo = cells[3].text.strip()
                        digito = cells[5].text.strip()
                        contrato = cells[6].text.strip()
                        
                        if progress_callback:
                            progress_callback(f"✅ Cota {cota_number} encontrada: {nome_cliente}")
                        
                        # Clica na linha
                        row.click()
                        time.sleep(3)  # Aguarda redirecionamento
                        
                        return {
                            'cota': cota_number,
                            'nome': nome_cliente,
                            'valor': valor,
                            'grupo': grupo,
                            'digito': digito,
                            'contrato': contrato
                        }
                        
            except Exception as cell_error:
                continue
        
        # Se chegou aqui, não encontrou a cota
        if progress_callback:
            progress_callback(f"❌ Cota {cota_number} não encontrada na tabela")
        
        return None
        
    except Exception as e:
        if progress_callback:
            progress_callback(f"❌ Erro ao selecionar cota: {e}")
        return None


def navegar_para_lances(driver, progress_callback=None):
    """
    Clica no link 'Lances' para ir para a página de lances
    
    Args:
        driver: Instância do WebDriver
        progress_callback: Função para atualizar progresso na UI
        
    Returns:
        bool: True se bem-sucedido
    """
    try:
        wait = WebDriverWait(driver, TIMEOUT)
        
        if progress_callback:
            progress_callback("🎯 Navegando para página de Lances...")
        
        # Procura o link de lances
        lances_link = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//a[@href='https://www.consorcioservopa.com.br/vendas/lances' or contains(text(), 'Lances')]")
        ))
        
        lances_link.click()
        time.sleep(3)  # Aguarda carregamento
        
        if progress_callback:
            progress_callback("✅ Página de lances carregada")
        
        return True
        
    except Exception as e:
        if progress_callback:
            progress_callback(f"❌ Erro ao navegar para lances: {e}")
        return False


def executar_lance(driver, progress_callback=None):
    """
    Executa o lance completo:
    1. Copia valor de tx_lanfix para tx_lanfix_emb
    2. Clica em 'Simular Lance'
    3. Clica em 'Registrar'
    
    Args:
        driver: Instância do WebDriver
        progress_callback: Função para atualizar progresso na UI
        
    Returns:
        bool: True se lance executado com sucesso
    """
    try:
        wait = WebDriverWait(driver, TIMEOUT)
        
        # Passo 1: Copiar valor de tx_lanfix
        if progress_callback:
            progress_callback("📋 Copiando valor do lance fixo...")
        
        tx_lanfix = wait.until(EC.presence_of_element_located((By.ID, "tx_lanfix")))
        valor_lanfix = tx_lanfix.get_attribute('value')
        
        if progress_callback:
            progress_callback(f"📋 Valor do lance fixo: {valor_lanfix}%")
        
        # Passo 2: Colar valor em tx_lanfix_emb
        tx_lanfix_emb = wait.until(EC.presence_of_element_located((By.ID, "tx_lanfix_emb")))
        tx_lanfix_emb.clear()
        time.sleep(0.5)
        
        # Digita com delay natural
        for char in valor_lanfix:
            tx_lanfix_emb.send_keys(char)
            time.sleep(0.1)
        
        time.sleep(1)
        
        if progress_callback:
            progress_callback(f"✅ Valor {valor_lanfix}% preenchido no campo embutido")
        
        # Passo 3: Clicar em 'Simular Lance'
        if progress_callback:
            progress_callback("🎲 Simulando lance...")
        
        simular_button = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "a#btn_simular, a[name='btn_simular']")
        ))
        
        simular_button.click()
        time.sleep(3)  # Aguarda simulação processar
        
        if progress_callback:
            progress_callback("✅ Simulação concluída")
        
        # Passo 4: Clicar em 'Registrar'
        if progress_callback:
            progress_callback("💾 Registrando lance...")
        
        registrar_button = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "a.printBt")
        ))
        
        registrar_button.click()
        time.sleep(3)  # Aguarda registro processar
        
        if progress_callback:
            progress_callback("✅ Lance registrado com sucesso!")
        
        return True
        
    except Exception as e:
        if progress_callback:
            progress_callback(f"❌ Erro ao executar lance: {e}")
        return False


def processar_lance_completo(driver, grupo, cota, progress_callback=None):
    """
    Processa um lance completo do início ao fim
    
    Args:
        driver: Instância do WebDriver
        grupo: Número do grupo
        cota: Número da cota
        progress_callback: Função para atualizar progresso na UI
        
    Returns:
        dict: Resultado do processamento
    """
    result = {
        'success': False,
        'grupo': grupo,
        'cota': cota,
        'steps_completed': []
    }
    
    try:
        # Passo 1: Alterar consórcio (se não for o primeiro lance)
        current_url = driver.current_url
        if 'painel' not in current_url:
            if not alterar_consorcio(driver, progress_callback):
                return result
            result['steps_completed'].append('alterar_consorcio')
        
        # Passo 2: Buscar grupo
        if not buscar_grupo(driver, grupo, progress_callback):
            return result
        result['steps_completed'].append('buscar_grupo')
        
        # Passo 3: Selecionar cota
        cota_data = selecionar_cota(driver, cota, progress_callback)
        if not cota_data:
            return result
        result['steps_completed'].append('selecionar_cota')
        result['cota_data'] = cota_data
        
        # Passo 4: Navegar para lances
        if not navegar_para_lances(driver, progress_callback):
            return result
        result['steps_completed'].append('navegar_lances')
        
        # Passo 5: Executar lance
        if not executar_lance(driver, progress_callback):
            return result
        result['steps_completed'].append('executar_lance')
        
        # Sucesso!
        result['success'] = True
        return result
        
    except Exception as e:
        if progress_callback:
            progress_callback(f"❌ Erro no processamento completo: {e}")
        return result


if __name__ == "__main__":
    # Teste do módulo
    print("Este módulo deve ser importado e usado com uma instância do WebDriver")
    print("Exemplo:")
    print("  from auth.servopa_auth import create_driver, login_servopa")
    print("  from automation.servopa_lances import processar_lance_completo")
    print("  ")
    print("  driver = create_driver()")
    print("  login_servopa(driver)")
    print("  result = processar_lance_completo(driver, '1550', '1123')")
