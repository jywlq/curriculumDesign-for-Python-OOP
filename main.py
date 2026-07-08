# 程序入口
from src.services import personService
from src.models import teacher,experimenter

s1=personService()
tc=teacher('T001','张三','男','35','计算机系','副教授')
exp=experimenter('E001','李四','女','28','化学实验室','实验员')
s1.addPerson(tc)
s1.addPerson(exp)
print(len(s1.personList))
s1.deletePerson("T001")
print(len(s1.personList))
