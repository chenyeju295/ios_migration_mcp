#!/usr/bin/env python3
"""
iOS Migration MCP Server 主启动文件
专注于项目分析、cursorrule注入和改造进度记录
"""

from fastmcp import FastMCP
import json
import os
import shutil
from typing import List, Dict, Any
from datetime import datetime
from pathlib import Path

from src.analyzers.project_scanner import ProjectScanner
from src.analyzers.file_analyzer import FileAnalyzer

# 创建FastMCP服务器实例
mcp = FastMCP("iOS Migration Analyzer")

# 创建功能组件
project_scanner = ProjectScanner()
file_analyzer = FileAnalyzer()

@mcp.tool()
def ios_scan_project(
    project_path: str,
    include_tests: bool = False
) -> str:
    """
    扫描分析iOS项目代码结构，详细记录类和方法信息
    
    Args:
        project_path: iOS项目根目录路径
        include_tests: 是否包含测试文件
    
    Returns:
        JSON格式的项目扫描结果，包含详细的文件、类、方法分析
    """
    try:
        # 创建记录目录
        record_dir = _create_record_directory(project_path)
        
        # 扫描项目
        scan_result = project_scanner.scan_project(project_path, include_tests)
        
        # 详细分析每个文件的类和方法
        detailed_analysis = _analyze_files_in_detail(scan_result.get('files', []))
        scan_result['detailed_analysis'] = detailed_analysis
        
        # 创建简化的进度跟踪
        progress_data = _initialize_simple_progress_tracking(scan_result)
        
        # 保存扫描记录
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        record_file = os.path.join(record_dir, f"scan_result_{timestamp}.json")
        with open(record_file, 'w', encoding='utf-8') as f:
            json.dump(scan_result, f, indent=2, ensure_ascii=False)
        
        # 保存进度跟踪文件
        progress_file = os.path.join(record_dir, "transformation_progress.json")
        with open(progress_file, 'w', encoding='utf-8') as f:
            json.dump(progress_data, f, indent=2, ensure_ascii=False)
        
        # 添加记录信息到结果
        scan_result['record_info'] = {
            'record_directory': record_dir,
            'scan_record_file': record_file,
            'progress_file': progress_file,
            'timestamp': timestamp
        }
        
        return json.dumps(scan_result, indent=2, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)

def _analyze_files_in_detail(files: List[Dict]) -> Dict[str, Any]:
    """详细分析文件中的类和方法信息"""
    detailed_analysis = {
        "total_files": len(files),
        "total_classes": 0,
        "total_methods": 0,
        "total_properties": 0,
        "files_by_complexity": {"low": 0, "medium": 0, "high": 0},
        "framework_usage": {"UIKit": 0, "Foundation": 0, "GCD": 0},
        "files_detail": []
    }
    
    for file_info in files:
        analysis = file_info.get('analysis', {})
        
        # 统计类和方法数量
        classes = analysis.get('classes', [])
        methods = analysis.get('methods', [])
        properties = analysis.get('properties', [])
        
        detailed_analysis["total_classes"] += len(classes)
        detailed_analysis["total_methods"] += len(methods)
        detailed_analysis["total_properties"] += len(properties)
        
        # 统计复杂度分布
        complexity = file_info.get('complexity', 'low')
        detailed_analysis["files_by_complexity"][complexity] += 1
        
        # 统计框架使用
        if analysis.get('has_uikit'):
            detailed_analysis["framework_usage"]["UIKit"] += 1
        if analysis.get('has_foundation'):
            detailed_analysis["framework_usage"]["Foundation"] += 1
        if analysis.get('has_gcd'):
            detailed_analysis["framework_usage"]["GCD"] += 1
        
        # 详细记录文件信息
        file_detail = {
            "file_path": file_info.get('path'),
            "complexity": complexity,
            "classes": classes,
            "methods": methods,
            "properties": properties,
            "line_count": analysis.get('line_count', 0),
            "imports": analysis.get('imports', []),
            "framework_usage": {
                "UIKit": analysis.get('has_uikit', False),
                "Foundation": analysis.get('has_foundation', False),
                "GCD": analysis.get('has_gcd', False)
            }
        }
        detailed_analysis["files_detail"].append(file_detail)
    
    return detailed_analysis

