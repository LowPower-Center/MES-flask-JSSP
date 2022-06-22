# MES-flask-JSSP

## 说明
### Part1 flask_part
+ 基于flask-adminlte模板,源码在此https://github.com/app-generator/flask-adminlte
+ 使用js-grid制作了简单页面，包括：物料、产品、工艺路线、订单管理
+ 加入了两个WebGL文件，分别演示仓储和装配单元简易运动
+ 引入了车间调度算法，根据生产订单绘制出甘特图
+ 视频演示参见https://www.bilibili.com/video/BV12g411Q7yb

### Part2 L2D算法
+ 基于L2D算法，源码在此https://github.com/zcaicaros/L2D
+ 修改了部分算法接口，将处理数据进行了调整
+ env_lab.py用于实现车间调度


### Part3 node-red
+ 配置文件为ai.json，在node-red直接导入流程即可
+ 对应的exec模块中将文件路径改为算法实际部署路径即可运行


### 部署说明
+ flask部分单独部署，使用pipenv构建虚拟环境,启动flask即可
  + ```pip install pipenv```
  + ```pipenv install```
  + ```pipenv shell```
  + ```flask run```

+ node-red部分可部署到局域网主机中或其他位置，对应的需要修改flask项目中请求的http地址
+ 以kali虚拟机为例，node-red和L2D算法部署在虚拟机中，L2D算法部署不再使用虚拟环境
  + ```pip install -r requirement.txt  ```
  + 进入L2D算法目录下，```python env_lab.py ```测试算法




