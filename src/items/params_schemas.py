from pydantic import BaseModel, Field
from datetime import date
from typing import List, Optional


# === Модели электроники ===

class SmartphoneParams(BaseModel):
    brand: str = Field(..., description="Производитель устройства")
    model: str = Field(..., description="Модель устройства")
    release_date: str = Field(..., description="Дата релиза (строка, например '2022-09-16')")
    screen_size: float = Field(..., description="Диагональ экрана в дюймах")
    battery_capacity: int = Field(..., description="Ёмкость батареи в мА·ч")
    ram: int = Field(..., description="Оперативная память в ГБ")
    storage: int = Field(..., description="Встроенная память в ГБ")
    camera_megapixels: float = Field(..., description="Разрешение основной камеры в мегапикселях")
    os: str = Field(..., description="Операционная система")
    connectivity: List[str] = Field(..., description="Список поддерживаемых соединений, напр. ['4G','5G','WiFi']")


class LaptopParams(BaseModel):
    brand: str = Field(..., description="Производитель")
    model: str = Field(..., description="Модель")
    release_date: date = Field(..., description="Дата релиза (YYYY-MM-DD)")
    cpu: str = Field(..., description="Модель процессора")
    gpu: Optional[str] = Field(None, description="Модель видеокарты, если есть")
    ram: int = Field(..., description="Оперативная память в ГБ")
    storage: int = Field(..., description="Объём накопителя в ГБ")
    screen_size: float = Field(..., description="Диагональ экрана в дюймах")
    weight: float = Field(..., description="Вес в килограммах")
    battery_life: Optional[float] = Field(None, description="Время работы от батареи в часах (если известно)")
    os: str = Field(..., description="Операционная система")


class TabletParams(BaseModel):
    brand: str = Field(..., description="Производитель")
    model: str = Field(..., description="Модель")
    release_date: date = Field(..., description="Дата релиза")
    screen_size: float = Field(..., description="Диагональ экрана в дюймах")
    battery_capacity: int = Field(..., description="Ёмкость батареи в мА·ч")
    ram: int = Field(..., description="Оперативная память в ГБ")
    storage: int = Field(..., description="Встроенная память в ГБ")
    os: str = Field(..., description="Операционная система")
    stylus_support: bool = Field(False, description="Поддержка стилуса (True/False)")


class MonitorParams(BaseModel):
    brand: str = Field(..., description="Производитель")
    model: str = Field(..., description="Модель")
    release_date: Optional[date] = Field(None, description="Дата релиза (если известна)")
    size: float = Field(..., description="Диагональ в дюймах")
    resolution: str = Field(..., description="Разрешение, напр. '1920x1080'")
    refresh_rate: int = Field(..., description="Частота обновления в Гц")
    panel_type: Optional[str] = Field(None, description="Тип матрицы (IPS/VA/TN и т.д.)")
    ports: List[str] = Field(..., description="Список портов, напр. ['HDMI','DP']")


class TVParams(BaseModel):
    brand: str = Field(..., description="Производитель")
    model: str = Field(..., description="Модель")
    release_date: Optional[date] = Field(None, description="Дата релиза (если есть)")
    size: float = Field(..., description="Диагональ телевизора в дюймах")
    resolution: str = Field(..., description="Разрешение экрана")
    smart_tv: bool = Field(False, description="Является ли Smart TV")
    hdmi_ports: int = Field(..., description="Количество HDMI-портов")
    hdr_supported: bool = Field(False, description="Поддержка HDR")


class PCParams(BaseModel):
    brand: Optional[str] = Field(None, description="Производитель (опционально)")
    model: Optional[str] = Field(None, description="Модель (опционально)")
    cpu: str = Field(..., description="Процессор")
    gpu: Optional[str] = Field(None, description="Видеокарта (опционально)")
    ram: int = Field(..., description="Оперативная память в ГБ")
    storage: int = Field(..., description="Объём накопителя в ГБ")
    form_factor: Optional[str] = Field(None, description="Форм-фактор корпуса (ATX/Mini-ITX и т.п.)")


class GamingConsoleParams(BaseModel):
    brand: str = Field(..., description="Производитель")
    model: str = Field(..., description="Модель")
    release_date: date = Field(..., description="Дата релиза")
    cpu: str = Field(..., description="Процессор консоли")
    gpu: str = Field(..., description="Графический процессор консоли")
    ram: int = Field(..., description="Оперативная память в ГБ")
    storage: int = Field(..., description="Встроенная память в ГБ")
    max_resolution: str = Field(..., description="Максимальное поддерживаемое разрешение")
    optical_drive: bool = Field(False, description="Наличие оптического привода")


