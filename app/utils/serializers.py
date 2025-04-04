from sqlalchemy.types import TypeDecorator, JSON


class JSONSerializable(TypeDecorator):
    impl = JSON
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is not None:
            return self._make_serializable(value)
        return None

    def _make_serializable(self, obj):
        if hasattr(obj, "__dict__"):
            return str(obj)
        elif isinstance(obj, dict):
            return {k: self._make_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._make_serializable(i) for i in obj]
        return obj

    def __repr__(self):
        return "JSONSerializable"


def make_json_serializable(obj):
    def _make_serializable(obj):
        if hasattr(obj, "__dict__"):
            return str(obj)
        elif isinstance(obj, dict):
            return {k: _make_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [_make_serializable(i) for i in obj]
        return obj

    return _make_serializable(obj)
