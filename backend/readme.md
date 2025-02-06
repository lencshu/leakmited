# quickstart

## lib install

```sh
pip install -r requirements.txt
```

## cmd

```sh
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
pytest tests -m sls
```