class VRHeadsetParams(BaseModel):
    brand: str = Field(..., description="Производитель")
    model: str = Field(..., description="Модель")
    release_date: Optional[date] = Field(None, description="Дата релиза (если известна)")
    resolution_per_eye: str = Field(..., description="Разрешение на глаз, напр. '1832x1920'")
    refresh_rate: int = Field(..., description="Частота обновления в Гц")
    tracking: List[str] = Field(..., description="Типы отслеживания, напр. ['inside-out']")
    standalone: bool = Field(False, description="Является ли автономным устройством")


class CameraParams(BaseModel):
    brand: str = Field(..., description="Производитель")
    model: str = Field(..., description="Модель")
    sensor_type: str = Field(..., description="Тип сенсора, напр. 'CMOS'")
    resolution_megapixels: float = Field(..., description="Разрешение сенсора в мегапикселях")
    lens_mount: Optional[str] = Field(None, description="Крепление объектива (если применимо)")
    video_resolution: Optional[str] = Field(None, description="Макс. разрешение видео, напр. '4K'")


class RouterParams(BaseModel):
    brand: str = Field(..., description="Производитель")
    model: str = Field(..., description="Модель")
    wifi_standard: List[str] = Field(..., description="Поддерживаемые стандарты Wi‑Fi, напр. ['802.11ax']")
    lan_ports: int = Field(..., description="Количество LAN-портов")
    wan_ports: int = Field(..., description="Количество WAN-портов")
    supports_guest_network: bool = Field(False, description="Поддержка гостевой сети")


class SmartwatchParams(BaseModel):
    brand: str = Field(..., description="Производитель")
    model: str = Field(..., description="Модель")
    release_date: Optional[date] = Field(None, description="Дата релиза (если есть)")
    os: str = Field(..., description="Операционная система часов")
    battery_life_days: Optional[float] = Field(None, description="Время работы в днях")
    water_resistant: bool = Field(False, description="Водонепроницаемость (True/False)")


class FitnessTrackerParams(BaseModel):
    brand: str = Field(..., description="Производитель")
    model: str = Field(..., description="Модель")
    heart_rate_monitor: bool = Field(True, description="Наличие датчика сердечного ритма")
    gps: bool = Field(False, description="Наличие GPS")
    battery_life_days: Optional[float] = Field(None, description="Время работы в днях")


class DroneParams(BaseModel):
    brand: str = Field(..., description="Производитель")
    model: str = Field(..., description="Модель")
    max_flight_time: float = Field(..., description="Максимальное время полета в минутах")
    max_range: float = Field(..., description="Максимальная дальность полёта в километрах")
    camera_resolution: Optional[float] = Field(None, description="Разрешение камеры в мегапикселях (если есть)")


class VRControllerParams(BaseModel):
    brand: str = Field(..., description="Производитель")
    model: str = Field(..., description="Модель")
    tracking_type: str = Field(..., description="Тип отслеживания контроллера")
    battery_type: str = Field(..., description="Тип батареи")


class ARGlassesParams(BaseModel):
    brand: str = Field(..., description="Производитель")
    model: str = Field(..., description="Модель")
    display_type: str = Field(..., description="Тип дисплея (waveguide, microLED и т.д.)")
    field_of_view: float = Field(..., description="Угол обзора в градусах")


class Printer3DParams(BaseModel):
    brand: str = Field(..., description="Производитель")
    model: str = Field(..., description="Модель")
    technology: str = Field(..., description="Технология печати, напр. 'FDM' или 'SLA'")
    build_volume: str = Field(..., description="Рабочий объём, напр. '220x220x250 mm'")
    layer_resolution: Optional[float] = Field(None, description="Высота слоя в микронах (если указана)")


# === Бытовая техника ===

class RefrigeratorParams(BaseModel):
    brand: str = Field(..., description="Производитель")
    model: str = Field(..., description="Модель")
    capacity_liters: int = Field(..., description="Объём внутреннего пространства в литрах")
    energy_rating: Optional[str] = Field(None, description="Класс энергоэффективности")
    has_freezer: bool = Field(True, description="Наличие морозильной камеры")
    dimensions_mm: Optional[str] = Field(None, description="Габариты W x D x H в мм")


