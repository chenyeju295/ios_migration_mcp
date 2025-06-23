"""
简化的项目扫描器
只扫描文件并提供基本统计信息
"""

import os
import json
from datetime import datetime
from typing import List, Dict, Any
from .file_analyzer import FileAnalyzer


class ProjectScanner:
    """简化的项目扫描器"""
    
    # 支持的文件扩展名
    SUPPORTED_EXTENSIONS = ['.swift', '.m', '.h', '.mm', '.cpp', '.cc', '.c']
    
    def __init__(self):
        self.file_analyzer = FileAnalyzer()
        
    def scan_project(self, project_path: str, include_tests: bool = False) -> Dict[str, Any]:
        """
        扫描项目，返回简化的结果
        """
        try:
            print(f"🔍 开始扫描项目: {project_path}")
            
            # 查找代码文件
            code_files = self._find_code_files(project_path, include_tests)
            
            if not code_files:
                return {
                    "project_path": project_path,
                    "total_files": 0,
                    "files": [],
                    "error": "未找到任何代码文件"
                }
            
            # 分析文件
            analyzed_files = []
            total_lines = 0
            
            for file_path in code_files:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    analysis = self.file_analyzer.analyze_file(file_path, content)
                    analyzed_files.append(analysis)
                    total_lines += analysis.get('line_count', 0)
                    
                except Exception as e:
                    print(f"⚠️  分析文件失败: {file_path} - {e}")
                    analyzed_files.append({
                        'path': os.path.relpath(file_path),
                        'line_count': 0,
                        'has_sensitive_content': True,
                        'file_size': 'unknown',
                        'ready_for_transformation': False,
                        'error': str(e)
                    })
            
            # 创建扫描结果
            result = {
                "project_path": project_path,
                "total_files": len(analyzed_files),
                "total_lines": total_lines,
                "files": analyzed_files,
                "scan_timestamp": datetime.now().isoformat()
            }
            
            # 保存扫描记录
            self._save_scan_record(project_path, result)
            
            print(f"✅ 扫描完成，找到 {len(analyzed_files)} 个文件")
            return result
            
        except Exception as e:
            print(f"❌ 扫描项目失败: {e}")
            return {
                "project_path": project_path,
                "total_files": 0,
                "files": [],
                "error": str(e)
            }
    
    def _find_code_files(self, project_path: str, include_tests: bool) -> List[str]:
        """查找代码文件"""
        code_files = []
        
        print(f"📂 扫描目录: {project_path}")
        
        for root, dirs, files in os.walk(project_path):
            # 跳过隐藏目录和非代码目录
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['Pods', 'build', 'DerivedData', 'Carthage']]
            
            # 如果不包含测试文件，跳过测试目录
            if not include_tests:
                dirs[:] = [d for d in dirs if not any(test_pattern in d.lower() for test_pattern in ['tests', 'testing', 'unittest', 'uitest'])]
            
            for file in files:
                if any(file.endswith(ext) for ext in self.SUPPORTED_EXTENSIONS):
                    # 检查是否为测试文件
                    if not include_tests and self._is_test_file(file):
                        continue
                    
                    file_path = os.path.join(root, file)
                    code_files.append(file_path)
                    print(f"✅ 找到文件: {os.path.relpath(file_path, project_path)}")
        
        return code_files
    
    def _is_test_file(self, filename: str) -> bool:
        """判断是否为测试文件"""
        test_patterns = ['test', 'spec', 'tests']
        filename_lower = filename.lower()
        return any(pattern in filename_lower for pattern in test_patterns)
    
    def _save_scan_record(self, project_path: str, scan_result: Dict[str, Any]):
        """保存扫描记录（统一命名，覆盖旧文件）"""
        try:
            record_dir = os.path.join(project_path, '.record')
            os.makedirs(record_dir, exist_ok=True)
            
            record_file = os.path.join(record_dir, "latest_scan_result.json")
            
            with open(record_file, 'w', encoding='utf-8') as f:
                json.dump(scan_result, f, indent=2, ensure_ascii=False)
            
            print(f"📄 扫描记录已保存: {record_file}")
            
        except Exception as e:
            print(f"⚠️  保存扫描记录失败: {e}") 