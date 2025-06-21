# iOS Migration MCP Analyzer - 快速开始

这是一个专注于iOS代码迁移分析和改造规划的MCP工具，帮助您制定有效的代码多样性优化策略。

## 🚀 快速开始

### 1. 安装MCP工具

```bash
cd ios_migration_mcp
pip install -r requirements.txt
```

### 2. 启动MCP服务器

```bash
python main.py
```

### 3. 在Cursor中配置MCP

将以下配置添加到Cursor的MCP设置中：

```json
{
  "mcpServers": {
    "ios-migration-analyzer": {
      "command": "python",
      "args": ["/path/to/ios_migration_mcp/main.py"],
      "env": {}
    }
  }
}
```

## 📋 基本使用流程

### 步骤1: 扫描项目

首先扫描您的iOS项目以获得全面分析：

```python
# 自动检测主题
ios_scan_project('/path/to/your/ios/project', 'auto', false)

# 或指定特定主题
ios_scan_project('/path/to/your/ios/project', 'social', false)
```

### 步骤2: 分析单个文件

对特定文件进行详细分析：

```python
ios_analyze_file(
    'ViewController.swift',
    'import UIKit\nclass ViewController: UIViewController {...}',
    'social'
)
```

### 步骤3: 生成改造计划

基于扫描结果生成详细的改造计划：

```python
ios_generate_plan(scan_results_json, 'safety')
```

### 步骤4: 验证代码合规性

检查代码是否符合iOS迁移要求：

```python
ios_validate_requirements(file_content, 'social')
```

## 🎯 主题选择指南

### 自动检测 (推荐)
```python
ios_scan_project('/path/to/project', 'auto', false)
```

### 手动指定主题
- **social**: 社交类APP (聊天、分享、好友功能)
- **ecommerce**: 电商类APP (购物、商品、订单功能)
- **tool**: 工具类APP (实用工具、管理功能)
- **entertainment**: 娱乐类APP (视频、音乐、游戏功能)
- **education**: 教育类APP (课程、学习、测验功能)

## 📊 理解分析结果

### 项目扫描结果
```json
{
  "project_path": "/path/to/project",
  "theme": "social",
  "total_files": 15,
  "files": [
    {
      "path": "ViewController.swift",
      "risk_level": "low",
      "transformation_potential": "high",
      "line_count": 150
    }
  ]
}
```

### 文件分析结果
```json
{
  "complexity": "medium",
  "transformation_suggestions": [
    "建议添加Social相关的辅助类",
    "已使用UIKit，可以添加UI相关的主题功能"
  ],
  "recommended_strategy": "progressive",
  "estimated_code_ratio": 0.4
}
```

## 🛠️ 改造策略选择

### 渐进式主题注入法 (Progressive)
- **适用**: 低风险文件，代码结构简单
- **特点**: 侵入性小，易于实现
- **代码占比**: 40-50%

### 扩展式改造法 (Extension)
- **适用**: 中高风险文件，复杂业务逻辑
- **特点**: 最小侵入，结构清晰
- **代码占比**: 30-40%

## ✅ 合规性检查

### 必须包含的技术栈
- ✅ UIKit框架
- ✅ Foundation系统函数
- ✅ DispatchQueue(GCD)
- ✅ 主题相关功能

### 禁止的敏感功能
- ❌ 支付相关功能
- ❌ WebView/JavaScript
- ❌ 内购功能
- ❌ 敏感数据处理

## 📝 实际操作示例

### 完整分析流程

1. **扫描项目**
```python
scan_result = ios_scan_project('/Users/dev/MyApp', 'auto', false)
```

2. **生成改造计划**
```python
plan = ios_generate_plan(scan_result, 'safety')
```

3. **按计划执行改造**
根据计划中的指导步骤手动修改代码

4. **验证改造结果**
```python
validation = ios_validate_requirements(modified_code, 'social')
```

### 获取支持信息

```python
# 查看所有支持的主题
themes = ios_get_themes()

# 查看所有改造策略
strategies = ios_get_strategies()
```

## 🔧 故障排除

### 常见问题

1. **MCP服务器无法启动**
   - 检查Python环境和依赖安装
   - 确认端口未被占用

2. **项目扫描失败**
   - 验证项目路径是否正确
   - 确认项目包含Swift/Objective-C文件

3. **主题检测不准确**
   - 手动指定正确的主题类型
   - 检查项目代码是否包含相关关键词

### 调试模式

启用详细日志输出：
```bash
DEBUG=1 python main.py
```

## 📚 进阶使用

### 自定义优先级策略

- **safety**: 优先处理低风险文件
- **speed**: 优先处理小文件
- **coverage**: 均匀分布改造任务

### 分阶段实施

工具会自动将改造任务分为5个阶段，每个阶段包含：
- 具体的文件列表
- 详细的实施指导
- 风险评估和时间估算

## 💡 最佳实践

1. **改造前准备**
   - 备份原始代码
   - 确保项目可正常编译运行
   - 准备充分的测试环境

2. **改造过程中**
   - 严格按照计划执行
   - 每完成一个文件就进行测试
   - 记录遇到的问题和解决方案

3. **改造完成后**
   - 全面测试所有功能
   - 验证代码合规性
   - 准备提交审核

## 📞 技术支持

如有问题或建议，请：
- 查看项目文档
- 检查日志输出
- 联系开发团队 