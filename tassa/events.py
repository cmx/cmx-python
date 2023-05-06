from tassa.schemas import Element


class Event:
    """
    An event is a message sent from the server to the client.
    """

    def __eq__(self, etype):
        """
        Check if the event is of a certain type.
        :param etype: The type to check.
        :return: True if the event is of the given type, False otherwise.
        """
        return self.etype == etype


class ClientEvent(Event):
    def __init__(self, etype=None, **kwargs):
        self.etype = etype
        self.__dict__.update(kwargs)

        if self == "UPLOAD":
            import base64
            import io
            from PIL import Image

            image = Image.open(io.BytesIO(base64.b64decode(self.value)))
            self.value = image


class NullEvent(ClientEvent):
    def __init__(self, **kwargs):
        super().__init__(etype="NULL", **kwargs)


# class Meta(type):
#     def __matmul__(cls, data):
#         instance = cls.__new__(cls)
#         return cls.__init__(instance, data)

from typing import Sequence


def serializer(data):
    if hasattr(data, "serialize"):
        return data.serialize()

    if isinstance(data, str):
        # return Text(data)
        return data

    # this could be dangerous.
    if isinstance(data, Sequence):
        return [serializer(d) for d in data]

    # this could be dangerous
    if isinstance(data, dict):
        return {k: serializer(v) for k, v in data.items()}

    NotImplementedError(f"Cannot serialize {data}")


class ServerEvent(Event):  # , metaclass=Meta):
    def __init__(self, data, **kwargs):
        self.data = data
        self.__dict__.update(etype=self.etype, **kwargs)

    def serialize(self):
        """
        Serialize the event to a dictionary for sending over the websocket.
        :return: A dictionary representing the event.
        """
        # Sequence includes text
        return {**self.__dict__, "data": serializer(self.data)}


class Noop(ServerEvent):
    etype = "NOOP"

    def __init__(self, **kwargs):
        super().__init__(data=None, **kwargs)


NOOP = Noop()


class Set(ServerEvent):
    """
    A Set ServerEvent is sent to the client when the client first connects to the server.
    It replaces the client's current state with the state sent in the Set ServerEvent.
    """

    etype = "SET"

    def __init__(self, data: Element, **kwargs):
        super().__init__(data, **kwargs)


class Update(ServerEvent):
    """
    An Update ServerEvent is sent to the client when the server wants to update the client's state.
    It appends the data sent in the Update ServerEvent to the client's current state.
    """

    etype = "UPDATE"

    def __init__(self, *elements, data: Element = None, **kwargs):
        # tuple is not serializable
        elements = [*elements, data] if data else list(elements)
        super().__init__(elements, **kwargs)


class Frame(ServerEvent):
    """
    A higher-level ServerEvent that wraps other ServerEvents
    """

    ServerEvent: ServerEvent
    etype = "FRAME"

    def __init__(self, data: ServerEvent, **kwargs):
        super().__init__(data, **kwargs)


class End(ServerEvent):
    """
    A higher-level ServerEvent that wraps other ServerEvents
    """

    etype = "TERMINATE"

    def __init__(self, **kwargs):
        super().__init__(None, **kwargs)


END = End()

# if __name__ == "__main__":
#     e = Frame @ {"hey": "yo"}
#     print(e)
#     print(e.data)
#
#     e = Set @ {"data": "new"}
#     print(e.serialize())
