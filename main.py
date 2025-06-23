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
    扫描iOS项目，返回简单的文件列表
    
    Args:
        project_path: iOS项目根目录路径
        include_tests: 是否包含测试文件
    
    Returns:
        JSON格式的项目扫描结果
    """
    try:
        # 创建记录目录
        record_dir = _create_record_directory(project_path)
        
        # 扫描项目
        scan_result = project_scanner.scan_project(project_path, include_tests)
        
        # 初始化进度跟踪
        progress_data = _initialize_progress_tracking(scan_result)
        
        # 保存进度跟踪文件（统一命名，覆盖旧文件）
        progress_file = os.path.join(record_dir, "transformation_progress.json")
        with open(progress_file, 'w', encoding='utf-8') as f:
            json.dump(progress_data, f, indent=2, ensure_ascii=False)
        
        # 添加记录信息到结果
        scan_result['record_info'] = {
            'record_directory': record_dir,
            'progress_file': progress_file,
            'timestamp': datetime.now().strftime("%Y%m%d_%H%M%S")
        }
        
        return json.dumps(scan_result, indent=2, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)

def _initialize_progress_tracking(scan_result: Dict) -> Dict[str, Any]:
    """初始化简化的改造进度跟踪数据"""
    files = scan_result.get('files', [])
    
    progress_data = {
        "project_info": {
            "total_files": len(files),
            "scan_timestamp": datetime.now().isoformat()
        },
        "transformation_progress": {
            "completed": [],
            "not_started": [file_info.get('path') for file_info in files]
        },
        "update_history": []
    }
    
    return progress_data

@mcp.tool()
def ios_setup_cursor_rules(
    project_path: str,
    cursor_project_root: str,
    app_theme: str = "",
    include_optimization_strategies: bool = True,
    include_code_creation_rules: bool = True
) -> str:
    """
    在指定的Cursor项目根目录中注入cursor rules配置文件
    
    Args:
        project_path: 目标iOS项目路径（用于生成规则内容）
        cursor_project_root: 当前Cursor项目根目录绝对路径
        app_theme: App项目主题
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
        
        # 动态生成iOS代码规范文件（基于目标项目信息和主题）
        ios_rules_content = _generate_ios_rules(project_path, app_theme)
        ios_rules_file = os.path.join(cursor_rules_dir, "iOS_Code_Rules.mdc")
        with open(ios_rules_file, 'w', encoding='utf-8') as f:
            f.write(ios_rules_content)
        injected_files.append("iOS_Code_Rules.mdc")
        
        # 记录注入操作（统一命名，覆盖旧文件）
        injection_record = {
            "last_updated": datetime.now().isoformat(),
            "operation": "cursor_rules_injection",
            "target_project_path": project_path,
            "cursor_project_root": cursor_project_root,
            "cursor_rules_directory": cursor_rules_dir,
            "app_theme": app_theme if app_theme else "未指定",
            "injected_files": injected_files,
            "total_files": len(injected_files),
            "note": f"Cursor规则文件已成功注入到指定的Cursor项目根目录{f'，应用主题：{app_theme}' if app_theme else ''}"
        }
        
        record_file = os.path.join(record_dir, "cursor_rules_injection.json")
        with open(record_file, 'w', encoding='utf-8') as f:
            json.dump(injection_record, f, indent=2, ensure_ascii=False)
        
        result = {
            "success": True,
            "injection_completed": True,
            "target_project_path": project_path,
            "cursor_project_root": cursor_project_root,
            "cursor_rules_directory": cursor_rules_dir,
            "app_theme": app_theme if app_theme else "未指定",
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
                f"代码生成时围绕'{app_theme}'主题进行设计" if app_theme else "代码生成时根据项目特点进行设计",
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
        record_dir = _create_record_directory(project_path)
        progress_file = os.path.join(record_dir, "transformation_progress.json")
        
        # 读取现有进度
        if os.path.exists(progress_file):
            with open(progress_file, 'r', encoding='utf-8') as f:
                progress_data = json.load(f)
        else:
            return json.dumps({"error": "进度文件不存在，请先运行项目扫描"}, ensure_ascii=False)
        
        # 更新进度数据
        timestamp = datetime.now().isoformat()
        
        # 验证文件是否存在于项目中
        valid_files = []
        invalid_files = []
        for file_path in completed_files:
            full_path = os.path.join(project_path, file_path)
            if os.path.exists(full_path):
                valid_files.append(file_path)
            else:
                invalid_files.append(file_path)
        
        # 更新进度统计
        total_files = progress_data.get("project_info", {}).get("total_files", 0)
        completed_count = len(valid_files)
        
        progress_data["transformation_progress"] = {
            "completed": completed_count,
            "not_started": max(0, total_files - completed_count),
            "completion_rate": round(completed_count / total_files * 100, 2) if total_files > 0 else 0
        }
        
        # 添加本次更新记录
        if "update_history" not in progress_data:
            progress_data["update_history"] = []
        
        update_record = {
            "timestamp": timestamp,
            "completed_files": valid_files,
            "notes": notes,
            "invalid_files": invalid_files,
            "session_stats": {
                "files_updated": len(valid_files),
                "total_completed": completed_count,
                "completion_rate": progress_data["transformation_progress"]["completion_rate"]
            }
        }
        
        progress_data["update_history"].append(update_record)
        progress_data["last_update"] = timestamp
        
        # 保存更新后的进度
        with open(progress_file, 'w', encoding='utf-8') as f:
            json.dump(progress_data, f, indent=2, ensure_ascii=False)
        
        # 生成统计报告
        result = {
            "success": True,
            "updated_at": timestamp,
            "progress_summary": {
                "total_files": total_files,
                "completed_files": completed_count,
                "completion_rate": f"{progress_data['transformation_progress']['completion_rate']}%",
                "remaining_files": total_files - completed_count
            },
            "this_session": {
                "files_processed": valid_files,
                "invalid_files": invalid_files,
                "notes": notes
            },
            "next_recommendations": _get_next_recommendations(progress_data, project_path)
        }
        
        return json.dumps(result, indent=2, ensure_ascii=False)
        
    except Exception as e:
        return json.dumps({"error": f"更新进度失败: {str(e)}"}, ensure_ascii=False)

def _get_next_recommendations(progress_data: Dict, project_path: str) -> List[str]:
    """获取下一步推荐操作"""
    recommendations = []
    
    completion_rate = progress_data.get("transformation_progress", {}).get("completion_rate", 0)
    
    if completion_rate < 25:
        recommendations.append("建议优先处理低复杂度文件以快速提升进度")
        recommendations.append("使用 ios_generate_cursor_instructions 获取具体改造指令")
    elif completion_rate < 50:
        recommendations.append("可以开始处理中等复杂度的文件")
        recommendations.append("注意保持代码风格一致性")
    elif completion_rate < 75:
        recommendations.append("开始处理高复杂度文件，建议使用Extension策略")
        recommendations.append("定期验证改造质量")
    else:
        recommendations.append("接近完成，建议进行最终质量检查")
        recommendations.append("验证所有新代码都被有效调用")
    
    return recommendations

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
        completed_data = progress_data["transformation_progress"]["completed"]
        
        # 处理不同的数据格式
        if isinstance(completed_data, list):
            completed_count = len(completed_data)
            completed_files = completed_data
        else:
            completed_count = completed_data if isinstance(completed_data, int) else 0
            # 从历史记录中获取文件列表
            completed_files = []
            if progress_data.get("update_history"):
                latest_update = progress_data["update_history"][-1]
                completed_files = latest_update.get("completed_files", [])
        
        completion_percentage = round((completed_count / total_files) * 100, 2) if total_files > 0 else 0
        
        statistics = {
            "project_overview": progress_data["project_info"],
            "overall_progress": progress_data["transformation_progress"],
            "completion_percentage": completion_percentage,
            "completed_files": completed_files,
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
    分析单个iOS代码文件的基本信息
    
    Args:
        file_path: 文件路径
        file_content: 文件内容
    
    Returns:
        JSON格式的文件分析结果
    """
    try:
        analysis = file_analyzer.analyze_file(file_path, file_content)
        return json.dumps(analysis, indent=2, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)



@mcp.tool()
def ios_generate_cursor_instructions(
    file_path: str,
    strategy: str = "flexible"
) -> str:
    """
    为特定文件生成简单的Cursor改造指令
    
    Args:
        file_path: 要改造的文件路径
        strategy: 改造策略 (flexible/progressive/extension)
    
    Returns:
        JSON格式的Cursor指令
    """
    try:
        # 检查文件是否存在
        if not os.path.exists(file_path):
            return json.dumps({"error": f"文件不存在: {file_path}"}, ensure_ascii=False)
        
        # 读取并分析文件
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        analysis = file_analyzer.analyze_file(file_path, content)
        
        # 生成简单指令
        instructions = {
            "step_1": "分析文件结构，识别可以安全插入新代码的位置",
            "step_2": "设计辅助功能，包含UIKit、Foundation、GCD使用",
            "step_3": "在合适位置插入新代码调用，不破坏原有逻辑",
            "step_4": "验证新代码被100%调用且编译正常"
        }
        
        result = {
            "file_path": file_path,
            "analysis": analysis,
            "strategy": strategy,
            "cursor_instructions": instructions
        }
        
        return json.dumps(result, indent=2, ensure_ascii=False)
        
    except Exception as e:
        return json.dumps({"error": f"生成指令失败: {str(e)}"}, ensure_ascii=False)



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

- `latest_scan_result.json` - 最新项目扫描结果记录
- `transformation_progress.json` - 改造进度跟踪文件
- `cursor_rules_injection.json` - Cursor规则注入记录
- `README.md` - 本说明文件

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

def _generate_ios_rules(project_path: str, app_theme: str = "") -> str:
    """动态生成iOS代码规范文件内容，结合App主题生成相关规则"""
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
    
    # 生成主题提示
    theme_guidance = ""
    if app_theme:
        theme_guidance = f"""
## 主题导向改造指引

**应用主题**: {app_theme}

**代码生成要求**:
- 所有新增代码应围绕"{app_theme}"主题进行设计
- 新增功能、类名、方法名应与{app_theme}主题相关
- 生成的业务逻辑应符合{app_theme}应用的特点
- 确保新代码与{app_theme}主题的整体性和一致性
"""

    content = f"""# iOS 代码改造规范

## 项目基本信息
- 主要语言: {primary_language}
- Swift文件数: {swift_files}
- Objective-C文件数: {objc_files}
- 总代码行数: {total_lines}
- 应用主题: {app_theme if app_theme else "未指定"}
{theme_guidance}
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

@mcp.tool()
def ios_evaluate_project_quality(
    project_path: str
) -> str:
    """
    简单的项目质量评估
    
    Args:
        project_path: 项目根目录路径
    
    Returns:
        JSON格式的质量评估报告
    """
    try:
        record_dir = os.path.join(project_path, '.record')
        progress_file = os.path.join(record_dir, "transformation_progress.json")
        
        if not os.path.exists(progress_file):
            return json.dumps({"error": "进度文件不存在，请先扫描项目"}, ensure_ascii=False)
        
        with open(progress_file, 'r', encoding='utf-8') as f:
            progress_data = json.load(f)
        
        # 简单的质量评估
        total_files = progress_data["project_info"]["total_files"]
        completed_data = progress_data["transformation_progress"].get("completed", [])
        
        # 处理两种数据格式：数组或数字
        if isinstance(completed_data, list):
            completed_files = len(completed_data)
        else:
            completed_files = completed_data if isinstance(completed_data, int) else 0
            
        completion_rate = round((completed_files / total_files) * 100, 2) if total_files > 0 else 0
        
        result = {
            "evaluation_timestamp": datetime.now().isoformat(),
            "project_overview": {
                "total_files": total_files,
                "completed_files": completed_files,
                "completion_rate": f"{completion_rate}%"
            },
            "quality_status": "优秀" if completion_rate >= 80 else "良好" if completion_rate >= 50 else "需要改进",
            "recommendations": [
                "继续完成剩余文件的改造" if completion_rate < 100 else "项目改造已完成",
                "定期检查代码质量",
                "确保新代码被正确调用"
            ]
        }
        
        return json.dumps(result, indent=2, ensure_ascii=False)
        
    except Exception as e:
        return json.dumps({"error": f"质量评估失败: {str(e)}"}, ensure_ascii=False)



def main():
    """主函数"""
    mcp.run()

if __name__ == "__main__":
    main()