def _initialize_simple_progress_tracking(scan_result: Dict) -> Dict[str, Any]:
    """初始化简化的改造进度跟踪数据"""
    files = scan_result.get('files', [])
    
    progress_data = {
        "project_info": {
            "total_files": len(files),
            "scan_timestamp": datetime.now().isoformat(),
            "project_stats": scan_result.get('project_stats', {})
        },
        "transformation_progress": {
            "not_started": len(files),
            "in_progress": 0,
            "completed": 0
        },
        "files_list": [file_info.get('path') for file_info in files]
    }
    
    return progress_data

@mcp.tool()
def ios_setup_cursor_rules(
    project_path: str,
    cursor_project_root: str,
    include_optimization_strategies: bool = True,
    include_code_creation_rules: bool = True
) -> str:
    """
    在指定的Cursor项目根目录中注入cursor rules配置文件
    
    Args:
        project_path: 目标iOS项目路径（用于生成规则内容）
        cursor_project_root: 当前Cursor项目根目录绝对路径
        include_optimization_strategies: 是否包含优化策略规则
        include_code_creation_rules: 是否包含代码创建规则
    
    Returns:
        JSON格式的注入结果
    """
    try:
        if not os.path.exists(project_path):
            return json.dumps({"error": f"目标项目路径不存在: {project_path}"}, ensure_ascii=False)
        
        if not os.path.exists(cursor_project_root):
            return json.dumps({"error": f"Cursor项目根目录不存在: {cursor_project_root}"}, ensure_ascii=False)
        
        # 创建记录目录（在目标项目中记录操作）
        record_dir = _create_record_directory(project_path)
        
        # 在指定的Cursor项目根目录创建.cursor/rules目录
        cursor_rules_dir = os.path.join(cursor_project_root, ".cursor", "rules")
        os.makedirs(cursor_rules_dir, exist_ok=True)
        
        injected_files = []
        
        # 获取当前脚本所在目录
        current_dir = os.path.dirname(os.path.abspath(__file__))
        cursorrules_dir = os.path.join(current_dir, "cursorrules")
        
        # 注入优化策略规则
        if include_optimization_strategies:
            source_file = os.path.join(cursorrules_dir, "cursor_optimization_strategies.mdc")
            if os.path.exists(source_file):
                dest_file = os.path.join(cursor_rules_dir, "cursor_optimization_strategies.mdc")
                shutil.copy2(source_file, dest_file)
                injected_files.append("cursor_optimization_strategies.mdc")
        
        # 注入代码创建规则
        if include_code_creation_rules:
            source_file = os.path.join(cursorrules_dir, "creater_new_code_file.mdc")
            if os.path.exists(source_file):
                dest_file = os.path.join(cursor_rules_dir, "creater_new_code_file.mdc")
                shutil.copy2(source_file, dest_file)
                injected_files.append("creater_new_code_file.mdc")
        
        # 动态生成iOS代码规范文件（基于目标项目信息）
        ios_rules_content = _generate_ios_rules(project_path)
        ios_rules_file = os.path.join(cursor_rules_dir, "iOS_Code_Rules.mdc")
        with open(ios_rules_file, 'w', encoding='utf-8') as f:
            f.write(ios_rules_content)
        injected_files.append("iOS_Code_Rules.mdc")
        
        # 记录注入操作（在目标项目的记录目录中）
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        injection_record = {
            "timestamp": timestamp,
            "operation": "cursor_rules_injection",
            "target_project_path": project_path,
            "cursor_project_root": cursor_project_root,
            "cursor_rules_directory": cursor_rules_dir,
            "injected_files": injected_files,
            "total_files": len(injected_files),
            "note": "Cursor规则文件已成功注入到指定的Cursor项目根目录"
        }
        
        record_file = os.path.join(record_dir, f"cursor_injection_{timestamp}.json")
        with open(record_file, 'w', encoding='utf-8') as f:
            json.dump(injection_record, f, indent=2, ensure_ascii=False)
        
        result = {
            "success": True,
            "injection_completed": True,
            "target_project_path": project_path,
            "cursor_project_root": cursor_project_root,
            "cursor_rules_directory": cursor_rules_dir,
            "injected_files": injected_files,
            "total_files": len(injected_files),
            "record_file": record_file,
            "cursor_commands": {
                "optimization_strategies": "@cursor_optimization_strategies.mdc",
                "code_creation_rules": "@creater_new_code_file.mdc", 
                "ios_code_rules": "@iOS_Code_Rules.mdc"
            },
            "usage_instructions": [
                "在Cursor中使用 @cursor_optimization_strategies.mdc 获取改造策略",
                "使用 @creater_new_code_file.mdc 指导代码创建",
                "使用 @iOS_Code_Rules.mdc 确保代码规范",
                "完成文件改造后调用 ios_update_progress 更新进度"
            ]
        }
        
        return json.dumps(result, indent=2, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)

