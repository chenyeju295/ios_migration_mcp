"""
项目扫描器模块
负责扫描iOS项目并分析代码文件
"""

import os
import json
from typing import List, Dict, Any
from .file_analyzer import FileAnalyzer
from ..core.config import BasicConfig

class ProjectScanner:
    """iOS项目扫描器"""
    
    def __init__(self):
        self.file_analyzer = FileAnalyzer()
    
    def scan_project(self, project_path: str, include_tests: bool = False) -> Dict[str, Any]:
        """
        扫描iOS项目
        
        Args:
            project_path: 项目根目录路径
            include_tests: 是否包含测试文件
            
        Returns:
            扫描结果字典
        """
        if not os.path.exists(project_path):
            raise ValueError(f"项目路径不存在: {project_path}")
        
        # 查找iOS代码文件
        code_files = self._find_code_files(project_path, include_tests)
        
        if not code_files:
            raise ValueError("未找到iOS代码文件(.swift, .m, .h)")
        
        # 分析文件
        analyzed_files = []
        for file_path in code_files:
            try:
                file_info = self._analyze_file(file_path)
                if file_info:
                    analyzed_files.append(file_info)
            except Exception as e:
                print(f"分析文件失败 {file_path}: {e}")
                continue
        
        # 生成项目统计
        project_stats = self._calculate_project_stats(analyzed_files)
        
        return {
            "project_path": project_path,
            "total_files": len(analyzed_files),
            "files": analyzed_files,
            "project_stats": project_stats,
            "scan_summary": {
                "low_complexity_files": len([f for f in analyzed_files if f.get('complexity') == 'low']),
                "medium_complexity_files": len([f for f in analyzed_files if f.get('complexity') == 'medium']),
                "high_complexity_files": len([f for f in analyzed_files if f.get('complexity') == 'high']),
                "total_lines": sum(f.get('line_count', 0) for f in analyzed_files),
                "recommended_strategy_distribution": self._get_strategy_distribution(analyzed_files)
            }
        }
    
    def _find_code_files(self, project_path: str, include_tests: bool) -> List[str]:
        """查找代码文件"""
        code_files = []
        
        for root, dirs, files in os.walk(project_path):
            # 跳过隐藏目录和常见的非代码目录
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['Pods', 'build', 'DerivedData']]
            
            # 如果不包含测试文件，跳过测试目录
            if not include_tests:
                dirs[:] = [d for d in dirs if 'test' not in d.lower()]
            
            for file in files:
                if any(file.endswith(ext) for ext in BasicConfig.SUPPORTED_EXTENSIONS):
                    if not include_tests and 'test' in file.lower():
                        continue
                    code_files.append(os.path.join(root, file))
        
        return code_files
    
    def _analyze_file(self, file_path: str) -> Dict[str, Any]:
        """分析单个文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            # 尝试其他编码
            try:
                with open(file_path, 'r', encoding='latin-1') as f:
                    content = f.read()
            except:
                return None
        except Exception:
            return None
        
        # 使用文件分析器分析代码结构
        analysis = self.file_analyzer.analyze_code_structure(content)
        
        # 计算复杂度
        line_count = analysis.get('line_count', 0)
        complexity = self._calculate_complexity(line_count)
        
        # 评估改造潜力
        transformation_potential = self._assess_transformation_potential(analysis)
        
        # 评估风险等级
        risk_level = self._assess_risk_level(analysis, complexity)
        
        return {
            "path": os.path.relpath(file_path),
            "full_path": file_path,
            "file_type": self._get_file_type(file_path),
            "line_count": line_count,
            "complexity": complexity,
            "transformation_potential": transformation_potential,
            "risk_level": risk_level,
            "analysis": analysis,
            "recommended_strategy": BasicConfig.get_strategy_for_complexity(complexity),
            "estimated_code_ratio": BasicConfig.get_target_ratio_for_complexity(complexity)
        }
    
    def _calculate_complexity(self, line_count: int) -> str:
        """计算文件复杂度"""
        if line_count <= BasicConfig.COMPLEXITY_THRESHOLDS['low']:
            return 'low'
        elif line_count <= BasicConfig.COMPLEXITY_THRESHOLDS['medium']:
            return 'medium'
        else:
            return 'high'
    
    def _assess_transformation_potential(self, analysis: Dict[str, Any]) -> str:
        """评估改造潜力"""
        score = 0
        
        # 基于代码特征评分
        if analysis.get('has_classes', False):
            score += 2
        if analysis.get('has_methods', False):
            score += 2
        if analysis.get('has_uikit', False):
            score += 1
        if analysis.get('has_gcd', False):
            score += 1
        if analysis.get('method_count', 0) > 3:
            score += 1
        
        if score >= 5:
            return 'high'
        elif score >= 3:
            return 'medium'
        else:
            return 'low'
    
    def _assess_risk_level(self, analysis: Dict[str, Any], complexity: str) -> str:
        """评估改造风险等级"""
        risk_factors = 0
        
        # 复杂度因素
        if complexity == 'high':
            risk_factors += 2
        elif complexity == 'medium':
            risk_factors += 1
        
        # 代码特征因素
        if analysis.get('has_core_data', False):
            risk_factors += 1
        if analysis.get('has_network', False):
            risk_factors += 1
        if analysis.get('method_count', 0) > 10:
            risk_factors += 1
        
        if risk_factors >= 3:
            return 'high'
        elif risk_factors >= 1:
            return 'medium'
        else:
            return 'low'
    
    def _get_file_type(self, file_path: str) -> str:
        """获取文件类型"""
        if file_path.endswith('.swift'):
            return 'swift'
        elif file_path.endswith('.m'):
            return 'objective-c-implementation'
        elif file_path.endswith('.h'):
            return 'objective-c-header'
        else:
            return 'unknown'
    
    def _calculate_project_stats(self, files: List[Dict[str, Any]]) -> Dict[str, Any]:
        """计算项目统计信息"""
        if not files:
            return {}
        
        total_lines = sum(f.get('line_count', 0) for f in files)
        swift_files = len([f for f in files if f.get('file_type') == 'swift'])
        objc_files = len([f for f in files if f.get('file_type') in ['objective-c-implementation', 'objective-c-header']])
        
        return {
            "total_lines": total_lines,
            "average_file_size": total_lines // len(files) if files else 0,
            "swift_files": swift_files,
            "objective_c_files": objc_files,
            "language_distribution": {
                "swift": f"{swift_files / len(files) * 100:.1f}%",
                "objective_c": f"{objc_files / len(files) * 100:.1f}%"
            }
        }
    
    def _get_strategy_distribution(self, files: List[Dict[str, Any]]) -> Dict[str, int]:
        """获取推荐策略分布"""
        distribution = {'progressive': 0, 'extension': 0}
        
        for file_info in files:
            strategy = file_info.get('recommended_strategy', 'progressive')
            distribution[strategy] = distribution.get(strategy, 0) + 1
        
        return distribution 