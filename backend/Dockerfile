FROM python:3.12

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0

RUN python -m pip install uv

RUN uv pip install --system --no-cache-dir -r requirements.txt

COPY . /code

CMD ["fastapi", "run", "main.py", "--port", "80"]
