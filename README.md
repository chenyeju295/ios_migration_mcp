# iOS Migration MCP Server

![MCP Badge](https://img.shields.io/badge/MCP-Model%20Context%20Protocol-blue)
![Swift Badge](https://img.shields.io/badge/Swift-iOS-orange)
![Cursor Badge](https://img.shields.io/badge/Cursor-AI%20IDE-green)

一个专门为iOS代码迁移和改造设计的MCP服务器，帮助避免因重复代码而被Apple审核拒绝。该工具基于MCP协议与Cursor AI深度集成，提供智能代码改造、进度跟踪和项目规则制定。

## 🚀 核心特性

### 简化的6个MCP工具
- **项目扫描** (`ios_scan_project`) - 快速分析项目结构和文件信息
- **规则注入** (`ios_setup_cursor_rules`) - 自动注入Cursor规则到IDE
- **文件分析** (`ios_analyze_file`) - 分析单个文件的基本信息
- **指令生成** (`ios_generate_cursor_instructions`) - 生成具体改造指令
- **进度管理** (`ios_update_progress`) - 跟踪改造进度
- **质量评估** (`ios_get_progress_statistics`, `ios_evaluate_project_quality`) - 评估改造质量

### 统一文件管理
采用统一命名的记录文件，避免文件累积：
- `latest_scan_result.json` - 最新项目扫描结果
- `transformation_progress.json` - 改造进度跟踪
- `cursor_rules_injection.json` - 规则注入记录
- `README.md` - 说明文档

### 智能代码生成规则
- **多样性保证** - 每个类/扩展内容唯一，禁止模板化
- **技术栈要求** - 强制使用UIKit+Foundation+GCD技术栈
- **安全性约束** - 严禁支付、WebView、JavaScript等敏感功能
- **调用完整性** - 确保100%新代码被调用，70%方法覆盖率

## 📦 快速开始

### 1. 安装依赖
```bash
cd ios_migration_mcp
pip install -r requirements.txt
```

### 2. 启动MCP服务器
```bash
uv run --with fastmcp fastmcp dev ./main.py
```

### 3. 在Cursor中配置MCP工具
服务器启动后，在Cursor中配置MCP连接，即可使用6个iOS迁移工具。

## 🔧 使用工作流

### 阶段1：项目初始化
```python
# 1. 扫描iOS项目
ios_scan_project("/path/to/ios/project")

# 2. 注入Cursor规则
ios_setup_cursor_rules("/path/to/ios/project", "/path/to/cursor/workspace")

# 3. 在Cursor中引用规则
# @iOS_Code_Rules.mdc
# @creater_new_code_file.mdc 
# @cursor_optimization_strategies.mdc
```

### 阶段2：文件改造
```python
# 对每个文件执行：
# 1. 分析文件
ios_analyze_file("file_path", "file_content")

# 2. 获取改造指令
ios_generate_cursor_instructions("file_path", strategy="flexible")

# 3. 在Cursor中执行改造
# 4. 更新进度
ios_update_progress("/path/to/project", ["completed_file"], "改造完成")
```

### 阶段3：质量验证
```python
# 1. 查看整体进度
ios_get_progress_statistics("/path/to/project")

# 2. 评估项目质量
ios_evaluate_project_quality("/path/to/project")
```

## 📋 Cursor Rules 文件说明

### 1. `creater_new_code_file.mdc`
**代码创建核心规则**
- MCP工具集成说明
- 详细技术要求（GCD+UIKit+Foundation+闭包）
- 安全性约束和禁用敏感词列表
- 标准改造流程和检查清单

### 2. `cursor_optimization_strategies.mdc`
**Cursor优化策略指南**
- 6个MCP工具的详细使用说明
- 渐进式和扩展式改造策略
- 代码模板库（数据处理、UI增强、缓存管理）
- 插入策略和质量检查清单
- 统一文件管理优势说明

### 3. `iOS_Code_Rules.mdc`
**项目特定规则**（动态生成）
- 基于项目扫描结果生成的特定规则
- 包含项目统计信息和技术栈建议
- MCP工具集成命令说明

## 🎯 核心改造原则

### 功能逻辑不变
- 严格保持原有代码的所有功能逻辑
- 不改变任何现有的业务流程和数据处理
- 确保改造后的代码与原有系统完全兼容

### 代码丰富化
- 在不改变逻辑的前提下丰富现有功能
- 根据文件特点选择合适的改造方式
- 适度添加相关功能，不强制固定比例

### 技术栈多样性
- 强制使用UIKit+Foundation+GCD技术栈
- 每个类必须包含私有属性、闭包、系统函数调用
- 使用不同设计模式避免模板化

### 安全合规
- 禁止支付、WebView、JavaScript等敏感功能
- 不收集任何敏感数据
- 遵循Apple审核指南

## 📊 统计和监控

### 代码占比要求
- 新增代码占比：30-50%
- 新代码调用率：100%
- 方法覆盖率：70%以上

### 质量指标
- 编译通过率：100%
- 功能完整性：保持原有逻辑不变
- 代码风格：与原项目保持一致
- 安全性：通过敏感内容检测

## 🔍 故障排除

### 常见问题

1. **MCP服务器无法启动**
   - 检查Python依赖是否安装完整
   - 确认端口6277没有被占用
   - 查看控制台错误信息

2. **Cursor中无法识别MCP工具**
   - 重启MCP服务器
   - 检查Cursor的MCP配置
   - 确认网络连接正常

3. **记录文件过多**
   - 现在已使用统一文件命名，避免累积
   - 如有旧的时间戳文件可手动清理

4. **规则注入失败**
   - 确认Cursor项目根目录路径正确
   - 检查`.cursor/rules`目录权限
   - 重新运行`ios_setup_cursor_rules`

## 🤝 贡献指南

欢迎提交Issue和Pull Request来改进这个工具。请确保：
1. 遵循现有的代码风格
2. 添加适当的测试
3. 更新相关文档
4. 确保不引入敏感功能

## 📄 许可证

本项目采用MIT许可证。详见 [LICENSE](LICENSE) 文件。

## 🎉 致谢

感谢Cursor AI和MCP协议为开发者提供的强大工具链支持。

---

**注意**: 本工具专门用于合法的iOS代码迁移和改造，请确保使用时遵循相关法律法规和平台政策。 