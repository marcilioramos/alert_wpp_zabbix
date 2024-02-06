## Doações 
##### Se esse projeto te ajudou, leva em consideração ajudar o desenvolvedor :-)
###### (Pix Mercado Pago ou PayPal)


[<img src="https://github.com/marcilioramos/estudos_msr/blob/main/repoimagens/logo-mercadopago.jpg?raw=true" width="200">](https://seu_link_de_doacao_no_Mercado_Pago)
[<img src="https://raw.githubusercontent.com/marcilioramos/estudos_msr/main/repoimagens/qrcode-mercadolivre.jpeg?raw=true" width="100">](https://seu_QR_Code_no_Mercado_Pago)
[<img src="https://raw.githubusercontent.com/marcilioramos/estudos_msr/main/repoimagens/paypal.jpg?raw=true" width="200">](https://seu_link_de_doacao_no_Mercado_Pago)
[<img src="https://raw.githubusercontent.com/marcilioramos/estudos_msr/main/repoimagens/QR%20Code.png?raw=true" width="100">](https://seu_QR_Code_no_Mercado_Pago)



## Alertas Zabbix com Whatsapp

### Requisitos:

- **Uma VM para configurar o sistema WPPConnect (API OpenSource Whatsapp):** Ubuntu 22.04 LTS Server.
  - **Recursos:** 2GB de RAM, 2vCPU, 20GB de armazenamento e acesso à internet.

- **Postman:** Para testes e geração do token.
- **Celular com WhatsApp:** Para escanear o QR Code e usar como linha para enviar mensagens.
- **Zabbix configurado:** Testado com Zabbix 6.0 LTS.

### Procedimento:

1. **Provisione a VM.**
2. **Instale o sistema [WppConnect](https://wppconnect.io/pt-BR/)** para habilitar a API do WhatsApp.
   - O WppConnect permite o uso do WhatsApp em um navegador Google Chrome com NodeJS. Para mais detalhes, consulte a [documentação oficial](https://wppconnect.io/pt-BR/).
   
3. Para configurar o sistema, execute o script disponível em [config_ambiente.sh](https://github.com/marcilioramos/alert_wpp_zabbix/blob/main/config_ambiente.sh).
4. Após a configuração, o sistema estará acessível via URL: [http://localhost/api-docs/](http://localhost/api-docs/).
5. Iremos importar o arquivo [postman_collection Referente a esse projeto](https://github.com/marcilioramos/alert_wpp_zabbix/blob/main/WPPConnect%20API%20REST.postman_collection.json)
6. Alimente as variáveis no postman.
7. Scaneie o QRCode com um conta valida no whatsapp
8. Copie o token e cole no codigo que deve estar no diretorio de scripts de alertas do zabbix.
9. Preencha as variáveis do script:
    - `token = 'token'`
    - `ip_wpp = 'ip'`
    - `ip_zabbix_web = 'ip zabbix'`
    - `zbx_user = 'usuario'` (verificar permissões)
    - `zbx_pass = 'senha'`

10. Crie a midia no Zabbix com o nome do script.
    - Use esse modelo de mensagem:
    ![image](https://github.com/marcilioramos/alert_wpp_zabbix/assets/48597831/92194b00-4586-4e5f-961a-391285b152b3)

    - **Note a primeira linha "ON#{TRIGGER.ID}#True#{ITEM.ID}#FF0000#900#200#{HOST.HOST}", ela é que irá alimentar as variáveis do script e todas são separadas por um #, segue o significado delas:**
      - `ON/OFF` = Com ou sem gráfico
      - `{TRIGGER.ID}`
      - `True/False` = True = envio para grupo False = envio para usuário
      - `{ITEM.ID}` = Item ID
      - `FF0000` = Cor do gráfico
      - `900` = Largura do Gráfico
      - `200` = Altura do Gráfico
      - `{HOST.HOST}` = HostName

11. Associe a midia a um usuário e depois a um alerta.
12. O número precisa estar no formato:
    - Usuário: `55"DDD""numero-do-usuario"`
    - Grupo: `precisará buscar via API, com o Método "GET All Groups"`
14. Teste o envio :-)
15. Qualquer dúvida, siga o vídeo do meu canal do youtube: https://www.youtube.com/watch?v=xgxF6CEPJws

## Creditos
https://github.com/sansaoipb/Graphical_notifications_Zabbix

