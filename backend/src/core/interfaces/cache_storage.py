from abc import ABC, abstractmethod


class ICacheStorage(ABC):
    @abstractmethod
    def set_value(self, key, value, expiration=None):
        """Set a value in the cache with an optional expiration."""
        pass

    @abstractmethod
    def get_value(self, key):
        """Get a value from the cache."""
        pass

    @abstractmethod
    def delete_value(self, key):
        """Delete a value from the cache."""
        pass

    @abstractmethod
    def publish(self, channel, message):
        """Publish a message to a channel."""
        pass

    @abstractmethod
    def subscribe(self, channel, callback):
        """Subscribe to a channel. The callback function is called when a message is published to the channel."""
        pass

    @abstractmethod
    def unsubscribe(self, channel):
        """Unsubscribe from a channel."""
        pass
