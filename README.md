## simple_rpc

RPC的设计思想是力图**使远程调用中的通讯细节对于使用者透明**，调用双方无需关心网络通讯的具体实现。因而实现RPC要进行一定的封装。 

### 调用流程

![RPC结构](https://github.com/LMFrank/simple_rpc/blob/master/images/RPC1.png)

1. Client在本地发起调用
2. Client Stub收到调用后负责将调用的方法及参数等按照消息协议打包并进行网络发送
3. Server Stub收到后按照消息协议拆包，并且根据方法名和参数进行本地调用
4. Server本地调用执行后将执行结果传给Server Stub
5. Server Stub将返回结果按照消息协议打包并进行网络发送
6. Client Stub收到消息后进行拆包将结果返回给Client
7. Client得到本次RPC调用的结果

### 二进制消息协议的实现

#### 调用请求消息

- 方法名为`divide`

- 第1个调用参数为整型int，名为`num1`

- 第2个调用参数为整型int，名为`num2`，默认值为1

![调用请求消息](https://github.com/LMFrank/simple_rpc/blob/master/images/RPC2.png)

#### 调用返回消息

- 正常返回float类型
- 错误会抛出`InvalidOperation`异常

![调用返回消息](https://github.com/LMFrank/simple_rpc/blob/master/images/RPC3.png)

### RPC传输完整实现

- 传输方式：TCP

- 二进制作为数据传输格式

  - 使用`struct`模块，[使用文档]( https://docs.python.org/3/library/struct.html#format-characters )

- 加入了多线程的RPC服务器

- 项目结构：

  ![项目结构](https://github.com/LMFrank/simple_rpc/blob/master/images/treefile.bmp)

- 使用方法：先开启`server`目录下的main.py再开启`client`目录下的main.py