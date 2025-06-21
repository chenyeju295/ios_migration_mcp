#!/usr/bin/env python3
"""
iOS Migration MCP Server 主启动文件
专注于项目分析、改造规划和指导建议
"""

from fastmcp import FastMCP
import json
import os
import shutil
from typing import List, Dict, Any

from src.analyzers.project_scanner import ProjectScanner

# 创建FastMCP服务器实例
mcp = FastMCP("iOS Migration Analyzer")

# 创建功能组件
project_scanner = ProjectScanner()

@mcp.tool()
def ios_scan_project(
    project_path: str,
    include_tests: bool = False
) -> str:
    """
    扫描分析iOS项目代码结构
    
    Args:
        project_path: iOS项目根目录路径
        include_tests: 是否包含测试文件
    
    Returns:
        JSON格式的扫描结果，包含文件分析和改造建议
    """
    try:
        result = project_scanner.scan_project(project_path, include_tests)
        return json.dumps(result, indent=2, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)

@mcp.tool()
def ios_analyze_file(
    file_path: str,
    file_content: str
) -> str:
    """
    分析单个iOS代码文件的特征和改造潜力
    
    Args:
        file_path: 文件路径
        file_content: 文件内容
    
    Returns:
        JSON格式的文件分析结果和改造建议
    """
    try:
        from src.analyzers.file_analyzer import FileAnalyzer
        from src.core.config import BasicConfig
        
        analyzer = FileAnalyzer()
        analysis = analyzer.analyze_code_structure(file_content)
        
        # 计算改造建议
        suggestions = []
        
        # 基于代码结构生成建议
        if analysis.get('has_uikit'):
            suggestions.append("已使用UIKit，可以添加更多UI相关功能")
        else:
            suggestions.append("建议添加UIKit相关代码以增强技术栈多样性")
            
        if analysis.get('has_gcd'):
            suggestions.append("已使用GCD，可以扩展并发处理功能")
        else:
            suggestions.append("建议添加DispatchQueue相关代码")
            
        if analysis.get('has_foundation'):
            suggestions.append("已使用Foundation，可以添加更多系统API调用")
        else:
            suggestions.append("建议添加Foundation系统函数调用")
        
        # 估算改造复杂度
        line_count = analysis.get('line_count', 0)
        complexity = "low"
        if line_count > BasicConfig.COMPLEXITY_THRESHOLDS['low']:
            complexity = "medium"
        if line_count > BasicConfig.COMPLEXITY_THRESHOLDS['medium']:
            complexity = "high"
        
        result = {
            "file_path": file_path,
            "analysis": analysis,
            "complexity": complexity,
            "transformation_suggestions": suggestions,
            "recommended_strategy": BasicConfig.get_strategy_for_complexity(complexity),
            "estimated_code_ratio": BasicConfig.get_target_ratio_for_complexity(complexity),
            "risk_assessment": {
                "level": "low" if complexity == "low" else "medium",
                "factors": _assess_risk_factors(analysis, complexity)
            }
        }
        
        return json.dumps(result, indent=2, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)

def _assess_risk_factors(analysis: Dict[str, Any], complexity: str) -> List[str]:
    """评估风险因素"""
    factors = []
    
    if complexity == "high":
        factors.append("文件复杂度较高")
    if analysis.get('method_count', 0) > 10:
        factors.append("方法数量较多")
    if analysis.get('has_core_data'):
        factors.append("涉及Core Data操作")
    if analysis.get('has_network'):
        factors.append("涉及网络操作")
    
    if not factors:
        factors.append("风险较低，适合改造")
    
    return factors

