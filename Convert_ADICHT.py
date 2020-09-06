from matplotlib.pyplot import rcParams
import matplotlib.pyplot as PLT
from tkinter import filedialog as Tk_F
import tkinter as TK
import progressbar
import os
import adi


# Поиск файла
def FileFinder():
    def character_mentions():
        F = Tk_F.askopenfilename()
        return F
    return character_mentions()

# Поиск дирректории
def DirectoryFinder():
    def character_mentions():
        F = Tk_F.askdirectory()
        return F
    return character_mentions()

# Рисуем один график из ADICHT
def Grid_ADICHT(ADI,Channels,Rec,Title,LabelY):
    DarkGraph("ADICHT")
    DataADI = ADI.channels[Channels].get_data(Rec)
    PLT.title(Title + " Rec " + str(Rec))
    PLT.xlabel("Time (Делить на частоту указанную в файле INFO)")
    PLT.ylabel(LabelY)
    PLT.plot(DataADI,color="yellow")
    PLT.show()

# Конвертирование строки в список с двумя числовыми значениями
def STR_LIST_2_FLOAT(Text):
    LS, N = [], ""
    for S in range(1,len(Text)-1):
        if(Text[S] != ","): N += Text[S]
        else: 
            LS.append(float(N))
            N = ""
    LS.append(float(N))
    return LS

# Конвертирование строки в список с двумя строчными значениями
def STR_LIST_2_STR(Text):
    LS, N = [], ""
    for S in range(1,len(Text)-1):
        if(Text[S] != ","): N += Text[S]
        else: 
            LS.append(N)
            N = ""
    LS.append(N)
    return LS

# Дизайнер графиков
# TitleSTR -> Название окна 
def DarkGraph(TitleSTR):
    rcParams['figure.edgecolor'] = "333333"
    rcParams['figure.facecolor'] = "333333"
    rcParams['figure.figsize'] = 15, 9

    rcParams['text.color'] = "CCCC00"

    rcParams['legend.edgecolor'] = "CCCC00"
    rcParams['legend.facecolor'] = "CCCC00"

    rcParams['axes.labelcolor'] = "ffffff"
    rcParams['axes.edgecolor'] = "ffffff"
    rcParams['axes.facecolor'] = "222222"

    rcParams['savefig.edgecolor'] = "222222"
    rcParams['savefig.facecolor'] = "222222"

    rcParams['xtick.color'] = "CCAA00"
    rcParams['ytick.color'] = "CCAA00"

    rcParams['xtick.minor.visible'] = True
    rcParams['ytick.minor.visible'] = True

    rcParams['boxplot.meanline'] = True
    rcParams['figure.frameon'] = False
    rcParams['grid.color'] = "055212"

    rcParams['font.size'] = 8

    PLT.grid(True)
    man = PLT.get_current_fig_manager()
    man.canvas.set_window_title(TitleSTR)

# Возвращаем информацию об данных в списке по стандарту ADICHT
def INFO_ADICHT(ADI_CHANNELS):

    Str_None = str(ADI_CHANNELS)
    ADI_NONE, NAME_S, DATA_S, DATA_B = {}, "", "", False 
 
    # Создание списка
    for Char_S in Str_None:
        
        if(Char_S == ":"):
            DATA_B = True
        elif(Char_S == "\n"):
            DATA_B = False
            ADI_NONE[NAME_S] = DATA_S
            NAME_S, DATA_S, = "", ""
        else:
            if(Char_S != " "):
                if(DATA_B): DATA_S+=Char_S
                else: NAME_S+=Char_S

    # Корректировка мета данных
    ADI_NONE['tick_dt'] = STR_LIST_2_FLOAT(ADI_NONE['tick_dt'])
    ADI_NONE['n_samples'] = STR_LIST_2_FLOAT(ADI_NONE['n_samples'])
    ADI_NONE['dt'] = STR_LIST_2_FLOAT(ADI_NONE['dt'])
    ADI_NONE['fs'] = STR_LIST_2_FLOAT(ADI_NONE['fs'])
    ADI_NONE['units'] = STR_LIST_2_STR(ADI_NONE['units'])
    
    return ADI_NONE

# Рисовать графики по одному
def ADICHT_MATPLOTLIB(ADI):
    for ID in range(0,len(ADI.channels)):
        INFO_ADI = INFO_ADICHT(ADI.channels[ID])
        REC = int(INFO_ADI['n_records']) +1
        for R in range(1,REC):
            print("Рисуем... (Rec ", R,")")
            Grid_ADICHT(ADI,ID,R,INFO_ADI['name'],INFO_ADI['units'][0])

# Нарисовать определённый график
def ADICHT_GRID_NAME(ADI):
    print("\nВыберите сигнал для визуализации: ")
    for ID in range(0,len(ADI.channels)):
        INFO_ADI = INFO_ADICHT(ADI.channels[ID])
        print("Нажмите ", ID, ", чтобы нарисовать " , INFO_ADI['name'])
    CMD = int(input("Ваш выбор: "))
    if(CMD < 0 and CMD >= len(ADI.channels)): return 0
    INFO_ADI = INFO_ADICHT(ADI.channels[CMD])
    for R in range(1,int(INFO_ADI['n_records'])+1):
        print("Рисуем... (Rec ", R,")")
        Grid_ADICHT(ADI,ID,R,INFO_ADI['name'],INFO_ADI['units'][0])

