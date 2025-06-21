"""
文件分析器
负责分析单个iOS代码文件的特征
"""

import os
import re
from typing import Dict, Any, Optional


class FileAnalyzer:
    """文件分析器类"""
    
    def analyze_file(self, file_path: str, theme: str) -> Optional[Dict[str, Any]]:
        """分析文件特征"""
        if file_path.endswith('.swift'):
            return self._analyze_swift_file(file_path, theme)
        elif file_path.endswith(('.m', '.h', '.mm')):
            return self._analyze_objc_file(file_path, theme)
        else:
            return None
    
    def _analyze_swift_file(self, file_path: str, theme: str) -> Dict[str, Any]:
        """分析Swift文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            relative_path = os.path.relpath(file_path)
            
            return {
                'path': relative_path,
                'full_path': file_path,
                'type': 'swift',
                'line_count': len(content.split('\n')),
                'class_count': len(re.findall(r'class\s+\w+', content)),
                'method_count': len(re.findall(r'func\s+\w+', content)),
                'complexity': 'medium',
                'theme_relevance': 'medium',
                'transformation_potential': 'high',
                'risk_level': 'low'
            }
        except Exception as e:
            return {'path': file_path, 'error': str(e)}
    
    def _analyze_objc_file(self, file_path: str, theme: str) -> Dict[str, Any]:
        """分析Objective-C文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            relative_path = os.path.relpath(file_path)
            
            return {
                'path': relative_path,
                'full_path': file_path,
                'type': 'objc',
                'line_count': len(content.split('\n')),
                'class_count': len(re.findall(r'@interface\s+\w+', content)),
                'method_count': len(re.findall(r'[-+]\s*\(', content)),
                'complexity': 'medium',
                'theme_relevance': 'medium',
                'transformation_potential': 'high',
                'risk_level': 'low'
            }
        except Exception as e:
            return {'path': file_path, 'error': str(e)}
    
    def analyze_code_structure(self, content: str) -> Dict[str, Any]:
        """分析代码结构"""
        return {
            "classes": re.findall(r'class\s+(\w+)', content),
            "methods": re.findall(r'func\s+(\w+)', content),
            "properties": re.findall(r'(?:var|let)\s+(\w+)', content),
            "imports": re.findall(r'import\s+(\w+)', content),
            "line_count": len(content.split('\n')),
            "has_uikit": 'UIKit' in content,
            "has_foundation": 'Foundation' in content,
            "has_gcd": 'DispatchQueue' in content
        } 