class FreezerParams(BaseModel):
    brand: str = Field(..., description="Производитель")
    model: str = Field(..., description="Модель")
    capacity_liters: int = Field(..., description="Объём в литрах")
    type: Optional[str] = Field(None, description="Тип: 'Upright' или 'Chest'")
    energy_rating: Optional[str] = Field(None, description="Класс энергоэффективности")
    dimensions_mm: Optional[str] = Field(None, description="Габариты в мм")


class WashingMachineParams(BaseModel):
    brand: str = Field(..., description="Производитель")
    model: str = Field(..., description="Модель")
    load_capacity_kg: float = Field(..., description="Максимальная загрузка в килограммах")
    spin_speed_rpm: Optional[int] = Field(None, description="Максимальная скорость отjима в об/мин")
    type: Optional[str] = Field(None, description="Тип: 'Front-loading' или 'Top-loading'")
    energy_rating: Optional[str] = Field(None, description="Класс энергоэффективности")


class DishwasherParams(BaseModel):
    brand: str = Field(..., description="Производитель")
    model: str = Field(..., description="Модель")
    place_settings: int = Field(..., description="Число комплектов посуды (place settings)")
    energy_rating: Optional[str] = Field(None, description="Класс энергоэффективности")
    noise_level_db: Optional[float] = Field(None, description="Уровень шума в децибелах")


class MicrowaveParams(BaseModel):
    brand: str = Field(..., description="Производитель")
    model: str = Field(..., description="Модель")
    capacity_liters: int = Field(..., description="Объём камеры в литрах")
    power_watts: int = Field(..., description="Мощность в ваттах")
    has_grill: bool = Field(False, description="Наличие гриля")
    dimensions_mm: Optional[str] = Field(None, description="Габариты в мм")


class OvenParams(BaseModel):
    brand: str = Field(..., description="Производитель")
    model: str = Field(..., description="Модель")
    capacity_liters: int = Field(..., description="Объём духовки в литрах")
    fuel_type: Optional[str] = Field(None, description="Тип топлива: 'Electric' или 'Gas'")
    has_convection: bool = Field(False, description="Наличие конвекции")
    dimensions_mm: Optional[str] = Field(None, description="Габариты в мм")


class CoffeeMakerParams(BaseModel):
    brand: str = Field(..., description="Производитель")
    model: str = Field(..., description="Модель")
    type: Optional[str] = Field(None, description="Тип: 'Drip', 'Espresso', 'Pod' и т.д.")
    water_tank_capacity_ml: Optional[int] = Field(None, description="Объём бака для воды в мл")
    programmable: bool = Field(False, description="Наличие программируемых функций")


class BlenderParams(BaseModel):
    brand: str = Field(..., description="Производитель")
    model: str = Field(..., description="Модель")
    power_watts: int = Field(..., description="Мощность в ваттах")
    capacity_liters: float = Field(..., description="Объём в литрах")
    number_of_speeds: Optional[int] = Field(None, description="Число скоростей")


class ToasterParams(BaseModel):
    brand: str = Field(..., description="Производитель")
    model: str = Field(..., description="Модель")
    slots: int = Field(..., description="Число слотов для тостов")
    browning_levels: int = Field(..., description="Уровни поджаривания")


class KettleParams(BaseModel):
    brand: str = Field(..., description="Производитель")
    model: str = Field(..., description="Модель")
    capacity_liters: float = Field(..., description="Объём в литрах")
    power_watts: int = Field(..., description="Мощность в ваттах")
    auto_shutoff: bool = Field(True, description="Автоматическое отключение после закипания")


class JuicerParams(BaseModel):
    brand: str = Field(..., description="Производитель")
    model: str = Field(..., description="Модель")
    type: Optional[str] = Field(None, description="Тип: 'Centrifugal' или 'Masticating'")
    power_watts: int = Field(..., description="Мощность в ваттах")
    pulp_ejection: bool = Field(False, description="Наличие механизма удаления мякоти")


class SlowCookerParams(BaseModel):
    brand: str = Field(..., description="Производитель")
    model: str = Field(..., description="Модель")
    capacity_liters: float = Field(..., description="Объём в литрах")
    programmable: bool = Field(False, description="Программируемый режим")
    number_of_heat_settings: Optional[int] = Field(None, description="Число температурных режимов")


class RiceCookerParams(BaseModel):
    brand: str = Field(..., description="Производитель")
    model: str = Field(..., description="Модель")
    capacity_cups: int = Field(..., description="Вместимость в чашках")
    keep_warm: bool = Field(True, description="Функция Поддержания тепла")
    programmable: bool = Field(False, description="Программируемая модель")


