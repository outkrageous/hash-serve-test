from framework.hashserve import HashServe

# If I were really building this out I'd add a platform handler for
# windows systems that extends HashServe


class WindowsHashserve(HashServe):
    def __init__(self, ip, port, path):  # Add default values here to make it easier to consume
        super().__init__(ip=ip, port=port, path_to_exe=path)
        pass

    """Implement windows specific functions here and they will override HashServe functions"""

    def launch(self):
        # windows way to launch
        pass

    def _set_port(self):
        # windows way to set the port
        pass


"""
Hypothetically this factory would detect the local os and give me the right object
"""
class HashServeFactory():
    def __init__(self):
        pass

    def current_os(self):
        """find current os"""
        pass

    def get_hashserve(self):
        """based on current os conditionally return WindowsHashserve or Hashserve"""
        pass


