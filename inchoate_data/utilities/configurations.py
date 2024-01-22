class Configurations:
    def __init__(self, data):
        """_summary_

        Args:
            data (_type_): _description_
        """
        self._data = data
        for key, value in data.items():
            if isinstance(value, dict):
                setattr(self, key, Configurations(value))
            else:
                setattr(self.__class__, key, property(self.getter(key), self.setter(key)))

    def getter(self, key):
        def get_property(self):
            return self._data.get(key, None)
        return get_property

    def setter(self, key):
        def set_property(self, value):
            # You can add validation or processing logic here if needed

            # Check if the property exists
            if key not in self._data:
                raise AttributeError(f"'Configurations' object has no attribute '{key}'")

            # Check if the value is an instance of Configurations or None
            if not isinstance(value, Configurations) and value is not None:
                raise ValueError(f"The value for the nested key '{key}' must be an instance of Configurations or None.")

            self._data[key] = value

        return set_property
