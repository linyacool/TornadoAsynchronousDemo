# TornadoAsynchronousDemo
###一个简单的Tornado异步Demo
使用Python3.5/3.6开发<br>
数据库为MongoDB,用motor连接<br>
###三层结构：
MongoDB_control负责直接与数据库交互，编写数据库通用函数<br>
ORM负责一个MongoDB中具体的表与上层handler的交互，调用control中的函数操纵数据库中某一个属性<br>
Router编写各种具体的Handler<br>
