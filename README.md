## Doações 
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

1. Provisione a VM.
2. Instale o sistema [WppConnect](https://wppconnect.io/pt-BR/) para habilitar a API do WhatsApp.
   - O WppConnect permite o uso do WhatsApp em um navegador Google Chrome com NodeJS. Para mais detalhes, consulte a documentação oficial.
   
3. Para configurar o sistema, execute o script disponível em [config_ambiente.sh](https://github.com/marcilioramos/alert_wpp_zabbix/blob/main/config_ambiente.sh).
4. Após a configuração, o sistema estará acessível via URL: [http://localhost/api-docs/](http://localhost/api-docs/).
5. Iremos importar o arquivo [postman_collection Referente a esse projeto](https://github.com/marcilioramos/alert_wpp_zabbix/blob/main/WPPConnect%20API%20REST.postman_collection.json)
6. E depois seguir as instruções no video de meu canal.
