"""
iOS Migration 基础配置模块
"""

class BasicConfig:
    """基础配置类"""
    
    # 支持的文件扩展名
    SUPPORTED_EXTENSIONS = ['.swift', '.m', '.h']
    
    # 必需的框架检查
    REQUIRED_FRAMEWORKS = ['UIKit', 'Foundation']
    
    # 推荐的技术栈
    RECOMMENDED_TECH = ['DispatchQueue', 'NotificationCenter', 'UserDefaults']
    
    # 敏感功能关键词（需要避免）
    SENSITIVE_KEYWORDS = [
        'payment', 'webview', 'javascript', 'evaluateJavaScript', 
        'purchase', 'in-app', 'billing', 'paypal', 'stripe'
    ]
    
    # 代码复杂度阈值
    COMPLEXITY_THRESHOLDS = {
        'low': 100,      # 100行以下为低复杂度
        'medium': 200,   # 100-200行为中等复杂度
        'high': 200      # 200行以上为高复杂度
    }
    
    # 改造策略配置
    STRATEGIES = {
        'progressive': {
            'name': '渐进式改造',
            'description': '在原代码中分散插入新功能调用',
            '适用场景': '低复杂度文件',
            '代码占比': '40-50%'
        },
        'extension': {
            'name': '扩展式改造',
            'description': '通过Extension添加新功能',
            '适用场景': '中高复杂度文件',
            '代码占比': '30-40%'
        }
    }
    
    @classmethod
    def get_strategy_for_complexity(cls, complexity: str) -> str:
        """根据复杂度推荐策略"""
        if complexity == 'low':
            return 'progressive'
        else:
            return 'extension'
    
    @classmethod
    def get_target_ratio_for_complexity(cls, complexity: str) -> float:
        """根据复杂度推荐代码占比"""
        if complexity == 'low':
            return 0.45  # 45%
        elif complexity == 'medium':
            return 0.35  # 35%
        else:
            return 0.30  # 30% 