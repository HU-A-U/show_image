FROM daocloud.io/ubuntu:16.04
MAINTAINER hu_a_u@163.com

# APT 自动安装 Python 相关的依赖包，如需其他依赖包在此添加
RUN apt-get update && \
    apt-get install -y python3 \
                       python-dev \
                       python-pip  \
    # 用完包管理器后安排打扫卫生可以显著的减少镜像大小
    && apt-get clean \
    && apt-get autoclean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*


# 配置默认放置 App 的目录
RUN mkdir /code
WORKDIR /code
COPY . /code
RUN chmod +x docker-entrypoint.sh

ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY docker-entrypoint.sh /usr/local/bin/

EXPOSE 6666
CMD /code/docker-entrypoint.sh