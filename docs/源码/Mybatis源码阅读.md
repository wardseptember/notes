# Mybatis

mybatis是把字段映射为对象的属性。

MapperRegistry类处理mapper类，MapperProxyFactory动态代理实现mapper接口类，MapperAnnotationBuilder类负责解析mapper接口类

SqlSourceBuilder负责构建sql语句，例如把`select * from student where sno=#{sno}`解析为`select * from student where sno=?`