# В Программе на python3 осуществляется
# применение генетического алгоритма для поиска бинарных кодовых последовательностей 
# с заданными параметрами автокорреляционной функции
# способ формирования родительских пар : лучшие с лучшими
# способ селекци : турнир


# Исходные данные :

N   = 31 									# Длина кодовой последовательности (КП)
P   = 70 									# Размер начальной популяции - количество генерируемых КП
PSL = 2 									# Допустимый максимальный уровень положительных боковых лепестков АКФ
K   = 4 									# Количество искомых КП, с заданным PSL
Pk  = 0,85 									# Вероятность скрещивания
Pm  = 0,15									# Вероятность мутации

import matplotlib.pyplot as plt
import numpy as np
import random
 
class Individ:                              # <--- Обьявление класса индивида --->
    def __init__(self):
        self.CHR=np.random.randint(0,2,N)   #Объявляем хромосому индивида в виде строки из 0 и 1
        self.fit=0                          # Автокорреляционная функция (АКФ) КП (Rki)(первоначальное значение 0)
											#"живучесть" индивида (это будет сумма элементов строки 010..101) 
 
    def fitness(self):                      #Эта функция выполняет подсчёт "живучести" (считает сумму)
        summa=0
        for i in range(N):                  #Цикл в 30 итераций (i принимает значения от 0 до 29)
            summa=summa+self.CHR[i]         #Сумма вбирает поочерёдно в себя все элементы строки 
        self.fit=summa
 
    def info(self):                         #Функция вывода на экран индивида. 
        print(self.CHR)                     # Вывод на экран строки хромосомы
        self.fitness()                      # функция fitness() подсчитывает сумму ряда.
        print(self.fit)                     # результат этой суммы (fit) выводится на экран.
 
class Population:                           # <--- Обьявление класса популяции --->
    def __init__(self):
        self.inhabitants = []             	# Массив индивидов размером начальной популяции 
                                            #  - количеству генерируемых КП (P)
        for i in range(P):                  #Цикл для заполнения этого массива
            self.inhabitants.append(Individ())

    def info(self):              		    #Функция вывода популяции на экран.
        for i in range(P):            		#Для каждого индивида
            for j in range(N):        		#все гены его хромосомы :
                print(self.inhabitants[i].CHR[j], end ="")
            print("=",end="")          
            print(self.inhabitants[i].fit) 	#вывод fit i-го индивида популяции.
    
    def draw(self,virus):
	    plt.xlim((-100,100))
	    plt.ylim((-100,100))
	    plt.scatter(self.inhabitants[0].fit, virus[1], c ="green", s = 12)
	    plt.scatter(virus[0], virus[1], c ="red", s = 60)
        plt.show()


People=Population()                      	#Создание экземпляр класса популяции. 
People.info()                            	#Выводим информации о начальной популяции.
People.draw(virus = "12")								#Инициализация переменных для работаты:
Mother = Individ()                     		# индивида мамы
Father = Individ()                     		# индивида папы
Child1 = Individ()                          # индивида первого ребенка
Child2 = Individ()							# индивида второго ребенка

Family = []                                 # массив для отбора и селекцми
 
for j in range(20):                  		#Тут мы "придаём форму" нашему массиву "Родителей и детей". Инициализируем его рандомными индивидами.
    Family.append(Individ())                #Чтобы в дальнейшем иметь возможность напрямую работать с этим массивом с помощью наших атрибутов (А, fit)
                                       #Рандомные значения, которыми мы забили этот массив, нам не помешают. Т.к. мы поэлементно все элементы этого массива забьём актуальными данными вручную по ходу программы.
 
print("\n")                            #Отступаем две строчки после вывода нашей стартовой популяции. И да начнётся.. ЕСТЕСТВЕННЫЙ ОТБОР!!!11
 
for p in range(60):                    #Это наш основной цикл. Сейчас стоит 60 итераций. Т.е. мы ставим ограничение в 60 поколений.
                                       #За них мы должны успеть вырастить целое поколение мутантов-переростков. Мы всегда можем увеличить количество поколений и увеличить вероятность нахождения ответа. Или уменьшить, если наш механизм скрещиваний очень крутой, и мы очень быстро (за 20-30 поколений) находим ответ.
    for i in range(P):                #Заносим в первые 10 элементов массива "Отцы и дети" всю нашу входную популяцию.
        for j in range(N):
            Family[i].CHR[j]=People.inhabitants[i].CHR[j]
 
    tt=0                                       #Счётчик, который нужён для реализации небанального скрещивания.
    for s in range(0,10,2):                    #Цикл. От 0 до 10 с шагом 2. Т.е. тут мы берём 5 пар родителей.
        for j in range(30):                    #Как ты заметил, цикл из 30 итераций есть практически везде. Т.к. все операции мы проводим поэлементно (большая честь каждому нолику и каждой единичке).
            Mother.A[j]=pop1.B[tt+5].A[j]      #Пусть мамами у нас будут последние 5 индивидов нашей популяции (т.к. они у нас в последствии всегда будут отранжированы (наши популяции), беря последние 5, мы тем самым берём лучших представителей и с ними работаем. Чего с посредственностей-то взять, ну.
            Father.A[j]=pop1.B[random.randint(0,9)].A[j] #А папами пусть будет любой случайный индивид из нашей популяции. (использовали рандом от 0 до 9). Кстати, если делать совсем по-умному, то надо и папу и маму выбирать случайным образом. Но вероятность выбора в качестве родителя у индивида должна быть тем выше, чем выше у него живучесть (fit). Предлагаю (после того как со всем остальным хорошенько разберёшься) тебе подумать о том, как это можно сделать. Ничего особенно сложного в этом и нет на самом деле.



        tt=tt+1    # Двигаем наш счётчик ручками.
 
        ran=random.random()

