import configparser

def import_settings(*args, **kwargs):
    filepath = kwargs.get('filepath')
    if not filepath:
        if platform.system() == "Windows":
            filepath = os.path.dirname(os.path.realpath(__file__)) + "\keebalert.conf"
        elif platform.system() == "Linux":
            filepath = os.path.dirname(os.path.realpath(__file__)) + "/keebalert.conf"