@mcp.tool()
def ios_update_progress(
    project_path: str,
    completed_files: List[str],
    notes: str = ""
) -> str:
    """
    更新项目改造进度
    
    Args:
        project_path: 项目根目录路径
        completed_files: 已完成改造的文件列表
        notes: 改造备注
    
    Returns:
        JSON格式的更新结果
    """
    try:
        record_dir = os.path.join(project_path, '.record')
        progress_file = os.path.join(record_dir, "transformation_progress.json")
        
        if not os.path.exists(progress_file):
            return json.dumps({"error": "进度文件不存在，请先扫描项目"}, ensure_ascii=False)
        
        # 读取当前进度
        with open(progress_file, 'r', encoding='utf-8') as f:
            progress_data = json.load(f)
        
        # 更新进度统计
        total_files = progress_data["project_info"]["total_files"]
        completed_count = len(completed_files)
        in_progress_count = 0  # 简化处理，不跟踪进行中状态
        not_started_count = total_files - completed_count
        
        progress_data["transformation_progress"] = {
            "not_started": not_started_count,
            "in_progress": in_progress_count,
            "completed": completed_count
        }
        
        # 添加完成文件列表
        progress_data["completed_files"] = completed_files
        
        # 更新时间戳
        progress_data["last_update"] = datetime.now().isoformat()
        
        # 保存更新后的进度
        with open(progress_file, 'w', encoding='utf-8') as f:
            json.dump(progress_data, f, indent=2, ensure_ascii=False)
        
        # 记录此次更新
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        update_record = {
            "timestamp": timestamp,
            "operation": "progress_update",
            "completed_files": completed_files,
            "completed_count": completed_count,
            "total_files": total_files,
            "completion_percentage": round((completed_count / total_files) * 100, 2) if total_files > 0 else 0,
            "notes": notes
        }
        
        update_record_file = os.path.join(record_dir, f"progress_update_{timestamp}.json")
        with open(update_record_file, 'w', encoding='utf-8') as f:
            json.dump(update_record, f, indent=2, ensure_ascii=False)
        
        result = {
            "success": True,
            "completed_files": completed_files,
            "completed_count": completed_count,
            "total_files": total_files,
            "completion_percentage": round((completed_count / total_files) * 100, 2) if total_files > 0 else 0,
            "remaining_files": not_started_count,
            "timestamp": datetime.now().isoformat(),
            "record_file": update_record_file
        }
        
        return json.dumps(result, indent=2, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)

