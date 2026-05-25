from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Label
import cpuinfo

class CpuPage(Vertical):

    def compose(self) -> ComposeResult:

        cache_info = self.__get_cache_info()
        yield Label(f"Unidade de processamento: {self.__get_cpu_info()}")
        yield Label(f"Número de núcleos: {self.__get_cpu_cores()}")
        yield Label(f"""Cache:
- Nível 1: {cache_info['L1']}
- Nível 2: {cache_info['L2']}
- Nível 3: {cache_info['L3']}""")
        yield Label (f"Clock base: {self.__get_cpu_clock()}")
        yield Label (f"Clock atual: {self.__get_cpu_actual_clock()}")




    def on_mount(self) -> None:
        self.set_interval(0.5, self.__get_cpu_actual_clock)


    def __get_cpu_info(self) -> str:
        cpu_name = cpuinfo.get_cpu_info()['brand_raw']
        return cpu_name

    def __get_cpu_cores(self) -> str:
        return cpuinfo.get_cpu_info()['count']

    def __get_cpu_clock(self) -> str:
        return cpuinfo.get_cpu_info().get('hz_advertised_friendly', 'N/A')

    def __get_cpu_actual_clock(self) -> str:
        return cpuinfo.get_cpu_info().get('hz_actual_friendly', 'N/A')

    def __get_cache_info(self) -> str:
        cache_info_dict = {
            'L1': cpuinfo.get_cpu_info().get('l1_data_cache_size', 'N/A'),
            'L2': cpuinfo.get_cpu_info().get('l2_cache_size', 'N/A'),
            'L3': cpuinfo.get_cpu_info().get('l3_cache_size', 'N/A')
        }
        return cache_info_dict
    
