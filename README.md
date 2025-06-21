# iOS Migration MCP Analyzer

一个专注于iOS代码迁移分析和改造规划的MCP工具，帮助开发者制定有效的代码多样性优化策略，并与Cursor AI深度集成。

## 核心功能

### 🔍 项目分析
- 自动扫描iOS项目代码结构
- 分析文件复杂度和改造潜力
- 评估代码风险等级
- 识别技术栈使用情况

### 📋 改造规划
- 生成详细的分阶段改造计划
- 提供具体的实施指导步骤
- 推荐最适合的改造策略
- 估算改造时间和复杂度

### ✅ 合规验证
- 检查代码是否符合iOS审核要求
- 验证敏感功能和框架使用
- 提供改进建议和最佳实践
- 确保代码质量标准

### 🎯 Cursor集成
- **自动设置Cursor Rules**: 在项目中创建`.cursor/rules`文件夹
- **智能指令生成**: 为特定文件生成Cursor改造指令
- **策略指导**: 提供详细的改造策略和模板
- **质量保证**: 与Cursor AI配合确保改造质量

## MCP工具列表

### 1. `ios_scan_project`
扫描分析iOS项目代码结构
```json
{
  "project_path": "/path/to/ios/project",
  "include_tests": false
}
```

### 2. `ios_analyze_file`
分析单个iOS代码文件的特征和改造潜力
```json
{
  "file_path": "ViewController.swift",
  "file_content": "class ViewController..."
}
```

### 3. `ios_generate_plan`
基于扫描结果生成详细的改造计划
```json
{
  "scan_results": "{...}",
  "priority": "safety"
}
```

### 4. `ios_validate_requirements`
验证代码是否符合iOS迁移要求
```json
{
  "file_content": "import UIKit..."
}
```

### 5. `ios_setup_cursor_rules` ⭐
**在项目目录中创建.cursor/rules文件夹并插入相关的cursor rules**
```json
{
  "project_path": "/path/to/ios/project",
  "include_optimization_strategies": true,
  "include_code_creation_rules": true
}
```

### 6. `ios_generate_cursor_instructions` ⭐
**为特定文件生成Cursor改造指令**
```json
{
  "file_path": "UserManager.swift",
  "strategy": "progressive"
}
```

### 7. `ios_get_strategies`
获取所有支持的改造策略和使用指南

### 8. `ios_get_requirements`
获取iOS代码迁移的基本要求和规范

## 改造策略

### 渐进式改造 (Progressive)
- **适用场景**: 低复杂度文件 (<100行)
- **代码占比**: 40-50%
- **优点**: 侵入性小，易于实现，风险低

### 扩展式改造 (Extension)
- **适用场景**: 中高复杂度文件 (>100行)
- **代码占比**: 30-40%
- **优点**: 最小侵入，结构清晰，易于维护

## 安全规范

### ✅ 必须包含
- UIKit框架使用
- Foundation系统函数
- DispatchQueue(GCD)
- NotificationCenter通知机制

### ❌ 禁止包含
- 支付相关功能
- WebView/JavaScript
- 内购功能
- 敏感数据处理

## 快速开始

### 1. 安装MCP工具
```bash
cd ios_migration_mcp
pip install -r requirements.txt
python main.py
```

### 2. 配置Cursor MCP
在Cursor的MCP设置中添加：
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

### 3. 完整工作流程

#### 步骤1: 项目初始化
```bash
# 扫描项目
ios_scan_project('/path/to/your/ios/project')

# 设置Cursor Rules
ios_setup_cursor_rules('/path/to/your/ios/project')
```

#### 步骤2: 生成改造计划
```bash
# 基于扫描结果生成计划
ios_generate_plan(scan_results, 'safety')
```

#### 步骤3: 执行改造
```bash
# 为特定文件生成Cursor指令
ios_generate_cursor_instructions('UserManager.swift', 'progressive')

# 在Cursor中使用生成的指令进行改造
# 引用: @iOS_Code_Rules.mdc @cursor_optimization_strategies.mdc
```

#### 步骤4: 验证结果
```bash
# 验证改造后的代码
ios_validate_requirements(modified_code)
```

## Cursor Rules 文件说明

使用`ios_setup_cursor_rules`后，会在项目中创建以下文件：

### `.cursor/rules/iOS_Code_Rules.mdc`
- 基于项目扫描结果自动生成
- 包含项目特定的代码规范
- 定义技术栈要求和安全规范

### `.cursor/rules/cursor_optimization_strategies.mdc`
- 详细的改造策略指导
- Cursor AI操作模板
- 代码示例和最佳实践

### `.cursor/rules/creater_new_code_file.mdc`
- 代码创建规则
- 多样性要求说明
- 质量检查标准

## 在Cursor中的使用方法

### 1. 引用规则文件
```
@iOS_Code_Rules.mdc
@cursor_optimization_strategies.mdc
@creater_new_code_file.mdc

请对当前文件进行iOS代码迁移改造
```

### 2. 使用生成的指令
```
# 使用MCP工具生成的具体指令
请对文件 UserManager.swift 进行渐进式改造:

1. **分析阶段**
   - 分析当前类的业务功能和代码结构
   - 识别可以插入新代码的安全位置
   - 评估每个方法的改造潜力

2. **设计阶段**
   - 创建3-5个相关的辅助类/工具类
   - 每个辅助类必须包含：
     * 私有属性 (private var/let)
     * GCD队列处理 (DispatchQueue)
     * UIKit组件使用
     * Foundation系统API调用
     * 闭包/回调机制

3. **实施阶段**
   - 在每个原有方法的开始、中间或结束位置插入辅助类调用
   - 确保插入位置自然，不破坏原有逻辑
   - 保证70%以上的方法都调用新代码
   - 控制新增代码占比在40-45%

4. **验证阶段**
   - 检查代码编译无误
   - 验证所有新代码都被调用
   - 确认无敏感功能实现

请严格按照 @iOS_Code_Rules.mdc 中的规范执行改造。
```

## 项目结构

```
ios_migration_mcp/
├── cursorrules/                    # Cursor规则模板
│   ├── cursor_optimization_strategies.mdc
│   └── creater_new_code_file.mdc
├── src/
│   ├── core/
│   │   └── config.py              # 基础配置管理
│   └── analyzers/
│       ├── project_scanner.py     # 项目扫描器
│       └── file_analyzer.py       # 文件分析器
├── tests/                         # 单元测试
├── docs/                          # API文档
├── main.py                        # MCP服务器
└── requirements.txt               # 依赖列表
```

## 最佳实践

### 1. 改造前准备
- 备份原始代码
- 确保项目可正常编译运行
- 使用MCP工具进行全面分析

### 2. 改造过程中
- 严格按照MCP生成的计划执行
- 每完成一个文件就进行测试
- 使用Cursor Rules确保代码质量

### 3. 改造完成后
- 全面测试所有功能
- 使用MCP工具验证合规性
- 准备提交审核

## 技术特点

- **智能分析**: 基于代码结构自动分析改造潜力
- **策略推荐**: 根据文件复杂度推荐最适合的改造策略
- **Cursor集成**: 深度集成Cursor AI，提供智能改造指导
- **质量保证**: 多重验证机制确保改造质量
- **安全合规**: 严格的安全规范防止审核风险

## 注意事项

- 本工具专注于分析和规划，实际代码改造由Cursor AI执行
- 所有改造建议需要开发者结合实际情况判断
- 建议在改造前充分测试和备份
- 改造后需要进行全面的功能验证

## 技术支持

如有问题或建议，请查看项目文档或联系开发团队。 