
import json
import os
from kafka import KafkaProducer
from threading import Thread
import time

KAFKA_BROKER = os.getenv("KAFKA_BROKER", "localhost:9092")

class EventProducer:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EventProducer, cls).__new__(cls)
            cls._instance.producer = None
            cls._instance.connect()
        return cls._instance

    def connect(self):
        def _connect_loop():
            while not self.producer:
                try:
                    self.producer = KafkaProducer(
                        bootstrap_servers=KAFKA_BROKER,
                        value_serializer=lambda v: json.dumps(v).encode('utf-8')
                    )
                    print("Connected to Kafka")
                except Exception as e:
                    print(f"Failed to connect to Kafka ({e}), retrying in 5s...")
                    time.sleep(5)
        
        # Connect in background to avoid blocking startup if Kafka is slow
        Thread(target=_connect_loop, daemon=True).start()

    def send_event(self, topic: str, event_type: str, payload: dict):
        if self.producer:
            try:
                message = {
                    "event_type": event_type,
                    "payload": payload,
                    "timestamp": time.time()
                }
                self.producer.send(topic, value=message)
                self.producer.flush() 
                print(f"Sent event {event_type} to {topic}")
            except Exception as e:
                print(f"Error sending event: {e}")
        else:
            print(f"Kafka producer not ready. Dropped event {event_type}")

producer = EventProducer()
