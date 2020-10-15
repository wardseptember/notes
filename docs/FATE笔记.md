# 单机版

```shell
#获取安装包
wget https://webank-ai-1251170195.cos.ap-guangzhou.myqcloud.com/docker_standalone-fate-1.4.1.tar.gz
tar -xzvf docker_standalone-fate-1.4.1.tar.gz

#执行部署
cd docker_standalone-fate-1.4.1
bash install_standalone_docker.sh
```

测试

```shell
CONTAINER_ID=`docker ps -aqf "name=fate_python"`
docker exec -t -i ${CONTAINER_ID} bash
bash ./federatedml/test/run_test.sh
```

## 快速开始

```
CONTAINER_ID=`docker ps -aqf "name=fate_python"`
docker exec -t -i ${CONTAINER_ID} bash
cd /fate/examples/federatedml-1.x-examples
```

## 实现Catboost联邦化过程

