# Mybatis

用于实现面向对象编程语言里，不同类型系统的数据之间的转换。

mybatis是把字段映射为对象的属性。

MapperRegistry类处理mapper类，MapperProxyFactory动态代理实现mapper接口类，MapperAnnotationBuilder类负责解析mapper接口类

SqlSourceBuilder负责构建sql语句，例如把`select * from student where sno=#{sno}`解析为`select * from student where sno=?`

<div align="center"> <img src="https://gitee.com/wardseptember/images/raw/master/imgs/20201105193330.png" width="600"/> </div><br>