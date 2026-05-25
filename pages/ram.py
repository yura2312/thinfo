from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Label
import psutil
import cpuinfo

# TODO: Adicionar mais informações sobre a RAM, como tipo, frequência, etc. (talvez usando wmi para Windows)

class RamPage(Vertical):

    def compose(self) -> ComposeResult:

        yield Label(f"Memória RAM total: {self.__get_ram_info()}")
        yield Label(f"Porcentagem de uso: {self.__get_ram_usage()}%")
        yield Label(f"Memória RAM disponível: {self.__get_ram_available():.2f} GB")

        yield Label(f"Memoria swap total: {self.__get_swap_info():.2f} GB")



    def on_mount(self) -> None:
        self.set_interval(0.5, self.__get_ram_usage)


    def __get_ram_info(self) -> str:
        ram = psutil.virtual_memory()
        return f"{ram.total / (1024 ** 3)} GB"

    def __get_ram_usage(self) -> float:
        ram = psutil.virtual_memory()
        return ram.percent

    def __get_ram_available(self) -> float:
        ram = psutil.virtual_memory()
        return ram.available / (1024 ** 3)
    
    def __get_swap_info(self) -> float:
        swap = psutil.swap_memory()
        return swap.total / (1024 ** 3)