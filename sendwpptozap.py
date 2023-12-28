#!/bin/python3

import requests
import re
import time
import base64
import sys


## Variaveis

phone = sys.argv[1]
subject = sys.argv[2]
message = sys.argv[3]
token = ''
periodo = '3600'
ip_wpp = ''
ip_zabbix_web = ''
zabbixuser = ''
zabbixpass = ''

# Varrendo a primeira linha para pegar as variaveis

linhas = message.splitlines()
primeira_linha = linhas[0]
array = primeira_linha.split('#')

# Limpando a message

linhas2 = message.splitlines()  # Divide o texto em linhas
message_real = '\n'.join(linhas2[1:])  # Pega todas as linhas após a primeira e as junta em uma string

## Logs, habilitar se preciso para debub

#with open('/tmp/output.txt', 'a') as file:
#    file.write(f'{phone}\n')
#    file.write(f'{token}\n')
#    file.write(f'{subject}\n')
#    file.write(f'{message_real}\n')
#    file.write(f'{array}\n')

trigger_name = array[0]
isGroup = array[1]
item_ids = array[2].split(',')

with open('/tmp/output.txt', 'a') as file:
    file.write(f'{item_ids}\n')

def send_image(subject, message_real, token, base64_image):
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
    except requests.exceptions.RequestException as err:
        print("Erro na solicitação:", err)

zbx_server = zbx_server = f'http://{ip_zabbix_web}'.format(ip_zabbix_web)
zbx_user = zabbixuser
zbx_pass = zabbixpass
width = 900
height = 200
color = '00C800'

stime = 3600
dictCores = {
    'FF0000': [
        'FF0000',
    ],
    '00C800': [
        '008000',
    ]
}

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
    urlGraph = f"{zbx_server}/chart3.php?name={host_name}: {{}}&{periodo}&width={width}&height={height}&stime={stime}"

    j = 0
    for i in range(len(item_ids)):
        try:
            cor = dictCores[color][i]
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
            #with open('/tmp/output.txt', 'a') as file:
            #    file.write(f'{base64_image}\n')
            send_image(subject, message_real, token, base64_image)
    else:
        pass

except BaseException as e:
    print("Erro:", e)
