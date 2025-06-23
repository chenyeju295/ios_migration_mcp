#!/usr/bin/env python3
"""
iOS代码迁移MCP服务器 - 简化版
专注于文件改造进度跟踪
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

from fastmcp import FastMCP

# 创建MCP应用
mcp = FastMCP("iOS Migration Tracker")

# 支持的文件扩展名
SUPPORTED_EXTENSIONS = ['.swift', '.m', '.mm', '.h']

def get_project_files(project_path: str) -> List[str]:
    """获取项目中的所有代码文件"""
    files = []
    for root, dirs, filenames in os.walk(project_path):
        # 跳过隐藏目录和常见的非代码目录
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['Pods', 'build', 'DerivedData']]
        
        for filename in filenames:
            if any(filename.endswith(ext) for ext in SUPPORTED_EXTENSIONS):
                files.append(os.path.join(root, filename))
    return files

def get_record_file_path(project_path: str) -> str:
    """获取记录文件路径"""
    record_dir = os.path.join(project_path, '.migration_record')
    os.makedirs(record_dir, exist_ok=True)
    return os.path.join(record_dir, 'progress.json')

def load_progress(project_path: str) -> Dict[str, Any]:
    """加载进度记录"""
    record_file = get_record_file_path(project_path)
    
    if os.path.exists(record_file):
        try:
            with open(record_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            pass
    
    # 默认记录结构
    return {
        "project_path": project_path,
        "created_at": datetime.now().isoformat(),
        "last_updated": datetime.now().isoformat(),
        "completed_files": [],
        "total_files": 0,
        "file_list": []
    }

def save_progress(project_path: str, progress_data: Dict[str, Any]):
    """保存进度记录"""
    record_file = get_record_file_path(project_path)
    progress_data["last_updated"] = datetime.now().isoformat()
    
    with open(record_file, 'w', encoding='utf-8') as f:
        json.dump(progress_data, f, indent=2, ensure_ascii=False)

@mcp.tool()
def scan_project(project_path: str) -> Dict[str, Any]:
    """
    扫描项目并初始化进度跟踪
    
    Args:
        project_path: iOS项目路径
    
    Returns:
        项目文件列表和基本统计
    """
    if not os.path.exists(project_path):
        return {"error": "项目路径不存在"}
    
    # 获取所有代码文件
    all_files = get_project_files(project_path)
    relative_files = [os.path.relpath(f, project_path) for f in all_files]
    
    # 加载或创建进度记录
    progress = load_progress(project_path)
    progress["total_files"] = len(relative_files)
    progress["file_list"] = relative_files
    
    # 保存进度
    save_progress(project_path, progress)
    
    return {
        "project_path": project_path,
        "total_files": len(relative_files),
        "files": relative_files,
        "completed_files": len(progress["completed_files"]),
        "completion_rate": f"{len(progress['completed_files']) / len(relative_files) * 100:.1f}%" if relative_files else "0%"
    }

@mcp.tool()
def mark_file_completed(project_path: str, file_path: str, notes: str = "") -> Dict[str, Any]:
    """
    标记文件改造完成
    
    Args:
        project_path: 项目路径
        file_path: 完成改造的文件路径（相对路径）
        notes: 改造备注
    
    Returns:
        更新后的进度信息
    """
    progress = load_progress(project_path)
    
    # 标准化文件路径
    if file_path.startswith(project_path):
        file_path = os.path.relpath(file_path, project_path)
    
    # 检查文件是否在项目中
    if file_path not in progress["file_list"]:
        return {"error": f"文件 {file_path} 不在项目文件列表中"}
    
    # 检查是否已经完成
    if file_path in progress["completed_files"]:
        return {"error": f"文件 {file_path} 已经标记为完成"}
    
    # 标记为完成
    progress["completed_files"].append(file_path)
    
    # 添加完成记录
    if "completion_history" not in progress:
        progress["completion_history"] = []
    
    progress["completion_history"].append({
        "file": file_path,
        "completed_at": datetime.now().isoformat(),
        "notes": notes
    })
    
    # 保存进度
    save_progress(project_path, progress)
    
    completion_rate = len(progress["completed_files"]) / progress["total_files"] * 100
    
    return {
        "success": True,
        "file": file_path,
        "completed_files": len(progress["completed_files"]),
        "total_files": progress["total_files"],
        "completion_rate": f"{completion_rate:.1f}%",
        "remaining_files": progress["total_files"] - len(progress["completed_files"])
    }

@mcp.tool()
def get_progress(project_path: str) -> Dict[str, Any]:
    """
    获取项目改造进度
    
    Args:
        project_path: 项目路径
    
    Returns:
        详细的进度信息
    """
    progress = load_progress(project_path)
    
    if progress["total_files"] == 0:
        return {"error": "项目尚未扫描，请先运行 scan_project"}
    
    completion_rate = len(progress["completed_files"]) / progress["total_files"] * 100
    remaining_files = [f for f in progress["file_list"] if f not in progress["completed_files"]]
    
    return {
        "project_path": progress["project_path"],
        "total_files": progress["total_files"],
        "completed_files": len(progress["completed_files"]),
        "completion_rate": f"{completion_rate:.1f}%",
        "remaining_files": len(remaining_files),
        "completed_list": progress["completed_files"],
        "remaining_list": remaining_files[:10],  # 只显示前10个待完成文件
        "last_updated": progress["last_updated"],
        "recent_completions": progress.get("completion_history", [])[-5:]  # 最近5个完成记录
    }

@mcp.tool()
def reset_progress(project_path: str) -> Dict[str, Any]:
    """
    重置项目进度（清空所有完成记录）
    
    Args:
        project_path: 项目路径
    
    Returns:
        重置结果
    """
    progress = load_progress(project_path)
    progress["completed_files"] = []
    progress["completion_history"] = []
    save_progress(project_path, progress)
    
    return {
        "success": True,
        "message": "项目进度已重置",
        "total_files": progress["total_files"]
    }

@mcp.tool()
def setup_cursor_rules(project_path: str, cursor_project_root: str) -> Dict[str, Any]:
    """
    在Cursor项目中设置iOS代码改造规则
    
    Args:
        project_path: iOS项目路径
        cursor_project_root: Cursor项目根目录
    
    Returns:
        设置结果
    """
    # 创建.cursor/rules目录
    rules_dir = os.path.join(cursor_project_root, '.cursor', 'rules')
    os.makedirs(rules_dir, exist_ok=True)
    
    # 基本的iOS代码规则
    ios_rules = """# iOS代码迁移规则

## 核心要求
1. 每个文件新增代码占比30-50%
2. 所有新代码必须被原有代码调用
3. 保持代码风格一致
4. 不影响原有功能

## 技术要求
- 使用UIKit、Foundation、GCD等系统框架
- 避免敏感功能：支付、WebView、JavaScript
- 增加代码多样性，避免模板化

## 改造步骤
1. 分析现有代码结构
2. 设计辅助功能类
3. 分散插入新代码
4. 验证调用关系
5. 测试功能完整性
"""
    
    # 写入规则文件
    rules_file = os.path.join(rules_dir, 'ios_migration_rules.md')
    with open(rules_file, 'w', encoding='utf-8') as f:
        f.write(ios_rules)
    
    return {
        "success": True,
        "rules_file": rules_file,
        "message": "iOS代码改造规则已设置到 .cursor/rules/ 目录"
    }

if __name__ == "__main__":
    mcp.run() 