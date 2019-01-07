![](img/Diagram.png)

1. Message LoRaWAN envoyé par le waspmote à TTN (1 par 30 secondes) contenant 3 valeurs de l’accéléromètre (x, y et z) et l’état de la LED1 en hexadécimal. 

   * Message en hexadécimal : 

     x : 16 bits, y 16 bits, z 16 bits et led state 8 bits. 

   * Exemple :  `04 82 FF 97 00 5F 00 01`

   * En arrivant dans le portail de TTN, ce message sera décodé (Payload Format decoder) et retourné en format JSON :

   ```json
   {"led_state": 1, "x_acc": 1154, "y_acc": -105, "z_acc": 95}
   ```

2. Message MQTT envoyé par ESP32 (1 pat minute) contenant la valeur du capteur de température en degré Celsius. Exemple JSON :

   ```json
   {"Name": "Inside", "temp": 24.2}
   ```

3. Lors de la réception de données du waspmote, une action est lancée avec la *Rule query statement* suivante (concerne l'accéléromètre) :

   ```mysql
   SELECT dev_id, payload_fields.x_acc AS x_acc, payload_fields.y_acc AS y_acc, payload_fields.z_acc AS z_acc, timestamp() AS Time FROM 'iot_2018_19_abdennadher_gindre/devices/waspmote_0/up'
   ```

   Cette action va lancer un script d'une fonction *Lambda* qui recevera les données sous forme JSON. Exemple :

   ```json
   {"dev_id": "waspmote_0", "x_acc": 1154, "y_acc": -105, "z_acc": 95, "Time": 1546533762406}
   ```

   ![](img/accelero.png)

4. Lors de la réception de données du waspmote, une autre action est lancée avec la *Rule query statement* suivante (concerne l'état de la LED) :

   ```mysql
   SELECT payload_fields.led_state AS led_state FROM 'iot_2018_19_abdennadher_gindre/devices/waspmote_0/up'
   ```

   Cette action va lancer un script d'une fonction *Lambda* qui recevera les données sous forme JSON. Exemple :

   ```json
   {"led_state": "1"}
   ```

   ![](img/led.png)

