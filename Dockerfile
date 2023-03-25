FROM explainable-ai-display-base

ARG HOST_ADDRESS
ENV HOST_ADDRESS ${HOST_ADDRESS}

COPY . /jason/
WORKDIR /jason

#RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
#RUN #pip install --timeout 900 --no-cache-dir -r requirements.txt
#
RUN pip install aiofiles
RUN chmod +x bin/start.sh


EXPOSE 8080
EXPOSE 5000
ENTRYPOINT ["/bin/bash","bin/start.sh"]