@mcp.tool()
def ios_get_progress_statistics(
    project_path: str
) -> str:
    """
    获取完整的改造进度统计信息
    
    Args:
        project_path: 项目根目录路径
    
    Returns:
        JSON格式的详细统计信息
    """
    try:
        record_dir = os.path.join(project_path, '.record')
        progress_file = os.path.join(record_dir, "transformation_progress.json")
        
        if not os.path.exists(progress_file):
            return json.dumps({"error": "进度文件不存在，请先扫描项目"}, ensure_ascii=False)
        
        # 读取进度数据
        with open(progress_file, 'r', encoding='utf-8') as f:
            progress_data = json.load(f)
        
        # 计算统计信息
        total_files = progress_data["project_info"]["total_files"]
        completed_count = progress_data["transformation_progress"]["completed"]
        completion_percentage = round((completed_count / total_files) * 100, 2) if total_files > 0 else 0
        
        statistics = {
            "project_overview": progress_data["project_info"],
            "overall_progress": progress_data["transformation_progress"],
            "completion_percentage": completion_percentage,
            "completed_files": progress_data.get("completed_files", []),
            "remaining_files": total_files - completed_count,
            "last_update": progress_data.get("last_update", "未更新")
        }
        
        return json.dumps(statistics, indent=2, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)

@mcp.tool()
def ios_analyze_file(
    file_path: str,
    file_content: str
) -> str:
    """
    分析单个iOS代码文件的特征和详细信息
    
    Args:
        file_path: 文件路径
        file_content: 文件内容
    
    Returns:
        JSON格式的详细文件分析结果
    """
    try:
        analysis = file_analyzer.analyze_file(file_path, file_content)
        
        # 计算复杂度
        complexity = _calculate_complexity(file_content)
        
        # 详细分析类和方法
        detailed_info = _analyze_code_structure(file_content)
        
        result = {
            "file_path": file_path,
            "complexity": complexity,
            "basic_analysis": analysis,
            "detailed_structure": detailed_info,
            "enhancement_suggestions": _generate_enhancement_suggestions(analysis, complexity),
            "analysis_timestamp": datetime.now().isoformat()
        }
        
        return json.dumps(result, indent=2, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)

def _analyze_code_structure(content: str) -> Dict[str, Any]:
    """详细分析代码结构"""
    lines = content.split('\n')
    
    structure = {
        "total_lines": len(lines),
        "non_empty_lines": len([line for line in lines if line.strip()]),
        "comment_lines": len([line for line in lines if line.strip().startswith('//')]),
        "classes_detail": [],
        "methods_detail": [],
        "properties_detail": [],
        "imports_detail": []
    }
    
    # 分析导入语句
    for i, line in enumerate(lines):
        if line.strip().startswith('import '):
            structure["imports_detail"].append({
                "line_number": i + 1,
                "import_statement": line.strip(),
                "framework": line.strip().replace('import ', '')
            })
    
    # 分析类定义
    for i, line in enumerate(lines):
        if 'class ' in line and not line.strip().startswith('//'):
            class_name = line.split('class ')[1].split(':')[0].split('{')[0].strip()
            structure["classes_detail"].append({
                "line_number": i + 1,
                "class_name": class_name,
                "full_declaration": line.strip()
            })
    
    # 分析方法定义
    for i, line in enumerate(lines):
        if 'func ' in line and not line.strip().startswith('//'):
            method_name = line.split('func ')[1].split('(')[0].strip()
            structure["methods_detail"].append({
                "line_number": i + 1,
                "method_name": method_name,
                "full_declaration": line.strip()
            })
    
    # 分析属性定义
    for i, line in enumerate(lines):
        stripped = line.strip()
        if (stripped.startswith('var ') or stripped.startswith('let ')) and not stripped.startswith('//'):
            prop_name = stripped.split(' ')[1].split(':')[0].split('=')[0].strip()
            structure["properties_detail"].append({
                "line_number": i + 1,
                "property_name": prop_name,
                "property_type": "var" if stripped.startswith('var ') else "let",
                "full_declaration": stripped
            })
    
    return structure

def _calculate_complexity(content: str) -> str:
    """计算代码复杂度"""
    lines = len(content.split('\n'))
    classes = content.count('class ')
    functions = content.count('func ')
    
    if lines > 500 or classes > 5 or functions > 20:
        return "high"
    elif lines > 200 or classes > 2 or functions > 10:
        return "medium"
    return "low"