@mcp.tool()
def ios_generate_plan(
    scan_results: str,
    priority: str = "safety"
) -> str:
    """
    基于扫描结果生成详细的改造计划
    
    Args:
        scan_results: 项目扫描结果的JSON字符串
        priority: 优化策略 (safety/speed/coverage)
    
    Returns:
        JSON格式的详细改造计划
    """
    try:
        scan_data = json.loads(scan_results)
        files = scan_data.get('files', [])
        
        # 按优先级排序文件
        if priority == "safety":
            sorted_files = sorted(files, key=lambda f: (
                f.get('risk_level', 'low') == 'low',
                f.get('transformation_potential', 'low') == 'high'
            ))
        elif priority == "speed":
            sorted_files = sorted(files, key=lambda f: f.get('line_count', 0))
        else:  # coverage
            sorted_files = files
        
        # 分5个阶段
        phases = {"phase_1": [], "phase_2": [], "phase_3": [], "phase_4": [], "phase_5": []}
        
        for i, file_info in enumerate(sorted_files):
            phase_key = f"phase_{(i % 5) + 1}"
            
            # 生成具体的改造指导
            instructions = []
            instructions.append(f"1. 分析{file_info.get('path')}的现有结构")
            instructions.append(f"2. 设计相关的辅助类和扩展功能")
            instructions.append(f"3. 在关键方法中插入辅助类调用")
            instructions.append(f"4. 验证代码编译和功能正常")
            
            phases[phase_key].append({
                "file_path": file_info.get('path'),
                "strategy": file_info.get('recommended_strategy', 'progressive'),
                "estimated_time": max(file_info.get('line_count', 0) // 10, 5),
                "risk_level": file_info.get('risk_level', 'low'),
                "instructions": instructions,
                "target_code_ratio": file_info.get('estimated_code_ratio', 0.4)
            })
        
        plan = {
            "project_path": scan_data.get('project_path'),
            "total_files": len(files),
            "priority": priority,
            "phases": phases,
            "estimated_total_time": sum(max(f.get('line_count', 0) // 10, 5) for f in files),
            "global_guidelines": [
                "确保新代码100%被原有代码调用",
                "每个类的70%以上函数都要调用新代码",
                "禁止包含敏感功能：支付、WebView、JavaScript等",
                "必须集成UIKit、Foundation、GCD技术栈",
                "保持代码风格和命名规范一致"
            ]
        }
        
        return json.dumps(plan, indent=2, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)

@mcp.tool()
def ios_validate_requirements(
    file_content: str
) -> str:
    """
    验证代码是否符合iOS迁移要求
    
    Args:
        file_content: 要验证的代码内容
    
    Returns:
        JSON格式的验证结果和改进建议
    """
    try:
        from src.core.config import BasicConfig
        
        violations = []
        warnings = []
        passed_checks = []
        
        # 检查敏感功能
        for keyword in BasicConfig.SENSITIVE_KEYWORDS:
            if keyword.lower() in file_content.lower():
                violations.append(f"包含敏感功能: {keyword}")
        
        if not violations:
            passed_checks.append("✅ 无敏感功能")
        
        # 检查必需框架
        missing_frameworks = []
        for framework in BasicConfig.REQUIRED_FRAMEWORKS:
            if framework not in file_content:
                missing_frameworks.append(framework)
                warnings.append(f"缺少框架: {framework}")
            else:
                passed_checks.append(f"✅ 包含{framework}框架")
        
        # 检查推荐技术栈
        missing_tech = []
        for tech in BasicConfig.RECOMMENDED_TECH:
            if tech not in file_content:
                missing_tech.append(tech)
            else:
                passed_checks.append(f"✅ 使用了{tech}")
        
        if missing_tech:
            warnings.append(f"建议添加技术栈: {', '.join(missing_tech)}")
        
        # 检查代码结构
        has_classes = 'class ' in file_content
        has_methods = 'func ' in file_content
        
        if has_classes:
            passed_checks.append("✅ 包含类定义")
        if has_methods:
            passed_checks.append("✅ 包含方法定义")
        
        validation_result = {
            "is_compliant": len(violations) == 0,
            "violations": violations,
            "warnings": warnings,
            "passed_checks": passed_checks,
            "recommendations": []
        }
        
        # 生成改进建议
        if violations:
            validation_result["recommendations"].append("🚫 必须移除所有敏感功能")
        if missing_frameworks:
            validation_result["recommendations"].append(f"📦 添加缺失框架: {', '.join(missing_frameworks)}")
        if missing_tech:
            validation_result["recommendations"].append(f"⚡ 添加推荐技术栈: {', '.join(missing_tech)}")
        if len(violations) == 0 and len(warnings) == 0:
            validation_result["recommendations"].append("🎉 代码完全符合iOS迁移要求")
        
        return json.dumps(validation_result, indent=2, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)

@mcp.tool()
def ios_setup_cursor_rules(
    project_path: str,
    include_optimization_strategies: bool = True,
    include_code_creation_rules: bool = True
) -> str:
    """
    在项目目录中创建.cursor/rules文件夹并插入相关的cursor rules
    
    Args:
        project_path: 项目根目录路径
        include_optimization_strategies: 是否包含优化策略规则
        include_code_creation_rules: 是否包含代码创建规则
    
    Returns:
        JSON格式的操作结果
    """
    try:
        if not os.path.exists(project_path):
            return json.dumps({"error": f"项目路径不存在: {project_path}"}, ensure_ascii=False)
        
        # 创建.cursor/rules目录
        cursor_rules_dir = os.path.join(project_path, ".cursor", "rules")
        os.makedirs(cursor_rules_dir, exist_ok=True)
        
        copied_files = []
        
        # 获取当前脚本所在目录
        current_dir = os.path.dirname(os.path.abspath(__file__))
        cursorrules_dir = os.path.join(current_dir, "cursorrules")
        
        # 复制优化策略规则
        if include_optimization_strategies:
            source_file = os.path.join(cursorrules_dir, "cursor_optimization_strategies.mdc")
            if os.path.exists(source_file):
                dest_file = os.path.join(cursor_rules_dir, "cursor_optimization_strategies.mdc")
                shutil.copy2(source_file, dest_file)
                copied_files.append("cursor_optimization_strategies.mdc")
        
        # 复制代码创建规则
        if include_code_creation_rules:
            source_file = os.path.join(cursorrules_dir, "creater_new_code_file.mdc")
            if os.path.exists(source_file):
                dest_file = os.path.join(cursor_rules_dir, "creater_new_code_file.mdc")
                shutil.copy2(source_file, dest_file)
                copied_files.append("creater_new_code_file.mdc")
        
        # 创建iOS代码规范文件（基于项目扫描结果）
        ios_rules_content = _generate_ios_code_rules(project_path)
        ios_rules_file = os.path.join(cursor_rules_dir, "iOS_Code_Rules.mdc")
        with open(ios_rules_file, 'w', encoding='utf-8') as f:
            f.write(ios_rules_content)
        copied_files.append("iOS_Code_Rules.mdc")
        
        result = {
            "success": True,
            "cursor_rules_directory": cursor_rules_dir,
            "copied_files": copied_files,
            "total_files": len(copied_files),
            "instructions": [
                "1. 重启Cursor编辑器以加载新的规则",
                "2. 在Cursor中可以通过@cursor_optimization_strategies.mdc引用优化策略",
                "3. 在Cursor中可以通过@creater_new_code_file.mdc引用代码创建规则",
                "4. 在Cursor中可以通过@iOS_Code_Rules.mdc引用iOS代码规范",
                "5. 开始使用这些规则进行iOS代码改造"
            ]
        }
        
        return json.dumps(result, indent=2, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)

def _generate_ios_code_rules(project_path: str) -> str:
    """生成iOS代码规范文件内容"""
    try:
        # 尝试扫描项目获取信息
        scan_result = project_scanner.scan_project(project_path, False)
        project_stats = scan_result.get('project_stats', {})
        
        swift_files = project_stats.get('swift_files', 0)
        objc_files = project_stats.get('objective_c_files', 0)
        
        # 确定主要语言
        primary_language = "Swift" if swift_files >= objc_files else "Objective-C"
        
    except:
        primary_language = "Swift"
        swift_files = 0
        objc_files = 0
    
    content = f"""# iOS 代码迁移规范

## 项目基本信息
- 主要语言: {primary_language}
- Swift文件数: {swift_files}
- Objective-C文件数: {objc_files}

## 代码迁移核心规则

### 1. 代码生成要求
- **代码占比**: 新增代码占原代码的33%-50%
- **调用覆盖**: 100%的新代码必须被原有代码调用
- **函数覆盖**: 每个类的70%以上函数都要调用新代码
- **文件覆盖**: 100%的文件都要被修改

### 2. 技术栈要求
#### 必须包含的框架
- UIKit: 用于UI相关功能
- Foundation: 用于基础系统功能
- Grand Central Dispatch (GCD): 用于多线程处理

#### 推荐使用的技术
- NotificationCenter: 通知机制
- UserDefaults: 数据持久化
- Core Graphics: 图形处理

### 3. 代码结构要求
#### 每个新增类/扩展必须包含
- 私有属性 (private/protected)
- 变量和常量 (var/let)
- 类方法 (static/class func)
- 实例方法 (func)
- 闭包/回调机制
- 自定义getter/setter

#### 代码实现要求
- 禁止空实现，所有成员必须有实际功能
- 所有属性和方法必须在内部有实际调用
- 每个类至少包含一次GCD相关代码
- 每个类至少包含一次UIKit相关代码
- 每个类至少包含一次系统函数调用

### 4. 安全规范
#### 禁止的敏感功能
- 支付相关功能 (payment, purchase, billing)
- WebView/JavaScript功能
- 内购功能 (in-app)
- 匹配、约会、1v1等敏感功能

#### 禁止的关键词
- Review, WebView, js, Pay, In-app, purchase
- evaluateJavaScript
- 任何支付相关API

### 5. 代码风格规范
#### 命名规范
- 类名使用大驼峰命名法 (PascalCase)
- 方法和属性使用小驼峰命名法 (camelCase)
- 常量使用全大写加下划线
- 私有成员添加适当前缀

#### 注释规范
- 所有公开方法必须有注释
- 复杂逻辑必须有行内注释
- 类和扩展必须有文档注释

### 6. 改造策略
#### 渐进式改造 (推荐)
- 适用于低复杂度文件 (<100行)
- 在原代码中分散插入新功能调用
- 代码占比: 40-50%

#### 扩展式改造
- 适用于中高复杂度文件 (>100行)
- 通过Extension添加新功能
- 代码占比: 30-40%

### 7. 质量检查清单
- [ ] 新代码完全被原有代码调用
- [ ] 包含所有必需的技术栈
- [ ] 无敏感功能实现
- [ ] 代码可正常编译运行
- [ ] 符合项目代码风格
- [ ] 通过所有单元测试

### 8. 实施指导
1. **改造前**: 备份原始代码，确保项目可正常运行
2. **改造中**: 分阶段实施，每完成一个文件就测试
3. **改造后**: 全面测试，验证功能完整性

## 使用说明
在Cursor中使用 `@iOS_Code_Rules.mdc` 引用此规范文件，确保所有代码改造都符合上述要求。
"""
    
    return content

@mcp.tool()
def ios_get_strategies() -> str:
    """
    获取所有支持的改造策略和使用指南
    
    Returns:
        JSON格式的策略列表和详细说明
    """
    try:
        from src.core.config import BasicConfig
        
        strategies_info = {}
        for strategy_key, strategy_config in BasicConfig.STRATEGIES.items():
            strategies_info[strategy_key] = {
                **strategy_config,
                "实施步骤": [
                    "1. 分析现有代码结构和功能",
                    "2. 设计相关的辅助类和方法",
                    "3. 在原有代码中插入调用",
                    "4. 验证功能完整性和编译正确性"
                ]
            }
        
        return json.dumps({
            "available_strategies": list(strategies_info.keys()),
            "strategy_details": strategies_info,
            "selection_guide": {
                "low_complexity": "推荐使用progressive策略",
                "medium_complexity": "推荐使用extension策略",
                "high_complexity": "推荐使用extension策略，谨慎处理"
            },
            "general_principles": [
                "优先选择风险较低的改造方式",
                "确保改造后代码可维护性",
                "保持原有功能逻辑不变",
                "分阶段实施，逐步验证"
            ]
        }, indent=2, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)

@mcp.tool()
def ios_get_requirements() -> str:
    """
    获取iOS代码迁移的基本要求和规范
    
    Returns:
        JSON格式的要求列表和规范说明
    """
    try:
        from src.core.config import BasicConfig
        
        return json.dumps({
            "required_frameworks": BasicConfig.REQUIRED_FRAMEWORKS,
            "recommended_technologies": BasicConfig.RECOMMENDED_TECH,
            "prohibited_keywords": BasicConfig.SENSITIVE_KEYWORDS,
            "complexity_thresholds": BasicConfig.COMPLEXITY_THRESHOLDS,
            "code_quality_standards": [
                "代码必须可编译通过",
                "新增代码必须被原有代码调用",
                "保持代码风格一致性",
                "避免破坏现有功能逻辑",
                "确保内存管理正确"
            ],
            "best_practices": [
                "改造前备份原始代码",
                "分阶段实施改造计划",
                "每个阶段完成后进行测试",
                "记录改造过程和遇到的问题",
                "保持代码可读性和可维护性"
            ]
        }, indent=2, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)

@mcp.tool()
def ios_generate_cursor_instructions(
    file_path: str,
    strategy: str = "progressive"
) -> str:
    """
    为特定文件生成Cursor改造指令
    
    Args:
        file_path: 要改造的文件路径
        strategy: 改造策略 (progressive/extension)
    
    Returns:
        JSON格式的Cursor指令
    """
    try:
        instructions = []
        
        if strategy == "progressive":
            instructions = [
                f"请对文件 {file_path} 进行渐进式改造:",
                "",
                "1. **分析阶段**",
                "   - 分析当前类的业务功能和代码结构",
                "   - 识别可以插入新代码的位置",
                "   - 评估改造复杂度和风险",
                "",
                "2. **设计阶段**",
                "   - 设计3-5个相关的辅助类",
                "   - 每个辅助类包含: 私有属性、GCD队列、UIKit组件、系统API调用",
                "   - 确保辅助类功能与原业务相关",
                "",
                "3. **实施阶段**",
                "   - 在原类的每个方法中适当位置插入对辅助类的调用",
                "   - 确保插入位置自然，不影响原有逻辑",
                "   - 生成代码占比控制在40-45%",
                "   - 确保70%以上的方法都调用新代码",
                "",
                "4. **验证阶段**",
                "   - 检查代码是否可以正常编译",
                "   - 验证新代码是否100%被调用",
                "   - 确认无敏感功能实现",
                "",
                "请严格按照 @iOS_Code_Rules.mdc 中的规范执行改造。"
            ]
        else:  # extension
            instructions = [
                f"请对文件 {file_path} 进行扩展式改造:",
                "",
                "1. **分析阶段**",
                "   - 分析当前类的复杂度和核心功能",
                "   - 确定适合添加扩展的功能模块",
                "",
                "2. **设计阶段**",
                "   - 为当前类创建2-3个Extension",
                "   - 每个Extension包含不同的功能模块",
                "   - 使用不同的设计模式实现每个模块",
                "",
                "3. **实施阶段**",
                "   - 在原有方法的关键位置调用Extension方法",
                "   - 确保Extension功能不改变原有业务流程",
                "   - 生成代码占比控制在30-35%",
                "",
                "4. **验证阶段**",
                "   - 确保所有Extension方法都被调用",
                "   - 验证代码编译和功能正确性",
                "",
                "请严格按照 @iOS_Code_Rules.mdc 中的规范执行改造。"
            ]
        
        result = {
            "file_path": file_path,
            "strategy": strategy,
            "cursor_instructions": "\n".join(instructions),
            "required_rules": [
                "@iOS_Code_Rules.mdc",
                "@cursor_optimization_strategies.mdc",
                "@creater_new_code_file.mdc"
            ],
            "success_criteria": [
                "新代码占比达到目标范围",
                "100%新代码被原有代码调用",
                "70%以上方法调用新代码",
                "代码可正常编译运行",
                "无敏感功能实现"
            ]
        }
        
        return json.dumps(result, indent=2, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)

def main():
    """主函数"""
    mcp.run()

if __name__ == "__main__":
    main() 