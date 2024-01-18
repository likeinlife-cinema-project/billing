from typing import Any, Callable, Coroutine, TypeAlias

from models.queue_message import UserProvidedQueueMessage

SenderType: TypeAlias = Callable[[UserProvidedQueueMessage], Coroutine[Any, Any, bool]]
