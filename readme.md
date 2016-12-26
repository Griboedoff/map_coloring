#Раскраска карты

Сделано с использованием PyQt5

Автор: Дубровин Алексей

###Запуск:
- `main.py -e` - запуск редактора карты
- `main.py -f имя_файла` - запуск раскраски карты из файла "имя_файла"
- Справка доступна при запуске с ключом `-h` 

###Алгоритм раскраски
На каждой итерации нам известно N - текущее минимальное число цветов, необходимое для раскраски карты. При рассмотрении следующей страны выполняются действия:
1. Собрать все цвета соседей
2. Если есть доступный цвет от 1 до N который не в цветах соседей, то красим в этот цвет. Иначе N++ и красим в новый цвет.

Алгоритм завершает работу если:
 - N больше чем размер палитры
 - Раскрашена вся карта
 
после номеру ставится в соответствие цвет из палитры по возрастанию цены. 

Доступна возможность установить цвет после начальной раскраски карты.
###Редактор карты
Текущая реализация редактора поддерживает: 
- Добавление страны - `add country`, следующая страна должна быть привязана к одному из отрезков уже существующих стран
- Добавление куска страны - `add piece`
- Завершение куска страны - `Finish piece` - позволяет соединить последнюю поставленную точку с одной из уже поставленных
- Сохранение карты - `save` - в папку `./maps` с уникальным именем

Логика лежит в пакете `model`, алгоритм раскраски реализовани в классе `colorer`, отрисовка в классе `vizualizer`. Вся логика редактора карты в пакете `editor`.
Тесты в пакпе `tests`. Сохраненные карты в `maps`.