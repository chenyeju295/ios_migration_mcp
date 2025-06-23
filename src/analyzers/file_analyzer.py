"""
简化的文件分析器
只提供基本的文件信息，用于项目改造跟踪
"""

import os
from typing import Dict, Any


class FileAnalyzer:
    """简化的文件分析器 - 只提供基本文件信息"""
    
    # 敏感关键词检测
    SENSITIVE_KEYWORDS = [
        'payment', 'purchase', 'webview', 'javascript', 'js', 'pay', 'in-app'
    ]
    
    def analyze_file(self, file_path: str, content: str) -> Dict[str, Any]:
        """
        简化的文件分析 - 只返回基本信息
        """
        try:
            lines = content.split('\n')
            line_count = len(lines)
            
            # 检测敏感关键词
            has_sensitive = self._check_sensitive_keywords(content.lower())
            
            # 基本文件信息
            result = {
                'path': os.path.relpath(file_path),
                'line_count': line_count,
                'has_sensitive_content': has_sensitive,
                'file_size': 'small' if line_count < 100 else 'medium' if line_count < 300 else 'large',
                'ready_for_transformation': not has_sensitive
            }
            
            return result
            
        except Exception as e:
            return {
                'path': os.path.relpath(file_path) if file_path else 'unknown',
                'line_count': 0,
                'has_sensitive_content': True,
                'file_size': 'unknown',
                'ready_for_transformation': False,
                'error': str(e)
            }
    
    def _check_sensitive_keywords(self, content: str) -> bool:
        """检查是否包含敏感关键词"""
        return any(keyword in content for keyword in self.SENSITIVE_KEYWORDS)