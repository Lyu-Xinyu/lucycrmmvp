import streamlit as st
import anthropic
import pandas as pd
import io
from datetime import datetime

# 页面配置
st.set_page_config(
    page_title="数据分析助手",
    page_icon="📊",
    layout="wide"
)

# 初始化 session state
if 'analysis_history' not in st.session_state:
    st.session_state.analysis_history = []

# 标题
st.title("📊 数据分析助手")
st.markdown("---")

# 侧边栏配置
with st.sidebar:
    st.header("⚙️ 配置")
    
    # API Key 输入（优先使用 secrets，否则手动输入）
    if "ANTHROPIC_API_KEY" in st.secrets:
        api_key = st.secrets["ANTHROPIC_API_KEY"]
        st.success("✅ API Key 已配置")
    else:
        api_key = st.text_input("Claude API Key", type="password")
        if not api_key:
            st.warning("⚠️ 请输入 API Key")
    
    st.markdown("---")
    st.markdown("### 📖 使用说明")
    st.markdown("""
    1. 上传数据文件（CSV/Excel）
    2. 选择分析类型
    3. 输入分析需求
    4. 下载分析报告
    """)

# 主界面布局
col1, col2 = st.columns([1, 1])

with col1:
    st.header("📁 文件上传")
    uploaded_file = st.file_uploader(
        "上传指标文件",
        type=['csv', 'xlsx', 'xls'],
        help="支持 CSV 和 Excel 格式"
    )
    
    if uploaded_file:
        try:
            # 读取文件
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            st.success(f"✅ 文件加载成功！共 {len(df)} 行 {len(df.columns)} 列")
            
            # 数据预览
            with st.expander("📋 数据预览"):
                st.dataframe(df.head(10))
                
            # 数据统计
            with st.expander("📈 数据统计"):
                st.write(df.describe())
                
        except Exception as e:
            st.error(f"❌ 文件读取失败: {str(e)}")
            df = None
    else:
        df = None

with col2:
    st.header("🤖 Claude 分析")
    
    if not api_key:
        st.warning("⚠️ 请先在侧边栏配置 API Key")
    else:
        # 分析类型选择
        analysis_type = st.selectbox(
            "选择分析类型",
            ["数据摘要", "趋势分析", "异常检测", "自定义分析"]
        )
        
        # 用户输入
        if analysis_type == "自定义分析":
            user_prompt = st.text_area(
                "输入分析需求",
                placeholder="例如：分析销售额的月度趋势，找出表现最好的产品类别...",
                height=100
            )
        else:
            user_prompt = None
            st.info(f"将自动执行 {analysis_type}")
        
        # 分析按钮
        if st.button("🚀 开始分析", type="primary", disabled=(df is None)):
            if df is not None:
                with st.spinner("🤔 Claude 正在分析中..."):
                    try:
                        # 准备数据摘要
                        data_summary = f"""
数据文件：{uploaded_file.name}
行数：{len(df)}
列数：{len(df.columns)}
列名：{', '.join(df.columns.tolist())}

前5行数据：
{df.head().to_string()}

数据统计：
{df.describe().to_string()}
"""
                        
                        # 构建提示词
                        if analysis_type == "数据摘要":
                            prompt = f"请对以下数据进行摘要分析，包括关键指标、数据特征和主要发现：\n\n{data_summary}"
                        elif analysis_type == "趋势分析":
                            prompt = f"请分析以下数据的趋势和模式：\n\n{data_summary}"
                        elif analysis_type == "异常检测":
                            prompt = f"请检测以下数据中的异常值和潜在问题：\n\n{data_summary}"
                        else:
                            prompt = f"{user_prompt}\n\n数据信息：\n{data_summary}"
                        
                        # 调用 Claude API
                        client = anthropic.Anthropic(api_key=api_key)
                        message = client.messages.create(
                            model="claude-sonnet-4-5-20250929",
                            max_tokens=4096,
                            messages=[
                                {"role": "user", "content": prompt}
                            ]
                        )
                        
                        # 提取响应
                        analysis_result = message.content[0].text
                        
                        # 显示结果
                        st.markdown("### 📊 分析结果")
                        st.markdown(analysis_result)
                        
                        # 保存到历史
                        st.session_state.analysis_history.append({
                            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            'type': analysis_type,
                            'result': analysis_result
                        })
                        
                    except Exception as e:
                        st.error(f"❌ 分析失败: {str(e)}")

# 结果下载区域
st.markdown("---")
st.header("💾 下载报告")

col3, col4, col5 = st.columns(3)

with col3:
    if df is not None:
        # 下载原始数据
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False, encoding='utf-8-sig')
        st.download_button(
            label="📥 下载数据文件",
            data=csv_buffer.getvalue(),
            file_name=f"data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )

with col4:
    if st.session_state.analysis_history:
        # 下载分析报告
        report = "# 数据分析报告\n\n"
        for item in st.session_state.analysis_history:
            report += f"## {item['type']} - {item['timestamp']}\n\n"
            report += f"{item['result']}\n\n---\n\n"
        
        st.download_button(
            label="📥 下载分析报告",
            data=report,
            file_name=f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
            mime="text/markdown"
        )

with col5:
    if st.session_state.analysis_history:
        if st.button("🗑️ 清除历史"):
            st.session_state.analysis_history = []
            st.rerun()

# 分析历史
if st.session_state.analysis_history:
    st.markdown("---")
    st.header("📜 分析历史")
    for idx, item in enumerate(reversed(st.session_state.analysis_history)):
        with st.expander(f"{item['type']} - {item['timestamp']}"):
            st.markdown(item['result'])
