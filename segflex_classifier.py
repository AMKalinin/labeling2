code_base = ([  "Вода",
                "Растительность",
                "Площадные объекты",
                "Объекты и сооружения"                              ])

code_100 = ([       "100_Объект отсутствует",
                    "110_Река, канал",
                    "120_Озеро, пруд, водохранилище",
                    "130_Болото, рисовое поле",
                    "140_Океан, море"                                 ])

code_200 = ([       "200_Объект отсутствует",
                    "210_Заросли кустарников и прочей низкой растительности (в т.ч. луга и степи)",
                    "220_Редкий лесной массив (редко стоящие деревья)",
                    "230_Лесной массив (в т. ч. густые массивы)"        ])

code_300 =([        "300_Объект отсутствует",
                    "310_Город или другой населенный пункт",
                    "320_Промышленное предприятие неопределённого типа",
                    "350_Пески"                                        ])

code_320 =([            "321_Порт",
                        "322_Эл. Станция",
                        "323_НПЗ"                                       ])

code_400 =([        "400_Объект отсутствует",
                    "410_Плотина, дамба",
                    "420_Автомобильная дорога",
                    "430_Линия эл. передач",
                    "440_Скалы",
                    "450_Здание неопределенного типа",
                    "460_Аэродром",
                    "490_Особые здания"                                 ])


code_490 =([            "401_Объект неопределенного типа"               ])

code_410 =([            "411_Мост"                                      ])

code_420 =([            "421_Железная дорога"                           ])

code_440 =([            "441_Террикон, отвал, насыпь, курган"           ])

code_450 =([            "451_Жилое строение",
                        "452_Промышленное строение или сооружение",
                        "453_Причал",
                        "454_Культурные и религиозные здания и сооружения",
                        "455_Склад",
                        "456_Склад горючего"                            ])

code_460 =([            "461_Портовые сооружения и краны"               ])

project_classes = []

HDF_GROUP_SRCS_NAME = '__srcs_images'
HDF_GROUP_FEATURES_NAME = '__features'
HDF_GROUP_OBJECT_LAYERS_NAME = '__object_layers'
HDF_POSTFIX = '.hdf5'

HDF_FILE_NAME = 'name'
HDF_FILE_CLASSES = 'classes'
HDF_FILE_TIME_C = 'time_created'
HDF_FILE_TIME_U = 'time_updated'
HDF_FILE_DESCRIPTION = 'description'
HDF_FILE_TASK_COUNT = 'task_count'

HDF_TASK_POLYGON_COUNT = '__polygon_count'
HDF_TASK_STATUS = '__task_status'
HDF_TASK_STATUS_0 = 'to do' #при создании файла проекта, при добавлении задачи
HDF_TASK_STATUS_1 = 'in progress' #у задачи есть хотя бы один атрибут маски
HDF_TASK_STATUS_2 = 'review' #нажата кнопка отправить на проверку
HDF_TASK_STATUS_3 = 'done' #модератор нажал кнопку 


TASK_WIDGET_MODE_0 = 'to do'
TASK_WIDGET_MODE_1 = 'to check'



import os

ICON_FOLDER_NAME = '__icons'
ICON_FOLDER_NAME_FULL = os.getcwd() + '/' + ICON_FOLDER_NAME

IMAGES_FOLDER_NAME = '__images'
IMAGES_FOLDER_NAME_FULL = os.getcwd() + '/' + IMAGES_FOLDER_NAME

ICON_SEG_TBTN_PREVIOUS = 'previous_tbtn.png'
ICON_SEG_TBTN_PREVIOUS_FULL = ICON_FOLDER_NAME_FULL + '/' + ICON_SEG_TBTN_PREVIOUS

ICON_SEG_TBTN_NEXT = 'next_tbtn.png'
ICON_SEG_TBTN_NEXT_FULL = ICON_FOLDER_NAME_FULL + '/' + ICON_SEG_TBTN_NEXT

ICON_SEG_TBTN_TOFIRST = 'tofirst_tbtn.png'
ICON_SEG_TBTN_TOFIRST_FULL = ICON_FOLDER_NAME_FULL + '/' + ICON_SEG_TBTN_TOFIRST

ICON_SEG_TBTN_TOLAST = 'tolast_tbtn.png'
ICON_SEG_TBTN_TOLAST_FULL = ICON_FOLDER_NAME_FULL + '/' + ICON_SEG_TBTN_TOLAST

ICON_SEG_TBTN_DOTS_INSTRUMENT = 'dots_instrument_tbtn.png'
ICON_SEG_TBTN_DOTS_INSTRUMENT_FULL = ICON_FOLDER_NAME_FULL + '/' + ICON_SEG_TBTN_DOTS_INSTRUMENT

ICON_PENCIL_TBTN_DRAW_INSTRUMENT = 'pencil_tbtn.png'
ICON_PENCIL_TBTN_DRAW_INSTRUMENT_FULL = ICON_FOLDER_NAME_FULL + '/' + ICON_PENCIL_TBTN_DRAW_INSTRUMENT

ICON_POLYGON_TBTN_DRAW_INSTRUMENT = 'polygon_tbtn'
ICON_POLYGON_TBTN_DRAW_INSTRUMENT_FULL = ICON_FOLDER_NAME_FULL + '/' + ICON_POLYGON_TBTN_DRAW_INSTRUMENT

ICON_CANCEL_TBTN_DRAW_INSTRUMENT = 'cancel_tbtn.png'
ICON_CANCEL_TBTN_DRAW_INSTRUMENT_FULL = ICON_FOLDER_NAME_FULL + '/' + ICON_CANCEL_TBTN_DRAW_INSTRUMENT

ICON_SAVE_TO_ATTRS_TBTN = 'save_to_attrs_tbtn.png'
ICON_SAVE_TO_ATTRS_TBTN_FULL = ICON_FOLDER_NAME_FULL + '/' + ICON_SAVE_TO_ATTRS_TBTN


PROJECTS_FOLDER_NAME = '__projects'
PROJECTS_FOLDER_FULL_NAME = os.getcwd() + '/' + PROJECTS_FOLDER_NAME
#PROJECTS_LIST = os.listdir(PROJECTS_FOLDER_FULL_NAME)



import time

class project_ini():
    name = ""
    id = 0
    author = ""
    time_start = time.localtime()
    time_last_change = time.localtime()
    classes = []
    description = ""
    base_project = None
    selected_files = []

current_project = project_ini()