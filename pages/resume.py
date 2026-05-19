import platform
import wmi
import cpuinfo
import psutil
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Label, ProgressBar

class ResumePage(Vertical):

    def compose(self) -> ComposeResult:
        yield Label(f"Arquitetura: {platform.machine()}")
        yield Label(f"Sistema Operacional: {platform.system()} {platform.release()}")
        yield Label(f"Unidade de Processamento: {self.__get_cpu_info()}")
        yield Label(f"Placa(s) de vídeo: {self.__get_gpu_info()}")
        yield Label(f"Placa mãe: {self.__get_motherboard_info()}")
        yield Label(f"Memória RAM: {self.__get_ram_info()}")
        yield Label(f"Memória Secundária: {self.__get_storage_wmi()}")
        # Yield any other widgets you want on this page here!

        yield Label("\nUso de CPU:")
        yield ProgressBar(total=100, show_eta=False, id="cpu_bar")
        
        yield Label("Uso de RAM:")
        yield ProgressBar(total=100, show_eta=False, id="ram_bar")


    def on_mount(self) -> None:
        self.set_interval(0.5, self.__update_bars)

    def __update_bars(self) -> None:
        cpu_usage = psutil.cpu_percent()
        ram_usage = psutil.virtual_memory().percent

        cpu_bar = self.query_one("#cpu_bar", ProgressBar)
        ram_bar = self.query_one("#ram_bar", ProgressBar)

        cpu_bar.update(progress=cpu_usage)
        ram_bar.update(progress=ram_usage)

        self.__update_bars_colors(cpu_bar, cpu_usage)
        self.__update_bars_colors(ram_bar, ram_usage)

    def __update_bars_colors(self, bar: ProgressBar, percent: float) -> None:
        bar.remove_class("low", "medium", "high")

        if percent < 25:
            bar.add_class("low")
        elif percent >= 25 and percent < 75:
            bar.add_class("medium")
        elif percent >= 75:
            bar.add_class("high")

    def __get_cpu_info(self) -> str:
        return cpuinfo.get_cpu_info()['brand_raw']
    
    def __get_gpu_info(self) -> str:

        # class MockGPU:
        #     def __init__(self, name):
        #         self.Name = name
                
        # gpus = [
        #     MockGPU("AMD Radeon RX 6700 XT"),
        #     # MockGPU("NVIDIA GeForce RTX 3060")
        # ]
        w = wmi.WMI()
        gpus = w.Win32_VideoController()
        
        if len(gpus) == 1:
            return f"{gpus[0].Name}"

        else:
            return "".join([f"\n - {gpu.Name}" for gpu in gpus])
    
    def __get_ram_info(self) -> str:
        ram = psutil.virtual_memory()
        return f"{ram.total / (1024 ** 3):.0f} GB"
    
    def __get_motherboard_info(self) -> str:
        w = wmi.WMI()
        mb = w.Win32_BaseBoard()[0]
        return mb.Product
    
    # # def __get_total_storage_info(self) -> str:
    #     partitions = psutil.disk_partitions()

    #     for partition in partitions:
    #         disk = psutil.disk_usage(partition.mountpoint)
    #         total = disk.total / (1024 ** 3)
    #         return f"{total:.0f} GB" 
        
    def __get_storage_wmi(self) -> str:

        info_list= []

        w = wmi.WMI()
        disks = w.Win32_DiskDrive()
        for disk in disks:
            size = int(disk.Size) / (1024 ** 3)
            info_list.append(f"\n - Modelo: {disk.Model} | Capacidade: {size:.0f} GB")

        return "".join(info_list)