def _generate_enhancement_suggestions(analysis: Dict[str, Any], complexity: str) -> List[str]:
    """生成增强建议"""
    suggestions = []
    
    # 核心原则
    suggestions.append("确保不改变原有代码的功能逻辑")
    suggestions.append("重点在于丰富和增强现有代码")
    
    # 根据复杂度给出建议
    if complexity == "high":
        suggestions.append("建议通过Extension方式扩展功能")
        suggestions.append("分模块逐步丰富，避免一次性大改动")
    else:
        suggestions.append("可以直接在类中添加相关功能方法")
        suggestions.append("适合添加更多的属性和计算方法")
    
    # 技术栈建议
    if not analysis.get('has_uikit', False):
        suggestions.append("可以适当引入UIKit相关功能")
    if not analysis.get('has_gcd', False):
        suggestions.append("可以添加GCD多线程处理功能")
    if not analysis.get('has_foundation', False):
        suggestions.append("可以利用Foundation框架功能")
    
    suggestions.append("使用不同的设计模式保持代码多样性")
    
    return suggestions

@mcp.tool()
def ios_generate_cursor_instructions(
    file_path: str,
    strategy: str = "flexible"
) -> str:
    """
    为特定文件生成Cursor改造指令
    
    Args:
        file_path: 要改造的文件路径
        strategy: 改造策略 (flexible/direct/extension)
    
    Returns:
        JSON格式的Cursor指令
    """
    try:
        instructions = {
            "file_path": file_path,
            "strategy": strategy,
            "cursor_commands": [
                f"分析 {file_path} 的现有代码结构",
                "使用 @iOS_Code_Rules.mdc 了解改造规范",
                "使用 @creater_new_code_file.mdc 指导功能增强"
            ],
            "step_by_step_instructions": [
                f"仔细分析 {file_path} 的现有功能和结构",
                "识别可以丰富和增强的功能点",
                "根据@iOS_Code_Rules.mdc选择合适的改造方式",
                "适当添加相关功能方法或属性",
                "确保新增功能与原有代码和谐集成",
                "验证原有功能完全不受影响",
                "调用 ios_update_progress 更新改造状态"
            ],
            "cursor_usage": [
                "在Cursor中使用 @文件名.mdc 来引用规则文件",
                "利用Cursor的智能分析来理解代码结构",
                "使用Cursor验证改造后的代码质量",
                "让Cursor协助生成符合规范的代码"
            ],
            "progress_tracking": [
                "完成改造后调用 ios_update_progress 更新项目进度",
                "传入已完成的文件列表更新整体统计"
            ]
        }
        
        return json.dumps(instructions, indent=2, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)

def _create_record_directory(project_path: str) -> str:
    """创建记录目录"""
    record_dir = os.path.join(project_path, '.record')
    os.makedirs(record_dir, exist_ok=True)
    
    # 创建README文件说明记录文件夹用途
    readme_file = os.path.join(record_dir, 'README.md')
    if not os.path.exists(readme_file):
        readme_content = """# iOS代码改造记录文件夹

此文件夹用于记录iOS代码改造过程中的各种操作和结果：

## 文件类型说明

- `scan_result_*.json` - 项目扫描结果记录
- `transformation_progress.json` - 改造进度跟踪文件
- `cursor_injection_*.json` - Cursor规则注入记录
- `progress_update_*.json` - 进度更新记录

## MCP工具功能

### 核心功能
1. **cursorrule注入**: 将改造规则注入到当前Cursor工作目录的.cursor/rules目录
2. **文件分析记录**: 详细分析并记录项目中的类、方法、属性信息
3. **进度跟踪**: 跟踪项目整体改造进度
4. **统计报告**: 提供完整的改造统计信息

### 使用流程
1. `ios_scan_project` - 扫描项目并初始化进度跟踪
2. `ios_setup_cursor_rules` - 注入cursor规则文件
3. `ios_generate_cursor_instructions` - 获取具体改造指令
4. `ios_update_progress` - 更新项目改造进度
5. `ios_get_progress_statistics` - 获取完整统计信息

## 改造原则

1. **功能逻辑不变**: 严格保持原有代码的功能逻辑
2. **丰富现有代码**: 重点在于增强和丰富现有功能
3. **灵活调整**: 根据实际情况灵活选择改造方式
4. **统一规则**: 整个项目使用统一的改造规则

注意：请不要手动删除或修改这些记录文件
"""
        with open(readme_file, 'w', encoding='utf-8') as f:
            f.write(readme_content)
    
    return record_dir

