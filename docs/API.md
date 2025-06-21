# iOS Migration MCP Server API 文档

## 概述

iOS Migration MCP Server 提供两个主要的MCP工具，用于iOS代码的扫描分析和优化改造。

## MCP 工具

### 1. ios_scan_project

扫描分析iOS项目代码结构，自动检测APP主题并分析文件特征。

#### 函数签名

```python
ios_scan_project(
    project_path: str,
    theme: str = "auto",
    include_tests: bool = False
) -> str
```

#### 参数说明

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| project_path | str | - | iOS项目根目录的绝对路径 |
| theme | str | "auto" | APP主题类型，可选值: auto/social/ecommerce/tool/entertainment/education |
| include_tests | bool | False | 是否包含测试文件 |

#### 返回值

返回JSON格式的扫描结果，包含以下字段：

```json
{
  "project_path": "项目路径",
  "theme": "检测到的主题",
  "timestamp": "扫描时间",
  "summary": {
    "total_files": "总文件数",
    "swift_files": "Swift文件数",
    "objc_files": "Objective-C文件数",
    "total_lines": "总行数"
  },
  "files": [
    {
      "path": "文件相对路径",
      "type": "文件类型(swift/objc)",
      "line_count": "行数",
      "class_count": "类数量",
      "method_count": "方法数量",
      "complexity": "复杂度(low/medium/high)",
      "theme_relevance": "主题相关性",
      "transformation_potential": "改造潜力",
      "risk_level": "风险级别"
    }
  ],
  "recommendations": ["建议列表"]
}
```

#### 使用示例

```python
# 自动检测主题
result = ios_scan_project('/path/to/ios/project')

# 指定主题
result = ios_scan_project('/path/to/ios/project', 'social')

# 包含测试文件
result = ios_scan_project('/path/to/ios/project', 'auto', True)
```

### 2. ios_optimize_file

对单个iOS代码文件进行多样性优化改造，生成符合主题的辅助代码。

#### 函数签名

```python
ios_optimize_file(
    file_path: str,
    file_content: str,
    theme: str,
    strategy: str = "progressive",
    code_ratio: float = 0.5
) -> str
```

#### 参数说明

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| file_path | str | - | 要优化的文件路径 |
| file_content | str | - | 文件的完整内容 |
| theme | str | - | APP主题类型: social/ecommerce/tool/entertainment/education |
| strategy | str | "progressive" | 改造策略: progressive/extension |
| code_ratio | float | 0.5 | 新增代码占比 (0.3-0.8) |

#### 返回值

返回JSON格式的优化结果：

```json
{
  "success": true,
  "original_path": "原文件路径",
  "optimized_code": "优化后的完整代码",
  "statistics": {
    "original_lines": "原始行数",
    "optimized_lines": "优化后行数",
    "added_lines": "新增行数",
    "code_ratio": "代码占比",
    "code_ratio_percentage": "占比百分比"
  },
  "recommendations": ["建议列表"]
}
```

#### 使用示例

```python
# 读取文件内容
with open('UserManager.swift', 'r') as f:
    content = f.read()

# 渐进式改造
result = ios_optimize_file('UserManager.swift', content, 'social', 'progressive', 0.5)

# 扩展式改造
result = ios_optimize_file('UserManager.swift', content, 'social', 'extension', 0.3)
```

## 主题类型说明

### social (社交类)
- **关键词**: user, friend, message, chat
- **前缀**: Social
- **特色功能**: 社交数据处理、用户关系管理

### ecommerce (电商类)
- **关键词**: product, cart, order, shop
- **前缀**: Commerce
- **特色功能**: 商品管理、订单处理

### tool (工具类)
- **关键词**: tool, utility, process, convert
- **前缀**: Utility
- **特色功能**: 数据处理、格式转换

### entertainment (娱乐类)
- **关键词**: media, play, game, content
- **前缀**: Media
- **特色功能**: 媒体处理、内容管理

### education (教育类)
- **关键词**: learn, course, study, education
- **前缀**: Learning
- **特色功能**: 学习进度、课程管理

## 改造策略说明

### progressive (渐进式)
- 在原代码中插入主题相关的辅助类
- 通过方法调用建立关联
- 适合大多数场景，推荐使用

### extension (扩展式)
- 为原有类添加扩展功能
- 保持原有代码结构不变
- 适合需要最小侵入性的场景

## 错误处理

当操作失败时，返回包含错误信息的JSON：

```json
{
  "error": "错误描述信息"
}
```

## 注意事项

1. **文件路径**: 建议使用绝对路径以避免路径问题
2. **文件编码**: 确保代码文件使用UTF-8编码
3. **代码占比**: 建议设置在0.3-0.8之间，过高可能影响性能
4. **主题选择**: 选择与实际APP功能最匹配的主题以获得最佳效果
5. **备份原文件**: 在应用优化结果前建议备份原始文件 