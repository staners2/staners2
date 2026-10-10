# Оформление профиля staners2

Оформление ориентировано на людей, нанимающих DevOps-инженеров: краткая специализация, статистика GitHub и один проект — **Boosty for Samsung TV**. Репозиторий профиля: [staners2/staners2](https://github.com/staners2/staners2).

## Bio и закреплённый проект

Готовый текст для Bio:

```text
DevOps engineer | Kubernetes, CI/CD & automation | Python, Go | Building infrastructure tools and practical integrations.
```

Имя: **Dima Aratin**. Telegram и LinkedIn перенесены из текущего публичного профиля. Работодатель, стаж и сертификаты не добавлены.

Закрепить только [boosty-samsung-tv](https://github.com/staners2/boosty-samsung-tv). Описание и topics у него уже заполнены; в README он представлен скриншотом, назначением и четырьмя направлениями работы: развёртывание, интеграция, медиа и доставка изменений.

## Что показывает статистика

Цифры находятся в assets/stats.json; дата обновления указана на изображениях.

| Показатель | Источник и границы |
| --- | --- |
| Contributions | Сумма ежедневной активности за последние 365 дней из публичного календаря GitHub. Включает анонимизированную приватную активность, если она уже показана в профиле. Это не число коммитов. |
| Public commits | GitHub Search: author:staners2 is:public, за всё доступное время. Поиск индексирует default branches; коммиты в других ветках, приватных репозиториях и на других Git-хостах сюда не входят. |
| Original repos | Число собственных публичных репозиториев с fork=false. Форки исключены. |
| Pull requests | GitHub Search: author:staners2 type:pr is:public, за всё доступное время. |
| График | Contributions из того же окна в 365 дней, сгруппированные по месяцам. Первый и последний месяцы могут быть неполными. |
| Языки | Основной язык каждого публичного репозитория без форков. Это число репозиториев, а не процент строк кода или оценка навыка. |

Статистика относится ко всему GitHub-профилю. В витрине проектов остаётся только Boosty. Пустые или неполные ответы источников останавливают обновление; опубликованные карточки сохраняются.

## Пересборка и просмотр

```sh
python3 tools/update_stats.py
python3 tools/build_preview.py
python3 -m http.server 8765 --bind 127.0.0.1
```

Открыть http://127.0.0.1:8765/preview.html. Можно переключать тему и ширину README. HTML обрабатывается GitHub Markdown API; окружающий интерфейс — локальная имитация. После публикации нужна проверка на самом GitHub.

update_stats.py использует стандартную библиотеку Python. Для публичных данных локально токен не обязателен; GITHUB_TOKEN повышает лимиты GitHub API. Токен отправляется только в api.github.com и не записывается в файлы. Статистика собирается из публичных источников; имена приватных репозиториев не запрашиваются.

Цвета и баннеры задаются в tools/build_preview.py; композиция статистики — в tools/update_stats.py. SVG являются производными файлами: менять генераторы и пересобирать. Изображения для узких экранов выбираются через picture при ширине до 600 px.

Скриншот assets/boosty-feed.png взят без изменений из публичного README Boosty. Он показывает настольный браузер с демонстрационными материалами; работа нативного плеера на физическом TV этим скриншотом не подтверждается.

## Ежедневное обновление

.github/workflows/profile-stats.yml настроен для staners2/staners2: ежедневный запуск в 03:23 UTC и ручной workflow_dispatch. Он запускает проверки, собирает публичные данные и сохраняет только SVG статистики и stats.json.

Используется штатный github.token с contents: write, отдельный PAT не нужен. Коммиты делает github-actions[bot], поэтому они не попадают в поисковый счётчик коммитов автора staners2. Ручной запуск: gh workflow run profile-stats.yml --repo staners2/staners2.

## Публикация

Публичный репозиторий **staners2/staners2** содержит:

```text
README.md
PROFILE-SETUP.md
.gitignore
.github/workflows/profile-stats.yml
assets/
tools/build_preview.py
tools/update_stats.py
tools/test_update_stats.py
```

preview.html и Python __pycache__ исключены из Git. После изменения генераторов нужно пересобрать изображения; после публикации — проверить README на самом GitHub и запустить Update profile statistics вручную. Bio и закреплённые репозитории настраиваются отдельно от README.

## Проверка

```sh
python3 -m unittest discover -s tools -p 'test_*.py'
```

Проверки покрывают счётчики календаря, отсутствующие или изменившиеся tooltip, дубли дат, исключение форков и приватных репозиториев, неполный поиск и корректный нулевой результат. Ссылка LinkedIn совпадает с текущим профилем, но LinkedIn блокирует автоматическое чтение страницы.

## Источники

- [Публичный профиль](https://github.com/staners2)
- [Публичный календарь](https://github.com/users/staners2/contributions)
- [Boosty: README и скриншоты](https://github.com/staners2/boosty-samsung-tv)
- [GitHub: contributions и приватная активность](https://docs.github.com/en/account-and-profile/concepts/contributions-on-your-profile)
- [GitHub: поиск коммитов](https://docs.github.com/en/search-github/searching-on-github/searching-commits)
- [GitHub: profile README](https://docs.github.com/en/account-and-profile/how-tos/profile-customization/managing-your-profile-readme)