def _generate_ios_rules(project_path: str) -> str:
    """动态生成iOS代码规范文件内容"""
    try:
        # 尝试扫描项目获取信息
        scan_result = project_scanner.scan_project(project_path, False)
        project_stats = scan_result.get('project_stats', {})
        
        swift_files = project_stats.get('swift_files', 0)
        objc_files = project_stats.get('objective_c_files', 0)
        total_lines = project_stats.get('total_lines', 0)
        
        # 确定主要语言
        primary_language = "Swift" if swift_files >= objc_files else "Objective-C"
        
    except:
        primary_language = "Swift"
        swift_files = 0
        objc_files = 0
        total_lines = 0
    
    content = f"""# iOS 代码改造规范

## 项目基本信息
- 主要语言: {primary_language}
- Swift文件数: {swift_files}
- Objective-C文件数: {objc_files}
- 总代码行数: {total_lines}

## 核心改造原则

### 1. 功能逻辑不变原则
- **严格保持**: 原有代码的所有功能逻辑必须完全保持不变
- **不破坏**: 不改变任何现有的业务流程和数据处理
- **兼容性**: 确保改造后的代码与原有系统完全兼容

### 2. 代码丰富化目标
- **增强功能**: 在不改变逻辑的前提下丰富现有功能
- **灵活改造**: 根据文件特点选择合适的改造方式
- **适度添加**: 根据实际需要添加相关功能，不强制要求固定比例

### 3. 改造方式指导
#### 低复杂度文件
- 可以直接在类中添加相关方法和属性
- 适合添加辅助功能和计算属性
- 可以增加一些工具方法

#### 中高复杂度文件
- 建议使用Extension方式扩展功能
- 分模块添加相关功能
- 避免一次性大幅修改

### 4. 技术栈建议
#### 可以适当引入的框架
- UIKit: 当需要UI相关功能时
- Foundation: 用于系统基础功能
- Grand Central Dispatch (GCD): 当需要多线程处理时
- Core Graphics: 当需要绘制功能时
- URLSession: 当需要网络请求时

### 5. 代码多样性要求
- 避免模板化的重复代码
- 使用不同的实现方式和设计模式
- 保持命名的多样性和独特性

### 6. 安全合规要求
- 禁止添加支付、WebView、JavaScript相关功能
- 不收集任何敏感数据
- 遵循Apple审核指南
- 避免使用可能引起审核问题的API

### 7. 质量保证
- 所有新增代码必须有实际功能，不允许空实现
- 新增的方法和属性应该被合理调用
- 保持代码的可读性和可维护性
- 确保编译通过和功能正常

## MCP工具集成

### 进度跟踪命令
在Cursor中完成改造后，调用以下MCP命令更新进度：

```
// 更新项目进度
ios_update_progress(project_path, completed_files_list, "改造完成备注")
```

### 统计查看命令
```
// 查看整体进度
ios_get_progress_statistics(project_path)
```

## Cursor使用指南

### 引用规则文件
- `@cursor_optimization_strategies.mdc` - 获取优化策略
- `@creater_new_code_file.mdc` - 创建新代码指导
- `@iOS_Code_Rules.mdc` - 引用本规范文件

### 工作流程
1. 仔细分析现有代码结构和功能
2. 根据代码特点制定改造方案
3. 选择合适的改造方式（直接添加/Extension）
4. 确保新代码与原有代码和谐集成
5. 验证功能完整性和代码质量
6. 调用MCP工具更新改造进度
7. 测试确保原有功能不受影响

## 重要提醒

- 改造的目标是丰富和增强代码，而不是达到特定的数量指标
- 任何改造都不能影响原有的功能逻辑
- 完成改造后务必调用MCP工具更新进度记录
"""
    
    return content

def main():
    """主函数"""
    mcp.run()

if __name__ == "__main__":
    main() 