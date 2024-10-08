# API для работы со балансом пользователя

Это тестовый сервис API для работы со балансом пользователя для LighTech

Входные условия:
- У каждого пользователя есть свой баланс, изначально он равен 0.
- Разработать API, который принимает число (количество копеек) и увеличивает баланс залогиненного пользователя на данное число. Абстрагируемся от реально оплаты и денег, реализуя лишь последний шаг зачисления денег на  баланс. Он может пополнить свой баланс в любой момент времени.
- Разработать API, который производит списание с текущего баланса пользователя на баланс другого пользователя по user_id по требованию (перевод денег). Только залогиненный пользователь может производить списания со своего баланса, но начисления возможны без каких-либо подтверждений со стороны получателя.
- Разработать API, который возвращает значение текущего баланса авторизованного пользователя в рублях.
- Вести учет операций с балансом


## Дисклеймер:
1. Какое количество запросов в минуту/секунду надо заложить?
Ответ: нет критериев
2. Известно ли уникальное количество пользователей?
Ответ: нет критериев
3. Какая документация требуются для api?
Ответ: абсолютно любое решение- swagger автодока вполне сойдет
4. Есть ли лимиты пополнения/списания?
Ответ: нет лимитов, задание заведомо упрощено
5. Уведомления при транзакции не нужно реализовывать?
Ответ: не нужно
6. Могут ли быть сценарии, когда транзакция может быть заблокирована?
Ответ: блокировок на уровне бизнес-логики нет, задание заведомо упрощено
7. Валюта может измениться?
Ответ: нет
8. Какая информация нужна для истории транзакций? 
Ответ: дата и время, сумма, кто/кому
9. Есть ли требования к покрытию тестами?
Ответ: требования нет, на свое усмотрение
10. Есть ли требования к мониторингу и логам?
Ответ: логи приветствуются, можно без мониторинга
11. Решение надо деплоить? Docker это ок?
Ответ: показать уровень знания Docker приветствуется, достаточно docker compose
12. Требуются ли интерфейсы пользователей? Если да, какие?
Ответ: не требуется, если будет базовая настройка админки, уже хорошо.


## Что можно улучшить:
- Сделать интерфейс logout  пользователя
- Сценарий, если нет счета у получателя при переводе. Сейчас создается, если его нет, но то может быть неочевидным поведением.
- Добавить логи
- Настроить мониторинг логов
- Настроить админку
- Провести/написать тесты с существенным кол-вом пользователей


# Инструкция по установке

1. Клонируйте репозиторий и перейдите в созданную директорию
```sh
git clone https://github.com/Staskosh/lightech_testcase
```

2. Создайте файл `.env` и заполните его по образцу
```
SECRET_KEY=<secret key>
ALLOWED_HOSTS=<allowed hosts>
DEBUG=<set up debug mode>
DB_PATH=<local db path>
POSTGRES_USER=<postger user>
POSTGRES_PASSWORD=<postgres password>
POSTGRES_DB=<postgres db name>
POSTGRES_HOST=<postgres host>
POSTGRES_PORT=<postgres port>
```

3. Соберите и поднимите проект с помощью `docker compose`
```sh
docker compose -f docker-compose.dev.yaml up -d --build
```

4. Запустите команду для создания суперпользователя
```sh
docker compose -f docker-compose.dev.yaml exec django ./manage.py createsuperuser
```

5. Запустите сервер и откройте сайт в браузере по адресу [http://localhost:8000/](http://localhost:8000/)

6. Для тестирования запустите.
```sh
docker compose -f docker-compose.dev.yaml exec django ./manage.py test payments_api
```

7. Ознакомьтесь с документацией API по адресу [http://localhost:8000/swagger/](http://localhost:8000/swagger/)
