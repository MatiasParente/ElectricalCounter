import paho.mqtt.client as mqtt

client = mqtt.Client()
client.connect("192.168.169.2", 1883, 1)
client.publish("controlar_reles", "**1")
