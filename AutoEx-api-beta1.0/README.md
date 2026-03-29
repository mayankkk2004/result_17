# AutoEx
Well, its a small bot to get RGPV result
and (now) it uses a fancy neural network specifically trained to solve the Captchas used by the website. 

## Setup

```bash
pip install -r requirements.txt
```

## Running the API Server

```bash
python api.py <PORT>
# Example:
python api.py 8080
```

The server exposes:
- `GET /` — health check (`Hello, World!`)
- `POST /requests` — submit a result-fetch job; body: `{"department":"0","semester":"3","maxroll":"60","rollPrefix":"0318EX010"}`; returns `{"uuid":"..."}`
- `GET /progress?uuid=<uuid>` — check progress of a job
- `GET /getfile?uuid=<uuid>` — download the generated CSV once complete

## Running as a Standalone Script

```bash
python main.py
```

## Verify the Neural Network Model

```bash
python run_captcha_model.py
```

## Note on Model File
The `captcha_model.hdf5` must be committed/transferred as a **binary** file (see `.gitattributes`). If it gets corrupted during text-mode transfer, re-upload the file. The API will still start and report the error gracefully.

# Windows

On Windows, Tensorflow requires Visual C++ 2015 redistributable to be installed, get it here https://www.microsoft.com/en-us/download/details.aspx?id=53587
