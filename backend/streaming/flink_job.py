
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors.kafka import KafkaSource, KafkaSink, KafkaRecordSerializationSchema, KafkaOffsetsInitializer
from pyflink.common.serialization import SimpleStringSchema
from pyflink.common import WatermarkStrategy
import json

def process_event(event_str):
    try:
        event = json.loads(event_str)
        print(f"PROCESSING: {event['event_type']} - Payload: {event['payload']}")
        # In a real scenario, this would update a database or call an external API.
        # For now, we just log to stdout which appears in Flink TaskManager logs.
        return json.dumps({"status": "processed", "original": event})
    except Exception as e:
        return json.dumps({"error": str(e)})

def main():
    env = StreamExecutionEnvironment.get_execution_environment()
    env.set_parallelism(1)

    # Kafka Connections
    # Note: Requires flink-sql-connector-kafka jar to be present in Flink lib/
    
    source = KafkaSource.builder() \
        .set_bootstrap_servers("kafka:29092") \
        .set_topics("capital_connect_events") \
        .set_group_id("flink_processor_group") \
        .set_starting_offsets(KafkaOffsetsInitializer.earliest()) \
        .set_value_only_deserializer(SimpleStringSchema()) \
        .build()

    stream = env.from_source(source, WatermarkStrategy.no_watermarks(), "Kafka Source")

    # Simple processing
    processed_stream = stream.map(process_event)

    processed_stream.print()

    env.execute("CapitalConnectEventProcessor")

if __name__ == '__main__':
    main()