class BreadMakerParams(BaseModel):
    brand: str = Field(..., description="Производитель")
    model: str = Field(..., description="Модель")
    loaf_capacity_grams: int = Field(..., description="Вместимость буханки в граммах")
    programs: List[str] = Field(..., description="Список программ приготовления")
    crust_settings: Optional[List[str]] = Field(None, description="Настройки корочки (если есть)")


class FoodProcessorParams(BaseModel):
    brand: str = Field(..., description="Производитель")
    model: str = Field(..., description="Модель")
    power_watts: int = Field(..., description="Мощность в ваттах")
    attachments: List[str] = Field(..., description="Список насадок")


class AirFryerParams(BaseModel):
    brand: str = Field(..., description="Производитель")
    model: str = Field(..., description="Модель")
    capacity_liters: float = Field(..., description="Объём в литрах")
    power_watts: int = Field(..., description="Мощность в ваттах")
    temperature_range_c: Optional[str] = Field(None, description="Диапазон температур, напр. '80-200°C'")


class DeepFryerParams(BaseModel):
    brand: str = Field(..., description="Производитель")
    model: str = Field(..., description="Модель")
    capacity_liters: float = Field(..., description="Объём во фритюрнице в литрах")
    power_watts: int = Field(..., description="Мощность в ваттах")
    oil_capacity_liters: Optional[float] = Field(None, description="Ёмкость под масло в литрах")


class GrillParams(BaseModel):
    brand: str = Field(..., description="Производитель")
    model: str = Field(..., description="Модель")
    type: Optional[str] = Field(None, description="Тип: 'Electric', 'Gas' или 'Charcoal'")
    cooking_area_sqcm: Optional[int] = Field(None, description="Площадь приготовления в кв.см")


class BarbecueParams(BaseModel):
    brand: str = Field(..., description="Производитель")
    model: str = Field(..., description="Модель")
    type: Optional[str] = Field(None, description="Тип гриля")
    fuel_type: Optional[str] = Field(None, description="Тип топлива")
    cooking_area_sqcm: Optional[int] = Field(None, description="Площадь приготовления в кв.см")


class SmokerParams(BaseModel):
    brand: str = Field(..., description="Производитель")
    model: str = Field(..., description="Модель")
    fuel_type: Optional[str] = Field(None, description="Тип топлива")
    cooking_area_sqcm: Optional[int] = Field(None, description="Площадь приготовления в кв.см")
    temperature_control: bool = Field(False, description="Наличие контроля температуры")


class AirPurifierParams(BaseModel):
    brand: str = Field(..., description="Производитель")
    model: str = Field(..., description="Модель")
    coverage_area_sqm: float = Field(..., description="Площадь покрытия в кв.м")
    filters: List[str] = Field(..., description="Список фильтров, напр. ['HEPA','Carbon']")
    noise_level_db: Optional[float] = Field(None, description="Уровень шума в дБ")


class HumidifierParams(BaseModel):
    brand: str = Field(..., description="Производитель")
    model: str = Field(..., description="Модель")
    capacity_liters: float = Field(..., description="Емкость резервуара в литрах")
    output_mlh: Optional[int] = Field(None, description="Выход в мл/ч (если указан)")


class DehumidifierParams(BaseModel):
    brand: str = Field(..., description="Производитель")
    model: str = Field(..., description="Модель")
    capacity_liters_per_day: float = Field(..., description="Производительность по осушению в л/сут")
    coverage_area_sqm: Optional[float] = Field(None, description="Площадь обслуживания в кв.м")


class HeaterParams(BaseModel):
    brand: str = Field(..., description="Производитель")
    model: str = Field(..., description="Модель")
    type: Optional[str] = Field(None, description="Тип обогревателя: 'Convection','Radiant','Infrared'")
    power_watts: int = Field(..., description="Мощность в ваттах")


class FanParams(BaseModel):
    brand: str = Field(..., description="Производитель")
    model: str = Field(..., description="Модель")
    type: Optional[str] = Field(None, description="Тип: 'Ceiling','Standing','Table'")
    speeds: int = Field(..., description="Число скоростей")


class VacuumCleanerParams(BaseModel):
    brand: str = Field(..., description="Производитель")
    model: str = Field(..., description="Модель")
    type: Optional[str] = Field(None, description="Тип: 'Upright','Canister','Stick'")
    power_watts: int = Field(..., description="Потребляемая мощность в ваттах")
    bagless: bool = Field(True, description="Пылесос без мешка (True/False)")


