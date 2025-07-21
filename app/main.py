import logging
import time
from make87_messages.core.header_pb2 import Header
from make87_messages.text.text_plain_pb2 import PlainText
from make87.encodings import ProtobufEncoder
from make87.interfaces.zenoh import ZenohInterface

logging.Formatter.converter = time.gmtime
logging.basicConfig(
    format="[%(asctime)sZ %(levelname)s  %(name)s] %(message)s", level=logging.INFO, datefmt="%Y-%m-%dT%H:%M:%S"
)


def main():
    message_encoder = ProtobufEncoder(message_type=PlainText)
    zenoh_interface = ZenohInterface(name="zenoh")

    querier = zenoh_interface.get_querier("message_endpoint")
    header = Header(entity_path="/pytest/req_prv", reference_id=0)

    while True:
        header.timestamp.GetCurrentTime()
        message = PlainText(header=header, body="Hello, World! 🐍")
        message_encoded = message_encoder.encode(message)
        response = querier.get(payload=message_encoded)
        for r in response:
            if r.ok is not None:
                response_message = message_encoder.decode(r.ok.payload.to_bytes())
                logging.info(f"Received response: {response_message.body}")
            else:
                logging.error(f"Received error: {r.err.payload.to_string()}")

        time.sleep(1)


if __name__ == "__main__":
    main()
