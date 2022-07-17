# LED-server

## RUN
```cmd
pipenv run uvicorn server:app  --reload
```

## Mypy check
```cmd
pipenv run mypy ./src
```

## Flake8 check
```cmd
pipenv run flake8 ./src
```

## Coverage check
```cmd
pipenv run coverage run -m pytest
```