class RobotVacuumParams(BaseModel):
    brand: str = Field(..., description="Производитель")
    model: str = Field(..., description="Модель")
    battery_life_min: int = Field(..., description="Время работы на одной зарядке в минутах")
    mapping: bool = Field(False, description="Наличие карты помещения")
    app_control: bool = Field(False, description="Управление через приложение")


# === Офис и периферия ===

class PrinterParams(BaseModel):
    brand: str = Field(..., description="Производитель")
    model: str = Field(..., description="Модель")
    type: Optional[str] = Field(None, description="Тип принтера: 'Laser','Inkjet','Thermal'")
    color: bool = Field(False, description="Цветная печать (True/False)")
    duplex: bool = Field(False, description="Двухсторонняя печать (True/False)")
    max_resolution_dpi: Optional[int] = Field(None, description="Максимальное разрешение в dpi")
    connectivity: List[str] = Field(default_factory=list, description="Способы подключения, напр. ['USB','WiFi']")


class ScannerParams(BaseModel):
    brand: str = Field(..., description="Производитель")
    model: str = Field(..., description="Модель")
    type: Optional[str] = Field(None, description="Тип: 'Flatbed','Sheet-fed','Handheld'")
    resolution_dpi: Optional[int] = Field(None, description="Разрешение сканирования в dpi")
    color: bool = Field(True, description="Сканирование в цвете (True/False)")
    connectivity: List[str] = Field(default_factory=list, description="Подключение")


class PhotocopierParams(BaseModel):
    brand: str = Field(..., description="Производитель")
    model: str = Field(..., description="Модель")
    speed_cpm: Optional[int] = Field(None, description="Скорость копирования в коп./мин")
    color: bool = Field(True, description="Цветная копия (True/False)")
    max_paper_size: Optional[str] = Field(None, description="Максимальный формат бумаги")


class FaxMachineParams(BaseModel):
    brand: str = Field(..., description="Производитель")
    model: str = Field(..., description="Модель")
    modem_speed_bps: Optional[int] = Field(None, description="Скорость модема в бит/с")
    paper_size: Optional[str] = Field(None, description="Формат бумаги")
    memory_pages: Optional[int] = Field(None, description="Память в страницах")


class PlotterParams(BaseModel):
    brand: str = Field(..., description="Производитель")
    model: str = Field(..., description="Модель")
    max_width_mm: Optional[int] = Field(None, description="Максимальная ширина в мм")
    technology: Optional[str] = Field(None, description="Технология: 'Inkjet' или 'Cutting'")


class MultifunctionDeviceParams(BaseModel):
    brand: str = Field(..., description="Производитель")
    model: str = Field(..., description="Модель")
    functions: List[str] = Field(..., description="Функции: ['print','scan','copy','fax']")
    color: bool = Field(True, description="Цветная печать")
    duplex: bool = Field(False, description="Двухсторонняя печать")


class PowerBankParams(BaseModel):
    brand: str = Field(..., description="Производитель")
    model: str = Field(..., description="Модель")
    capacity_mah: int = Field(..., description="Ёмкость в мА·ч")
    ports: List[str] = Field(..., description="Типы портов, напр. ['USB-A','USB-C']")
    output_watts: Optional[float] = Field(None, description="Максимальная выходная мощность в ваттах")


class ChargerParams(BaseModel):
    brand: str = Field(..., description="Производитель")
    model: str = Field(..., description="Модель")
    type: Optional[str] = Field(None, description="Тип: 'USB-A','USB-C','AC'")
    output_voltage: Optional[float] = Field(None, description="Выходное напряжение в вольтах")
    output_current_a: Optional[float] = Field(None, description="Выходной ток в амперах")


class UPSParams(BaseModel):
    brand: str = Field(..., description="Производитель")
    model: str = Field(..., description="Модель")
    capacity_va: int = Field(..., description="Ёмкость в ВА")
    backup_time_min: Optional[int] = Field(None, description="Примерное время работы при нагрузке в мин")
    outlets: int = Field(..., description="Число розеток")


# === Аудио/видео ===

class HeadphonesParams(BaseModel):
    brand: str = Field(..., description="Производитель")
    model: str = Field(..., description="Модель")
    type: Optional[str] = Field(None, description="Тип: 'Over-ear','In-ear','On-ear'")
    wireless: bool = Field(False, description="Беспроводные (True/False)")
    noise_cancellation: bool = Field(False, description="Активное шумоподавление")
    impedance_ohm: Optional[int] = Field(None, description="Импеданс в Ом")


