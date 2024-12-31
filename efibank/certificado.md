Sobre o Certificado

1. O que é o certificado?
   O certificado utilizado neste projeto é um arquivo `.pem` que contém as credenciais de segurança necessárias para autenticar a comunicação entre sua aplicação e a API da EfiPay.

2. Onde obtê-lo?
   O certificado deve ser fornecido pela EfiPay após o registro e configuração da sua conta. Você pode obter o certificado no painel administrativo da EfiPay ou entrando em contato com o suporte.

3. Como usar o certificado?
   - Salve o arquivo `.pem` no diretório `./database/`.
   - Certifique-se de que o caminho para o certificado está corretamente configurado no script, como no exemplo:
     ```
     'certificate': './database/certificado-combinado.pem'
     ```

4. Como gerar ou combinar certificados?
   Caso você possua um certificado `.p12`, é necessário convertê-lo para `.pem`. Aqui está um exemplo de comando para realizar a conversão utilizando o OpenSSL:
   - Converter `.p12` para `.pem`:
     ```
     openssl pkcs12 -in seu-certificado.p12 -out certificado.pem -nodes
     ```

5. Configuração de permissões
   Certifique-se de que o arquivo `.pem` tenha permissões adequadas para que o script possa acessá-lo. Um exemplo seria:
chmod 600 ./database/certificado-combinado.pem

6. Problemas comuns
- Certificado inválido: Verifique se o arquivo não está corrompido e se contém tanto a chave privada quanto o certificado.
- Senha no certificado: Caso o certificado exija uma senha, remova-a ou ajuste o script para lidar com a senha.

7. Segurança
- Nunca compartilhe o arquivo do certificado publicamente ou o armazene em repositórios públicos.
- Garanta que ele está em um local seguro e acessível apenas pela aplicação.
