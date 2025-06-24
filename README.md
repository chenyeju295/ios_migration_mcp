# iOS 代码迁移优化工具 - Cursorrules

## 项目简介

本项目是一个基于 Cursor AI 的 iOS 代码迁移优化工具，专门用于防止 iOS 应用提审时因重复代码而被拒绝的问题。通过智能代码分析和改造规划，帮助开发者制定有效的代码多样性优化策略。

## 核心功能

- ✅ **智能项目扫描**: 自动扫描分析iOS项目中的Swift/OC代码文件
- ✅ **改造计划生成**: 基于分析结果生成详细的改造计划和优先级
- ✅ **Cursor Rules集成**: 自动为项目创建.cursor/rules配置文件
- ✅ **改造指令生成**: 生成具体的Cursor指令，引导逐步完成改造
- ✅ **合规验证**: 检查代码是否符合Apple审核标准
- ✅ **策略指导**: 提供多种改造策略和实施建议

## MCP工具使用

### 安装和配置




1. MCP环境
** 安装python、uv **

- Python 环境 3.10+
- 下载地址： https://www.python.org/downloads/

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
uv --version
```
```bash
cd ios_migration_mcp
pip install -r requirements.txt
uv run --with fastmcp fastmcp dev ./main.py
```

2. **配置Cursor MCP**
在Cursor的MCP设置中添加：
```json
{
  "mcpServers": {
    "ios_migration_mcp": {
      "command": "uv",
      "args": [
        "run",
        "--with",
        "fastmcp",
        "fastmcp",
        "run",
        "/Users/chenyeju/Documents/cursorrules/ios_migration_mcp/main.py"
      ]
    }
  }
}
```

### 完整工作流程

#### 步骤1: 项目初始化

### 1️⃣ 项目初始化
```
请使用MCP工具扫描我的iOS项目：
目标目录：/Users/chenyeju/Documents/***
主题：******
请按照以下步骤执行：
1. 使用 ios_scan_project 扫描 project_path：/Users/chenyeju/Documents/***
2. 使用 ios_setup_cursor_rules 注入Cursor规则文件
3. 分析扫描结果，给出改造建议

开始执行MCP工具调用。
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

#### 步骤3: 执行改造
```bash
# 为特定文件生成Cursor改造指令
ios_generate_cursor_instructions('UserManager.swift', 'progressive')

# 在Cursor中使用生成的指令进行改造
# 引用: @iOS_Code_Rules.mdc @cursor_optimization_strategies.mdc
```
 

### MCP工具列表

- `ios_scan_project` - 扫描分析iOS项目代码结构
- `ios_analyze_file` - 分析单个文件的特征和改造潜力
- `ios_generate_plan` - 生成详细的改造计划 
- `ios_setup_cursor_rules` - 为项目创建Cursor rules配置
- `ios_generate_cursor_instructions` - 生成特定文件的改造指令
- `ios_get_strategies` - 获取所有支持的改造策略
- `ios_get_requirements` - 获取iOS迁移要求和规范

## 改造策略

### 渐进式改造 (Progressive)
- **适用场景**: 低复杂度文件 (<100行)
- **代码占比**: 40-50%
- **优点**: 侵入性小，易于实现，风险低

### 扩展式改造 (Extension)
- **适用场景**: 中高复杂度文件 (>100行)
- **代码占比**: 30-40%
- **优点**: 最小侵入，结构清晰，易于维护

## 安全合规要求

### ✅ 必须包含
- UIKit框架使用
- Foundation系统函数调用
- DispatchQueue(GCD)并发处理
- NotificationCenter通知机制

### ❌ 严禁包含
- 支付相关功能
- WebView/JavaScript注入
- 内购功能实现
- 敏感数据处理
- 网络匹配功能

## Cursor Rules自动配置

使用`ios_setup_cursor_rules`后，工具会在项目中自动创建：

- `.cursor/rules/iOS_Code_Rules.mdc` - 基于项目分析的代码规范
- `.cursor/rules/cursor_optimization_strategies.mdc` - 详细改造策略指导
- `.cursor/rules/creater_new_code_file.mdc` - 代码创建和多样性规则

## 项目结构

```
cursorrules/
├── ios_migration_mcp/          # MCP工具主目录
│   ├── main.py                 # MCP服务器主文件
│   │   ├── src/                    # 源代码目录
│   │   │   ├── analyzers/          # 代码分析器
│   │   │   └── core/               # 核心配置
│   │   ├── cursorrules/            # Cursor规则模板
│   │   └── docs/                   # API文档
│   ├── .cursor/                    # Cursor配置目录
│   └── README.md                   # 项目说明
```

## 质量验证流程

1. **编译检查**: 确保项目能正常编译
2. **功能测试**: 验证所有原有功能正常
3. **性能测试**: 确认性能无明显下降 

## 技术支持

- 基于FastMCP框架构建
- 支持Swift和Objective-C项目
- 与Cursor AI深度集成
- 提供完整的类型安全和错误处理

## 使用示例

```python
# 扫描项目
result = ios_scan_project('/Users/project/MyiOSApp')

# 分析单个文件  
analysis = ios_analyze_file('UserManager.swift', file_content)

# 生成改造计划
plan = ios_generate_plan(scan_results, 'safety')
 
```

更多详细信息请参考 `ios_migration_mcp/README.md` 和 API 文档。 
