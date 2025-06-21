#!/usr/bin/env python3
"""
iOS Migration MCP Server 测试客户端
"""

import sys
import os

# 添加项目路径到系统路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.analyzers.project_scanner import ProjectScanner
from src.generators.file_optimizer import FileOptimizer
from src.core.config import ThemeConfig


def test_project_scanner():
    """测试项目扫描器"""
    print("🔍 测试项目扫描器...")
    
    scanner = ProjectScanner()
    
    # 测试当前目录
    try:
        result = scanner.scan_project(".")
        print(f"✅ 扫描成功，检测到主题: {result['theme']}")
        print(f"📊 文件统计: {result['summary']}")
        return True
    except Exception as e:
        print(f"❌ 扫描失败: {e}")
        return False


def test_file_optimizer():
    """测试文件优化器"""
    print("\n🔧 测试文件优化器...")
    
    optimizer = FileOptimizer()
    
    # 测试Swift代码
    test_code = """
import UIKit

class UserManager {
    var users: [String] = []
    
    func addUser(_ name: String) {
        users.append(name)
        print("User added: \\(name)")
    }
    
    func getUsers() -> [String] {
        return users
    }
}
"""
    
    try:
        result = optimizer.optimize_file("UserManager.swift", test_code, "social", "progressive", 0.5)
        
        if result["success"]:
            print("✅ 优化成功")
            print(f"📊 统计信息: {result['statistics']}")
            print(f"📝 建议: {result['recommendations']}")
            
            # 显示部分优化后的代码
            optimized_lines = result["optimized_code"].split('\n')
            print("\n📄 优化后代码预览（前20行）:")
            for i, line in enumerate(optimized_lines[:20]):
                print(f"{i+1:2d}: {line}")
            
            if len(optimized_lines) > 20:
                print(f"... 还有 {len(optimized_lines) - 20} 行")
            
            return True
        else:
            print(f"❌ 优化失败: {result.get('error', '未知错误')}")
            return False
            
    except Exception as e:
        print(f"❌ 优化失败: {e}")
        return False


def test_theme_config():
    """测试主题配置"""
    print("\n⚙️ 测试主题配置...")
    
    try:
        themes = ThemeConfig.get_all_themes()
        print(f"✅ 支持的主题: {themes}")
        
        for theme in themes:
            config = ThemeConfig.get_theme_config(theme)
            keywords = ThemeConfig.get_theme_keywords(theme)
            print(f"  - {theme}: {config['prefix']} (关键词: {keywords})")
        
        return True
    except Exception as e:
        print(f"❌ 主题配置测试失败: {e}")
        return False


def show_usage_examples():
    """显示使用示例"""
    print("\n📚 使用示例:")
    print("=" * 60)
    
    examples = [
        {
            "title": "启动MCP服务器",
            "code": "python main.py"
        },
        {
            "title": "在Cursor中扫描项目",
            "code": "ios_scan_project('/path/to/ios/project', 'auto', false)"
        },
        {
            "title": "优化Swift文件",
            "code": "ios_optimize_file('UserManager.swift', file_content, 'social', 'progressive', 0.5)"
        },
        {
            "title": "扩展式改造",
            "code": "ios_optimize_file('ProductView.swift', file_content, 'ecommerce', 'extension', 0.4)"
        }
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"\n{i}. {example['title']}:")
        print(f"   {example['code']}")
    
    print("\n📋 支持的参数:")
    print("   - 主题 (theme): social, ecommerce, tool, entertainment, education")
    print("   - 策略 (strategy): progressive, extension")
    print("   - 代码占比 (code_ratio): 0.3-0.8")


def main():
    """主测试函数"""
    print("🚀 iOS Migration MCP Server 测试开始")
    print("=" * 50)
    
    test_results = []
    
    # 运行各项测试
    test_results.append(test_theme_config())
    test_results.append(test_project_scanner())
    test_results.append(test_file_optimizer())
    
    # 显示使用示例
    show_usage_examples()
    
    # 总结测试结果
    print("\n" + "=" * 50)
    print("📋 测试结果总结:")
    
    passed = sum(test_results)
    total = len(test_results)
    
    if passed == total:
        print(f"✅ 所有测试通过 ({passed}/{total})")
        print("🎉 iOS Migration MCP Server 运行正常！")
        
        print("\n📖 使用说明:")
        print("1. 安装依赖: pip install -r requirements.txt")
        print("2. 启动服务器: python main.py")
        print("3. 在Cursor中配置MCP服务器")
        print("4. 使用工具: ios_scan_project() 和 ios_optimize_file()")
        
        return 0
    else:
        print(f"❌ 部分测试失败 ({passed}/{total})")
        print("🔧 请检查相关组件")
        return 1


if __name__ == "__main__":
    sys.exit(main()) 