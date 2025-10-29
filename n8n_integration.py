"""
N8N Webhook 集成示例

未来可以将这个模块集成到主应用中，实现：
1. 文件上传后自动触发 N8N 工作流
2. 数据预处理
3. 结果通知
"""

import requests
import json

class N8NIntegration:
    def __init__(self, webhook_url):
        """
        初始化 N8N 集成
        
        Args:
            webhook_url: N8N Webhook URL
        """
        self.webhook_url = webhook_url
    
    def trigger_workflow(self, data):
        """
        触发 N8N 工作流
        
        Args:
            data: 要发送的数据字典
            
        Returns:
            响应结果
        """
        try:
            response = requests.post(
                self.webhook_url,
                json=data,
                headers={'Content-Type': 'application/json'}
            )
            response.raise_for_status()
            return {
                'success': True,
                'data': response.json()
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def send_file_upload_event(self, filename, file_size, user_id=None):
        """
        发送文件上传事件到 N8N
        
        Args:
            filename: 文件名
            file_size: 文件大小
            user_id: 用户ID（可选）
        """
        data = {
            'event': 'file_upload',
            'filename': filename,
            'file_size': file_size,
            'user_id': user_id,
            'timestamp': str(pd.Timestamp.now())
        }
        return self.trigger_workflow(data)
    
    def send_analysis_result(self, analysis_type, result, user_id=None):
        """
        发送分析结果到 N8N
        
        Args:
            analysis_type: 分析类型
            result: 分析结果
            user_id: 用户ID（可选）
        """
        data = {
            'event': 'analysis_complete',
            'analysis_type': analysis_type,
            'result': result,
            'user_id': user_id,
            'timestamp': str(pd.Timestamp.now())
        }
        return self.trigger_workflow(data)

# 使用示例
if __name__ == "__main__":
    # 配置 N8N Webhook URL（从环境变量或配置文件读取）
    N8N_WEBHOOK_URL = "https://your-n8n-instance.com/webhook/your-webhook-id"
    
    # 创建集成实例
    n8n = N8NIntegration(N8N_WEBHOOK_URL)
    
    # 发送测试事件
    result = n8n.trigger_workflow({
        'event': 'test',
        'message': 'Hello from Streamlit!'
    })
    
    print(result)