class SpeakerParams(BaseModel):
    brand: str = Field(..., description="Производитель")
    model: str = Field(..., description="Модель")
    type: Optional[str] = Field(None, description="Тип: 'Bookshelf','Floor-standing','Portable'")
    power_watts: Optional[int] = Field(None, description="Выходная мощность в ваттах")
    connectivity: List[str] = Field(default_factory=list, description="Подключения: ['Bluetooth','Wired']")


class SubwooferParams(BaseModel):
    brand: str = Field(..., description="Производитель")
    model: str = Field(..., description="Модель")
    power_watts: Optional[int] = Field(None, description="Мощность в ваттах")
    frequency_response_hz: Optional[str] = Field(None, description="Полоса воспроизводимых частот в Гц")


class MicrophoneParams(BaseModel):
    brand: str = Field(..., description="Производитель")
    model: str = Field(..., description="Модель")
    type: Optional[str] = Field(None, description="Тип микрофона: 'Dynamic','Condenser','Ribbon'")
    connectivity: Optional[str] = Field(None, description="Подключение: 'XLR' или 'USB'")


class AudioMixerParams(BaseModel):
    brand: str = Field(..., description="Производитель")
    model: str = Field(..., description="Модель")
    channels: int = Field(..., description="Количество каналов")
    phantom_power: bool = Field(False, description="Наличие фантомного питания 48В")
    usb_interface: bool = Field(False, description="USB-интерфейс для подключения к ПК")


from pydantic import BaseModel, Field
from datetime import date
from typing import List, Optional


# === Audio/Video Equipment ===

class AmplifierParams(BaseModel):
    brand: str = Field(..., description="Производитель")
    model: str = Field(..., description="Модель")
    power_output: int = Field(..., description="Выходная мощность (Вт)")
    channels: int = Field(..., description="Количество каналов")


class ReceiverParams(BaseModel):
    brand: str = Field(..., description="Производитель")
    model: str = Field(..., description="Модель")
    power_output: int = Field(..., description="Выходная мощность (Вт)")
    surround_support: bool = Field(False, description="Поддержка Surround (да/нет)")


class ProjectorParams(BaseModel):
    brand: str = Field(..., description="Производитель")
    model: str = Field(..., description="Модель")
    resolution: str = Field(..., description="Разрешение")
    brightness: int = Field(..., description="Яркость (люмены)")
    contrast_ratio: str = Field(..., description="Контрастность")


class ProjectorScreenParams(BaseModel):
    type: str = Field(..., description="Тип экрана (настенный, напольный)")
    size: float = Field(..., description="Диагональ (дюймы)")
    aspect_ratio: str = Field(..., description="Соотношение сторон")


class TurntableParams(BaseModel):
    brand: str = Field(..., description="Производитель")
    model: str = Field(..., description="Модель")
    drive_type: str = Field(..., description="Тип привода (ременной, прямой)")
    speed: List[int] = Field(..., description="Скорости вращения (об/мин)")


class DJControllerParams(BaseModel):
    brand: str = Field(..., description="Производитель")
    model: str = Field(..., description="Модель")
    channels: int = Field(..., description="Количество каналов")
    jog_wheels: bool = Field(..., description="Наличие джогов (да/нет)")


# === Furniture ===

class TableParams(BaseModel):
    material: str = Field(..., description="Материал")
    length: float = Field(..., description="Длина (см)")
    width: float = Field(..., description="Ширина (см)")
    height: float = Field(..., description="Высота (см)")


class DeskParams(BaseModel):
    material: str = Field(..., description="Материал")
    length: float = Field(..., description="Длина (см)")
    width: float = Field(..., description="Ширина (см)")
    height: float = Field(..., description="Высота (см)")
    drawers: Optional[int] = Field(None, description="Количество ящиков")


class ChairParams(BaseModel):
    material: str = Field(..., description="Материал")
    max_weight: int = Field(..., description="Макс. нагрузка (кг)")
    adjustable: bool = Field(False, description="Регулируемая (да/нет)")


class SofaParams(BaseModel):
    material: str = Field(..., description="Материал обивки")
    seats: int = Field(..., description="Количество мест")
    recliner: bool = Field(False, description="Реклайнер (да/нет)")


class BedParams(BaseModel):
    size: str = Field(..., description="Размер (например, Queen, King)")
    frame_material: str = Field(..., description="Материал каркаса")
    storage: bool = Field(False, description="Наличие ящиков (да/нет)")


