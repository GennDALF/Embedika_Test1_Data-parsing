# Тестовое задание 1. Парсинг данных и API
### Задание
>Необходимо распарсить открытые данные о цене на сырую нефть марки “Юралс” и предоставить к ним доступ по API ([данные](https://data.gov.ru/opendata/7710349494-urals))
#
### Описание API



| Метод | Параметры | Возвращаемый результат |
| :--- | :---: | :---: |
| ```get_price()``` <br/> Цена на заданную дату | date_string <br/> "DD MM YYYY" | float <br/> |
| ```get_average_price()``` <br/> Средняя цена за промежуток времени | date_range_string <br/> "DD MM YYYY - <br/>DD MM YYYY" | float <br/> |
| ```get_min_max_prices()``` <br/> Максимальная и минимальная цены за промежуток времени |date_range_string <br/> "DD MM YYYY - <br/>DD MM YYYY" | JSON str |
| ```get_stats()``` <br/> Статистика по загруженным данным |   –   | JSON str * |

\* structure of ```get_stats()``` JSON output is:
```
[
  {
    "all entries": <int>,  # number of all entries 
    "start of monitoring": <str>,  # date of first monitoring period start: "DD mmmm YYYY"
    "end of monitoring": <str>,  # date of last monitoring period end: "DD mmmm YYYY"
    "global min price": [<float>, <str>],  # list of minimal price and corresponding date
    "global max price": [<float>, <str>]  # list of maximal price and corresponding date
  }
]
```
