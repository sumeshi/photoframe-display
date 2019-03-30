# coding: utf-8
import yaml
from pathlib import Path

from usb import core

class Config(object):
    def __init__(self, config_file_path: str):
        self.config_file_path = config_file_path
        conf = self.load_yaml()
        self.id_vender = conf['id_vender']
        self.id_product = conf['id_product']

    def load_yaml(self) -> dict:
        text = Path(self.config_file_path).read_text()
        return yaml.load(text, Loader=yaml.SafeLoader)


def main():
    CONFIG = Config('./config.yml')
    dev = core.find(idVendor=CONFIG.id_vender, idProduct=CONFIG.id_product)

    if dev is None:
        print(*map(lambda dev: dev, core.find(find_all=True)))
        raise ValueError('Device not found')

    dev.detach_kernel_driver(0)
    dev.attach_kernel_driver(0)


if __name__ == '__main__':
    main()
