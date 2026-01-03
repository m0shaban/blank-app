import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import io

# تكوين الصفحة
st.set_page_config(
    page_title="لوحة تحكم الكاتمي | إدارة أسطول مولدات ديني",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ستايل CSS متقدم مع اللغة العربية
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;700&display=swap');
        
        * {
            font-family: 'Cairo', sans-serif;
            direction: rtl;
        }
        
        .stApp {
            background-color: #0e1117;
            color: #fafafa;
        }
        
        /* بطاقات المقاييس */
        div[data-testid="stMetric"] {
            background: linear-gradient(135deg, #1a2a3a 0%, #1f2937 100%);
            padding: 20px;
            border-radius: 12px;
            border-right: 5px solid #00a8e8;
            box-shadow: 0 4px 15px rgba(0, 168, 232, 0.2);
            text-align: right;
        }
        
        div[data-testid="stMetricValue"] {
            font-size: 32px;
            font-weight: 700;
            color: #00a8e8;
        }
        
        div[data-testid="stMetricLabel"] {
            font-size: 13px;
            color: #9ca3af;
            margin-top: 8px;
        }
        
        /* شريط جانبي */
        section[data-testid="stSidebar"] {
            background-color: #111827;
            border-left: 3px solid #00a8e8;
        }
        
        /* العناوين */
        h1, h2, h3 {
            color: #00a8e8;
            font-weight: 700;
        }
        
        /* الأزرار */
        .stButton > button {
            width: 100%;
            background: linear-gradient(135deg, #00a8e8 0%, #0087c9 100%);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 10px;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover {
            box-shadow: 0 4px 12px rgba(0, 168, 232, 0.4);
            transform: translateY(-2px);
        }
        
        /* الجداول */
        .stDataFrame {
            direction: rtl;
        }
        
        /* التبويبات */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }
        
        .stTabs [data-baseweb="tab"] {
            background-color: #1f2937;
            border-radius: 8px;
            padding: 12px 20px;
            color: #9ca3af;
            border: none;
        }
        
        .stTabs [aria-selected="true"] {
            background-color: #00a8e8;
            color: white;
        }
    </style>
    """, unsafe_allow_html=True)

# ========================
# 1️⃣ توليد البيانات المحاكاة
# ========================
@st.cache_data
def generate_fleet_data():
    """توليد بيانات 50 مولد ديني واقعية عبر محافظات مصر"""
    np.random.seed(42)
    
    models = ['DCA-18ESX', 'DCA-25USI', 'DCA-45USI', 'DCA-150ESK', 'DCA-400ESK']
    governorates = {
        'القاهرة': {'lat': 30.0444, 'lon': 31.2357},
        'الجيزة': {'lat': 30.0131, 'lon': 31.2089},
        'الإسكندرية': {'lat': 31.2001, 'lon': 29.9187},
        'أسوان': {'lat': 24.0889, 'lon': 32.8998},
        'البحر الأحمر': {'lat': 27.2579, 'lon': 33.8116},
        'السويس': {'lat': 29.9668, 'lon': 32.5498},
        'المنيا': {'lat': 28.1167, 'lon': 30.7500},
        'قنا': {'lat': 26.1592, 'lon': 33.7795}
    }
    
    statuses = ['نشط', 'معطل', 'صيانة', 'في الطريق']
    data = []
    
    for i in range(50):
        gov = np.random.choice(list(governorates.keys()))
        base_lat = governorates[gov]['lat']
        base_lon = governorates[gov]['lon']
        
        lat = base_lat + np.random.uniform(-0.1, 0.1)
        lon = base_lon + np.random.uniform(-0.1, 0.1)
        
        model = np.random.choice(models)
        kva_map = {'DCA-18ESX': 15, 'DCA-25USI': 20, 'DCA-45USI': 37, 'DCA-150ESK': 125, 'DCA-400ESK': 350}
        kva = kva_map[model]
        
        revenue = np.random.randint(8000, 45000) * (kva/50)
        status = np.random.choice(statuses, p=[0.65, 0.15, 0.15, 0.05])
        fuel = np.random.randint(5, 100)
        temp = np.random.randint(65, 115)
        hours = np.random.randint(100, 5000)
        
        alert = "لا يوجد"
        if fuel < 15:
            alert = "⚠️ وقود منخفض"
        elif temp > 105:
            alert = "🔴 ارتفاع حرارة"
        elif status == 'صيانة':
            alert = "🔧 صيانة مجدولة"
        elif hours > 4500:
            alert = "🛠️ مراجعة شاملة"
        
        data.append({
            'معرف المولد': f'DNY-{1000+i}',
            'الموديل': model,
            'السعة': kva,
            'المحافظة': gov,
            'lat': lat,
            'lon': lon,
            'الحالة': status,
            'الإيراد الشهري': round(revenue, 2),
            'الوقود %': fuel,
            'الحرارة °C': temp,
            'ساعات العمل': hours,
            'التنبيه': alert,
            'الموقع': f"{gov} - موقع {np.random.randint(1,5)}"
        })
    
    return pd.DataFrame(data)

df = generate_fleet_data()

# ========================
# 2️⃣ الشريط الجانبي - التحكم المتقدم
# ========================
st.sidebar.title("🎛️ لوحة التحكم")
st.sidebar.markdown("### ⚙️ المرشحات والإعدادات")

# المرشحات
selected_govs = st.sidebar.multiselect(
    "🗺️ اختر المحافظات:",
    df['المحافظة'].unique(),
    default=df['المحافظة'].unique()
)

selected_status = st.sidebar.multiselect(
    "📊 حالة المولد:",
    df['الحالة'].unique(),
    default=df['الحالة'].unique()
)

capacity_range = st.sidebar.slider(
    "⚡ نطاق السعة (kVA):",
    int(df['السعة'].min()),
    int(df['السعة'].max()),
    (int(df['السعة'].min()), int(df['السعة'].max()))
)

fuel_threshold = st.sidebar.slider(
    "⛽ حد الوقود الحرج (%):",
    5, 50, 20
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📋 إجراءات سريعة")

col1, col2 = st.sidebar.columns(2)
with col1:
    if st.button("📥 تصدير بيانات"):
        csv = df.to_csv(index=False, encoding='utf-8-sig')
        st.download_button(
            label="تحميل CSV",
            data=csv,
            file_name=f"أسطول_مولدات_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

with col2:
    if st.button("🔄 تحديث البيانات"):
        st.rerun()

# تطبيق المرشحات
df_filtered = df[
    (df['المحافظة'].isin(selected_govs)) &
    (df['الحالة'].isin(selected_status)) &
    (df['السعة'].between(capacity_range[0], capacity_range[1]))
]

# ========================
# 3️⃣ رأس لوحة التحكم - المقاييس الرئيسية
# ========================
st.title("⚡ لوحة تحكم الكاتمي | إدارة أسطول مولدات ديني")
st.markdown(f"**📍 مراقبة حية**: تتبع **{len(df_filtered)}** مولد عبر جمهورية مصر العربية")

# حسابات المقاييس المتقدمة
total_revenue = df_filtered['الإيراد الشهري'].sum()
active_count = len(df_filtered[df_filtered['الحالة'] == 'نشط'])
utilization = (active_count / len(df_filtered) * 100) if len(df_filtered) > 0 else 0
critical_alerts = len(df_filtered[df_filtered['التنبيه'] != 'لا يوجد'])
avg_fuel = df_filtered['الوقود %'].mean()
avg_temp = df_filtered['الحرارة °C'].mean()
low_fuel_count = len(df_filtered[df_filtered['الوقود %'] < fuel_threshold])
total_capacity = df_filtered['السعة'].sum()

# عرض المقاييس في أربع صفوف
st.markdown("### 📊 المقاييس الرئيسية")

# الصف الأول
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "💰 إجمالي الإيراد",
        f"{total_revenue/1_000_000:.2f}M جنيه",
        f"↗ {np.random.randint(3,12)}% هذا الشهر"
    )

with col2:
    st.metric(
        "⚙️ معدل التشغيل",
        f"{utilization:.1f}%",
        f"{active_count} مولد نشط",
        delta_color="normal" if utilization > 70 else "inverse"
    )

with col3:
    st.metric(
        "🚨 تنبيهات حرجة",
        critical_alerts,
        "بحاجة للانتباه" if critical_alerts > 0 else "الوضع مستقر ✅"
    )

with col4:
    st.metric(
        "⚡ إجمالي السعة",
        f"{total_capacity:.0f} kVA",
        f"متوسط: {total_capacity/len(df_filtered):.0f} kVA"
    )

# الصف الثاني
col5, col6, col7, col8 = st.columns(4)

with col5:
    st.metric(
        "⛽ متوسط الوقود",
        f"{avg_fuel:.0f}%",
        f"🔴 {low_fuel_count} مولد وقود منخفض"
    )

with col6:
    st.metric(
        "🌡️ متوسط الحرارة",
        f"{avg_temp:.0f}°C",
        "✅ طبيعي" if avg_temp < 100 else "⚠️ مرتفع"
    )

with col7:
    st.metric(
        "🔧 بحاجة صيانة",
        len(df_filtered[df_filtered['الحالة'] == 'صيانة']),
        "مجدولة"
    )

with col8:
    st.metric(
        "🚛 معطل أو في الطريق",
        len(df_filtered[df_filtered['الحالة'].isin(['معطل', 'في الطريق'])]),
        "يحتاج متابعة"
    )

st.divider()

# ========================
# 4️⃣ التبويبات المتقدمة
# ========================
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["📍 الخريطة", "📈 التحليلات", "🤖 الذكاء الاصطناعي", "📋 الجدول", "📊 التقارير"]
)

# ==================
# التبويب الأول - الخريطة
# ==================
with tab1:
    st.subheader("📍 توزيع المولدات على الخريطة")
    
    col_map1, col_map2 = st.columns([2, 3])
    
    with col_map1:
        st.map(
            df_filtered[['lat', 'lon']].rename(
                columns={'lat': 'latitude', 'lon': 'longitude'}
            ),
            zoom=5,
            use_container_width=True
        )
        st.caption("🗺️ موقع جميع المولدات عبر الجمهورية - تحديث فوري من نظام GPS")
    
    with col_map2:
        st.markdown("### 📊 توزيع حسب المحافظة")
        gov_dist = df_filtered['المحافظة'].value_counts()
        
        fig_pie = px.pie(
            values=gov_dist.values,
            names=gov_dist.index,
            color_discrete_sequence=['#00a8e8', '#0087c9', '#006ea8', '#005587', '#004466', '#003344', '#002233', '#001122']
        )
        fig_pie.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(size=12, color='#fafafa', family='Arial')
        )
        st.plotly_chart(fig_pie, use_container_width=True)

# ==================
# التبويب الثاني - التحليلات
# ==================
with tab2:
    st.subheader("📈 التحليلات المتقدمة والرؤى")
    
    col_a1, col_a2 = st.columns(2)
    
    with col_a1:
        st.markdown("#### 💰 الإيراد حسب الموقع")
        revenue_by_loc = df_filtered.groupby('الموقع')['الإيراد الشهري'].sum().sort_values(ascending=False).head(10)
        
        fig_bar = go.Figure(data=[
            go.Bar(
                x=revenue_by_loc.values,
                y=revenue_by_loc.index,
                orientation='h',
                marker=dict(
                    color=revenue_by_loc.values,
                    colorscale='Blues',
                    showscale=True
                )
            )
        ])
        fig_bar.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=400,
            font=dict(color='#fafafa')
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    
    with col_a2:
        st.markdown("#### ⚡ توزيع السعات")
        capacity_dist = df_filtered.groupby('الموديل')['السعة'].count()
        
        fig_bar2 = px.bar(
            x=capacity_dist.index,
            y=capacity_dist.values,
            labels={'x': 'الموديل', 'y': 'العدد'},
            color=capacity_dist.values,
            color_continuous_scale='Viridis'
        )
        fig_bar2.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=400,
            font=dict(color='#fafafa')
        )
        st.plotly_chart(fig_bar2, use_container_width=True)
    
    # صف ثاني من التحليلات
    col_a3, col_a4 = st.columns(2)
    
    with col_a3:
        st.markdown("#### 🌡️ توزيع درجات الحرارة")
        
        fig_hist = go.Figure(data=[
            go.Histogram(
                x=df_filtered['الحرارة °C'],
                nbinsx=15,
                marker=dict(color='#00a8e8')
            )
        ])
        fig_hist.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=400,
            font=dict(color='#fafafa'),
            xaxis_title='درجة الحرارة °C',
            yaxis_title='العدد'
        )
        st.plotly_chart(fig_hist, use_container_width=True)
    
    with col_a4:
        st.markdown("#### ⛽ توزيع مستويات الوقود")
        
        fig_hist2 = go.Figure(data=[
            go.Histogram(
                x=df_filtered['الوقود %'],
                nbinsx=15,
                marker=dict(color='#ffd700')
            )
        ])
        fig_hist2.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=400,
            font=dict(color='#fafafa'),
            xaxis_title='مستوى الوقود %',
            yaxis_title='العدد'
        )
        st.plotly_chart(fig_hist2, use_container_width=True)

# ==================
# التبويب الثالث - الذكاء الاصطناعي
# ==================
with tab3:
    st.subheader("🤖 نظام الذكاء الاصطناعي للتنبؤ والصيانة الوقائية")
    
    col_ai1, col_ai2 = st.columns([1, 2])
    
    with col_ai1:
        st.markdown("### 🎯 التنبيهات الذكية")
        
        alerts_high = df_filtered[df_filtered['الحرارة °C'] > 105]
        alerts_fuel = df_filtered[df_filtered['الوقود %'] < fuel_threshold]
        alerts_maintenance = df_filtered[df_filtered['الحالة'] == 'صيانة']
        
        with st.container():
            st.metric("🔴 ارتفاع حرارة خطير", len(alerts_high))
            st.metric("⚠️ وقود منخفض", len(alerts_fuel))
            st.metric("🔧 يحتاج صيانة", len(alerts_maintenance))
    
    with col_ai2:
        st.markdown("### 📋 التوصيات الذكية")
        
        recommendations = []
        
        if len(alerts_high) > 0:
            recommendations.append(
                f"🔴 **{len(alerts_high)} مولد** درجات حرارتهم مرتفعة جداً - يجب إرسال فريق صيانة فوري من فرع {alerts_high['المحافظة'].mode()[0] if len(alerts_high) > 0 else ''}"
            )
        
        if len(alerts_fuel) > 0:
            recommendations.append(
                f"⚠️ **{len(alerts_fuel)} مولد** احتياطي الوقود منخفض - جدول إعادة تزويد خلال 24 ساعة"
            )
        
        if len(alerts_maintenance) > 0:
            recommendations.append(
                f"🔧 **{len(alerts_maintenance)} مولد** مجدول للصيانة - قيمة محتملة: {alerts_maintenance['السعة'].sum() * 500:.0f} جنيه"
            )
        
        if not recommendations:
            st.success("✅ **جميع المولدات في حالة جيدة!** - لا توصيات حالية")
        else:
            for i, rec in enumerate(recommendations, 1):
                st.warning(rec)
        
        st.markdown("---")
        st.markdown("### 📊 إحصائيات الأداء")
        
        col_stats1, col_stats2 = st.columns(2)
        
        with col_stats1:
            st.markdown(f"""
            **معدل الكفاءة**: {utilization:.1f}%
            
            **متوسط الحرارة**: {avg_temp:.0f}°C
            
            **متوسط الوقود**: {avg_fuel:.0f}%
            """)
        
        with col_stats2:
            st.markdown(f"""
            **إجمالي الإيراد**: {total_revenue/1_000_000:.2f}M جنيه
            
            **عمر المولدات**: {df_filtered['ساعات العمل'].mean():.0f} ساعة متوسط
            
            **السعة الإجمالية**: {total_capacity:.0f} kVA
            """)

# ==================
# التبويب الرابع - الجدول المتقدم
# ==================
with tab4:
    st.subheader("📋 جدول البيانات الكامل مع التصفية والفرز")
    
    # خيارات العرض
    col_opt1, col_opt2, col_opt3 = st.columns(3)
    
    with col_opt1:
        sort_by = st.selectbox(
            "فرز حسب:",
            ['معرف المولد', 'الإيراد الشهري', 'الوقود %', 'الحرارة °C', 'ساعات العمل']
        )
    
    with col_opt2:
        sort_order = st.selectbox("ترتيب:", ["تنازلي", "تصاعدي"])
    
    with col_opt3:
        show_cols = st.multiselect(
            "الأعمدة المراد عرضها:",
            df_filtered.columns.tolist(),
            default=['معرف المولد', 'الموديل', 'المحافظة', 'الحالة', 'الإيراد الشهري', 'التنبيه']
        )
    
    # فرز البيانات
    ascending = sort_order == "تصاعدي"
    df_sorted = df_filtered.sort_values(sort_by, ascending=ascending)
    
    # عرض الجدول مع التنسيق
    st.dataframe(
        df_sorted[show_cols].style.format({
            'الإيراد الشهري': '{:.2f}',
            'الوقود %': '{:.0f}%',
            'الحرارة °C': '{:.0f}',
            'السعة': '{:.0f}'
        }),
        use_container_width=True,
        height=500
    )
    
    # خيار التصدير
    st.markdown("---")
    csv_data = df_sorted[show_cols].to_csv(index=False, encoding='utf-8-sig')
    st.download_button(
        label="📥 تحميل الجدول كـ CSV",
        data=csv_data,
        file_name=f"تفاصيل_المولدات_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
        mime="text/csv"
    )

# ==================
# التبويب الخامس - التقارير
# ==================
with tab5:
    st.subheader("📊 التقارير التفصيلية والإحصائيات")
    
    # اختيار نوع التقرير
    report_type = st.selectbox(
        "نوع التقرير:",
        [
            "ملخص الأداء",
            "تقرير الإيرادات",
            "تقرير الصيانة",
            "تقرير السلامة",
            "تقرير الكفاءة"
        ]
    )
    
    if report_type == "ملخص الأداء":
        st.markdown(f"""
        ### 📊 ملخص الأداء الشامل
        
        **التاريخ**: {datetime.now().strftime('%d/%m/%Y - %H:%M')}
        
        #### 🎯 المقاييس الرئيسية
        - إجمالي المولدات المراقبة: **{len(df_filtered)}**
        - المولدات النشطة: **{active_count}** ({utilization:.1f}%)
        - معطل/في الطريق: **{len(df_filtered[df_filtered['الحالة'].isin(['معطل', 'في الطريق'])])}**
        - بحاجة صيانة: **{len(df_filtered[df_filtered['الحالة'] == 'صيانة'])}**
        
        #### 💰 الإيرادات
        - إجمالي الإيراد الشهري: **{total_revenue:,.2f} جنيه**
        - متوسط الإيراد لكل مولد: **{total_revenue/len(df_filtered):,.2f} جنيه**
        - أعلى موقع: **{df_filtered.groupby('الموقع')['الإيراد الشهري'].sum().idxmax()}**
        
        #### ⚙️ الأداء التقني
        - السعة الإجمالية: **{total_capacity:,.0f} kVA**
        - متوسط ساعات العمل: **{df_filtered['ساعات العمل'].mean():.0f} ساعة**
        - متوسط درجة الحرارة: **{avg_temp:.0f}°C**
        - متوسط مستوى الوقود: **{avg_fuel:.0f}%**
        
        #### 🚨 الحالات الحرجة
        - مولدات بحرارة عالية: **{len(df_filtered[df_filtered['الحرارة °C'] > 105])}**
        - مولدات بوقود منخفض: **{len(df_filtered[df_filtered['الوقود %'] < fuel_threshold])}**
        - إجمالي التنبيهات النشطة: **{critical_alerts}**
        """)
    
    elif report_type == "تقرير الإيرادات":
        st.markdown("### 💰 تقرير الإيرادات التفصيلي")
        
        revenue_by_gov = df_filtered.groupby('المحافظة')['الإيراد الشهري'].agg(['sum', 'mean', 'count']).round(2)
        revenue_by_gov.columns = ['الإجمالي', 'المتوسط', 'العدد']
        
        st.dataframe(revenue_by_gov, use_container_width=True)
        
        fig_revenue = px.bar(
            x=revenue_by_gov.index,
            y=revenue_by_gov['الإجمالي'],
            labels={'x': 'المحافظة', 'y': 'الإيراد'},
            color=revenue_by_gov['الإجمالي'],
            color_continuous_scale='Greens'
        )
        fig_revenue.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=400
        )
        st.plotly_chart(fig_revenue, use_container_width=True)
    
    elif report_type == "تقرير الصيانة":
        st.markdown("### 🔧 تقرير الصيانة والعمليات")
        
        maintenance_data = df_filtered[df_filtered['الحالة'] == 'صيانة'][
            ['معرف المولد', 'الموديل', 'المحافظة', 'ساعات العمل', 'الإيراد الشهري']
        ]
        
        if len(maintenance_data) > 0:
            st.dataframe(maintenance_data, use_container_width=True)
            st.metric("إجمالي قيمة الصيانة المتوقعة", f"{len(maintenance_data) * 500:,.0f} جنيه")
        else:
            st.info("لا توجد مولدات بحاجة صيانة حالياً")
    
    elif report_type == "تقرير السلامة":
        st.markdown("### 🚨 تقرير السلامة والتنبيهات")
        
        alert_summary = pd.DataFrame({
            'نوع التنبيه': ['وقود منخفض', 'حرارة مرتفعة', 'صيانة مجدولة', 'مراجعة شاملة'],
            'العدد': [
                len(df_filtered[df_filtered['الوقود %'] < fuel_threshold]),
                len(df_filtered[df_filtered['الحرارة °C'] > 105]),
                len(df_filtered[df_filtered['الحالة'] == 'صيانة']),
                len(df_filtered[df_filtered['ساعات العمل'] > 4500])
            ]
        })
        
        st.dataframe(alert_summary, use_container_width=True)
        
        fig_alerts = px.pie(
            values=alert_summary['العدد'],
            names=alert_summary['نوع التنبيه'],
            color_discrete_sequence=['#ff6b6b', '#ffa500', '#ffd700', '#ff9999']
        )
        fig_alerts.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig_alerts, use_container_width=True)
    
    elif report_type == "تقرير الكفاءة":
        st.markdown("### ⚙️ تقرير الكفاءة والإنتاجية")
        
        efficiency_by_model = df_filtered.groupby('الموديل').agg({
            'الحالة': lambda x: (x == 'نشط').sum() / len(x) * 100,
            'الإيراد الشهري': 'mean',
            'ساعات العمل': 'mean'
        }).round(2)
        efficiency_by_model.columns = ['نسبة التشغيل %', 'متوسط الإيراد', 'متوسط الساعات']
        
        st.dataframe(efficiency_by_model, use_container_width=True)

st.divider()

# ========================
# 5️⃣ التذييل والمعلومات
# ========================
col_footer1, col_footer2, col_footer3 = st.columns(3)

with col_footer1:
    st.markdown("### 📞 معلومات الاتصال")
    st.markdown("""
    **الكاتمي - الوكيل الحصري لمولدات ديني**
    
    📞 (202) XXXX-XXXX
    
    📧 info@elkatamy.com
    """)

with col_footer2:
    st.markdown("### 🔐 الحالة النظامية")
    st.markdown(f"""
    ✅ آخر تحديث: {datetime.now().strftime('%H:%M:%S')}
    
    ✅ جودة البيانات: {(1 - critical_alerts/len(df_filtered)*0.1)*100:.0f}%
    
    ✅ معدل التوفر: {utilization:.0f}%
    """)

with col_footer3:
    st.markdown("### 📊 إحصائيات النظام")
    st.markdown(f"""
    🔍 مولدات مراقبة: {len(df_filtered)}
    
    💾 حجم البيانات: {len(df)} سجل
    
    🔄 التحديثات: فوري
    """)

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #9ca3af; font-size: 11px; padding: 20px;">
    <p>© 2026 لوحة تحكم الكاتمي | نظام إدارة أسطول مولدات ديني | v3.0</p>
    <p>تم تطويره بواسطة Elkatamy BI Team | آخر تحديث: يناير 2026</p>
</div>
""", unsafe_allow_html=True)