class WardrobeParams(BaseModel):
    doors: int = Field(..., description="Количество дверей")
    mirror: bool = Field(False, description="Наличие зеркала (да/нет)")
    material: str = Field(..., description="Материал")


class DresserParams(BaseModel):
    drawers: int = Field(..., description="Количество ящиков")
    material: str = Field(..., description="Материал")


class NightstandParams(BaseModel):
    drawers: Optional[int] = Field(None, description="Количество ящиков")
    material: str = Field(..., description="Материал")


class ShelfParams(BaseModel):
    material: str = Field(..., description="Материал")
    levels: int = Field(..., description="Количество полок")


class MirrorParams(BaseModel):
    shape: str = Field(..., description="Форма (круглое, прямоугольное)")
    height: float = Field(..., description="Высота (см)")
    width: float = Field(..., description="Ширина (см)")


class RugParams(BaseModel):
    material: str = Field(..., description="Материал")
    length: float = Field(..., description="Длина (см)")
    width: float = Field(..., description="Ширина (см)")


class CabinetParams(BaseModel):
    doors: int = Field(..., description="Количество дверей")
    shelves: int = Field(..., description="Количество полок")
    material: str = Field(..., description="Материал")


# === Lighting ===

class DeskLampParams(BaseModel):
    light_type: str = Field(..., description="Тип лампы (LED, галоген)")
    brightness_levels: int = Field(..., description="Количество уровней яркости")


class FloorLampParams(BaseModel):
    light_type: str = Field(..., description="Тип лампы")
    height: float = Field(..., description="Высота (см)")
    dimmable: bool = Field(False, description="Регулировка яркости (да/нет)")


class ChandelierParams(BaseModel):
    bulbs: int = Field(..., description="Количество лампочек")
    material: str = Field(..., description="Материал")
    diameter: float = Field(..., description="Диаметр (см)")


class SpotlightParams(BaseModel):
    power: int = Field(..., description="Мощность (Вт)")
    beam_angle: int = Field(..., description="Угол освещения (градусы)")


# === Tools Electronics ===

class CNCMachineParams(BaseModel):
    work_area: str = Field(..., description="Рабочая зона (мм)")
    spindle_power: int = Field(..., description="Мощность шпинделя (Вт)")


class PCBPrinterParams(BaseModel):
    resolution: str = Field(..., description="Разрешение печати")
    pcb_size: str = Field(..., description="Макс. размер платы")


class SolderingStationParams(BaseModel):
    power: int = Field(..., description="Мощность (Вт)")
    temperature_range: str = Field(..., description="Диапазон температуры")


class MultimeterParams(BaseModel):
    measurement_types: List[str] = Field(..., description="Типы измерений (напряжение, ток, сопротивление)")
    auto_range: bool = Field(False, description="Автодиапазон (да/нет)")


class OscilloscopeParams(BaseModel):
    bandwidth: float = Field(..., description="Полоса пропускания (МГц)")
    channels: int = Field(..., description="Количество каналов")


class SignalGeneratorParams(BaseModel):
    frequency_range: str = Field(..., description="Диапазон частот")
    output_power: str = Field(..., description="Выходная мощность")


class PowerSupplyParams(BaseModel):
    output_voltage: str = Field(..., description="Выходное напряжение")
    output_current: str = Field(..., description="Выходной ток")


class BatteryTesterParams(BaseModel):
    supported_types: List[str] = Field(..., description="Поддерживаемые типы батарей")
    max_voltage: float = Field(..., description="Макс. напряжение (В)")


class VoltageStabilizerParams(BaseModel):
    power: int = Field(..., description="Мощность (Вт)")
    input_voltage: str = Field(..., description="Входное напряжение")


class InverterParams(BaseModel):
    input_voltage: str = Field(..., description="Входное напряжение")
    output_voltage: str = Field(..., description="Выходное напряжение")
    power: int = Field(..., description="Мощность (Вт)")


class TransformerParams(BaseModel):
    input_voltage: str = Field(..., description="Входное напряжение")
    output_voltage: str = Field(..., description="Выходное напряжение")
    power: int = Field(..., description="Мощность (Вт)")


class PortableGeneratorParams(BaseModel):
    power: int = Field(..., description="Мощность (Вт)")
    fuel_type: str = Field(..., description="Тип топлива")
    tank_capacity: float = Field(..., description="Ёмкость бака (л)")


class SolarPanelParams(BaseModel):
    power: int = Field(..., description="Мощность (Вт)")
    efficiency: float = Field(..., description="КПД (%)")
    size: str = Field(..., description="Размер панели")


# === Sports & Outdoors ===

