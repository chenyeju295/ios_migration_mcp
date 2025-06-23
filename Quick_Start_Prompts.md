# 🚀 iOS改造快速提示词卡片

## 📱 新项目开始（复制粘贴使用）

### 1️⃣ 项目初始化
```
请使用MCP工具扫描我的iOS项目：

项目路径：/Users/[username]/[ProjectName]

执行步骤：
1. ios_scan_project - 扫描项目结构  
2. ios_setup_cursor_rules - 注入Cursor规则
3. 分析结果并给出改造建议

立即开始执行。
```

### 2️⃣ 开始改造文件
```
@creater_new_code_file.mdc @iOS_Code_Rules.mdc 

请改造这个iOS文件：[文件名.swift]

要求：
1. 生成1-2个新辅助类，同目录下
2. 可包含UIKit、Foundation、GCD技术栈
3. 在原文件中调用新代码，100%被调用
4. 新代码占比30%-50%
5. 保持原功能不变
6. 禁用敏感功能

完成后提供代码统计。
```

### 3️⃣ 更新进度
```
请使用MCP工具更新改造进度：

completed_files: ["刚完成的文件.swift"]
notes: "完成XX文件改造，新增XX功能"

然后显示总体进度统计。
```

## 🎯 常用提示词模板

### 小文件（<50行）
```
@creater_new_code_file.mdc 

轻量级改造：[文件名.swift]（[X]行）
- 生成1个辅助类
- 新代码占比40%-60%
- 至少3处调用点
```

### 中等文件（50-200行）
```
@creater_new_code_file.mdc 

标准改造：[文件名.swift]（[X]行）
- 生成2个不同功能类
- 70%方法调用新代码
- 占比35%-45%
```

### 大文件（200+行）
```
@creater_new_code_file.mdc 

深度改造：[文件名.swift]（[X]行）
- 生成2-3个互补类
- 不同设计模式
- 包含扩展(Extension)
- 占比30%-40%
```

### 敏感文件处理
```
@creater_new_code_file.mdc 

敏感文件处理：[文件名.swift]
包含敏感词：[payment/webview/js等]

1. 先分析敏感内容
2. 提供安全替代方案
3. 确保改造后合规
```

## 🔧 MCP工具快速调用

### 完整流程
```
执行MCP工具链：

1. ios_scan_project(project_path="[路径]")
2. ios_setup_cursor_rules(project_path="[路径]", cursor_project_root="[规则路径]")  
3. ios_analyze_file(file_path="[文件]", file_content="[内容]")
4. ios_generate_cursor_instructions(file_path="[文件]")
5. ios_update_progress(completed_files=["[文件]"])
6. ios_get_progress_statistics()
```

### 快速查看进度
```
使用ios_get_progress_statistics显示：
- 完成率
- 已完成文件
- 剩余文件
- 下步建议
```

## ✅ 质量检查

### 验证改造质量
```
验证改造结果：
1. 统计代码行数和占比
2. 检查调用完整性
3. 验证技术栈使用
4. 确认无敏感功能
5. 代码风格一致性
```

### 合规性检查
```
@iOS_Code_Rules.mdc

检查合规性：
- iOS开发标准
- 无敏感关键词
- 实际功能价值
- Apple审核风险
```

## 🚨 故障排除

### Cursor识别问题
```
如果@规则文件无法识别：
1. 检查.cursor/rules目录
2. 重新执行ios_setup_cursor_rules
3. 重启Cursor IDE
```

### 编译错误
```
改造后编译失败：
1. 提供错误信息
2. 检查导入语句
3. 验证访问权限
4. 确认语法正确
```

### 占比不达标
```
代码占比[X]%不符合30%-50%要求：
- 占比低：增加功能类
- 占比高：精简代码
```

---

## 📋 改造检查清单

- [ ] MCP工具扫描完成
- [ ] Cursor规则注入成功
- [ ] 新代码包含UIKit/Foundation/GCD
- [ ] 所有新代码被调用
- [ ] 代码占比30%-50%
- [ ] 无敏感功能
- [ ] 编译通过
- [ ] 进度已更新

---

*💡 提示：保存此卡片到书签，改造时随时参考！* 