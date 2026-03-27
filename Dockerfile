FROM debian:latest

RUN apt-get update -y && apt upgrade -y
RUN apt-get install python3 python3.13-venv -y

WORKDIR /root

COPY . .

RUN tar --no-same-owner -xvf infection.tar

RUN python3 -m venv /opt/venv
ENV PATH=/opt/venv/bin:$PATH
RUN pip install --no-cache-dir -r requirements.txt

RUN echo "source /opt/venv/bin/activate" >> /root/.bashrc

ENTRYPOINT ["tail", "-f", "/dev/null"]