class BicycleParams(BaseModel):
    type: str = Field(..., description="Тип велосипеда (горный, шоссейный)")
    frame_material: str = Field(..., description="Материал рамы")
    gears: int = Field(..., description="Количество передач")


class ElectricScooterParams(BaseModel):
    max_speed: float = Field(..., description="Макс. скорость (км/ч)")
    battery_capacity: int = Field(..., description="Ёмкость батареи (мА·ч)")
    range_km: float = Field(..., description="Запас хода (км)")


class SkateboardParams(BaseModel):
    length: float = Field(..., description="Длина деки (см)")
    material: str = Field(..., description="Материал")
    type: str = Field(..., description="Тип (лонгборд, классический)")


class RollerSkatesParams(BaseModel):
    size: str = Field(..., description="Размер (EU/US)")
    wheel_diameter: float = Field(..., description="Диаметр колес (мм)")


class TentParams(BaseModel):
    capacity: int = Field(..., description="Вместимость (чел)")
    seasonality: str = Field(..., description="Сезонность (летняя, зимняя)")
    weight: float = Field(..., description="Вес (кг)")


class SleepingBagParams(BaseModel):
    comfort_temperature: float = Field(..., description="Комфортная температура (°C)")
    weight: float = Field(..., description="Вес (кг)")
    material: str = Field(..., description="Материал")


class CampingStoveParams(BaseModel):
    fuel_type: str = Field(..., description="Тип топлива")
    weight: float = Field(..., description="Вес (кг)")
    power: int = Field(..., description="Мощность (Вт)")


# === Apparel & Footwear ===

class ClothingParams(BaseModel):
    size: str = Field(..., description="Размер")
    material: str = Field(..., description="Материал")
    gender: Optional[str] = Field(None, description="Пол (мужской, женский)")
    season: Optional[str] = Field(None, description="Сезон (лето, зима)")


class FootwearParams(BaseModel):
    size: str = Field(..., description="Размер")
    material: str = Field(..., description="Материал")
    type: str = Field(..., description="Тип обуви (кроссовки, ботинки)")


# === Toys & Games ===

class BoardGameParams(BaseModel):
    players: str = Field(..., description="Количество игроков")
    age: str = Field(..., description="Возрастная категория")
    play_time: str = Field(..., description="Время игры")


class PuzzleParams(BaseModel):
    pieces: int = Field(..., description="Количество деталей")
    material: str = Field(..., description="Материал")


# === Baby & Kids ===

class BabyStrollerParams(BaseModel):
    type: str = Field(..., description="Тип коляски (прогулочная, универсальная)")
    weight: float = Field(..., description="Вес (кг)")
    foldable: bool = Field(False, description="Складываемая (да/нет)")


class CarSeatParams(BaseModel):
    group: str = Field(..., description="Группа (0,1,2,3)")
    weight_limit: float = Field(..., description="Ограничение по весу (кг)")
    isofix: bool = Field(False, description="Крепление ISOFIX (да/нет)")


class HighChairParams(BaseModel):
    adjustable_height: bool = Field(False, description="Регулируемая высота (да/нет)")
    material: str = Field(..., description="Материал")


class CribParams(BaseModel):
    material: str = Field(..., description="Материал")
    adjustable_height: bool = Field(False, description="Регулируемая высота (да/нет)")


class MattressParams(BaseModel):
    size: str = Field(..., description="Размер")
    material: str = Field(..., description="Материал")
    thickness: float = Field(..., description="Толщина (см)")


class PillowParams(BaseModel):
    size: str = Field(..., description="Размер")
    material: str = Field(..., description="Материал")
    filling: str = Field(..., description="Наполнитель")


class BlanketParams(BaseModel):
    size: str = Field(..., description="Размер")
    material: str = Field(..., description="Материал")
    filling: str = Field(..., description="Наполнитель")


# === Books & Stationery ===

class BookParams(BaseModel):
    author: str = Field(..., description="Автор")
    genre: Optional[str] = Field(None, description="Жанр")
    pages: int = Field(..., description="Количество страниц")


class StationeryParams(BaseModel):
    type: str = Field(..., description="Тип (ручка, тетрадь)")
    material: Optional[str] = Field(None, description="Материал")


# === Food ===

class FoodParams(BaseModel):
    name: str = Field(..., description="Название продукта")
    category: str = Field(..., description="Категория (фрукты, овощи, мясо)")
    weight: float = Field(..., description="Вес (г)")
    expiration_date: Optional[date] = Field(None, description="Срок годности")
