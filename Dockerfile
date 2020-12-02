FROM python:3

WORKDIR /root/dockerCtrl/MercadoPy

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "ServiceAPI.py" ]
