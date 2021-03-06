# 🤖 Кошельбот 
    
---  
  
### Задача кошельбота - помочь пользователю контролировать расходы.  
  
---  

#### Принцип работы  

Пользователь указывает определенную сумму денег, которую хотел бы растянуть до выбранной им даты (например, до следующей зарплаты).  
В свою очередь бот равномерно распределяет ежедневный бюджет, и принимает от пользователя сообщения с расходами, из которых актуализирует оставшуюся сумму.
  
---  
  
## Описание 
  
Следуя подсказкам бота станет понятен принцип его работы.  

Но могу кратко описать имеющийся на данный момент функционал:
* Создание своего кошелька, куда пользователь должен записывать траты;
* Создание ссылки-приглашения для пользователей;
* Совместная работа нескольких пользователей с одним кошельком;
* Удаление кошелька; 
* Разрыв связи с кошельком другого пользователя. 


---  
## Установка
  
1. Находясь директории проекта необходимо установить все зависимости из файла requirements.txt введя следующую команду в терминал:  
`pip install -r requirements.txt`
2. Выполнить создание миграций:
`python manage.py makemigration`
3. Выполнить миграцию:
`python manage.py migration`
4. В файле `bot/__init__.py` в переменной `bot` указать [токен от своего бота](https://core.telegram.org/bots/api#authorizing-your-bot);
5. Запустить бота командой в терминале:  
`python manage.py start`

##### Для работы автоматического обновления ежедневного бюджета потребуется:
6. Запустить redis [через docker](https://hub.docker.com/_/redis):
`docker run --name=redis -p 6379:6379 -v redisdata:/data redis`
7. Запустить celery в первом терминале:
`celery -A dengi beat -l info`
8. И запустить worker во втором:
`celery -A dengi worker -l info -P eventlet`
#### Готово! Бот работает, автообновления включены.
  
--