# Конвертирование данные в txt
def ADICHT_TXT(ADI,FILE):
    

    if os.path.exists("Data"): print()
    else: os.mkdir("Data")

    FS = ConvNameFile(FILE)

    if os.path.exists("Data/" + FS ): print()
    else: os.mkdir("Data/" + FS)

    FileSave = open("Data/" + FS + "/INFO_DATA.txt", 'w')
    FileSave.write(str(ADI.channels))

    for ID in range(0,len(ADI.channels)):

        INFO_ADI = INFO_ADICHT(ADI.channels[ID])

        for R in range(1,int(INFO_ADI['n_records'])+1):

            if os.path.exists("Data"): print()
            else: os.mkdir("Data")

            FileSave = open("Data/" + FS + "/" + INFO_ADI['name'] + "_Rec_" + str(R) + ".txt", 'w')
             
            DataADI = ADI.channels[ID].get_data(R)

            print("\nОбработка: " + INFO_ADI['name'] , ": (" ,R , "/" ,INFO_ADI['n_records'] , ")", ID+1 , "/" , len(ADI.channels))

            Bar = progressbar.ProgressBar().start()
            BarN,BarUp = 0, 100/(len(DataADI)) 

            for i in DataADI:

                BarN += BarUp 
                try:Bar.update(BarN)
                except ValueError: Bar.update(100)

                FileSave.write(str(i))
                FileSave.write("\n")

            Bar.finish()

# Конвертирование все данные в txt из папки
def ADICHT_TXT_MASS():
    print()

# Вытащить название файла
def ConvNameFile(FileAdd):
    N = FileAdd.rfind("/")
    FileNameAdd = ""
    for i in range(N+1,len(FileAdd)):
        FileNameAdd += FileAdd[i]

    return FileNameAdd[:-7]

# Командер
def ADI_COMMAND(FILE):

    ADI, CMD = adi.read_file(FILE), 1
    print("\nРабота с файлом: " + str(FILE))

    while(CMD > 0 and CMD < 5):
        
        print("\nНажмите 1, если хотите конвертировать данные в txt" +
              "\nНажмите 2, если хотите нарисовать конкретный график" +
              "\nНажмите 3, если хотите рисовать все графики по очерёдности" +
              "\nНажмите 4, если хотите получить данные о графиках" +
              "\nНажмите 0, если хотите выйти")
        
        CMD = int(input("Ваш выбор: "))
        if(CMD == 1): ADICHT_TXT(ADI,FILE)
        elif(CMD == 2): ADICHT_GRID_NAME(ADI)
        elif(CMD == 3): ADICHT_MATPLOTLIB(ADI)
        elif(CMD == 4): print(ADI.channels)


# Стартер
def StarterPrograms():
    print(">>  >> ADICHT Convert << Alpha 0.4b <<")

    print("\nДля работы нужно выбрать файл формата adicht")
    print("или папку с файлами формата adicht")

    input("(чтобы продолжить, нажмите enter)")

    print("\nНажмите 1, если хотите работать с одним файлом" +
            "\nНажмите 2, если хотите работать с множеством файлов" +
            "\nНажмите 0, если хотите выйти")

    CMD = int(input("Ваш выбор: "))
    if(CMD == 1): ADI_COMMAND(FileFinder())
    elif(CMD == 2):

        print("\nНажмите 1, для ручной настройки" +
                "\nНажмите 2, для автоматической настройки" +
                "\nНажмите 0, если хотите выйти")

        CMD = int(input("Ваш выбор: "))

        if(CMD == 1): 
            DIRECT, FLN = DirectoryFinder(), 0
            FileList = os.listdir(DIRECT)

            print("\nВы выбрали дирректорию: " + str(DIRECT))
            for FILE in FileList: 
                FLN += 1
                print("Файл: " + str(FLN) + "/" + str(len(FileList)))
                ADI_COMMAND(DIRECT + "/" + FILE)

        elif(CMD == 2):

            DIRECT, FLN = DirectoryFinder(), 0
            FileList = os.listdir(DIRECT)

            print("\nВы выбрали дирректорию: " + str(DIRECT))
            input("(для продолжения работы нажмите enter)")
            for FILE in FileList: 
                FLN += 1
                ADI = adi.read_file(DIRECT + "/" + FILE)
                
                print("\nРабота с файлом: " + str(FILE) + "; Файл: " + str(FLN) + "/" + str(len(FileList)))
                ADICHT_TXT(ADI, FILE)
    
    print("\nСпасибо за визит, приходите ещё!!!")
    input("(чтобы выйти, нажмите enter)")

#----------------------------------------------------------------------------------------------------------------------

StarterPrograms()
    