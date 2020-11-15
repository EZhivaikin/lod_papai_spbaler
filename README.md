# spbalert

В папке web находится FastAPI приложение, с которым общается фронтенд. Запускается:
```
cd web
uvicorn server:app --reload
```
Для запуска нужен uvicorn, FastAPI, sklearn

В ноутбуке date_processing основные моменты процессинга данных
В ноутбуке train_and_statistics попытки обучения на разных алгоритмах и немного статистики по данным
Для запуска ноутбуков нужен стандартный набор из sklearn, pandas, numpy, seaborn
