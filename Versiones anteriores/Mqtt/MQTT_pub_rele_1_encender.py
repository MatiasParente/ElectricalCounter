import paho.mqtt.client as mqtt

client = mqtt.Client()
client.connect("prueba12345.fastddns.org", 1883, 1)
client.publish("controlar_reles", "1**")

