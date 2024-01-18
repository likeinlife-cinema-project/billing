import services.consumer as consumer
import services.producer as producer
from resolver import type_resolver, user_resolver
from services.sender import smtp_sender, test_sender

from .container import Container


def setup():
    container = Container()
    container.init_resources()
    container.wire(
        modules=[
            producer,
            smtp_sender,
            test_sender,
            consumer,
            type_resolver,
            user_resolver,
        ],
    )
