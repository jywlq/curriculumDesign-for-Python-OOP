# 待实现的想法

## 方法重构
- deletePerson、updatePerson、getPersonStatistics 改为基于 findPerson 实现
- 给这些方法加 list 参数，默认为 self.personList，支持传入筛选后的列表

## findPerson 修复
- 无参调用时返回 self.personList.copy() 而不是内部引用