# <--------------------------------------------- Скрещивание ---------------------------------------------> 
 
        if (ran>0.8):                          #А это наши механизмы скрещивания.
            for n in range(5):                 #Берём первые 5 элементов у папы и у мамы (для сына1 и сына2 соответственно).
                Son1.A[n]=Father.A[n]
                Son2.A[n]=Mother.A[n]
 
            for n in range(5,30):              #И берём остальные 25 элементов у мамы и у папы для сына1 и сына2 соответственно (крест-накрест)
 
                Son1.A[n]=Mother.A[n]
                Son2.A[n]=Father.A[n]
 
        if ((ran>0.6) & (ran <=0.8)):          #Тот же самый крест-накрест, только теперь самого тривиального вида.
            for n in range(15):                #Первые 15 у папы и вторые 15 у мамы для сына1.
                Son1.A[n]=Father.A[n]          #И первые 15 у мамы и вторые 15 у папы для сына2.
                Son2.A[n]=Mother.A[n]
            for n in range(16,30):
                Son1.A[n]=Mother.A[n]
                Son2.A[n]=Father.A[n]
 
        if ((ran <0.6) & (ran >=0.4)):         #Крест накрест. Зеркален первому методу скрещивания. (только не первые 5 элементов берём, а последние)
            for n in range(25):
                Son1.A[n]=Father.A[n]
                Son2.A[n]=Mother.A[n]
            for n in range(25,30):
                Son1.A[n] = Mother.A[n]
                Son2.A[n] = Father.A[n]
 
        if ((ran <0.4) & (ran>=0.3)):          #Срединный крест-накрест + инверсия.
            for n in range(15):
                Son1.A[n]=Father.A[14-n]
                Son2.A[n]=Mother.A[14-n]
            for n in range(15,30):
                Son1.A[n]=Mother.A[44-n]
                Son2.A[n]=Father.A[44-n]
 
        if (ran<0.3):                          #Тут берём для сына1 первые 15 элементов папы + первые 15 элементов мамы.
            for n in range(15):                #А для сына2 берём вторые 15 элементов мамы + вторые 15 элементов папы.
                Son1.A[n]=Father.A[n]
                Son1.A[n+15]=Mother.A[n]
                Son2.A[n]=Mother.A[n+15]
                Son2.A[n+15]=Father.A[n+15]
 
        for i in range(30):                    #Тут мы закидываем наших получившихся в результате скрещивания s-той пары родителей Сына1 и Сына2 во вторую половину массива "Отцы и дети".
            ParAndSons[10+s].A[i]=Son1.A[i]
            ParAndSons[11+s].A[i]=Son2.A[i]
 
# <--------------------------------------------- Мутации ---------------------------------------------> 

    for r in range(17,18):                #Это мутации. Чтобы доказать крутость нашего скрещивания мы минимизируем мутации.
        for w in range(30):               #Т.к. при большой вероятности мутации верное решение находится даже при совершенно неработающем механизме скрещивания.
            if random.random()<Pm:   #Поэтому мы мутируем только одного (17-го) индивида. Т.е. мы с вероятностью 0.00001
                if ParAndSons[r].A[w]==1: #инвертируем каждую из его 30 нулей и единиц.
                    ParAndSons[r].A[w]=0  #((При решении задачи с уравнением будем мутировать 3-5 индивидов с вероятностью 0.01-0.05 примерно.))
                if ParAndSons[r].A[w]==0:
                    ParAndSons[r].A[w]=1

# <--------------------------------------------- Ранжирование и селекция --------------------------------------------->  

    for i in range(20):                     #Это важно. Далее мы будем ранжировать массив отцов и детей в порядке возрастания живучести (суммы (fit)).
        ParAndSons[i].fitness()             #Поэтому мы сначала должны посчитать для всех 20 индивидов в этом массиве это самое fit с помощью нашей клёвой функции fitness().
 
    for m in range(len(ParAndSons)-1,0,-1):             #Ранжирование (методом пузырька). Лёгкие всплывают наверх, а тяжёлые оказываются внизу. (вместо "len(ParAndSons)-1" можно просто написать 19, т.к. мы знаем длину нашего массива.) Напомню, что Range(19,0,-1)  означает, что мы в цикле идём от 19 до 0 с шагом "-1".
        for b in range(m):                              #Тут мы идём в цикле от 0 до "m" (а это счётчик предыдущего цикла). Т.е. каждая итерация внешнего цикла будет уменьшать и длину внутреннего цикла.
            if ParAndSons[b].fit > ParAndSons[b+1].fit: #Разобраться с методом пузырька проще всего нарисовав на бумаге ряд 31597 и проделать на нём письменно весь алгоритм, который выдаст гугл по запросу "ранжирование пузырьком".
                mem = ParAndSons[b]                     #Мы используем переменную "mem" (от слова memory) чтобы хранить в ней одно значение в момент, когда мы взаимно меняем местами два элемента массива.
                ParAndSons[b] = ParAndSons[b+1]
                ParAndSons[b+1] = mem
 
    for i in range(10):                             #Это финал нашего основного цикла.
        for j in range(30):                         #Тут мы перебрасываем лучших из массива "отцов и детей" (т.е. последние 10 индивидов)
            pop1.B[i].A[j]=ParAndSons[i+10].A[j]    #в массив нашей основной рабочей популяции pop1.
 
    pop1.inf