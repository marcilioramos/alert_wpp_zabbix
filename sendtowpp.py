#!/bin/python3

import requests
import re
import time
import base64
import sys

#########################################
# Variaveis que precisam ser alteradas
########################################
token = 'token'
ip_wpp = 'ip'
ip_zabbix_web = 'ip zabbix'
zbx_user = 'usuario'
zbx_pass = 'senha'
################################
# Variaveis coletadas no Zabbix
################################
phone = sys.argv[1]
subject = sys.argv[2]
message = sys.argv[3]

############################################################
# Tratamento da primeira linha da mensagem vindo da zabbix
############################################################
linhas = message.splitlines()
primeira_linha = linhas[0]
array = primeira_linha.split('#')

linhas2 = message.splitlines()  # Divide o texto em linhas
message_real = '\n'.join(linhas2[1:])  # Pega todas as linhas após a primeira e as junta em uma string

trigger_name = array[1]
isGroup = array[2]
item_ids = array[3].split(',')
host_name = array [7]

##########################################
# Envio de mensagem com imagem
##########################################

def send_image(phone, isGroup, subject, message_real, token, ip_wpp, base64_image):
    wppconnect_url = 'http://{}/api/{}/send-image'.format(ip_wpp, token)
    data = {
        "phone": phone,
        "isGroup": isGroup,
        "caption": subject + '\n' + message_real,
        "base64": 'data:image/png;base64,' + base64_image
    }

    headers = {
        "accept": "*/*",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(wppconnect_url, json=data, headers=headers)
        response.raise_for_status()
        print(response.text)
        with open('/tmp/output.txt', 'a') as file:
            file.write(f'{response.text}\n')
    except requests.exceptions.RequestException as err:
        with open('/tmp/output.txt', 'a') as file:
            file.write('Erro na solicitação\n')

if array[0] == 'ON':
    zbx_server = 'http://{}'.format(ip_zabbix_web)
    width = int(array[5])
    height = int(array[6])
    color = array[4]
    periodo = '3600'
    stime = 3600

    try:
        session = requests.Session()
        login_page = session.get(f'{zbx_server}/index.php', auth=(zbx_user, zbx_pass), verify=True).text
        enter = re.search('<button.*value=".*>(.*?)</button>', login_page)

        try:
            enter = str(enter.group(1))
            session.post(f'{zbx_server}/index.php?login=1', params={'name': zbx_user, 'password': zbx_pass, 'enter': enter}, verify=False).text
        except:
            pass

        stime = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time() - stime))
        urlGraph = f"{zbx_server}/chart3.php?name={array[7]}: {{}}&period={periodo}&width={array[5]}&height={array[6]}&stime={stime}"

        j = 0
        for i in range(len(item_ids)):
            try:
                cor = array[4]
            except:
                if j == len(dictCores['00C800']):
                    j = 0
                cor = dictCores[color][j]
                j += 1

            urlGraph += f"&items[{i}][itemid]={item_ids[i]}&items[{i}][drawtype]=5&items[{i}][color]={cor}"
            print(f"Item ID: {item_ids[i]}")

        get_graph = session.get(urlGraph)

        if get_graph.status_code == 200:
            with open('zap.png', 'wb') as f:
                f.write(get_graph.content)

            with open("zap.png", "rb") as img_file:
                base64_image = base64.b64encode(img_file.read()).decode("utf-8")
                send_image(phone, isGroup, subject, message_real, token, ip_wpp, base64_image) 
        else:
            pass

    except BaseException as e:
        print("Erro:", e)
        with open('/tmp/output.txt', 'a') as file:
            file.write('Erro\n')
            file.write(f'{e}\n')


##############################
# Envio de mensagem de imagem
##############################

if array[0] == 'OFF':
    wppconnect_url = 'http://{}/api/{}/send-message'.format(ip_wpp,token)

    data = {
        "phone": phone,
        "isGroup": isGroup,
        "message": subject + '\n' + message_real
    }

    headers = {
        "accept": "*/*",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(wppconnect_url, json=data, headers=headers)
        response.raise_for_status()
        print(response.text)
    except requests.exceptions.RequestException as err:
        print("Erro na solicitação:", err)

