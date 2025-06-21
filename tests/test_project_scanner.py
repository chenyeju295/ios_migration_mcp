"""
项目扫描器测试
"""

import unittest
import tempfile
import os
import sys

# 添加项目路径到系统路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.analyzers.project_scanner import ProjectScanner


class TestProjectScanner(unittest.TestCase):
    """项目扫描器测试类"""
    
    def setUp(self):
        """测试前准备"""
        self.scanner = ProjectScanner()
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """测试后清理"""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_scan_empty_project(self):
        """测试扫描空项目"""
        result = self.scanner.scan_project(self.temp_dir)
        
        self.assertEqual(result['project_path'], self.temp_dir)
        self.assertEqual(result['summary']['total_files'], 0)
        self.assertIn('theme', result)
    
    def test_scan_swift_files(self):
        """测试扫描Swift文件"""
        # 创建测试Swift文件
        swift_file = os.path.join(self.temp_dir, 'TestClass.swift')
        with open(swift_file, 'w', encoding='utf-8') as f:
            f.write("""
import UIKit

class TestClass {
    func testMethod() {
        print("Hello World")
    }
}
""")
        
        result = self.scanner.scan_project(self.temp_dir)
        
        self.assertEqual(result['summary']['total_files'], 1)
        self.assertEqual(result['summary']['swift_files'], 1)
        self.assertEqual(result['summary']['objc_files'], 0)


if __name__ == '__main__':
    unittest.main() 