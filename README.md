# 📊 CRM 助手 MVP

基于 Streamlit + Claude API 的智能CRM数据分析平台

## ✨ 功能特性

- 📁 **文件上传**：支持 CSV、Excel 格式
- 🤖 **AI 分析**：集成 Claude Sonnet 4.5 进行智能分析
- 📊 **多种分析类型**：数据摘要、趋势分析、异常检测
- 💾 **报告下载**：支持下载分析报告和处理后的数据
- 📜 **历史记录**：保存分析历史，方便回溯

## 🚀 快速部署到 Streamlit Cloud

### 步骤 1：上传到 GitHub

1. 在 GitHub 创建新仓库（例如：`data-analysis-mvp`）
2. 将本项目所有文件上传到仓库
3. 确保包含以下文件：
   - `app.py`
   - `requirements.txt`
   - `.streamlit/config.toml`
   - `.gitignore`
   - `README.md`

### 步骤 2：部署到 Streamlit Cloud

1. 访问 https://streamlit.io/cloud
2. 使用 GitHub 账号登录
3. 点击 **"New app"**
4. 选择你的仓库和分支（main）
5. 主文件路径填写：`app.py`
6. 点击 **"Deploy"**

### 步骤 3：配置 API Key

在 Streamlit Cloud 部署页面：

1. 点击 **"Settings"** → **"Secrets"**
2. 添加以下内容：

```toml
ANTHROPIC_API_KEY = "your-anthropic-api-key-here"
```

3. 点击 **"Save"**
4. 应用会自动重启

### 获取 Anthropic API Key

1. 访问 https://console.anthropic.com/
2. 注册/登录账号
3. 进入 **API Keys** 页面
4. 创建新的 API Key
5. 复制密钥（只显示一次，请妥善保存）

## 🛠️ 本地开发

### 安装依赖

```bash
pip install -r requirements.txt
```

### 配置密钥

创建 `.streamlit/secrets.toml` 文件：

```toml
ANTHROPIC_API_KEY = "your-api-key-here"
```

### 运行应用

```bash
streamlit run app.py
```

访问 http://localhost:8501

## 📝 后续开发计划

### 阶段 1：当前 MVP ✅
- [x] 文件上传和读取
- [x] Claude API 集成
- [x] 基础数据分析
- [x] 报告下载

### 阶段 2：增强功能
- [ ] 数据可视化（图表生成）
- [ ] 多文件对比分析
- [ ] 自定义分析模板
- [ ] 用户账号系统

### 阶段 3：高级功能
- [ ] 数据仪表板
- [ ] 定时报告生成
- [ ] 咨询专家系统集成
- [ ] N8N 工作流集成

## 🔧 技术栈

- **前端框架**：Streamlit
- **AI 模型**：Claude Sonnet 4.5
- **数据处理**：Pandas
- **文件格式**：CSV, Excel

## 📖 使用说明

1. **上传文件**：点击文件上传区域，选择 CSV 或 Excel 文件
2. **选择分析类型**：从下拉菜单选择分析方式
3. **开始分析**：点击"开始分析"按钮
4. **查看结果**：分析结果会显示在页面上
5. **下载报告**：点击下载按钮保存分析结果

## ⚠️ 注意事项

- 文件大小建议不超过 200MB
- API 调用会产生费用，请注意使用量
- 敏感数据请谨慎上传

## 📧 联系方式

如有问题或建议，欢迎提交 Issue

## 📄 许可证

MIT License
