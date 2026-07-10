# 待实现的想法

## 方法重构
- deletePerson、updatePerson、getPersonStatistics 改为基于 findPerson 实现
- 给这些方法加 list 参数，默认为 self.personList，支持传入筛选后的列表

## findPerson 修复
- 无参调用时返回 self.personList.copy() 而不是内部引用（已完成）

## 回收站

## rich库优化输出

## TUI界面（Textual库）
- 后续考虑用Textual库（基于rich）实现TUI界面
- 支持鼠标点击输入框、焦点切换等交互
- 实现类似GUI的体验
