# ema_books_downloader

## Information

> Download books from [ranobelib.me](https://ranobelib.me/) or [lightnovels.me](https://lightnovels.me/) \
> Depends on `Selenium` and `Xvfb`


## Running

> docker

```
docker build -t books_downloader . && \
docker run --privileged --name ema_books_downloader --rm \
-p 4000:4000 -d -v $(pwd):/usr/src/app  -it books_downloader && \
docker exec -it ema_books_downloader bash
```
```
bash start.sh
```

> docker-compose

```
docker compose stop && \
docker compose build && \
docker compose up -d && \
docker compose exec selenium bash
```
```
bash start.sh
```



## Exemple url

> [ranobelib.me](https://ranobelib.me/) \
>https://ranobelib.me/arifureta-shokugyou-de-sekai-saikyou-novel/v1/c0 \
>Arifureta


> [lightnovels.me](https://lightnovels.me/) \
>https://lightnovels.me/i-alone-level-up/chapter-1.html \
>Solo leveling
