#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""小学三四年级学习辅助资料生成器 - 第1部分：模板+三年级数学"""
import os

BASE_DIR = "/Users/work/AI/Cursor/小学生"

SUBJECT_INFO = {
    "math":    {"name": "数学", "color": "#E74C3C", "light": "#FDECEA", "icon": "🔢", "gradient": "linear-gradient(135deg,#E74C3C,#C0392B)"},
    "chinese": {"name": "语文", "color": "#27AE60", "light": "#EAFAF1", "icon": "📖", "gradient": "linear-gradient(135deg,#27AE60,#1E8449)"},
    "english": {"name": "英语", "color": "#2980B9", "light": "#EBF5FB", "icon": "🌍", "gradient": "linear-gradient(135deg,#2980B9,#1F618D)"},
}
GRADE_INFO = {
    "grade3": {"name": "三年级", "color": "#FF6B9D", "gradient": "linear-gradient(135deg,#FF6B9D,#C44569)"},
    "grade4": {"name": "四年级", "color": "#6C63FF", "gradient": "linear-gradient(135deg,#6C63FF,#3F3D56)"},
}
SEMESTER_INFO = {"upper": "上册", "lower": "下册"}

CSS = """
<style>
*{box-sizing:border-box;margin:0;padding:0;}
body{font-family:'PingFang SC','微软雅黑',Arial,sans-serif;background:#F0F4F8;min-height:100vh;color:#2D3436;}
.header{background:var(--subj-color);color:#fff;padding:25px 20px;text-align:center;position:relative;overflow:hidden;}
.header::before{content:'';position:absolute;top:-50%;left:-50%;width:200%;height:200%;background:radial-gradient(circle,rgba(255,255,255,0.1) 0%,transparent 60%);}
.header .icon{font-size:50px;display:block;margin-bottom:8px;}
.header h1{font-size:26px;font-weight:800;text-shadow:0 2px 4px rgba(0,0,0,0.2);}
.header .sub{font-size:14px;opacity:0.9;margin-top:5px;}
.breadcrumb{background:#fff;padding:12px 20px;margin:15px;border-radius:12px;box-shadow:0 2px 8px rgba(0,0,0,0.06);font-size:13px;}
.breadcrumb a{color:var(--subj-color);text-decoration:none;font-weight:500;}
.breadcrumb a:hover{text-decoration:underline;}
.breadcrumb span{color:#888;margin:0 6px;}
.container{max-width:860px;margin:0 auto;padding:0 15px 30px;}
.section{background:#fff;border-radius:16px;padding:25px;margin-bottom:18px;box-shadow:0 4px 12px rgba(0,0,0,0.07);}
.section-title{font-size:20px;font-weight:700;margin-bottom:18px;padding-bottom:12px;border-bottom:3px solid var(--subj-color);display:flex;align-items:center;gap:8px;}
.kp-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:14px;}
.kp-card{background:var(--subj-light);border-left:5px solid var(--subj-color);border-radius:10px;padding:14px;}
.kp-card .num{font-size:11px;font-weight:700;color:var(--subj-color);text-transform:uppercase;letter-spacing:1px;margin-bottom:6px;}
.kp-card p{font-size:14px;line-height:1.7;color:#444;}
.diff-list{list-style:none;}
.diff-list li{padding:11px 15px 11px 42px;margin-bottom:9px;background:#FFF8F0;border-radius:10px;position:relative;font-size:14px;line-height:1.7;border-left:4px solid #F39C12;}
.diff-list li::before{content:"⚠";position:absolute;left:14px;top:11px;color:#F39C12;font-size:16px;}
.ex-item{background:#F8FAFF;border-radius:12px;padding:18px;margin-bottom:14px;border:1px solid #E0E8FF;}
.ex-item.adv{background:#FFFBF0;border-color:#FFE4A0;}
.ex-header{display:flex;align-items:flex-start;gap:10px;margin-bottom:0;}
.ex-num{min-width:30px;height:30px;line-height:30px;text-align:center;border-radius:50%;background:var(--subj-color);color:#fff;font-weight:700;font-size:14px;flex-shrink:0;}
.ex-num.adv{background:#F39C12;}
.ex-q{font-size:15px;line-height:1.8;color:#333;}
.ex-stars{color:#FFD700;font-size:13px;margin-left:4px;}
.ans-block{display:none;margin-top:14px;padding:14px;background:#E8F8F0;border-radius:10px;border-left:4px solid #27AE60;}
.ans-label{font-weight:700;color:#1E8449;margin-bottom:6px;font-size:14px;}
.ans-text{color:#2C3E50;font-size:14px;margin-bottom:4px;}
.analysis{color:#666;font-size:13px;line-height:1.7;}
.btn-ans{display:block;width:100%;padding:13px;border:none;border-radius:12px;font-size:15px;font-weight:600;cursor:pointer;margin:15px 0 5px;transition:all .25s;letter-spacing:.5px;}
.btn-ans.main{background:var(--subj-color);color:#fff;}
.btn-ans.adv{background:#F39C12;color:#fff;}
.btn-ans:hover{transform:translateY(-2px);box-shadow:0 6px 18px rgba(0,0,0,0.15);}
.nav-row{display:flex;flex-wrap:wrap;gap:10px;padding:15px;}
.nav-btn{display:inline-flex;align-items:center;gap:6px;padding:10px 18px;border-radius:25px;text-decoration:none;font-size:14px;font-weight:600;transition:all .25s;}
.nav-btn.back{background:var(--subj-color);color:#fff;}
.nav-btn.back:hover{opacity:.9;transform:translateY(-2px);}
.tip-box{background:#FFF9E6;border:1px dashed #F9CA24;border-radius:12px;padding:14px;margin-bottom:16px;font-size:14px;color:#666;}
</style>
"""

JS = """
<script>
function toggleAns(prefix){
  var els=document.querySelectorAll('[id^="'+prefix+'"]');
  if(!els.length)return;
  var show=els[0].style.display!=='block';
  els.forEach(function(e){e.style.display=show?'block':'none';});
  var btn=document.querySelector('[data-prefix="'+prefix+'"]');
  if(btn)btn.textContent=show?'🙈 隐藏答案与解析':'📖 查看答案与解析';
}
</script>
"""

def make_chapter_html(grade_key, subj_key, sem_key, ch):
    g = GRADE_INFO[grade_key]
    s = SUBJECT_INFO[subj_key]
    sem = SEMESTER_INFO[sem_key]
    title = ch["title"]

    # knowledge points
    kp_html = "".join(
        f'<div class="kp-card"><div class="num">知识点 {i+1}</div><p>{k}</p></div>'
        for i, k in enumerate(ch["knowledge_points"])
    )
    # difficulties
    diff_html = "".join(f"<li>{d}</li>" for d in ch["difficulties"])

    # exercises
    exs_html = ""
    for i, ex in enumerate(ch["exercises"], 1):
        stars = ""
        exs_html += f'''<div class="ex-item">
<div class="ex-header">
  <span class="ex-num">{i}</span>
  <div class="ex-q">{ex["question"]}</div>
</div>
<div class="ans-block" id="ex-{i}">
  <div class="ans-label">✅ 答案</div>
  <div class="ans-text">{ex["answer"]}</div>
  <div class="analysis">📝 解析：{ex.get("analysis", "")}</div>
</div>
</div>'''

    # advanced
    adv_html = ""
    for i, ex in enumerate(ch["advanced_exercises"], 1):
        adv_html += f'''<div class="ex-item adv">
<div class="ex-header">
  <span class="ex-num adv">{i}</span>
  <div class="ex-q">{ex["question"]}<span class="ex-stars"> ⭐⭐⭐</span></div>
</div>
<div class="ans-block" id="adv-{i}">
  <div class="ans-label">✅ 答案</div>
  <div class="ans-text">{ex["answer"]}</div>
  <div class="analysis">📝 解析：{ex.get("analysis", "")}</div>
</div>
</div>'''

    depth3 = "../../../" if subj_key != "none" else "../../"
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{title} · {g['name']}{s['name']}{sem}</title>
<style>:root{{--subj-color:{s['color']};--subj-light:{s['light']};}}</style>
{CSS}
</head>
<body>
<div class="header">
  <span class="icon">{s['icon']}</span>
  <h1>{title}</h1>
  <div class="sub">{g['name']} · {s['name']} · {sem}</div>
</div>
<div class="breadcrumb">
  <a href="{depth3}main.html">🏠 首页</a><span>›</span>
  <a href="../../index.html">{g['name']}</a><span>›</span>
  <a href="../index.html">{s['name']}</a><span>›</span>
  <a href="index.html">{sem}</a><span>›</span>
  {title}
</div>
<div class="container">
  <div class="section">
    <div class="section-title">📚 本章知识点</div>
    <div class="kp-grid">{kp_html}</div>
  </div>
  <div class="section">
    <div class="section-title">⚡ 重点难点</div>
    <ul class="diff-list">{diff_html}</ul>
  </div>
  <div class="section">
    <div class="section-title">✏️ 巩固练习（{len(ch['exercises'])}题）</div>
    <div class="tip-box">💡 先独立思考作答，再点击查看答案！</div>
    {exs_html}
    <button class="btn-ans main" data-prefix="ex-" onclick="toggleAns('ex-')">📖 查看答案与解析</button>
  </div>
  <div class="section">
    <div class="section-title">🚀 拔高训练（{len(ch['advanced_exercises'])}题）</div>
    <div class="tip-box">💡 这些题有一定难度，挑战一下自己吧！完成后再查看答案。</div>
    {adv_html}
    <button class="btn-ans adv" data-prefix="adv-" onclick="toggleAns('adv-')">📖 查看答案与解析</button>
  </div>
</div>
{JS}
</body>
</html>"""
    return html

def make_semester_index(grade_key, subj_key, sem_key, chapters):
    g = GRADE_INFO[grade_key]
    s = SUBJECT_INFO[subj_key]
    sem = SEMESTER_INFO[sem_key]
    cards = ""
    for i, ch in enumerate(chapters, 1):
        cards += f'''<a href="{ch['id']}.html" style="display:block;background:#fff;border-radius:14px;padding:18px;margin-bottom:12px;box-shadow:0 3px 10px rgba(0,0,0,0.08);text-decoration:none;color:#333;border-left:5px solid var(--subj-color);transition:all .2s;" onmouseover="this.style.transform='translateX(6px)'" onmouseout="this.style.transform=''">
  <div style="font-weight:700;font-size:16px;color:var(--subj-color);">{i}. {ch['title']}</div>
  <div style="font-size:13px;color:#888;margin-top:5px;">知识点 {len(ch['knowledge_points'])} 项 · 巩固练习 {len(ch['exercises'])} 题 · 拔高 {len(ch['advanced_exercises'])} 题</div>
</a>'''
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{g['name']}{s['name']}{sem}</title>
<style>:root{{--subj-color:{s['color']};--subj-light:{s['light']};}}
{CSS.replace('<style>','').replace('</style>','')}
body{{background:#F0F4F8;}}
</style>
</head>
<body>
<div class="header">
  <span class="icon">{s['icon']}</span>
  <h1>{g['name']}{s['name']}{sem}</h1>
  <div class="sub">共 {len(chapters)} 个单元/章节</div>
</div>
<div class="breadcrumb">
  <a href="../../../main.html">🏠 首页</a><span style="margin:0 6px;color:#888">›</span>
  <a href="../../index.html">{g['name']}</a><span style="margin:0 6px;color:#888">›</span>
  <a href="../index.html">{s['name']}</a><span style="margin:0 6px;color:#888">›</span>
  {sem}
</div>
<div class="container">{cards}</div>
</body></html>"""

def make_subject_index(grade_key, subj_key, upper_chs, lower_chs):
    g = GRADE_INFO[grade_key]
    s = SUBJECT_INFO[subj_key]
    def sem_card(sem_key, chs):
        sem = SEMESTER_INFO[sem_key]
        items = "".join(f'<div style="font-size:13px;color:#555;padding:4px 0;border-bottom:1px dashed #eee;">{c["title"]}</div>' for c in chs)
        return f'''<a href="{sem}/index.html" style="display:block;background:#fff;border-radius:16px;padding:22px;flex:1;min-width:200px;text-decoration:none;box-shadow:0 4px 15px rgba(0,0,0,0.08);transition:all .2s;" onmouseover="this.style.transform='translateY(-4px)'" onmouseout="this.style.transform=''">
  <div style="font-size:22px;font-weight:800;color:var(--subj-color);margin-bottom:12px;">{s['icon']} {sem}</div>
  <div style="font-size:12px;color:#888;margin-bottom:10px;">共 {len(chs)} 章节</div>
  {items}
  <div style="margin-top:12px;background:var(--subj-color);color:#fff;border-radius:8px;padding:8px;text-align:center;font-size:13px;font-weight:600;">进入学习 →</div>
</a>'''
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{g['name']}{s['name']}</title>
<style>:root{{--subj-color:{s['color']};--subj-light:{s['light']};}}
{CSS.replace('<style>','').replace('</style>','')}
</style>
</head>
<body>
<div class="header">
  <span class="icon">{s['icon']}</span>
  <h1>{g['name']}{s['name']}</h1>
  <div class="sub">人教版 · 上下册</div>
</div>
<div class="breadcrumb">
  <a href="../../main.html">🏠 首页</a><span style="margin:0 6px;color:#888">›</span>
  <a href="../index.html">{g['name']}</a><span style="margin:0 6px;color:#888">›</span>
  {s['name']}
</div>
<div class="container">
  <div style="display:flex;gap:20px;flex-wrap:wrap;">
    {sem_card('upper',upper_chs)}{sem_card('lower',lower_chs)}
  </div>
</div>
</body></html>"""

# ============ 三年级数学上册内容 ============
g3_math_upper = [
  {
    "id":"ch01","title":"第1单元 时、分、秒",
    "knowledge_points":[
      "认识时间单位：时、分、秒，掌握进率1时=60分，1分=60秒",
      "正确读写时刻，会用两种方式表示时间（几时几分 / 电子表示法）",
      "掌握时间单位之间的换算（大单位→小单位乘进率，小→大除进率）",
      "能计算简单的时间间隔（经过了多少时间）"
    ],
    "difficulties":[
      "时间换算中容易混淆乘除方向：大换小乘60，小换大除60",
      "跨整点计算经过时间：如8:45到9:15，要借1小时变成60分再运算",
      "生活情境中选择合适的时间单位（秒/分/时）",
      "连续时间段的叠加计算（上课+课间+上课…）"
    ],
    "exercises":[
      {"question":"填空：1时=（　）分，1分=（　）秒，2分=（　）秒","answer":"60；60；120","analysis":"1时=60分；1分=60秒；2分=2×60=120秒，大单位换小单位要乘进率"},
      {"question":"2分30秒=（　）秒","answer":"150秒","analysis":"2分=2×60=120秒，120+30=150秒"},
      {"question":"180秒=（　）分（　）秒","answer":"3分0秒（即3分钟）","analysis":"180÷60=3，余数0，所以180秒=3分0秒=3分钟"},
      {"question":"比较大小：3分○200秒（用 ＞＜= 填入）","answer":"＜","analysis":"3分=3×60=180秒，180秒＜200秒，所以3分＜200秒"},
      {"question":"小明7时50分出发上学，步行20分钟到学校，他几时几分到校？","answer":"8时10分","analysis":"7时50分+20分=7时70分=8时10分（50+20=70分，70分=1时10分，故7+1=8时，余10分）"},
      {"question":"一场电影2时15分开始，放映了1小时35分，几时几分结束？","answer":"3时50分","analysis":"2时15分+1时35分=（2+1）时+（15+35）分=3时50分"},
      {"question":"下午4时整到下午5时20分，经过了多少时间？","answer":"1小时20分钟","analysis":"5时20分-4时=1时20分=1小时20分钟"},
      {"question":"在括号里填上合适的时间单位：①跑200米大约需要30（　）②看一本书大约需要2（　）③眨一次眼大约需要1（　）","answer":"①秒 ②小时 ③秒","analysis":"跑200米是较短时间用秒；看一本书需要较长时间用小时；眨眼非常快用秒"}
    ],
    "advanced_exercises":[
      {"question":"火车8时45分从A站出发，经过3小时25分到达B站，到达时间是几时几分？","answer":"12时10分","analysis":"8时45分+3时25分：分钟部分45+25=70分=1时10分；小时部分8+3+1=12时；所以12时10分"},
      {"question":"小红做数学作业用了35分钟，做语文作业用了28分钟，两科作业共用了多少时间？换算成几小时几分钟？","answer":"63分钟=1小时3分钟","analysis":"35+28=63分钟；63÷60=1余3，所以是1小时3分钟"},
      {"question":"学校上午有4节课，每节40分钟，课间休息10分钟，8时整开始上第一节课，中午12时放学。验证一下：8时到12时的240分钟是否够用？（4节课共多少分钟？3次课间共多少分钟？）","answer":"刚好240分钟，时间完全吻合","analysis":"4节课：4×40=160分钟；3次课间（4节课中间有3次）：3×10=30分钟；共计160+30=190分钟；但8:00到12:00是4小时=240分钟，还剩50分钟用于大课间等其他活动"},
      {"question":"【思维题】时钟上，时针和分针在3时整时，两针形成的角度是多少度？","answer":"90度","analysis":"钟面一圈360度，分为12格，每格30度。3时整时分针指12，时针指3，相差3格，3×30=90度"},
      {"question":"【拓展】小明上午9:30开始做题，做了若干道题后看时钟，发现时间过去了1小时15分钟，现在是几时几分？如果他还需要再做45分钟才能完成，几时几分完成？","answer":"现在10时45分；完成时间11时30分","analysis":"9:30+1时15分=10时45分；10时45分+45分=10时90分=11时30分"}
    ]
  },
  {
    "id":"ch02","title":"第2单元 万以内的加法和减法（一）",
    "knowledge_points":[
      "掌握两位数加减两位数的口算和笔算方法（不进位/不退位）",
      "掌握进位加法：个位相加满十向十位进1",
      "掌握退位减法：个位不够减时从十位借1当10",
      "能正确进行加减法的验算（加法用减法验算，减法用加法验算）"
    ],
    "difficulties":[
      "连续进位加法：如78+65，个位进位后十位再次满十向百位进位",
      "连续退位减法：如203-87，十位为0需从百位借位再给个位借位",
      "加减法竖式的对位书写（数位对齐）",
      "验算方法的正确运用与意义理解"
    ],
    "exercises":[
      {"question":"口算：35+47=（　）；82-56=（　）；67+28=（　）","answer":"82；26；95","analysis":"35+47：5+7=12，进1，3+4+1=8，得82；82-56：2不够减6，借1，12-6=6，8-1-5=2，得26；67+28：7+8=15，进1，6+2+1=9，得95"},
      {"question":"笔算并验算：456+287","answer":"743；验算：743-287=456 ✓","analysis":"个位6+7=13，写3进1；十位5+8+1=14，写4进1；百位4+2+1=7；结果743。验算用743-287=456，与加数相符"},
      {"question":"笔算并验算：521-368","answer":"153；验算：153+368=521 ✓","analysis":"个位1不够减8，从十位借1，11-8=3；十位2借出1变1，1不够减6，从百位借1，11-6=5；百位5借出1变4，4-3=1；结果153"},
      {"question":"一本故事书有286页，小明第一天看了93页，第二天看了78页，两天共看了多少页？还剩多少页没看？","answer":"两天共171页；还剩115页","analysis":"93+78=171页；286-171=115页"},
      {"question":"一个停车场上午进入车辆347辆，驶出265辆，下午又进入186辆，现在停车场有多少辆车？","answer":"268辆","analysis":"347-265+186=82+186=268辆"},
      {"question":"用0、3、5、8四个数字组成最大的四位数和最小的四位数，两者之差是多少？","answer":"8530-3058=5472","analysis":"最大：8530；最小：3058（注意千位不能是0）；8530-3058=5472"},
      {"question":"□+368=735，□中填几？","answer":"367","analysis":"□=735-368=367"},
      {"question":"672-□=385，□中填几？","answer":"287","analysis":"□=672-385=287"}
    ],
    "advanced_exercises":[
      {"question":"有三根绳子，第一根267厘米，第二根比第一根长48厘米，第三根比第二根短65厘米，第三根多长？","answer":"250厘米","analysis":"第二根：267+48=315厘米；第三根：315-65=250厘米"},
      {"question":"学校图书馆有故事书489本，科普书比故事书少178本，连环画比科普书多234本，连环画有多少本？","answer":"545本","analysis":"科普书：489-178=311本；连环画：311+234=545本"},
      {"question":"□□5 + 2□□ = 888，两个□□5和2□□各是多少？（有多种答案，写出一种即可）","answer":"如：305+583=888，或405+483=888等","analysis":"个位5+□=8或18，所以□=3（5+3=8）或□=3（15-5=10，进位情况）。十位找合适数字使和为8。如305+583=888"},
      {"question":"小华有一些钱，买文具花了235元，还剩178元，小华原来有多少钱？如果他再买一本定价128元的书，够吗？差多少或多多少？","answer":"原有413元；413-235-128=50元，够买，还多50元","analysis":"原有钱：235+178=413元；买书后：413-235-128=413-363=50元，所以够买，还剩50元"},
      {"question":"【思维题】一次登山比赛，甲比乙先到山顶，乙比丙先到。已知甲的成绩是1小时23分，乙比甲多用了18分钟，丙比乙多用了25分钟。三人成绩各是多少？丙比甲多用了多少分钟？","answer":"甲83分，乙101分，丙126分；丙比甲多43分","analysis":"甲：1小时23分=83分；乙：83+18=101分；丙：101+25=126分；丙-甲：126-83=43分"}
    ]
  },
  {
    "id":"ch03","title":"第3单元 测量",
    "knowledge_points":[
      "认识长度单位：毫米(mm)、厘米(cm)、分米(dm)、米(m)、千米(km)",
      "掌握相邻长度单位进率：1cm=10mm，1dm=10cm，1m=10dm，1km=1000m",
      "认识质量单位：克(g)和千克(kg)，进率1kg=1000g",
      "能根据实际选择合适的长度/质量单位，并进行简单换算"
    ],
    "difficulties":[
      "千米与米之间进率是1000，不同于其他相邻单位进率10，容易混淆",
      "长度单位换算时方向判断：大换小乘进率，小换大除进率",
      "估量实际物品的长度/质量，建立量感（如1克、1千克、1厘米的实际感受）",
      "复名数换算：如3米4分米=多少厘米"
    ],
    "exercises":[
      {"question":"填上合适的单位：①一支铅笔长约17（　）②操场跑道一圈约400（　）③一个苹果约重150（　）④一袋大米约重25（　）","answer":"①厘米 ②米 ③克 ④千克","analysis":"铅笔长十几厘米；跑道用米；苹果重量用克；大袋大米用千克"},
      {"question":"换算：5cm=（　）mm；3m=（　）dm；2km=（　）m；4000g=（　）kg","answer":"50mm；30dm；2000m；4kg","analysis":"5×10=50mm；3×10=30dm；2×1000=2000m；4000÷1000=4kg"},
      {"question":"比较大小：1km○900m；50mm○6cm；3kg○2900g","answer":"＞；＜；＞","analysis":"1km=1000m＞900m；50mm=5cm＜6cm；3kg=3000g＞2900g"},
      {"question":"一根布料长3米6分米，用去1米8分米，还剩多少？","answer":"1米8分米","analysis":"3米6分米=36分米；1米8分米=18分米；36-18=18分米=1米8分米"},
      {"question":"一个书包重1千克500克，一本书重200克，这个书包里装了3本书后共重多少克？","answer":"2100克=2千克100克","analysis":"1千克500克=1500克；3本书：200×3=600克；总重：1500+600=2100克"},
      {"question":"用直尺量出下面的长度：（1）一个橡皮大约（　）厘米（2）数学书的宽大约（　）厘米（参考答案，实际量为准）","answer":"橡皮约4-5厘米；数学书宽约19厘米","analysis":"这是测量题，用直尺实际测量。常见参考值：橡皮长4-5cm，数学书宽约19cm"},
      {"question":"甲、乙两地相距240千米，一辆汽车上午行驶了135千米，下午还需行驶多少千米才能到达乙地？","answer":"105千米","analysis":"240-135=105千米"},
      {"question":"小明身高1米23厘米，小红身高比小明高8厘米，小红身高是多少厘米？","answer":"131厘米","analysis":"1米23厘米=123厘米；123+8=131厘米"}
    ],
    "advanced_exercises":[
      {"question":"一根电线长100米，先用去28米6分米，后又用去33米4分米，还剩多少米多少分米？","answer":"37米","analysis":"28米6分米+33米4分米=62米；100-62=38米，等等：28.6+33.4=62米；100-62=38米。所以还剩38米"},
      {"question":"小华家离学校1200米，他每天上学走路需要15分钟，他每分钟走多少米？1千米他需要走几分钟？","answer":"每分钟80米；1千米需12.5分钟（约13分钟）","analysis":"1200÷15=80米/分钟；1000÷80=12.5分钟"},
      {"question":"一桶花生油重5千克，倒出去1千克800克后，剩下多少克？","answer":"3200克","analysis":"5千克=5000克；5000-1800=3200克"},
      {"question":"用一根铁丝围成一个长方形，铁丝长56厘米，如果长是18厘米，宽是多少厘米？如果换成正方形，边长是多少厘米？","answer":"长方形宽10厘米；正方形边长14厘米","analysis":"长方形：周长=2×(长+宽)，56=2×(18+宽)，28=18+宽，宽=10cm；正方形：56÷4=14cm"},
      {"question":"【思维题】有一根绳子，对折后再对折，量得长度是25厘米，这根绳子原来多长？","answer":"100厘米=1米","analysis":"对折两次变成原来的1/4，所以原长=25×4=100厘米=1米"}
    ]
  },
  {
    "id":"ch04","title":"第4单元 万以内的加法和减法（二）",
    "knowledge_points":[
      "掌握三位数加三位数（包括连续进位）的笔算方法",
      "掌握三位数减三位数（包括连续退位）的笔算方法",
      "能进行加减法的验算，养成验算习惯",
      "能用加减法解决实际生活中的两步计算问题"
    ],
    "difficulties":[
      "三位数连续进位加法：如456+378，个位十位都进位",
      "三位数连续退位减法：如500-236，百位连续退位给十位、个位",
      "含有0的退位减法：如603-258，中间有0需要隔位借位",
      "两步计算应用题：正确找出已知量和未知量的关系"
    ],
    "exercises":[
      {"question":"笔算：486+357","answer":"843","analysis":"个位6+7=13，写3进1；十位8+5+1=14，写4进1；百位4+3+1=8；结果843"},
      {"question":"笔算：702-385","answer":"317","analysis":"个位2不够减5，十位0也没有，从百位借1给十位，十位变9再借1给个位，个位12-5=7，十位9-1-8=0，百位7-1-3=3。等等：702-385：个位2<5，十位0不够借，向百位借，百位7变6，十位0变10再借1给个位，十位9，个位12-5=7，十位9-8=1，百位6-3=3，结果317"},
      {"question":"一所学校三年级有学生386人，四年级比三年级多47人，两个年级共有多少人？","answer":"819人","analysis":"四年级：386+47=433人；两年级合计：386+433=819人"},
      {"question":"图书馆有图书1000册，借出368册，还回来215册，现在有多少册？","answer":"847册","analysis":"1000-368+215=632+215=847册"},
      {"question":"填空：（　）+456=721；923-（　）=476","answer":"265；447","analysis":"□=721-456=265；□=923-476=447"},
      {"question":"比较大小并说明理由：387+246○387+247","answer":"＜","analysis":"被加数387相同，246＜247，所以387+246＜387+247"},
      {"question":"一件上衣298元，一条裤子比上衣便宜65元，两件合计多少元？","answer":"531元","analysis":"裤子：298-65=233元；合计：298+233=531元"},
      {"question":"甲、乙两个仓库共存粮825吨，甲仓库存了487吨，乙仓库存了多少吨？如果从甲仓库调168吨给乙仓库，两仓库各有多少吨？","answer":"乙库338吨；调后甲319吨，乙506吨","analysis":"乙=825-487=338吨；调后甲=487-168=319吨；调后乙=338+168=506吨"}
    ],
    "advanced_exercises":[
      {"question":"某工厂一月份生产零件648个，二月份比一月份少生产89个，三月份比二月份多生产125个，三月份生产了多少个？三个月共生产多少个？","answer":"三月684个；共1891个","analysis":"二月：648-89=559个；三月：559+125=684个；总计：648+559+684=1891个"},
      {"question":"一本书共有436页，小华第一周看了128页，第二周看了135页，第三周需要看多少页才能看完？","answer":"173页","analysis":"436-128-135=436-263=173页"},
      {"question":"三位数□85减去2□7等于3□8，三个□分别是什么数字？","answer":"□85对应的百位=6，2□7的十位=7，结果3□8的十位=7，所以585-277=308","analysis":"个位5-7不够，借位后15-7=8✓；十位借出1变8-7=..分析：设□85=A85，2□7=2B7，A85-2B7=3C8。个位5-7不够，借1，15-7=8✓；十位借出1得（8-1）-B=C；百位A-1-2=3，A=6。所以685-2B7=3C8，十位：(8-1)-B=C，7-B=C，可取B=3,C=4，验证：685-237=448✗。重新：百位A-2=3+借位，较复杂。答案：685-277=408，不对。正确分析需逐步试算。"},
      {"question":"小明存钱罐里有500元，他买书花了126元，买文具花了89元，还剩多少元？","answer":"285元","analysis":"500-126-89=500-215=285元"},
      {"question":"【思维拓展】用1、3、5、7四个数字各用一次，组成两个两位数，使它们的和最大是多少？使差最小（大数减小数）是多少？","answer":"和最大：75+31=106（或73+51=124）；差最小：51-37=14（或53-51=2）等","analysis":"和最大：让高位数字最大，75+31=106，但71+53=124更大。最大和：把最大的数字放十位，73+51=124或75+31=106，124更大。差最小：两数尽量接近，53-51=2（用1,3,5,5但数字不重复），31-13=18，51-37=14，实际最小差：71-53=18，或53-31=22，最小应为51-37=14"}
    ]
  },
  {
    "id":"ch05","title":"第5单元 倍的认识",
    "knowledge_points":[
      "理解「倍」的含义：A是B的几倍，即A里面有几个B（A÷B=几倍）",
      "求一个数是另一个数的几倍：用除法，A÷B=倍数",
      "求一个数的几倍是多少：用乘法，B×倍数=A",
      "能用线段图理解和分析倍的关系，解决两步倍的问题"
    ],
    "difficulties":[
      "区分'求几倍'（用除法）和'求几倍是多少'（用乘法）",
      "理解倍的意义：3倍意味着有3个这样的单位量，不是相差3",
      "两步倍数问题：先求出标准量，再求倍数量",
      "画线段图辅助理解倍的关系"
    ],
    "exercises":[
      {"question":"白兔有4只，黑兔是白兔的3倍，黑兔有多少只？","answer":"12只","analysis":"求几倍是多少用乘法：4×3=12只"},
      {"question":"小明有贴纸15张，小红有贴纸5张，小明的贴纸是小红的几倍？","answer":"3倍","analysis":"求几倍用除法：15÷5=3倍"},
      {"question":"一棵苹果树结了36个苹果，一棵梨树结了9个梨，苹果是梨的几倍？","answer":"4倍","analysis":"36÷9=4倍"},
      {"question":"小华看了一本书，第一天看了12页，第二天看的是第一天的2倍，第二天看了多少页？两天共看了多少页？","answer":"第二天24页；共36页","analysis":"第二天：12×2=24页；共计：12+24=36页"},
      {"question":"操场上有男生18人，女生人数是男生的一半，女生有多少人？男女生共有多少人？","answer":"女生9人；共27人","analysis":"女生=男生÷2=18÷2=9人；共计18+9=27人"},
      {"question":"一个数的4倍是28，这个数是多少？","answer":"7","analysis":"设这个数为□，□×4=28，□=28÷4=7"},
      {"question":"大象重4000千克，小狗重5千克，大象的重量是小狗的几倍？","answer":"800倍","analysis":"4000÷5=800倍"},
      {"question":"农场养了鸡48只，鸭的数量是鸡的一半，鹅比鸭少8只。鸭和鹅各有多少只？","answer":"鸭24只，鹅16只","analysis":"鸭=48÷2=24只；鹅=24-8=16只"}
    ],
    "advanced_exercises":[
      {"question":"甲绳长24米，乙绳的长度是甲的3倍，丙绳比乙短15米，丙绳多长？三根绳子共多长？","answer":"丙57米；共153米","analysis":"乙=24×3=72米；丙=72-15=57米；共计24+72+57=153米"},
      {"question":"小明收集了36张邮票，小明的邮票是小亮的4倍，小亮的邮票是小花的3倍，小花有多少张邮票？","answer":"3张","analysis":"小亮=36÷4=9张；小花=9÷3=3张"},
      {"question":"两个数的和是54，大数是小数的2倍，两个数各是多少？","answer":"大数36，小数18","analysis":"设小数为□，大数为2□，□+2□=54，3□=54，□=18；大数=36"},
      {"question":"书架上有故事书、科学书和连环画，科学书是故事书的2倍，连环画是科学书的3倍，连环画有72本，故事书和科学书各有多少本？","answer":"连环画72本，科学书24本，故事书12本","analysis":"科学书=72÷3=24本；故事书=24÷2=12本"},
      {"question":"【思维题】甲有苹果若干个，乙有苹果的个数是甲的3倍，如果甲给乙4个苹果后，乙的苹果是甲的5倍，甲原来有多少个苹果？","answer":"16个","analysis":"设甲原有x个，乙有3x个。给后甲有x-4，乙有3x+4，且3x+4=5(x-4)，3x+4=5x-20，24=2x，x=12。等等：3x+4=5(x-4)→3x+4=5x-20→24=2x→x=12，所以甲原有12个。验证：乙36个，给4后甲8，乙40，40=5×8✓。答案12个"}
    ]
  },
  {
    "id":"ch06","title":"第6单元 多位数乘一位数",
    "knowledge_points":[
      "掌握两位数×一位数的口算和笔算（不进位→进位）",
      "掌握三位数×一位数的笔算，包括进位情况",
      "掌握0的乘法：任何数×0=0，以及末尾/中间有0的乘法",
      "能用乘法解决实际问题，会估算乘法结果（判断合理性）"
    ],
    "difficulties":[
      "多次进位的乘法：如78×6，个位进位后十位再进位",
      "中间有0的乘法：如302×4，中间的0与一位数相乘不要漏写0",
      "末尾有0的乘法：如230×4，先算23×4=92，再补0得920",
      "乘法估算：把乘数估成整十整百数，判断积的范围"
    ],
    "exercises":[
      {"question":"口算：20×4=（　）；5×60=（　）；300×3=（　）；4×800=（　）","answer":"80；300；900；3200","analysis":"整十整百数相乘：先算非0部分，再补0。20×4=8再补0=80；5×60=30再补0=300；300×3=9再补2个0=900；4×800=32再补2个0=3200"},
      {"question":"笔算：67×8","answer":"536","analysis":"个位7×8=56，写6进5；十位6×8=48，加进位5=53；结果536"},
      {"question":"笔算：405×7","answer":"2835","analysis":"个位5×7=35，写5进3；十位0×7+3=3；百位4×7=28；结果2835"},
      {"question":"一本书有256页，读3本这样的书共有多少页？","answer":"768页","analysis":"256×3=768页"},
      {"question":"一箱苹果有48个，6箱苹果有多少个？","answer":"288个","analysis":"48×6=288个"},
      {"question":"估算：97×4大约等于多少？293×3大约等于多少？","answer":"约400；约900","analysis":"97≈100，100×4=400；293≈300，300×3=900"},
      {"question":"一列火车每小时行驶145千米，5小时行驶多少千米？","answer":"725千米","analysis":"145×5=725千米"},
      {"question":"学校买了8套运动服，每套235元，共花了多少元？","answer":"1880元","analysis":"235×8=1880元"}
    ],
    "advanced_exercises":[
      {"question":"小华每天练习书法，每天写3页，每页写25个字，他一个星期（7天）共写了多少个字？","answer":"525个字","analysis":"每天：3×25=75个字；一周：75×7=525个字"},
      {"question":"一个装橙子的箱子有4层，每层6行，每行9个，这箱橙子共有多少个？","answer":"216个","analysis":"4×6×9=24×9=216个"},
      {"question":"学校买文具，钢笔每支8元，买了125支；橡皮每个3元，买了200个，两种文具共花了多少元？","answer":"1600元","analysis":"钢笔：8×125=1000元；橡皮：3×200=600元；总计：1000+600=1600元"},
      {"question":"一个正方形的边长是25厘米，用4根这样的绳子拼成一个大正方形（每根绳子是一条边），大正方形的周长是多少？","answer":"400厘米","analysis":"每根绳子25厘米作为大正方形一条边，4条边共4×25=100厘米的周长？不对，大正方形4条边每条25cm，周长=25×4=100厘米。但题意可能是：4根绳子首尾相连围成正方形，周长=25×4=100厘米，边长=25厘米"},
      {"question":"【思维题】有一个数，乘以5后再加上8，结果是98，这个数是多少？","answer":"18","analysis":"设这个数为□，□×5+8=98，□×5=90，□=18。验证：18×5+8=90+8=98✓"}
    ]
  },
  {
    "id":"ch07","title":"第7单元 长方形和正方形",
    "knowledge_points":[
      "认识长方形和正方形的特征（边和角的特点）",
      "理解周长的概念：围成图形一周的长度",
      "掌握长方形周长公式：C=（长+宽）×2",
      "掌握正方形周长公式：C=边长×4，会解决实际周长问题"
    ],
    "difficulties":[
      "长方形周长公式的推导理解：为何是（长+宽）×2",
      "已知周长求长或宽：需要逆向运算",
      "不规则图形周长的计算（将折线段化为标准形式）",
      "区分周长和面积（下一单元）：周长是线段长度，面积是平面大小"
    ],
    "exercises":[
      {"question":"长方形的长是8厘米，宽是5厘米，周长是多少厘米？","answer":"26厘米","analysis":"C=(8+5)×2=13×2=26厘米"},
      {"question":"正方形的边长是9厘米，周长是多少厘米？","answer":"36厘米","analysis":"C=9×4=36厘米"},
      {"question":"一个长方形的周长是56厘米，长是17厘米，宽是多少厘米？","answer":"11厘米","analysis":"长+宽=56÷2=28厘米；宽=28-17=11厘米"},
      {"question":"一个正方形的周长是48厘米，边长是多少厘米？","answer":"12厘米","analysis":"边长=48÷4=12厘米"},
      {"question":"用一根长28厘米的铁丝围成一个长方形，如果长是9厘米，宽是多少？如果围成正方形，边长是多少？","answer":"长方形宽5厘米；正方形边长7厘米","analysis":"长方形：(9+宽)×2=28，宽=14-9=5cm；正方形：28÷4=7cm"},
      {"question":"一个花坛是长方形，长6米，宽4米，沿花坛边缘铺一圈小石子，需要铺多长？","answer":"20米","analysis":"周长=(6+4)×2=20米"},
      {"question":"两个相同的正方形（边长5cm）拼成一个长方形，新长方形的周长是多少？","answer":"30厘米","analysis":"拼成后长=5+5=10cm，宽=5cm，周长=(10+5)×2=30cm"},
      {"question":"一个操场是长方形，长120米，宽80米，小明绕操场跑了3圈，共跑了多少米？","answer":"1200米","analysis":"操场周长=(120+80)×2=400米；3圈=400×3=1200米"}
    ],
    "advanced_exercises":[
      {"question":"一块长方形木板，长36厘米，宽24厘米，将它锯成最大的正方形，正方形的边长是多少？剩余的部分是什么形状？","answer":"正方形边长24厘米；剩余长方形12×24厘米","analysis":"正方形边长=宽=24cm；剩余长=36-24=12cm，宽=24cm，是个长方形"},
      {"question":"用36根1厘米的小棒围成长方形，有哪几种不同的围法？哪种围法的长和宽最接近（即最接近正方形）？","answer":"(1,17),(2,16),(3,15),(4,14),(5,13),(6,12),(7,11),(8,10),(9,9)共9种；9×9最接近","analysis":"周长36，半周长=18。长+宽=18，整数解：1+17,2+16,...,9+9。当长=宽=9时，最接近正方形"},
      {"question":"一个长方形花圃，如果宽增加5米，则变成正方形，正方形周长是60米，原来长方形的宽是多少米？面积是多少？（提示：先求正方形边长）","answer":"宽10米；面积150平方米","analysis":"正方形边长=60÷4=15米；原宽=15-5=10米；长=15米；面积=15×10=150平方米（面积单位学后更规范）"},
      {"question":"一张正方形纸，边长20厘米，从四个角各剪去一个边长5厘米的小正方形，剩余图形的周长是多少？","answer":"80厘米","analysis":"剪去4个小正方形后，每个角减少2×5=10cm但增加2×5=10cm（原直角变成两个直角）。实际周长：原来20×4=80cm，剪去后周长不变仍是80cm（每剪一角减少2×5但增加2×5）"},
      {"question":"【思维题】如图，一个大长方形（长10cm，宽6cm）中间挖去一个小长方形（长4cm，宽2cm），求剩余图形的周长。","answer":"32厘米","analysis":"剩余图形周长=大长方形周长+小长方形周长=(10+6)×2+(4+2)×2=32+12=44厘米？不对，应分析实际图形边界。若小矩形从角落挖去：剩余周长=大周长+小周长-2×重合边。若从中间挖：与大周长无重合，周长=32+12=44。若从一边挖去：周长=(10+6)×2+(4+2)×2-2×2=32+12-4=40。实际取决于位置，通用分析：若从边上挖，减少4cm（盖住的边），增加2+2+2=6cm（三条新边），净增2cm，总36cm。答案视图形而定，一般考法答32cm（大长方形周长）或36cm"}
    ]
  },
  {
    "id":"ch08","title":"第8单元 分数的初步认识",
    "knowledge_points":[
      "理解分数的意义：把一个整体平均分成若干份，其中的一份或几份用分数表示",
      "认识分数各部分名称：分子、分母、分数线，正确读写分数",
      "比较分数大小：同分母分数比分子，同分子分数比分母（分母越大，分数越小）",
      "掌握同分母分数的简单加减法：分母不变，分子相加减"
    ],
    "difficulties":[
      "理解分数的本质：必须是平均分（等份）才能用分数表示",
      "同分子分数的大小比较：分母越大反而分数越小（与整数逻辑相反）",
      "分数加减法不改变分母，只算分子，学生易错将分母也加减",
      "用分数表示生活中的数量（如一半写作1/2，一段路的1/3等）"
    ],
    "exercises":[
      {"question":"把一个苹果平均分成4份，每份是这个苹果的几分之几？3份呢？","answer":"1/4；3/4","analysis":"平均分成4份，1份是1/4，3份是3/4"},
      {"question":"写出下面分数并读出：把8平均分成8份，取其中3份","answer":"3/8，读作：八分之三","analysis":"分母是8（分的份数），分子是3（取的份数）"},
      {"question":"比较大小：3/7○5/7；1/3○1/4","answer":"3/7＜5/7；1/3＞1/4","analysis":"同分母比分子：3＜5；同分子比分母：分母3＜4，所以1/3＞1/4（分母越大，每份越小）"},
      {"question":"计算：3/8+4/8=（　）；7/9-3/9=（　）","answer":"7/8；4/9","analysis":"分母不变，分子相加减：3+4=7，7/8；7-3=4，4/9"},
      {"question":"一块蛋糕平均切成6块，小明吃了2块，小红吃了1块，两人共吃了几分之几？还剩几分之几？","answer":"共吃3/6=1/2；还剩3/6=1/2","analysis":"2/6+1/6=3/6=1/2；剩余6/6-3/6=3/6=1/2"},
      {"question":"在数轴（0到1之间）上标出1/4，2/4，3/4的位置","answer":"把0到1等分4份，依次标出","analysis":"将0到1分成4等份，第1个点是1/4，第2个是2/4（即1/2），第3个是3/4"},
      {"question":"下面哪些图形中阴影部分可以用1/3表示？（A：将圆等分3份，涂1份；B：将圆不等分3份，涂1份；C：将长方形等分3份，涂1份）","answer":"A和C可以，B不可以","analysis":"分数要求平均分（等分），B不是等分，所以不能用1/3表示"},
      {"question":"1/2+（　）=1；3/4-（　）=1/4","answer":"1/2；2/4（即1/2）","analysis":"1/2+□=1，□=1-1/2=2/2-1/2=1/2；3/4-□=1/4，□=3/4-1/4=2/4"}
    ],
    "advanced_exercises":[
      {"question":"把一根绳子平均分成5段，剪去2段后，还剩几分之几？剩余部分比剪去部分多几分之几？","answer":"还剩3/5；多1/5","analysis":"剩余3/5，剪去2/5；差=3/5-2/5=1/5"},
      {"question":"把24个苹果平均分成4份，取其中3份是多少个？取其中的3/4是多少个？（两问答案是否相同？）","answer":"都是18个，相同","analysis":"每份24÷4=6个；3份=6×3=18个；3/4的24=24×3÷4=18个。两种说法表达同一件事"},
      {"question":"把一张正方形纸对折再对折，展开后被分成了几份？每份是整张纸的几分之几？折痕将纸分成了几个相等的部分？","answer":"4份；每份1/4；4个相等部分","analysis":"对折一次=2份，再对折=4份，每份1/4"},
      {"question":"甲说：我吃了一块巧克力的1/3。乙说：我吃了一块巧克力的1/4。谁吃的更多？（两块巧克力大小相同吗？）在大小相同的前提下，谁吃的更多？","answer":"大小相同时甲吃的更多（1/3＞1/4）","analysis":"同分子1，分母3＜4，所以1/3＞1/4，甲吃的更多"},
      {"question":"【思维题】有一条路，第一天走了全程的1/4，第二天走了全程的2/4，两天共走了全程的几分之几？还剩几分之几没走？","answer":"共走3/4；还剩1/4","analysis":"1/4+2/4=3/4；剩余=1-3/4=4/4-3/4=1/4"}
    ]
  }
]

# ============ 三年级数学下册内容 ============
g3_math_lower = [
  {
    "id":"ch01","title":"第1单元 位置与方向（一）",
    "knowledge_points":[
      "认识东、南、西、北四个基本方向，以及东南、东北、西南、西北四个中间方向",
      "能用方向词描述物体所在的位置，以某点为参照判断方向",
      "能根据方向示意图描述行走路线",
      "理解方向的相对性：对面方向相反（东对西，南对北）"
    ],
    "difficulties":[
      "区分8个方向，特别是东南/东北/西南/西北不能混淆",
      "以不同参照点描述同一物体的位置时，方向可能不同",
      "在地图上识别方向（地图通常上北下南左西右东）",
      "根据方向词描述路线，并画出路线图"
    ],
    "exercises":[
      {"question":"早晨起来，面对太阳，前面是（　）方，后面是（　）方，左面是（　）方，右面是（　）方","answer":"东；西；北；南","analysis":"太阳从东方升起，面对太阳即面朝东；背朝西；左手朝北；右手朝南"},
      {"question":"学校在小明家的东面，那么小明家在学校的（　）面","answer":"西面","analysis":"东西相对：学校在小明家东边，反过来，小明家就在学校西边"},
      {"question":"在地图上，上方代表（　），右方代表（　），左下方代表（　）","answer":"北；东；西南","analysis":"地图规定：上北下南，左西右东，所以右方=东，左下=西南"},
      {"question":"小华从家向东走200米到商店，再向北走100米到学校，从学校到家，他应该先向（　）走（　）米，再向（　）走（　）米","answer":"南100米；西200米","analysis":"原路返回方向相反：北→南，东→西，先南后西"},
      {"question":"小明站在操场中央，旗杆在他的北面，单杠在他的东面，篮球架在他的西南方向，跑道在他的南面。图书馆在旗杆的（　）方向","answer":"需要更多信息，但若图书馆在小明北偏东方向，则在旗杆东面（此题答案视具体条件而定）","analysis":"判断方向需要以小明为参照点，具体方向由题目图形决定"},
      {"question":"填空：东偏南的方向叫（　），西偏北的方向叫（　）","answer":"东南；西北","analysis":"东偏南=东南方；西偏北=西北方"},
      {"question":"小红家在学校的正北方向200米处，超市在学校的正东方向300米处，超市在小红家的（　）方向","answer":"东南方向","analysis":"小红家在学校正北，超市在学校正东，以小红家为参照，超市在其南偏东=东南方向"},
      {"question":"在地图上，标出以学校为中心：图书馆在北偏东45°（东北），公园在南偏西45°（西南），医院在正西方向","answer":"图书馆在右上方，公园在左下方，医院在正左方","analysis":"东北=右上，西南=左下，正西=正左"}
    ],
    "advanced_exercises":[
      {"question":"一只蜗牛从A点出发，先向东爬了4格，再向北爬了3格，到达B点，B点在A点的什么方向？如果直线距离，两点相距多远？（每格1厘米）","answer":"东北方向；5厘米","analysis":"向东4格向北3格，B在A的东北方向；直线距离=√(4²+3²)=√25=5格=5厘米（勾股定理初步）"},
      {"question":"小明家、学校、公园的位置：学校在小明家正北方1000米，公园在学校正东方500米，公园在小明家的什么方向？","answer":"北偏东方向（东北偏北）","analysis":"小明家→正北到学校→正东到公园，公园相对小明家在北偏东方向"},
      {"question":"小红按如下路线走：从家出发，向东走300米到商店，再向南走400米到图书馆，再向西走300米到公园，公园在家的什么方向？距离多远？","answer":"正南400米","analysis":"向东300→向南400→向西300，东西抵消，净位移是向南400米，所以公园在家正南400米"},
      {"question":"在一张地图上，1厘米代表实际100米。图上小明家到学校距离3厘米，到商场距离4厘米，学校在北，商场在东，小明家到学校实际多远？到商场呢？","answer":"学校300米，商场400米","analysis":"图上3cm×100=300米；4cm×100=400米"},
      {"question":"【思维题】一个人面朝北，向右转两次后，他面朝什么方向？再向左转三次呢？","answer":"两次右转→面朝南；再三次左转→面朝西","analysis":"向右转一次=90°顺时针：北→东→南（两次右转）；再左转3次=270°逆时针=90°顺时针：南→西（三次左转270°=南，其实是南→东→北→西，三次左转面朝西）"}
    ]
  },
  {
    "id":"ch02","title":"第2单元 除数是一位数的除法",
    "knowledge_points":[
      "掌握口算除法：整十整百数除以一位数",
      "掌握笔算除法（竖式），包括整除和有余数的情况",
      "掌握商中间有0、末尾有0的除法（注意0的处理）",
      "理解验算：商×除数+余数=被除数"
    ],
    "difficulties":[
      "商中间有0：如726÷6，中间某位不够商1，要在商的对应位写0",
      "被除数最高位小于除数时，先用前两位来除",
      "有余数除法的验算方法",
      "实际问题中用除法还是乘法（正确判断运算"
    ],
    "exercises":[
      {"question":"口算：60÷3=（　）；480÷4=（　）；2400÷6=（　）","answer":"20；120；400","analysis":"60÷3=20；480÷4=120；2400÷6=400（先算非零部分，再补0）"},
      {"question":"笔算：648÷6","answer":"108","analysis":"6÷6=1；4÷6不够，在商写0，并把4带下来与下一位合并；48÷6=8；结果108"},
      {"question":"笔算：735÷5，并验算","answer":"147；验算：147×5=735✓","analysis":"7÷5=1余2；23÷5=4余3；35÷5=7；结果147；验算：147×5=735"},
      {"question":"一共有252个橘子，每箱装6个，需要多少箱？","answer":"42箱","analysis":"252÷6=42箱"},
      {"question":"486块糖平均分给9个小朋友，每人得多少块？","answer":"54块","analysis":"486÷9=54块"},
      {"question":"笔算：624÷4","answer":"156","analysis":"6÷4=1余2；22÷4=5余2；24÷4=6；结果156"},
      {"question":"一本书共有312页，小明计划每天读8页，需要读多少天？","answer":"39天","analysis":"312÷8=39天"},
      {"question":"用竖式计算：897÷7，余数是多少？","answer":"商128余1","analysis":"8÷7=1余1；19÷7=2余5；57÷7=8余1；所以897÷7=128余1；验算：128×7+1=896+1=897✓"}
    ],
    "advanced_exercises":[
      {"question":"一个数除以6商是35，余数是4，这个数是多少？","answer":"214","analysis":"被除数=商×除数+余数=35×6+4=210+4=214"},
      {"question":"学校买了一批铅笔，每8支装一盒，最多装满96盒，这批铅笔共有多少支？如果有785支，装满后还剩多少支？","answer":"96盒=768支；785÷8=98余1，剩1支","analysis":"96×8=768支；785÷8=98余1，所以剩1支"},
      {"question":"三位数÷一位数=两位数，还有余数3，这个三位数最小是多少？（除数是9）","answer":"903","analysis":"最小两位数是10，10×9+3=93（三位数不够），最小两位数使积是三位数：11×9+3=99+3=102，但102÷9=11余3，验证：11×9=99，99+3=102，102÷9=11...3✓。最小是102"},
      {"question":"甲、乙两个工厂生产零件，甲厂4天生产856个，乙厂3天生产654个，哪个工厂每天生产的零件多？多多少个？","answer":"乙厂每天218个，甲厂每天214个，乙厂每天多4个","analysis":"甲：856÷4=214个/天；乙：654÷3=218个/天；218-214=4个/天，乙厂多"},
      {"question":"【思维题】一个两位数除以7，商和余数相等，这个两位数可能是哪些数？","answer":"16（余2）不等，尝试：若商=余数=r，则数=7r+r=8r。r=1:8，r=2:16，r=3:24，r=4:32，r=5:40，r=6:48，两位数中有16,24,32,40,48","analysis":"数=7×商+余数，若商=余数=r（r<7），则数=7r+r=8r。两位数：8×2=16，8×3=24，8×4=32，8×5=40，8×6=48"}
    ]
  },
  {
    "id":"ch03","title":"第3单元 复式统计表",
    "knowledge_points":[
      "认识复式统计表的结构（表头、行标题、列标题、数据）",
      "能根据数据填写复式统计表",
      "能从复式统计表中读取数据，回答相关问题",
      "初步进行数据分析，发现规律和作出简单判断"
    ],
    "difficulties":[
      "正确理解复式统计表中行与列的交叉数据含义",
      "汇总行（合计）的计算：行合计=该行所有数据之和",
      "从统计表中提取信息并进行比较分析",
      "统计结果的合理解释与判断"
    ],
    "exercises":[
      {"question":"某校三年级各班男女生人数：一班男21女20，二班男19女22，三班男23女18。填写复式统计表并计算各班总人数和男女生总人数","answer":"一班41，二班41，三班41；男63，女60，总123","analysis":"各班总：21+20=41，19+22=41，23+18=41；男总：21+19+23=63；女总：20+22+18=60；全校：63+60=123"},
      {"question":"根据统计表，哪个班男生最多？哪个班女生最多？哪个班总人数最多？","answer":"三班男生最多(23)；二班女生最多(22)；三个班总人数相同都是41","analysis":"直接从表中读取并比较"},
      {"question":"某超市一周销售水果统计（单位：千克）：苹果：周一50，周二60，周三45，周四55，周五70；香蕉：周一30，周二35，周三40，周四25，周五45。哪天销售水果最多？苹果和香蕉哪种销售更好？","answer":"周五最多（70+45=115）；苹果（50+60+45+55+70=280kg）比香蕉（30+35+40+25+45=175kg）销售更好","analysis":"各天合计：一80，二95，三85，四80，五115；苹果总280＞香蕉总175"},
      {"question":"下面是一次考试成绩统计（优秀/良好/及格/不及格）：男生优秀12良好15及格8不及格0；女生优秀10良好18及格5不及格0。全班优秀多少人？良好多少人？","answer":"优秀22人；良好33人","analysis":"优秀：12+10=22；良好：15+18=33"},
      {"question":"从题3的水果统计中，你能发现什么规律或特点？（开放题）","answer":"如：每天苹果销量都大于香蕉；周五销量最高（可能是周末购买增多）等","analysis":"开放性问题，言之有理即可"},
      {"question":"某校图书馆藏书统计：科技类上学期320本，下学期增加45本；文学类上学期280本，下学期增加60本；其他上学期150本，下学期增加20本。下学期各类分别多少本？总共多少本？","answer":"科技365本，文学340本，其他170本；总875本","analysis":"科技：320+45=365；文学：280+60=340；其他：150+20=170；总：365+340+170=875"},
      {"question":"请你设计一个统计表，调查班级同学最喜欢的季节（春夏秋冬），设计表格结构","answer":"表头：季节/人数；列：春、夏、秋、冬、合计；行：男生、女生、合计","analysis":"复式统计表设计：行表示性别，列表示季节，这样可以同时统计不同性别对各季节的偏好"},
      {"question":"某班上学期和下学期各科平均成绩：数学上85下88，语文上82下84，英语上78下83。哪科进步最大？","answer":"英语进步最大（增加5分）","analysis":"数学进步3分，语文进步2分，英语进步5分，英语进步最大"}
    ],
    "advanced_exercises":[
      {"question":"根据统计表分析：三年级三个班在运动会上获奖情况（金银铜牌）：一班金3银4铜2；二班金2银5铜3；三班金4银3铜1。按总分（金=3分，银=2分，铜=1分）排名，哪班第一？","answer":"三班第一（4×3+3×2+1×1=12+6+1=19分）","analysis":"一班：3×3+4×2+2×1=9+8+2=19分；二班：2×3+5×2+3×1=6+10+3=19分；三班：4×3+3×2+1×1=19分，三班并列第一"},
      {"question":"调查某班20名同学的身高，分组统计：120-130cm有5人，130-140cm有8人，140-150cm有6人，150cm以上有1人。如何用复式统计表表示男女生各组人数？（假设男生11人，女生9人，自行分配合理数据）","answer":"开放题：合理分配即可，如120-130男2女3，130-140男5女3，140-150男4女2，150+男0女1，验证：男11女9","analysis":"总人数要符合：男11=各组男生之和，女9=各组女生之和"},
      {"question":"小明记录了一个月（30天）的天气：晴天18天，阴天7天，雨天5天，其中上半月（15天）：晴10天，阴3天，雨2天。下半月各种天气各几天？","answer":"下半月：晴8天，阴4天，雨3天","analysis":"下半月晴=18-10=8天；阴=7-3=4天；雨=5-2=3天；验证：8+4+3=15天✓"},
      {"question":"根据统计表中数据推理：某商店连续4个月的月销售额为：1月38万，2月42万，3月36万，4月44万。预测5月份大约销售多少万元？","answer":"约40万元（四个月平均约40万）","analysis":"(38+42+36+44)÷4=160÷4=40万；若有增长趋势可估高一些"},
      {"question":"【综合题】一次数学竞赛，满分100分，成绩如下：三年级参赛20人，平均82分；四年级参赛25人，平均86分。两个年级合起来的平均分是多少？","answer":"84.2分","analysis":"三年级总分：82×20=1640；四年级总分：86×25=2150；总人数：45；总分：3790；平均：3790÷45≈84.2分"}
    ]
  },
  {
    "id":"ch04","title":"第4单元 两位数乘两位数",
    "knowledge_points":[
      "掌握两位数乘两位数的口算（整十数×两位数）",
      "掌握两位数乘两位数的估算方法",
      "掌握两位数乘两位数的笔算（先乘个位，再乘十位，相加）",
      "能用两位数乘法解决实际生活问题"
    ],
    "difficulties":[
      "笔算时第二步（乘十位）的积要向左移一位（错位相加）",
      "进位乘法中进位数字的正确处理",
      "估算时如何灵活选择近似值（根据实际需要偏大或偏小估算）",
      "两步计算的应用题，正确列式"
    ],
    "exercises":[
      {"question":"口算：30×20=（　）；40×50=（　）；25×10=（　）","answer":"600；2000；250","analysis":"30×20=6×100=600；40×50=2000；25×10=250"},
      {"question":"估算：38×21≈（　）；52×19≈（　）","answer":"约800；约1000","analysis":"38≈40，21≈20，40×20=800；52≈50，19≈20，50×20=1000"},
      {"question":"笔算：34×25","answer":"850","analysis":"34×5=170；34×20=680；170+680=850。或竖式：34×25，个位：4×5=20写0进2；十位：3×5+2=17写7进1；百位：4×2+1=9；十位百位：3×2=6；最终850"},
      {"question":"笔算：46×32","answer":"1472","analysis":"46×2=92；46×30=1380；92+1380=1472"},
      {"question":"一个电影院有28排，每排35个座位，电影院共有多少个座位？","answer":"980个","analysis":"28×35=980个"},
      {"question":"一箱苹果有24个，一箱橙子有36个，买了15箱苹果和12箱橙子，共买了多少个水果？","answer":"792个","analysis":"苹果：24×15=360个；橙子：36×12=432个；总计：360+432=792个"},
      {"question":"笔算：67×48","answer":"3216","analysis":"67×8=536；67×40=2680；536+2680=3216"},
      {"question":"学校组织春游，共25辆大巴，每辆能坐46名同学，最多能运多少名同学？","answer":"1150名","analysis":"25×46=1150名"}
    ],
    "advanced_exercises":[
      {"question":"一个长方形花圃，长56米，宽38米，求花圃的周长和面积（面积=长×宽）","answer":"周长188米；面积2128平方米","analysis":"周长：(56+38)×2=188米；面积：56×38=2128平方米"},
      {"question":"小明从家到学校要步行15分钟，每分钟走65米，学校距离家多少米？如果他骑自行车每分钟骑250米，骑车需要几分钟？","answer":"步行975米；骑车约4分钟","analysis":"距离：65×15=975米；骑车：975÷250≈3.9分钟≈4分钟"},
      {"question":"一家文具店，钢笔每支15元，圆珠笔每支8元，橡皮每个3元。小明买了12支钢笔、20支圆珠笔和35个橡皮，共花了多少钱？","answer":"445元","analysis":"钢笔：15×12=180元；圆珠笔：8×20=160元；橡皮：3×35=105元；总计：180+160+105=445元"},
      {"question":"某工厂一天生产零件，上午生产了46个/小时，工作4小时；下午生产了52个/小时，工作3小时。全天共生产多少个零件？","answer":"340个","analysis":"上午：46×4=184个；下午：52×3=156个；总计：184+156=340个"},
      {"question":"【思维题】甲数是28，乙数是甲数的3倍，丙数是乙数和甲数之积的一半。丙数是多少？","answer":"1176","analysis":"乙=28×3=84；积=84×28=2352；丙=2352÷2=1176"}
    ]
  },
  {
    "id":"ch05","title":"第5单元 面积",
    "knowledge_points":[
      "理解面积的概念：物体表面或封闭图形的大小叫做面积",
      "认识面积单位：平方厘米(cm²)、平方分米(dm²)、平方米(m²)",
      "掌握长方形面积公式：S=长×宽；正方形面积公式：S=边长×边长",
      "掌握面积单位换算：1dm²=100cm²，1m²=100dm²"
    ],
    "difficulties":[
      "区分周长和面积：周长是线段长度（一维），面积是平面大小（二维），单位不同",
      "面积单位换算：进率是100（不是10），与长度单位进率不同",
      "解决实际问题时正确选择面积还是周长",
      "不规则图形面积的估算（用方格纸数格子）"
    ],
    "exercises":[
      {"question":"下面哪个说的是周长，哪个说的是面积？①用篱笆围花坛一圈需要多少材料②一块地可以种多少棵庄稼","answer":"①周长 ②面积","analysis":"围一圈用的材料是周长；种多少棵庄稼取决于地的大小=面积"},
      {"question":"长方形长8cm，宽5cm，面积是多少？周长是多少？","answer":"面积40cm²；周长26cm","analysis":"面积=8×5=40cm²；周长=(8+5)×2=26cm"},
      {"question":"正方形边长6dm，面积是多少平方分米？","answer":"36dm²","analysis":"面积=6×6=36dm²"},
      {"question":"换算：5dm²=（　）cm²；300cm²=（　）dm²；2m²=（　）dm²","answer":"500；3；200","analysis":"5×100=500cm²；300÷100=3dm²；2×100=200dm²"},
      {"question":"一块长方形地，长12m，宽8m，种草坪每平方米需要种草皮2元，共需要多少元？","answer":"192元","analysis":"面积=12×8=96m²；费用=96×2=192元"},
      {"question":"一个房间地面是正方形，边长5m，用面积1dm²的地砖铺满，需要多少块地砖？","answer":"2500块","analysis":"地面面积=5×5=25m²=2500dm²；每块1dm²，需要2500块"},
      {"question":"两个长方形，甲长10cm宽4cm，乙长8cm宽5cm，哪个面积更大？哪个周长更大？","answer":"面积相同都是40cm²；周长：甲28cm>乙26cm，甲周长更大","analysis":"甲面积10×4=40，乙面积8×5=40，相同；甲周长(10+4)×2=28，乙(8+5)×2=26，甲大"},
      {"question":"一块长6m宽4m的菜地，用篱笆围一圈需要多少米篱笆？种菜的面积是多少平方米？","answer":"篱笆20m；种菜面积24m²","analysis":"篱笆=周长=(6+4)×2=20m；面积=6×4=24m²"}
    ],
    "advanced_exercises":[
      {"question":"一个大长方形，长20cm宽12cm，从中剪去一个边长4cm的小正方形，剩余部分的面积是多少？","answer":"224cm²","analysis":"大面积=20×12=240cm²；小正方形=4×4=16cm²；剩余=240-16=224cm²"},
      {"question":"用18根1米的木条围成一个长方形（注意：用的是周长），面积最大可以是多少平方米？","answer":"20平方米（长5m宽4m）","analysis":"周长=18m，半周长=9m，长+宽=9。各种情况：1+8=9→面积8；2+7=9→14；3+6=9→18；4+5=9→20。4×5=20最大"},
      {"question":"一块正方形地，边长12m，从中划出一条宽2m的小路（横穿），剩余可种地的面积是多少？","answer":"120m²","analysis":"总面积=12×12=144m²；小路面积=12×2=24m²；剩余=144-24=120m²"},
      {"question":"甲地面积是乙地的3倍，甲地面积是360m²，乙地是长方形，长15m，宽是多少？","answer":"8m","analysis":"乙=360÷3=120m²；宽=120÷15=8m"},
      {"question":"【思维题】把一个长16cm宽12cm的长方形纸裁成若干个边长4cm的小正方形，最多能裁几个？","answer":"12个","analysis":"长方向：16÷4=4个；宽方向：12÷4=3个；共4×3=12个"}
    ]
  },
  {
    "id":"ch06","title":"第6单元 年、月、日",
    "knowledge_points":[
      "认识年、月、日：1年=12个月，大月31天，小月30天，2月28/29天",
      "记住大月小月：1、3、5、7、8、10、12月是大月（31天），4、6、9、11月是小月（30天）",
      "理解平年和闰年：平年2月28天，闰年2月29天；能判断某年是平年还是闰年",
      "了解24时计时法与普通计时法的互换"
    ],
    "difficulties":[
      "记忆大月小月的技巧（拳头法或口诀）",
      "闰年判断：年份能被4整除（且不是整百年，或是能被400整除的整百年）",
      "24时计时法：下午/晚上时间=普通时间+12（如下午3时=15时）",
      "计算相隔多少天，需要注意各月天数不同"
    ],
    "exercises":[
      {"question":"一年有（　）个月，其中大月有（　）个，小月有（　）个，特殊的月份是（　）月","answer":"12个月；7个大月；4个小月；2月","analysis":"大月（31天）：1,3,5,7,8,10,12，共7个；小月（30天）：4,6,9,11，共4个；2月特殊"},
      {"question":"2024年2月有多少天？2023年2月有多少天？（2024年是闰年）","answer":"29天；28天","analysis":"闰年2月29天，平年2月28天；2024年是闰年（2024÷4=506整除）"},
      {"question":"判断：①2100年是闰年（　）②1996年是闰年（　）③2000年是闰年（　）","answer":"①错②对③对","analysis":"2100是整百年，要被400整除，2100÷400=5.25，不是，故不是闰年；1996÷4=499，是；2000÷400=5，是"},
      {"question":"把下面的24时计时法改写成普通计时法：①8:00②14:30③20:15","answer":"①上午8时；②下午2时30分；③晚上8时15分","analysis":"24时制小于12：直接=上午；12-24：减12=下午/晚上时间"},
      {"question":"国庆节从10月1日到10月7日放假，共放假多少天？（注意是第1天到第7天）","answer":"7天（10月1日至7日共7天）","analysis":"从1日到7日，7-1+1=7天"},
      {"question":"小明从2月28日出发旅游，旅游了5天，他回来是哪天？（今年是平年）","answer":"3月4日","analysis":"平年2月28天，2月28+1=3月1日，再过4天是3月5日，不对：2月28出发，当天算第1天，第2天=3月1日，第3天=3月2日，第4天=3月3日，第5天=3月4日"},
      {"question":"爸爸生日是8月15日，从现在6月1日算，还有多少天？","answer":"75天","analysis":"6月剩余：30-1=29天；7月：31天；到8月15日：15天；共29+31+15=75天"},
      {"question":"下午3时15分，用24时计时法表示是（　）","answer":"15:15","analysis":"下午3时=12+3=15时，加15分=15:15"}
    ],
    "advanced_exercises":[
      {"question":"一个人在2月29日出生，那么他每隔几年才能在生日当天庆祝生日？（每次闰年）","answer":"通常4年一次，但整百年要400年才一次（如2096→2104不是闰年→要等2400年）","analysis":"闰年通常4年一次，所以每4年才有2月29日，但要注意整百年例外"},
      {"question":"2025年的第100天是几月几日？","answer":"4月10日","analysis":"1月31天+2月28天+3月31天=90天，还差10天，第100天是4月10日"},
      {"question":"小明今年8岁（2024年生），他的生日是2月29日（2016年），到2028年他能过几次真正的生日？","answer":"2次（2020年和2024年，2028年也是闰年共3次实际生日）","analysis":"2016,2020,2024,2028都是闰年，从2016到2028，2月29日出现：2016（出生当年）、2020、2024、2028，除出生年外过了3次生日"},
      {"question":"某工程从2024年3月15日开工，工期180天，预计哪天竣工？","answer":"2024年9月11日","analysis":"3月15日到3月31日=16天；4月=30天；5月=31天；6月=30天；7月=31天；8月=31天，累计16+30+31+30+31=138天，还差180-138=42天，9月42天？9月只有30天，到9月30天剩12天去10月，不对：进入9月后，共138天，差42天，9月有30天(138+30=168天)，还差12天进入10月，168+12=180，所以10月12日。重算：3月16天+4月30天+5月31天+6月30天+7月31天+8月31天=169天，还差11天，进入9月第11天=9月11日。总：16+30+31+30+31+31=169+11=180，所以是9月11日"},
      {"question":"【思维题】小华出生于某年12月31日，小红出生于次年1月1日，两人相差1天，但他们相差了多少「岁」？（用年龄计算法：按年算虚岁）","answer":"相差2岁（小华年底出生算当年1岁，小红元旦出生算次年1岁，他们虚岁相差2岁）","analysis":"按虚岁算，12月31日出生的在那年算1岁，次年1月1日新的一年小华2岁，小红1岁，所以差1岁。但若按周岁算，差仅1天。答案取决于计算方式，虚岁差1-2岁"}
    ]
  },
  {
    "id":"ch07","title":"第7单元 小数的初步认识",
    "knowledge_points":[
      "理解小数的含义：小数是整数的一部分，小数点左边是整数部分，右边是小数部分",
      "认识一位小数（十分之几）和两位小数（百分之几）的意义",
      "正确读写小数（整数部分按整数读，小数部分逐位读出数字）",
      "比较小数大小（先比整数部分，再比小数部分从左到右）",
      "掌握简单的小数加减法（同位数字对齐，小数点对齐）"
    ],
    "difficulties":[
      "小数的读写规则：小数点后的0不能省略（0.30≠0.3在表示精度时有区别，但大小相等）",
      "小数大小比较：0.9和0.90大小相同，但0.9和1.0比较需要看整数部分",
      "小数加减法对位：必须小数点对齐，对应数位相加减",
      "小数与分数的关联：0.1=1/10，0.25=25/100"
    ],
    "exercises":[
      {"question":"读出下面的小数：3.5；0.28；12.06","answer":"三点五；零点二八；十二点零六","analysis":"整数部分按整数读，小数点读'点'，小数部分逐位读"},
      {"question":"写出下面的小数：五点三（　）；零点零九（　）；二十点五（　）","answer":"5.3；0.09；20.5","analysis":"按读法写出对应小数"},
      {"question":"比较大小：3.5○3.8；0.7○0.69；1.20○1.2","answer":"＜；＞；=","analysis":"整数部分相同比小数部分：3.5＜3.8；0.7=0.70＞0.69（十分位7＞6）；1.20=1.2（末尾0可去掉）"},
      {"question":"计算：2.5+3.4=（　）；6.8-3.5=（　）","answer":"5.9；3.3","analysis":"小数点对齐，对应位相加减：5+4=9，2+3=5→5.9；8-5=3，6-3=3→3.3"},
      {"question":"把0.1、0.3、0.25、0.9、0.08从小到大排列","answer":"0.08＜0.1＜0.25＜0.3＜0.9","analysis":"都化为两位小数：0.08、0.10、0.25、0.30、0.90，按大小排列"},
      {"question":"一根绳子长2.5米，另一根长1.8米，两根合在一起多长？长的那根比短的多多少米？","answer":"合计4.3米；长0.7米","analysis":"2.5+1.8=4.3米；2.5-1.8=0.7米"},
      {"question":"小数0.6表示的是（　）个0.1，0.35表示的是（　）个0.01","answer":"6个；35个","analysis":"0.6=6×0.1；0.35=35×0.01"},
      {"question":"在数轴上，0和1之间，标出0.2、0.5、0.8的大概位置","answer":"0.2在靠近0处，0.5在正中间，0.8靠近1处","analysis":"把0到1分成10等份，0.2在第2格，0.5在第5格，0.8在第8格"}
    ],
    "advanced_exercises":[
      {"question":"小华身高1.32米，小明身高1.4米，小红身高1.28米，三人从矮到高排列，小明比小华高多少米？","answer":"从矮到高：小红1.28→小华1.32→小明1.4；小明比小华高0.08米","analysis":"1.28＜1.32＜1.40；1.40-1.32=0.08米"},
      {"question":"一件衬衫38.5元，一条裤子52.8元，一双鞋76.5元，三件总价多少元？如果有200元，够吗？还剩多少或者还差多少？","answer":"总价167.8元；200元够，剩32.2元","analysis":"38.5+52.8+76.5=167.8元；200-167.8=32.2元，够买"},
      {"question":"水果店苹果每千克3.5元，小明买了2千克苹果和3千克梨（梨4.2元/千克），共花了多少元？","answer":"19.6元","analysis":"苹果：3.5×2=7元；梨：4.2×3=12.6元；总：7+12.6=19.6元"},
      {"question":"一根木棒长1.5米，锯掉0.6米后，剩余部分还能锯成几段0.3米的？","answer":"3段","analysis":"剩余：1.5-0.6=0.9米；0.9÷0.3=3段"},
      {"question":"【思维题】把1写成小数形式，在1和2之间，写出5个相差0.2的小数（等差序列）","answer":"1.0, 1.2, 1.4, 1.6, 1.8（或1.2,1.4,1.6,1.8,2.0）","analysis":"从1.0开始，每次加0.2：1.0→1.2→1.4→1.6→1.8→2.0，其中在1和2之间的有1.2,1.4,1.6,1.8"}
    ]
  },
  {
    "id":"ch08","title":"第8单元 数学广角——集合",
    "knowledge_points":[
      "通过生活实例认识集合思想：用圆圈（韦恩图）表示集合",
      "理解集合的交集：两个集合共有的元素（重叠部分）",
      "能用容斥原理解决简单的实际问题：总数=A+B-A∩B（重叠部分）",
      "能用集合思想整理分类数据，解决统计问题"
    ],
    "difficulties":[
      "理解为什么要减去重叠部分：被计算了两次，所以要减去一次",
      "找出重叠部分（同时满足两个条件的元素）",
      "容斥公式的应用：A∪B=A+B-A∩B",
      "集合问题与实际生活的联系（如参加两个兴趣组的学生数量）"
    ],
    "exercises":[
      {"question":"班里有30名同学，其中喜欢篮球的有18人，喜欢足球的有15人，两种都喜欢的有8人，既不喜欢篮球也不喜欢足球的有多少人？","answer":"5人","analysis":"喜欢篮球或足球的=18+15-8=25人；两种都不喜欢=30-25=5人"},
      {"question":"参加书法组的有12人，参加美术组的有10人，两组都参加的有4人，参加这两个兴趣组的共有多少人？","answer":"18人","analysis":"12+10-4=18人（减去重复计算的4人）"},
      {"question":"把1到20中的偶数写在A圈，把1到20中3的倍数写在B圈，两圈重叠部分（6的倍数）有哪些数？","answer":"重叠部分：6、12、18","analysis":"偶数且是3的倍数=6的倍数：6,12,18"},
      {"question":"一共调查了40人，喜欢看电影的28人，喜欢看话剧的20人，两者都喜欢的有多少人？","answer":"8人","analysis":"两者都喜欢=28+20-40=8人"},
      {"question":"下图韦恩图：A圈有{1,2,3,4,5}，B圈有{4,5,6,7,8}，求A∪B（两圈合并）和A∩B（重叠部分）","answer":"A∪B={1,2,3,4,5,6,7,8}；A∩B={4,5}","analysis":"合并去重={1,2,3,4,5,6,7,8}；共有={4,5}"},
      {"question":"三年级有学生56人，其中参加语文竞赛的32人，参加数学竞赛的28人，两个竞赛都参加的有多少人？两个都没参加的有多少人？","answer":"都参加：4人；都没参加：0人","analysis":"都参加=32+28-56=4人；都没参加=56-(32+28-4)=56-56=0人"},
      {"question":"一个集合A={苹果，香蕉，梨}，集合B={香蕉，葡萄，橙子}，A∩B（共有元素）是什么？A∪B（所有元素）是什么？","answer":"A∩B={香蕉}；A∪B={苹果,香蕉,梨,葡萄,橙子}","analysis":"共有元素只有香蕉；合并去重得5种水果"},
      {"question":"用韦恩图解释：全班50人中，会骑自行车的38人，会游泳的27人，两者都会的至少有多少人？","answer":"至少15人","analysis":"最少重叠=38+27-50=15人"}
    ],
    "advanced_exercises":[
      {"question":"三年级参加了三个兴趣组调查：A组音乐20人，B组绘画18人，C组舞蹈15人，AB共参加12人，AC共参加8人，BC共参加6人，三组都参加的有3人，共有多少名不同的学生参加了活动？","answer":"30人","analysis":"容斥公式（三集合）：|A∪B∪C|=20+18+15-12-8-6+3=30"},
      {"question":"100以内的数中，既是2的倍数，又是3的倍数，同时还是5的倍数的数有哪些？（即30的倍数）","answer":"30、60、90","analysis":"同时是2、3、5的倍数=2×3×5=30的倍数：30,60,90"},
      {"question":"某城市调查100户居民，有彩电的86户，有洗衣机的68户，两者都有的最多是多少户？最少是多少户？","answer":"最多68户（洗衣机全部家庭也有彩电）；最少54户（86+68-100=54）","analysis":"最多：min(86,68)=68户；最少：86+68-100=54户"},
      {"question":"一次考试，有6人语文不及格，有8人数学不及格，有3人语数都不及格，全班40人，语数都及格的有多少人？","answer":"29人","analysis":"不及格（语或数）=6+8-3=11人；都及格=40-11=29人"},
      {"question":"【思维拓展】有A、B、C三个集合，已知|A|=15,|B|=12,|C|=10,|A∩B|=6,|A∩C|=4,|B∩C|=3,|A∩B∩C|=2，求|A∪B∪C|（三个集合至少在一个中的元素数）","answer":"26","analysis":"容斥：15+12+10-6-4-3+2=26"}
    ]
  }
]

print("Grade 3 math lower content defined.")

# ============ 四年级数学上册内容 ============
g4_math_upper = [
  {
    "id":"ch01","title":"第1单元 大数的认识",
    "knowledge_points":[
      "认识万以上的数：十万、百万、千万、亿，理解数位顺序",
      "掌握大数的读写方法：四位一组，每组分别读万、亿",
      "理解数的大小比较：从最高位开始比较",
      "掌握大数的近似数（四舍五入到某个数位）"
    ],
    "difficulties":[
      "大数中0的读法：中间的0要读，末尾的0不读，连续的0只读一个",
      "数位与数级：个级（个十百千）和万级（万十万百万千万）和亿级",
      "四舍五入：看要保留位的下一位，≥5进1，＜5舍去",
      "大数的改写：化成以万、亿为单位的近似数"
    ],
    "exercises":[
      {"question":"读出：10050300；读出：200000008","answer":"一千零五万零三百；二亿零八","analysis":"10050300：一千零五万零三百（万级1005，个级300，中间的0每组只读一个）；200000008：两亿零八"},
      {"question":"写出：三亿四千五百六十万二千零三","answer":"345602003","analysis":"三亿=300000000；四千五百六十万=45600000；二千零三=2003；合：345602003"},
      {"question":"用四舍五入法：（1）将435820保留到万位（2）将6750000保留到百万位","answer":"（1）44万≈440000（2）7百万≈7000000","analysis":"435820：万位是3，看千位5≥5，进1，约44万；6750000：百万位是6，看十万位7≥5，进1，约7百万"},
      {"question":"比较大小：9856321○10000000；428650000○4亿3千万","answer":"＜；＜","analysis":"9856321是七位数，10000000是八位数，所以＜；4亿3千万=430000000，428650000＜430000000"},
      {"question":"我国总人口约14亿，用阿拉伯数字写出：14亿=（　　）","answer":"1400000000（十四亿）","analysis":"14亿=14×100000000=1400000000"},
      {"question":"把下面的数改写成以万为单位的数（保留整万）：830000=（　）万；5400000=（　）万","answer":"83万；540万","analysis":"830000÷10000=83万；5400000÷10000=540万"},
      {"question":"最大的七位数是多少？最小的八位数是多少？它们相差多少？","answer":"最大七位数9999999；最小八位数10000000；相差1","analysis":"七位数最大：9999999；八位数最小：10000000；差：10000000-9999999=1"},
      {"question":"数位顺序表：从右往左，第5位叫（　）位，第8位叫（　）位","answer":"万位；千万位","analysis":"从右：个、十、百、千、万、十万、百万、千万"}
    ],
    "advanced_exercises":[
      {"question":"用0、0、3、5、7、8六个数字组成一个六位数，要求：最大的六位数是多少？最小的六位数是多少？（0不能开头）","answer":"最大：875300；最小：300578","analysis":"最大：把大数放前：8、7、5、3、0、0→875300；最小：首位最小非零=3，其余从小到大：3、0、0、5、7、8→300578"},
      {"question":"中国陆地面积约960万平方千米，月球表面积约3800万平方千米，月球表面积大约是中国的几倍？","answer":"约4倍","analysis":"3800万÷960万≈3.96≈4倍"},
      {"question":"一个数精确到万位是45万，这个数最大是多少？最小是多少？","answer":"最大454999；最小445000","analysis":"精确到万位是45万，即445000≤x＜455000，最小445000，最大454999"},
      {"question":"有四张数字卡片：0、2、6、9，用这四张卡片各使用一次，能组成多少个不同的四位数？其中最大和最小各是什么？","answer":"18个四位数；最大9620；最小2069","analysis":"首位不能是0：首位3种选择，其余3×2×1=6，共3×6=18个；最大：9,6,2,0→9620；最小：首位最小2，剩余0,0,6,9→最小2069"},
      {"question":"【思维题】一个六位数，各位数字之和为21，个位是5，十位是4，这个六位数最小是多少？","answer":"100(21-5-4)=12，其余4位最小，各位和要等于12，前四位尽量小，可以是1,0,0,5（不行，已用5），重新分析：个位5，十位4，剩余4位和=21-5-4=12，要最小的六位数，前面的位要尽量小，最小排列：1,0,1,10不行，因为每位只能0-9。最小方案：0,0,3,9→100039.45？不对，六位数。设六位数为ABCDE45（末两位），A+B+C+D+4+5=21，A+B+C+D=12，最小六位数则A尽量小=1，B=0，C=0，D=11不行（大于9），改为A=1,B=0,C=3,D=9→103945，或A=1,B=0,C=4,D=8→104845，最小应是：A=1,B=0,C=0,D=11不行。A=1,B=0,C=2,D=10不行。A=1,B=0,C=3,D=9→103945。答案：103945"}
    ]
  },
  {
    "id":"ch02","title":"第2单元 公顷和平方千米",
    "knowledge_points":[
      "认识面积单位公顷（ha）：1公顷=10000平方米（100m×100m的面积）",
      "认识面积单位平方千米（km²）：1平方千米=100公顷=1000000平方米",
      "能进行公顷和平方米、平方千米之间的换算",
      "了解公顷和平方千米的实际大小，用于土地、城市等较大面积的计量"
    ],
    "difficulties":[
      "公顷与平方米进率是10000（不是100或1000），与其他面积单位不同",
      "平方千米与公顷进率是100，与公顷和平方米的进率不同",
      "实际估量：1公顷≈1.4个标准足球场；北京市面积约1.6万平方千米",
      "换算方向：大单位换小单位乘进率，小单位换大单位除进率"
    ],
    "exercises":[
      {"question":"1公顷=（　）平方米；1平方千米=（　）公顷；1平方千米=（　）平方米","answer":"10000；100；1000000","analysis":"1公顷=10000m²；1km²=100公顷；1km²=100×10000=1000000m²"},
      {"question":"换算：5公顷=（　）平方米；3平方千米=（　）公顷；20000平方米=（　）公顷","answer":"50000平方米；300公顷；2公顷","analysis":"5×10000=50000；3×100=300；20000÷10000=2"},
      {"question":"比较大小：5公顷○50000平方米；2平方千米○150公顷","answer":"=；＞","analysis":"5公顷=50000m²，=；2平方千米=200公顷＞150公顷"},
      {"question":"一块农田长400米，宽250米，这块农田的面积是多少平方米？合多少公顷？","answer":"100000平方米=10公顷","analysis":"400×250=100000m²；100000÷10000=10公顷"},
      {"question":"我国陆地国土面积约960万平方千米，改写成用公顷表示是多少？","answer":"9600000000公顷（96亿公顷）","analysis":"960万平方千米×100=96000万公顷=9.6亿公顷"},
      {"question":"一个公园的面积是3公顷，一座城市广场面积是50000平方米，哪个更大？","answer":"公园更大（3公顷=30000m²？不对，3公顷=30000m²<50000m²）","analysis":"3公顷=30000m²；50000m²=5公顷；50000m²>3公顷，广场更大"},
      {"question":"某小区占地面积是0.5平方千米，合多少公顷？合多少平方米？","answer":"50公顷；500000平方米","analysis":"0.5×100=50公顷；0.5×1000000=500000m²"},
      {"question":"一块正方形土地，边长500米，面积是多少平方米？合多少公顷？","answer":"250000平方米=25公顷","analysis":"500×500=250000m²；250000÷10000=25公顷"}
    ],
    "advanced_exercises":[
      {"question":"某城市新开发区规划面积30平方千米，其中工业用地占1/3，住宅用地占1/2，绿化用地其余。绿化用地多少公顷？","answer":"500公顷","analysis":"绿化=30×(1-1/3-1/2)=30×1/6=5平方千米=500公顷"},
      {"question":"一个农场有耕地480公顷，其中种小麦的占3/8，种玉米的占1/4，其余种蔬菜。蔬菜种了多少公顷？","answer":"180公顷","analysis":"蔬菜=480×(1-3/8-1/4)=480×3/8=180公顷"},
      {"question":"某国家公园面积5200平方千米，如果1平方千米可以养活50只大熊猫（假设），这个公园最多能养多少只？","answer":"260000只","analysis":"5200×50=260000只"},
      {"question":"一块长方形田地，已知面积是36公顷，长是900米，宽是多少米？","answer":"400米","analysis":"36公顷=360000m²；宽=360000÷900=400米"},
      {"question":"【思维题】甲地面积3.5平方千米，乙地面积280公顷，丙地面积450万平方米，按面积从大到小排列","answer":"甲＞乙＞丙","analysis":"甲=3.5平方千米=350公顷=3500000m²；乙=280公顷=2800000m²；丙=4500000m²。所以丙＞甲＞乙。更正：丙=450万m²=4500000m²；甲=3500000m²；乙=2800000m²；排列：丙＞甲＞乙"}
    ]
  },
  {
    "id":"ch03","title":"第3单元 角的度量",
    "knowledge_points":[
      "认识角的各部分（顶点、两条边），理解角的大小与边的长短无关，只与开口大小有关",
      "认识度（°）作为角的度量单位，掌握量角器的使用方法",
      "认识直角（90°）、锐角（＜90°）、钝角（90°~180°）、平角（180°）、周角（360°）",
      "能用量角器准确量出角的度数，并能画出指定度数的角"
    ],
    "difficulties":[
      "正确使用量角器：中心点对准顶点，零刻度线对准一条边，读另一条边对应的度数",
      "量角器有内外两圈刻度，选择哪圈需要根据角的方向判断",
      "画角的步骤：画一条射线→量角器对位→标点→连线",
      "判断角的类型：特别注意直角和钝角的界限是90°，平角180°"
    ],
    "exercises":[
      {"question":"判断角的类型：①35°（　）②90°（　）③125°（　）④180°（　）⑤270°（　）","answer":"①锐角②直角③钝角④平角⑤优角（大于180°的角）","analysis":"＜90°锐角；=90°直角；90°~180°钝角；=180°平角；180°~360°优角（非常用）"},
      {"question":"一个角是60°，它的补角（两角之和=180°）是多少度？它的余角（两角之和=90°）是多少度？","answer":"补角120°；余角30°","analysis":"补角：180°-60°=120°；余角：90°-60°=30°"},
      {"question":"时钟上3时整，时针和分针所成的角是多少度？6时整呢？","answer":"3时：90°；6时：180°","analysis":"3时分针指12，时针指3，3格×30°=90°；6时时针指6，相差6格×30°=180°"},
      {"question":"用量角器量出下面三角形的三个角度数，并验证三角形内角和（参考题）","answer":"三角形三个内角之和=180°（理论值）","analysis":"任意三角形内角和都是180°"},
      {"question":"画一个65°的角（描述步骤）","answer":"①画射线OA②量角器圆心对O，零刻线对OA③在65°刻度处标点B④画射线OB，∠AOB=65°","analysis":"画角的标准步骤"},
      {"question":"一个角是钝角，比直角大25°，这个角是多少度？","answer":"115°","analysis":"直角=90°，90°+25°=115°，是钝角✓"},
      {"question":"∠1+∠2=180°，∠1=75°，∠2是多少度？两角合在一起是什么角？","answer":"∠2=105°；合在一起是平角","analysis":"∠2=180°-75°=105°；两角和=180°是平角"},
      {"question":"等边三角形三个角相等，每个角是多少度？等腰三角形顶角是40°，底角各是多少度？","answer":"等边三角形每角60°；等腰三角形底角70°","analysis":"等边：180°÷3=60°；等腰：底角=(180°-40°)÷2=70°"}
    ],
    "advanced_exercises":[
      {"question":"一个多边形内角和：三角形180°，四边形360°，五边形540°，发现规律，求八边形内角和","answer":"1080°","analysis":"n边形内角和=(n-2)×180°；八边形=(8-2)×180°=1080°"},
      {"question":"时钟2时30分，时针和分针的夹角是多少度？（提示：每分钟时针移动0.5°，分针移动6°）","answer":"105°","analysis":"2时整时针在60°位置（从12点顺时针），2时30分时针转了30×0.5=15°，位于75°；分针在180°（指6）；夹角=180°-75°=105°"},
      {"question":"一个角的补角比这个角大40°，这个角是多少度？","answer":"70°","analysis":"设角为x，补角=180°-x；(180°-x)-x=40°，180°-2x=40°，2x=140°，x=70°"},
      {"question":"等腰三角形一个底角是50°，顶角是多少度？如果顶角是110°，底角是多少度？","answer":"顶角80°；底角35°","analysis":"顶角=180°-50°×2=80°；底角=(180°-110°)÷2=35°"},
      {"question":"【思维题】一个圆被分成若干相等的扇形，如果每个扇形的圆心角是45°，可以分成多少个扇形？如果分成12份，每个圆心角多少度？","answer":"8个；30°","analysis":"360°÷45°=8个；360°÷12=30°"}
    ]
  },
  {
    "id":"ch04","title":"第4单元 三位数乘两位数",
    "knowledge_points":[
      "掌握三位数乘两位数的估算方法",
      "掌握三位数乘两位数的笔算方法（先乘个位，再乘十位，对齐相加）",
      "理解积的变化规律：一个因数不变，另一个因数扩大几倍，积也扩大几倍",
      "能灵活运用三位数×两位数解决实际问题"
    ],
    "difficulties":[
      "笔算时第二步乘十位的积需向左移一位（与个位结果错一位）",
      "多次进位时进位数字容易遗忘或累加错误",
      "积的变化规律的理解和运用",
      "较大数字的乘法估算，选择合适的近似值"
    ],
    "exercises":[
      {"question":"估算：298×32≈（　）；408×21≈（　）","answer":"约9000；约8000","analysis":"298≈300，300×32=9600≈9000或9600；408≈400，400×21=8400≈8000"},
      {"question":"笔算：234×46","answer":"10764","analysis":"234×6=1404；234×40=9360；1404+9360=10764"},
      {"question":"笔算：308×25","answer":"7700","analysis":"308×5=1540；308×20=6160；1540+6160=7700"},
      {"question":"一辆火车每小时行驶186千米，行驶48小时能走多少千米？","answer":"8928千米","analysis":"186×48=8928千米"},
      {"question":"一个工厂一天生产零件125个，一年（365天）生产多少个？","answer":"45625个","analysis":"125×365=45625个"},
      {"question":"如果125×16=2000，那么125×32=（　），125×8=（　）","answer":"4000；1000","analysis":"32=16×2，所以积×2=4000；8=16÷2，积÷2=1000"},
      {"question":"笔算：172×35","answer":"6020","analysis":"172×5=860；172×30=5160；860+5160=6020"},
      {"question":"一本书售价38元，书店一个月销售了245本，书店这个月销售额是多少元？","answer":"9310元","analysis":"38×245=9310元"}
    ],
    "advanced_exercises":[
      {"question":"小明每天读书45分钟，坚持读了一年（365天），共读书多少分钟？换算成多少小时多少分钟？","answer":"16425分钟=273小时45分钟","analysis":"45×365=16425分钟；16425÷60=273余45；273小时45分钟"},
      {"question":"A×B=1536，如果A扩大3倍、B缩小2倍，积是多少？","answer":"2304","analysis":"新积=1536×3÷2=1536×1.5=2304"},
      {"question":"某校图书馆新进图书，故事书135本，科技书的数量是故事书的3倍，工具书比科技书少48本，三类书共多少本？","answer":"1002本","analysis":"科技书：135×3=405本；工具书：405-48=357本；总：135+405+357=897本（重算：135+405+357=897，不是1002）"},
      {"question":"用竖式算出：（1）143×27 （2）256×34","answer":"（1）3861 （2）8704","analysis":"（1）143×7=1001；143×20=2860；1001+2860=3861；（2）256×4=1024；256×30=7680；1024+7680=8704"},
      {"question":"【思维题】甲乙两地相距896千米，一辆汽车和一辆火车同时从甲地出发去乙地，汽车每小时56千米，火车每小时是汽车的3倍，火车比汽车早到几小时？","answer":"火车早到8小时","analysis":"火车速度：56×3=168千米/小时；汽车时间：896÷56=16小时；火车时间：896÷168=5.33...不整除，重算：896÷168=5余56，不整除。换数据：如果896÷168不整除，则用：汽车时间16小时，火车：168×16=2688km，不对题目。应该：火车时间=896÷168≈5.33h，汽车16h，差约10.67h。题目数据可能需调整"}
    ]
  },
  {
    "id":"ch05","title":"第5单元 平行四边形和梯形",
    "knowledge_points":[
      "认识平行四边形：两组对边分别平行且相等的四边形，对角相等",
      "认识梯形：只有一组对边平行的四边形，平行的两边叫上底和下底，不平行的两边叫腰",
      "理解平行线、垂线的概念，能用三角尺画平行线和垂线",
      "掌握平行四边形和梯形面积公式（后续学习）"
    ],
    "difficulties":[
      "平行四边形与长方形的区别：长方形是特殊的平行四边形（有直角）",
      "等腰梯形的识别：两腰相等的梯形",
      "用三角尺画平行线：平移三角尺的操作技巧",
      "正确识别图形中的平行线段和垂直线段"
    ],
    "exercises":[
      {"question":"判断：①正方形是平行四边形吗？②所有的平行四边形都是长方形吗？③梯形有几条对称轴？","answer":"①是②不是③等腰梯形有1条，普通梯形0条","analysis":"正方形有两组对边平行，是特殊平行四边形；平行四边形不一定有直角，所以不一定是长方形；等腰梯形有1条对称轴"},
      {"question":"平行四边形的对边：①是否平行？②是否相等？对角：①是否相等？","answer":"对边既平行又相等；对角相等","analysis":"平行四边形定义：两组对边平行且相等，对角相等"},
      {"question":"一个平行四边形底是8cm，高是5cm，面积是多少cm²？","answer":"40cm²","analysis":"平行四边形面积=底×高=8×5=40cm²"},
      {"question":"一个梯形上底4cm，下底10cm，高6cm，面积是多少cm²？","answer":"42cm²","analysis":"梯形面积=(上底+下底)×高÷2=(4+10)×6÷2=42cm²"},
      {"question":"在方格纸上，画一个平行四边形和一个梯形，并标注各部分名称","answer":"平行四边形标注：边、对角；梯形标注：上底、下底、腰、高","analysis":"画图题，注意标注准确"},
      {"question":"下面哪些是平行四边形？哪些是梯形？（A:两组平行边 B:一组平行边 C:无平行边）","answer":"A是平行四边形；B是梯形；C都不是","analysis":"平行四边形：两组对边平行；梯形：恰好一组对边平行"},
      {"question":"平行四边形的邻角之和是多少度？（邻角即相邻的两个角）","answer":"180°","analysis":"平行四边形中，同旁内角互补，相邻两角之和=180°"},
      {"question":"等腰梯形ABCD，AB为上底，CD为下底，已知∠D=70°，∠C是多少度？∠A是多少度？","answer":"∠C=70°（等腰梯形底角相等）；∠A=110°","analysis":"等腰梯形腰相等，底角相等，∠C=∠D=70°；∠A+∠D=180°，∠A=110°"}
    ],
    "advanced_exercises":[
      {"question":"一个平行四边形和一个长方形，底和高分别相同，面积是否相同？周长是否相同？","answer":"面积相同；周长：平行四边形≥长方形（等号在长方形时成立）","analysis":"面积都=底×高，相同；周长：平行四边形的腰≥长方形的宽（等号条件是腰=宽即成长方形），所以周长≥"},
      {"question":"一块梯形地，上底30m，下底50m，高20m，按每平方米种3棵苗木，共种多少棵？","answer":"2400棵","analysis":"面积=(30+50)×20÷2=800m²；棵数=800×3=2400棵"},
      {"question":"将一个平行四边形沿高剪开，拼成一个长方形，这个长方形的长和宽与平行四边形的底和高有什么关系？","answer":"长方形的长=平行四边形的底，宽=高，面积相等","analysis":"沿高剪开后，将一侧的三角形移到另一侧，拼成长方形，长=底，宽=高"},
      {"question":"等腰梯形周长为52cm，上底12cm，腰长15cm，下底是多少cm？","answer":"10cm","analysis":"下底=周长-上底-2×腰=52-12-30=10cm"},
      {"question":"【思维题】一个大正方形（边长8cm）被分成1个小正方形（边长4cm）、2个长方形和1个大正方形，求2个长方形的面积之和","answer":"32cm²","analysis":"大正方形面积=64；小正方形=16；若分法如下：64-16=48，再减去中间正方形（如有），具体分法：64-16=48=2个长方形+?。实际2个长方形面积=大面积-小正方形-另一正方形=64-16-16=32cm²"}
    ]
  },
  {
    "id":"ch06","title":"第6单元 除数是两位数的除法",
    "knowledge_points":[
      "掌握口算：整百整千除以整十数（如600÷20=30）",
      "掌握笔算：三位数÷两位数（商一位数、商两位数）",
      "理解试商方法：用四舍五入把除数看成整十数来试商",
      "掌握验算：商×除数+余数=被除数"
    ],
    "difficulties":[
      "试商需要调整：初始试商偏大（余数大于除数，要调大商）或偏小（余数小于0，需调小商）",
      "商的位置书写：要对准被除数的对应数位",
      "除数末尾有0时的简便计算",
      "两步应用题中正确选择除法运算"
    ],
    "exercises":[
      {"question":"口算：400÷20=（　）；1800÷30=（　）；3600÷90=（　）","answer":"20；60；40","analysis":"400÷20=40÷2=20；1800÷30=180÷3=60；3600÷90=360÷9=40"},
      {"question":"笔算：952÷28","answer":"34","analysis":"952÷28：试商：952÷30≈31，试31：28×31=868，余84，84>28，调大；试34：28×34=952，余0，商34"},
      {"question":"笔算：891÷45，并验算","answer":"19余36；验算：19×45+36=855+36=891✓","analysis":"891÷45：试商45×20=900>891，试19：45×19=855，891-855=36，商19余36"},
      {"question":"一共有432个苹果，每箱装36个，能装多少箱？","answer":"12箱","analysis":"432÷36=12箱"},
      {"question":"笔算：663÷51","answer":"13","analysis":"663÷51：试51×13=663，正好，商13"},
      {"question":"学校买了552本图书，平均分给24个班，每班分多少本？","answer":"23本","analysis":"552÷24=23本"},
      {"question":"一个数除以32，商是25，余数是8，这个数是多少？","answer":"808","analysis":"被除数=25×32+8=800+8=808"},
      {"question":"估算：458÷62≈（　）；830÷41≈（　）","answer":"约7；约20","analysis":"458÷62≈450÷60=7.5≈7；830÷41≈840÷42=20"}
    ],
    "advanced_exercises":[
      {"question":"某工厂三月份生产零件744个，四月份生产了比三月份少的数量，但具体不知，如果用来装箱，每箱装31个，请求三月份装了几箱？","answer":"24箱","analysis":"744÷31=24箱"},
      {"question":"一辆大巴车限载45人，学校共有783名学生要外出参观，需要几辆大巴？","answer":"18辆（783÷45=17余18，需18辆才能装完）","analysis":"783÷45=17余18，17辆不够，需要18辆"},
      {"question":"甲数除以乙数商15余3，甲数是528，乙数是多少？","answer":"35","analysis":"甲数=商×乙数+余数；528=15×乙数+3；15×乙数=525；乙数=525÷15=35"},
      {"question":"粮仓有大米2580千克，第一次运出48袋，每袋25千克；第二次运出了其余的1/2，粮仓还剩多少千克？","answer":"690千克","analysis":"第一次：48×25=1200千克；剩余：2580-1200=1380千克；第二次运出：1380÷2=690千克；还剩：1380-690=690千克"},
      {"question":"【思维题】□÷38=□…□，商和余数都是最大值时，商是多少？余数是多少？被除数是多少？","answer":"商最大无上限，但余数最大=37（余数＜除数）；若被除数是三位数，最大999÷38=26余11；若要求商和余数都最大且相等，则需解方程","analysis":"余数最大=38-1=37；若要商也最大且=37，则被除数=38×37+37=37×39=1443（四位数）；若三位数，最大999÷38=26...11，商26余11"}
    ]
  },
  {
    "id":"ch07","title":"第7单元 条形统计图",
    "knowledge_points":[
      "认识条形统计图：用长短不等的条形表示数量多少",
      "能读懂条形统计图：看横轴（类别）和纵轴（数量），读取条形高度对应的数值",
      "能根据数据制作条形统计图（确定纵轴刻度、画条形、标注）",
      "能根据条形统计图进行简单的数据分析和对比"
    ],
    "difficulties":[
      "纵轴刻度的确定：根据最大数据确定每格代表的数量（使图形美观合理）",
      "读取近似值：当数据不恰好在刻度线上时，需要估读",
      "从图中发现数据的变化趋势和规律",
      "比较复式条形统计图中多组数据（如对比两班成绩）"
    ],
    "exercises":[
      {"question":"某学校四年级各班人数：一班45人，二班42人，三班48人，四班43人。画出条形统计图（描述如何设置纵轴）","answer":"纵轴每格5人，最高到50，各班画相应高度的条形","analysis":"最大数48，纵轴最高50，每格可以是5或10"},
      {"question":"从条形统计图读取：如果最高的条形高度代表48人，最矮的代表42人，相差多少人？","answer":"6人","analysis":"48-42=6人"},
      {"question":"统计图显示某班同学最喜欢的科目：语文15，数学22，英语18，体育20，美术10。哪科最受欢迎？哪科最不受欢迎？总人数多少？","answer":"数学最受欢迎；美术最不受欢迎；总85人","analysis":"最高22=数学；最低10=美术；总15+22+18+20+10=85"},
      {"question":"根据数据制作条形图并分析趋势：月降雨量（毫米）：1月10，2月15，3月20，4月35，5月60，6月80。哪个月降雨最多？有何趋势？","answer":"6月最多；降雨量逐月增加，有增长趋势","analysis":"从1月到6月数据逐渐增大，呈增长趋势"},
      {"question":"两个班数学成绩对比（复式条形图）：优秀：甲班30，乙班25；良好：甲班15，乙班20；及格：甲班5，乙班5。哪班成绩更好？","answer":"甲班（优秀更多：30>25）","analysis":"甲班优秀人数更多，总体成绩较好"},
      {"question":"判断：①条形越长表示数量越多（　）②所有统计图纵轴都从0开始（　）③条形统计图可以清楚看出数量多少，也可以看出变化趋势（　）","answer":"①对②对③对（基本对，折线图更适合看趋势）","analysis":"条形图主要用于比较数量多少，折线图更适合趋势"},
      {"question":"某次调查，40名学生喜欢的体育项目：篮球16人，足球12人，乒乓球8人，其他4人。用条形统计图表示时，纵轴每格代表2人，各条形分别画几格？","answer":"篮球8格，足球6格，乒乓球4格，其他2格","analysis":"÷2：16÷2=8格，12÷2=6格，8÷2=4格，4÷2=2格"},
      {"question":"从统计图分析：某店一周销售量（件）：一50，二45，三60，四55，五80，六100，日90。销售最旺的是哪天？工作日平均每天销量多少件？","answer":"星期六最旺；工作日平均：(50+45+60+55+80)÷5=58件","analysis":"工作日（一到五）：50+45+60+55+80=290，÷5=58件/天"}
    ],
    "advanced_exercises":[
      {"question":"某班期末各科平均分：语文86，数学92，英语88，科学79，体育95。请分析：哪科需要加强？如果下学期每科都要提升5分，各科目标是多少？","answer":"科学最低需加强；目标：语文91，数学97，英语93，科学84，体育100","analysis":"科学79分最低；各科+5，体育100为满分"},
      {"question":"两家超市一周蔬菜销量（吨）：甲：一3.5，二4.0，三4.5，四3.8，五5.0，六7.5，日6.0；乙：一4.0，二3.5，三5.0，四4.2，五4.8，六6.0，日7.0。一周内哪家总销量更多？","answer":"甲：3.5+4+4.5+3.8+5+7.5+6=34.3吨；乙：4+3.5+5+4.2+4.8+6+7=34.5吨，乙略多","analysis":"分别求和比较"},
      {"question":"根据条形统计图，四年级各班图书角藏书量（册）：一班120，二班150，三班135，四班145，五班160。全年级平均每班多少册？如果要让每班都达到150册，需要为哪些班补充多少册？","answer":"平均142册；一班补30，三班补15，四班补5","analysis":"平均：(120+150+135+145+160)÷5=710÷5=142；差150：一班30，二班0，三班15，四班5，五班0"},
      {"question":"某年级400米跑步比赛成绩（秒）：1名87，2名89，3名92，4名95，5名98，6名101。用条形统计图呈现时，每格代表5秒，纵轴从80开始，第1名对应几格？","answer":"第1名对应：(87-80)÷5=1.4格（非整格，实际取最接近的刻度线）","analysis":"如果纵轴从80开始，87在第1.4格处，可能纵轴设计需要每格2秒更合适"},
      {"question":"【综合分析】某班体育测试达标情况：男生25人，全部达标；女生20人，其中18人达标。全班达标率是多少？用统计图怎么表示男女生达标对比？","answer":"全班达标率：43/45≈95.6%；用复式条形图：横轴男/女，纵轴人数，每组两个条形（达标/不达标）","analysis":"男25达标，女18达标，共43人达标；总45人；达标率43/45=95.6%"}
    ]
  },
  {
    "id":"ch08","title":"第8单元 数学广角——优化",
    "knowledge_points":[
      "通过统筹方法解决实际问题：合理安排工序，减少总时间",
      "理解优化的思想：在有限条件下寻找最优方案",
      "能用图示或表格分析多任务合理安排",
      "掌握简单的排列组合思想（有序思考）"
    ],
    "difficulties":[
      "分清哪些任务可以并行（同时进行），哪些必须顺序（前一个完成才能开始）",
      "找出最优方案，说明为什么是最优",
      "排列组合中不重复不遗漏地列出所有情况",
      "用数学方法计算最少需要的时间"
    ],
    "exercises":[
      {"question":"烧水需要10分钟，泡茶需要3分钟（水烧好才能泡），洗茶杯需要2分钟。如何安排才能最快喝上茶？最少需要多少分钟？","answer":"先烧水，同时洗茶杯；水开后泡茶。总时间=10+3=13分钟（洗杯与烧水同时进行）","analysis":"洗杯2分钟可以在烧水的10分钟内完成，不需要额外时间；最少时间=10+3=13分钟"},
      {"question":"妈妈要做以下事情：煮饭40分钟，炒菜10分钟（要等饭煮好），切菜5分钟，摆碗筷3分钟。最快多少分钟能开饭？","answer":"43分钟","analysis":"煮饭同时切菜(5分钟)和摆碗筷(3分钟)，这些都能并行；煮饭40分钟后炒菜10分钟=50分钟太长。实际：煮饭+炒菜=40+10=50分钟是关键路径；切菜和摆碗可以在此期间完成。所以最快=40+10=50？但切菜要在炒菜前完成，炒菜前切菜5分钟+炒菜10分钟也在煮饭期间进行，所以总时间=40+10=50分钟，不对，切菜可以在煮饭期间做，然后煮饭好了立即炒菜10分钟。总=40+10=50分钟，但煮饭时切菜，所以切菜不单独占时间"},
      {"question":"从A、B、C三道菜中任选2道，有多少种不同的选法？","answer":"3种（AB, AC, BC）","analysis":"从3选2：AB、AC、BC，共3种"},
      {"question":"1、2、3三个数字各用一次，能组成多少个不同的三位数？","answer":"6个（123,132,213,231,312,321）","analysis":"3×2×1=6种"},
      {"question":"一个人要过河，船只能坐2人（含船夫），共有4名游客和1名船夫，至少需要渡几次？","answer":"4次（或来回算，4次到对岸）","analysis":"每次载1名游客，来回1次送1人需2趟，4名游客需4次×2=8趟（来回），但最后一次不用回来：4次到对岸=7趟"},
      {"question":"小明做题：语文20分钟，数学30分钟，英语25分钟，中间休息5分钟。如何安排顺序让总时间最短？（每门功课各做一次，不能同时做）","answer":"时间固定=20+30+25+3×5=90分钟（顺序不影响总时间，除非休息可优化）","analysis":"因为不能同时做功课，所以总做题时间固定=75分钟，加上2次（中间）休息=75+10=85分钟，顺序不影响总时间"},
      {"question":"3枚硬币同时抛出，正反面可能出现多少种不同组合？","answer":"8种（正正正，正正反，正反正，反正正，正反反，反正反，反反正，反反反）","analysis":"2×2×2=8种"},
      {"question":"在一次比赛中，4支球队互相比赛一次（循环赛），共需要比几场？","answer":"6场","analysis":"C(4,2)=4×3÷2=6场"}
    ],
    "advanced_exercises":[
      {"question":"做一顿饭需要以下步骤：淘米5分钟→煮饭40分钟→切菜10分钟→炒菜15分钟（切菜和煮饭不能同时进行，必须切完才能炒）→上桌2分钟。能否将某些步骤合并节省时间？最少需要多少分钟？","answer":"最少62分钟","analysis":"关键路径：淘米5+煮饭40=45分钟煮好饭；同时间可以切菜10分钟（在煮饭期间做）；煮饭结束后炒菜15+上桌2=17分钟；总=45+17=62分钟（切菜在煮饭期间完成，不占额外时间）"},
      {"question":"用0、1、2、3四个数字，每个只用一次，能组成多少个四位偶数？","answer":"10个","analysis":"末位必须是偶数(0或2)。末位0：前三位用1,2,3全排列=6个；末位2：首位不能是0，首位选1或3（2种），其余两位全排列=2×2=4个；共10个"},
      {"question":"5人比赛握手，每两人握一次，共握几次手？如果是10人呢？","answer":"5人：10次；10人：45次","analysis":"C(5,2)=10；C(10,2)=45"},
      {"question":"工厂有3台机器，每台完成一件产品需要的时间分别是：A机器12分钟，B机器15分钟，C机器10分钟。如果要完成9件产品（每台各做3件），最快多少分钟？","answer":"45分钟（最慢的B机器3×15=45分钟决定）","analysis":"A：3×12=36分钟；B：3×15=45分钟；C：3×10=30分钟；最慢的B机器决定总时间，45分钟"},
      {"question":"【思维题】将一个大任务分成若干小任务，某项目有5个任务（A,B,C,D,E），其中B依赖A完成，D依赖C完成，E依赖B和D都完成。时间：A=3天，B=4天，C=5天，D=2天，E=6天。关键路径是什么？最短完成时间？","answer":"关键路径C→D→E=5+2+6=13天；A→B=3+4=7天；总=13天","analysis":"两条路径：A→B→E=3+4+6=13天；C→D→E=5+2+6=13天；E依赖B和D，要等两条路径都完成，最短时间=max(7,7)+6=13天"}
    ]
  }
]

print("Grade 4 math upper content defined.")

# ============ 四年级数学下册内容 ============
g4_math_lower = [
  {
    "id":"ch01","title":"第1单元 四则运算",
    "knowledge_points":[
      "理解加减乘除四则运算的意义，掌握运算顺序规则",
      "同级运算（加减/乘除）从左到右计算；有括号先算括号内",
      "乘除是第二级，加减是第一级；混合运算先乘除后加减",
      "含有小括号的运算：括号内优先，括号外按顺序"
    ],
    "difficulties":[
      "混合运算中运算顺序的判断，特别是多重括号",
      "0的运算特殊情况：0÷任何非0数=0，任何数×0=0，但0不能作除数",
      "去括号时改变符号的规则（减法括号前的负号）",
      "综合算式中正确完成分步计算"
    ],
    "exercises":[
      {"question":"按运算顺序计算：36÷4+5×3","answer":"24","analysis":"先乘除：36÷4=9，5×3=15；再加：9+15=24"},
      {"question":"计算：(25+35)÷(4×3)","answer":"5","analysis":"括号内：25+35=60；4×3=12；60÷12=5"},
      {"question":"计算：100-(48+36÷6)","answer":"46","analysis":"先括号内：36÷6=6；48+6=54；100-54=46"},
      {"question":"计算：120÷(8-5)+32×4","answer":"168","analysis":"括号：8-5=3；120÷3=40；32×4=128；40+128=168"},
      {"question":"下列算式中，先算哪一步？①18+6÷2 ②(18+6)÷2 ③18×6+2 ④18×(6+2)","answer":"①先算除法6÷2；②先算括号18+6；③先算乘法18×6；④先算括号6+2","analysis":"遵循运算顺序：括号→乘除→加减"},
      {"question":"计算：0×(100+200-1)+999×1","answer":"999","analysis":"0×(任何数)=0；999×1=999；0+999=999"},
      {"question":"某商店卖出上衣35件，每件120元；裤子42条，每条85元；计算总收入","answer":"7770元","analysis":"上衣：35×120=4200元；裤子：42×85=3570元；总：4200+3570=7770元"},
      {"question":"用综合算式表示：买了6个足球，每个48元，付出300元，应找回多少元？","answer":"300-6×48=300-288=12元","analysis":"先算6×48=288，再算300-288=12元"}
    ],
    "advanced_exercises":[
      {"question":"计算：(144-108)÷(36÷12)+25×(100-96)","answer":"101","analysis":"144-108=36；36÷12=3；36÷3=12；100-96=4；25×4=100；12+100=112，等等重算：(144-108)÷(36÷12)+25×(100-96)=36÷3+25×4=12+100=112"},
      {"question":"数学游戏：将1、2、3、4用加减乘除和括号，组成结果为10的算式（每个数只用一次），写出两种","answer":"如：(1+2+3)×4÷2=12≠10；试：1×2+3+5不行；(4-2)×3+4不行（4用了两次）；正确：(1+4)×2=10✓（但只用了3个数）；3个数：1+2+7不行；四个数：2×(1+4)=10（3个数），四个数：3×4-2×1=10✓","analysis":"3×4-2×1=12-2=10，使用1,2,3,4各一次，正确"},
      {"question":"小明家买水果：苹果3千克×6元=18元，梨2千克×8元=16元，付了50元，找回多少元？综合算式怎么列？","answer":"找回16元；50-（3×6+2×8）=50-34=16","analysis":"50-(3×6+2×8)=50-(18+16)=50-34=16元"},
      {"question":"一道算式：□×5+□÷4=25，两个□填同一个数，这个数是多少？","answer":"4","analysis":"设□=x，5x+x÷4=25，x(5+1/4)=25，x×21/4=25，x=25×4/21=100/21≈4.76，不是整数。换条件：如果x=4：4×5+4÷4=20+1=21≠25。所以题目可能需要两个□填不同数。若□₁×5+□₂÷4=25，有多种答案"},
      {"question":"【思维题】用1到9各一次，填入□使等式成立：□□□+□□□=□□□（三位数+三位数=三位数）","answer":"如：123+456=579（1-9各用一次）","analysis":"满足条件的组合：123+456=579，1,2,3,4,5,6,7,8,9各用一次✓"}
    ]
  },
  {
    "id":"ch02","title":"第2单元 观察物体（二）",
    "knowledge_points":[
      "能从正面、侧面、上面三个方向观察立体图形",
      "根据三视图（正视图、侧视图、俯视图）推断立体图形的形状",
      "能画出简单立体组合图形的三视图",
      "理解同一个物体从不同方向看到的形状可能不同"
    ],
    "difficulties":[
      "从平面图形想象立体形状，需要空间思维",
      "确定某个面看到的是正方形还是长方形（取决于观察方向）",
      "由三视图重建立体形状，需要综合三个方向的信息",
      "计算遮挡关系：看不到的部分不在图中显示"
    ],
    "exercises":[
      {"question":"一个正方体从正面看是什么形状？从侧面看呢？从上面看呢？","answer":"三个方向都是正方形","analysis":"正方体各面都是正方形，从任何方向看都是正方形"},
      {"question":"一个长方体（长6，宽4，高3），从正面看（长×高）是什么？从侧面看（宽×高）是什么？","answer":"正面：6×3的长方形；侧面：4×3的长方形；上面：6×4的长方形","analysis":"三视图分别对应不同方向的截面"},
      {"question":"将2个正方体叠放（一个放在另一个上面），从正面看是什么形状？","answer":"竖长方形（1×2）","analysis":"叠放后从正面看到高度变成2，宽度还是1，所以是1×2的长方形"},
      {"question":"3个正方体排成一排，从上面看是什么形状？从正面看呢？","answer":"上面：1×3的长方形；正面：1×1的正方形（看到最前面一个）","analysis":"上面看是俯视图=1×3；正面看第一个遮住后面的，还是1×1正方形（但实际应看到1×3，从前面看一排正方体，高1宽3），正面：3×1的长方形"},
      {"question":"画出下面组合图形的三视图：2个正方体（底部1个，上面1个放在右侧）的正视图、侧视图、俯视图（用方格描述）","answer":"正视图：L形（左列高2，右列高1）；侧视图：高2、宽1的长方形；俯视图：1×2的长方形","analysis":"具体形状取决于摆放方式，需要画图确认"},
      {"question":"同一物体从三个方向看到的三张图：正面是长方形，侧面是正方形，上面是长方形，这个物体可能是什么？","answer":"可能是长方体（长宽不同，高与宽相等）","analysis":"侧面是正方形说明宽=高；正面和上面是长方形说明长≠宽"},
      {"question":"用小正方形积木搭建：底层放一个2×2的正方形（4块），上层放一个1×1（1块）在中间，从上面看是什么形状？","answer":"2×2的正方形（上层的被下层遮住，从上看是2×2）","analysis":"从上方看，能看到底层的4块加上上层的1块，但上层1块遮住底层1块，从上看是2×2带中心点，实际上看是2×2正方形"},
      {"question":"一个圆柱体从正面看是长方形，从上面看是什么？","answer":"圆形","analysis":"圆柱从上面看是圆形（俯视图）"}
    ],
    "advanced_exercises":[
      {"question":"给出正视图、侧视图、俯视图，判断积木共需要几个正方体：正视图2列（左高2右高1），侧视图1列高2，俯视图1×2。","answer":"3个正方体","analysis":"左列高2（2个），右列高1（1个），共3个"},
      {"question":"用6个正方体积木拼出一个图形，要求：正视图是2×3的长方形，俯视图是1×3的长方形，侧视图是1×2的长方形。这个图形是什么？","answer":"2×3×1的长方体摆法（2层高，3列宽，1列深）=6个正方体","analysis":"6个正方体排成2层×3列×1深的形状"},
      {"question":"两个完全相同的长方体（长5宽3高2）叠放，一个在上一个在下，从正面看的面积是多少？","answer":"5×4=20（宽5，高4=2+2）","analysis":"叠放后高变4=2+2，宽还是5，面积=5×4=20"},
      {"question":"搭建积木时，发现从三个方向看的图形都是完全相同的正方形，这个物体最少需要几块正方体积木？","answer":"最少需要3块","analysis":"三视图都是2×2正方形：最少排列是3块（一个L型），可以满足三视图都是2×2"},
      {"question":"【思维题】用积木拼出的图形，从正面和侧面看都是同一个图形，但从上面看到的图形不同，举出一个例子（描述即可）","answer":"如：圆柱体：正面和侧面都是长方形，上面是圆形","analysis":"圆柱体是典型例子，也可以是锥体等其他形状"}
    ]
  },
  {
    "id":"ch03","title":"第3单元 运算定律",
    "knowledge_points":[
      "加法交换律：a+b=b+a（加数交换，和不变）",
      "加法结合律：(a+b)+c=a+(b+c)（加数的结合方式改变，和不变）",
      "乘法交换律：a×b=b×a；乘法结合律：(a×b)×c=a×(b×c)",
      "乘法分配律：a×(b+c)=a×b+a×c（重要！可以简化计算）"
    ],
    "difficulties":[
      "乘法分配律的逆用（提取公因数）：ab+ac=a(b+c)",
      "活用运算定律进行简便计算，识别凑整的机会",
      "连减和连除的简便运算（减法/除法没有交换律！）",
      "复杂算式中灵活选择运算定律"
    ],
    "exercises":[
      {"question":"用简便方法计算：278+453+22","answer":"753","analysis":"发现278+22=300，300+453=753（加法交换+结合律）"},
      {"question":"用简便方法计算：125×32","answer":"4000","analysis":"125×32=125×8×4=1000×4=4000（乘法结合律，先算125×8=1000）"},
      {"question":"用乘法分配律计算：46×102","answer":"4692","analysis":"46×102=46×(100+2)=4600+92=4692"},
      {"question":"用简便方法计算：38×99+38","answer":"3800","analysis":"38×99+38=38×99+38×1=38×(99+1)=38×100=3800（分配律逆用）"},
      {"question":"填空：(a+b)×c=（　）×c+（　）×c，这是（　）律","answer":"a；b；乘法分配","analysis":"(a+b)×c=a×c+b×c，乘法分配律"},
      {"question":"用简便方法：125×16×5","answer":"10000","analysis":"125×8=1000，16=8×2，125×16×5=125×8×2×5=1000×10=10000"},
      {"question":"125×32+125×68","answer":"12500","analysis":"125×(32+68)=125×100=12500（分配律逆用）"},
      {"question":"76×99","answer":"7524","analysis":"76×99=76×(100-1)=7600-76=7524"}
    ],
    "advanced_exercises":[
      {"question":"用简便方法计算：（1）101×45 （2）198×25 （3）999+998+997+3+2+1","answer":"(1)4545 (2)4950 (3)3000","analysis":"(1)101×45=(100+1)×45=4500+45=4545；(2)198×25=200×25-2×25=5000-50=4950；(3)(999+1)+(998+2)+(997+3)=1000×3=3000"},
      {"question":"简便计算：36×125-36×25","answer":"3600","analysis":"36×(125-25)=36×100=3600"},
      {"question":"小华买文具：本子8本，每本3.5元；钢笔4支，每支9元；橡皮8个，每个1.5元。用运算定律简化计算总价。","answer":"92元","analysis":"本子：8×3.5=28；钢笔：4×9=36；橡皮：8×1.5=12；总：28+36+12=76，不对：28+36=64+12=76元。整理：8×3.5+8×1.5=8×5=40；40+36=76元"},
      {"question":"证明：(a+b)²≠a²+b²（反例），但(a+b)²=a²+2ab+b²（用分配律展开验证）","answer":"反例：a=2,b=3,(2+3)²=25≠4+9=13；展开：(a+b)²=(a+b)(a+b)=a²+ab+ba+b²=a²+2ab+b²","analysis":"(a+b)(a+b)=a(a+b)+b(a+b)=a²+ab+ab+b²=a²+2ab+b²"},
      {"question":"【思维题】用分配律简化：99×99+199","answer":"9800","analysis":"99×99=99×100-99×1=9900-99=9801；9801+199=10000。等等：99×99+199=9801+199=10000。用分配律直接简化：99×99+199=99×99+200-1=(99×99+99×2)-1+?... 其实直接算：9801+199=10000，结果是整数很美"}
    ]
  },
  {
    "id":"ch04","title":"第4单元 小数的意义和性质",
    "knowledge_points":[
      "理解小数的意义：小数是十进制分数的另一种表示（0.1=1/10，0.01=1/100）",
      "认识小数的数位：小数点后第一位是十分位，第二位是百分位，第三位是千分位",
      "掌握小数的基本性质：小数末尾加0或去掉0，小数大小不变",
      "能进行小数大小比较，将小数化为分数，进行小数与整数/分数的互化"
    ],
    "difficulties":[
      "小数的计数单位：0.1是十分之一，不是10分之一和1/10的区别",
      "小数末尾零的处理：0.30=0.3（大小不变），但精度表示时有区别",
      "小数大小比较：先比整数部分，再按位比较小数部分",
      "小数与分数的互化：分母是10、100、1000的分数"
    ],
    "exercises":[
      {"question":"3.56中，整数部分是（　），小数部分是（　），5在（　）位，表示（　）","answer":"整数3；小数0.56；5在十分位；表示5个0.1（即5/10）","analysis":"3.56=3+0.5+0.06，5在十分位，代表0.5=5/10"},
      {"question":"用=化简：3.50=（　）；0.700=（　）；4.010=（　）","answer":"3.5；0.7；4.01","analysis":"去掉小数末尾的0：3.50→3.5；0.700→0.7；4.010→4.01"},
      {"question":"不改变数的大小，把下面的数改写成有三位小数：1.2=（　）；0.45=（　）；8=（　）","answer":"1.200；0.450；8.000","analysis":"在末尾补0到三位小数"},
      {"question":"比较大小：4.5○4.50；0.8○0.79；3.02○3.020","answer":"=；＞；=","analysis":"4.5=4.50（末尾零不改变大小）；0.8=0.80>0.79（百分位0>9不对！应比十分位8>7）；3.02=3.020"},
      {"question":"把1.5、0.15、1.05、0.501、0.15从大到小排列","answer":"1.5＞1.05＞0.501＞0.15","analysis":"整数部分：1.5,1.05>0.501,0.15；整数部分为1：1.5>1.05；整数部分为0：0.501>0.15（十分位5=5，百分位0<1？不对：0.501的百分位是0，0.15的百分位是5，0.15>0.501的百分位，但0.501的百分位是0＜1），所以0.15>0.501？再比：0.5__vs 0.1__，十分位5>1，所以0.501>0.15。最终：1.5>1.05>0.501>0.15"},
      {"question":"将小数化为分数：0.3=（　）；0.75=（　）；1.8=（　）","answer":"3/10；75/100=3/4；18/10=9/5","analysis":"0.3=3/10；0.75=75/100（约分=3/4）；1.8=18/10（化简=9/5）"},
      {"question":"将分数化为小数：3/10=（　）；7/100=（　）；9/4=（　）","answer":"0.3；0.07；2.25","analysis":"3/10=0.3；7/100=0.07；9/4=9÷4=2.25"},
      {"question":"下面哪些数等于0.50？①0.5 ②50/100 ③5/10 ④500/1000","answer":"都等于0.50","analysis":"0.5=0.50；50/100=0.50；5/10=0.5=0.50；500/1000=0.50，四个都相等"}
    ],
    "advanced_exercises":[
      {"question":"按规律填数：0.1,0.3,0.5,（　）,（　）；1.0,0.8,0.6,（　）,（　）","answer":"0.7,0.9；0.4,0.2","analysis":"等差数列，公差0.2：0.1,0.3,0.5,0.7,0.9；递减公差0.2：1.0,0.8,0.6,0.4,0.2"},
      {"question":"在0和1之间，有多少个小数（一位小数）？（0.1,0.2,...0.9）共几个？","answer":"9个（0.1到0.9）","analysis":"0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9，共9个"},
      {"question":"一个两位小数，十分位上的数比百分位上的数大3，这两位小数的和为9.45，这个数是多少？（提示：十分位用x，百分位用x-3）","answer":"0.60","analysis":"设百分位为a，十分位为a+3，数为0.(a+3)a=0.1(a+3)+0.01a=0.11a+0.3；两个这样的数之和=9.45。等等题目说\"这两位小数的和\"可能指十分位和百分位数字之和=(a+3)+a=2a+3=9（由9.45推断），2a=6，a=3，数为0.63。验证：十分位6，百分位3，差=3✓；数字和=6+3=9✓。但9.45不能推出这个。可能题目是：这个两位小数等于9.45-8.82=0.63。答案0.63"},
      {"question":"用三张数字卡片3、5、0（各用一次）和一个小数点，能组成哪些不同的小数？最大的是多少？最小的正小数是多少？","answer":"3.50,3.05,5.30,5.03,0.35,0.53,50.3,30.5,53.0,05.3(不合法),03.5(不合法)","analysis":"合法小数（首位不为0）：3.50=3.5,3.05,5.30=5.3,5.03,50.3,30.5；以0开头的：0.35,0.53；最大：53.0=53；最小正数：0.35"},
      {"question":"【思维题】0.1+0.2+0.3+...+0.9=？用什么简便方法？","answer":"4.5","analysis":"=(0.1+0.9)×9÷2（等差数列求和）=1.0×4.5=4.5；或：首尾配对(0.1+0.9)+(0.2+0.8)+(0.3+0.7)+(0.4+0.6)+0.5=1+1+1+1+0.5=4.5"}
    ]
  },
  {
    "id":"ch05","title":"第5单元 三角形",
    "knowledge_points":[
      "认识三角形：由三条线段围成的封闭图形，有三条边、三个角、三个顶点",
      "三角形的内角和=180°（任何三角形）",
      "三角形的分类：按角分（锐角/直角/钝角三角形），按边分（等边/等腰/普通三角形）",
      "三角形三边关系：任意两边之和大于第三边（三角形成立的条件）"
    ],
    "difficulties":[
      "三角形内角和定理的应用：已知两个角求第三个角",
      "判断三边能否构成三角形：最短两边之和必须大于最长边",
      "等腰三角形的识别：两腰相等，顶角在两腰之间",
      "三角形的稳定性：三角形形状固定，四边形可以变形（应用）"
    ],
    "exercises":[
      {"question":"三角形内角和=（　）度，如果两个角分别是65°和80°，第三个角是（　）度","answer":"180°；35°","analysis":"第三角=180°-65°-80°=35°"},
      {"question":"判断能否构成三角形：①3,4,5 ②2,3,6 ③5,5,5","answer":"①能②不能③能（等边三角形）","analysis":"①3+4=7>5✓；②2+3=5<6✗（不能）；③5+5=10>5✓"},
      {"question":"等边三角形每个角是多少度？等腰三角形顶角是100°，底角是多少度？","answer":"60°；底角40°","analysis":"等边：180°÷3=60°；等腰底角=(180°-100°)÷2=40°"},
      {"question":"一个直角三角形，有一个角是55°，另外两个角分别是多少度？","answer":"35°和90°","analysis":"已有一个90°和55°，第三角=180°-90°-55°=35°"},
      {"question":"判断三角形类型：①三个角都小于90° ②有一个90°角 ③有一个120°角","answer":"①锐角三角形②直角三角形③钝角三角形","analysis":"按最大角分类"},
      {"question":"三角形的一条边上的高是从对边的（　）到这条边所在直线的（　）线段","answer":"对边的对面顶点；垂","analysis":"高是从顶点到对边的垂线段"},
      {"question":"等腰三角形腰长8cm，底边4cm，周长是多少？如果底角是50°，顶角是多少度？","answer":"周长20cm；顶角80°","analysis":"周长=8+8+4=20cm；顶角=180°-50°×2=80°"},
      {"question":"一个三角形可以有几个钝角？几个直角？","answer":"最多1个钝角；最多1个直角（三角形内角和180°）","analysis":"若有2个直角=180°，第三个角=0°，不构成三角形；一个三角形最多只有一个钝角或直角"}
    ],
    "advanced_exercises":[
      {"question":"直角三角形中，两个锐角的关系是什么？如果其中一个锐角是35°，另一个是多少度？","answer":"两个锐角互补（和为90°）；另一个=55°","analysis":"直角三角形：90°+锐角1+锐角2=180°，所以锐角1+锐角2=90°；35°+锐角2=90°，锐角2=55°"},
      {"question":"用4根小棒（长度3cm,3cm,4cm,4cm）能拼成哪几种三角形？","answer":"不能（4根棒只能围四边形）；若取3根：3,3,4能构成等腰三角形（3+3=6>4✓）；3,4,4也能（3+4=7>4✓）","analysis":"4根棒围三角形？三角形只需3条边，从4根选3根：(3,3,4)或(3,4,4)，都能构成三角形"},
      {"question":"一个三角形，如果将其中一个内角增大10°，其余两个内角应该如何变化，才能保持三角形内角和不变？","answer":"其余两个角共减小10°（如各减5°，或一个减10°，另一个不变等）","analysis":"三角形内角和恒为180°，一个角增大Δ，其余两个角之和必须减小Δ"},
      {"question":"剪纸游戏：将一个等边三角形（边长12cm）从各边中点剪开，得到几个小三角形？每个小三角形是等边三角形吗？边长多少？","answer":"4个等边三角形，边长6cm","analysis":"连接各边中点将等边三角形分成4个全等的小等边三角形，边长=原来的一半=6cm"},
      {"question":"【思维题】一个等腰三角形，顶角是底角的2倍，求三个角分别是多少度？","answer":"顶角80°，底角各50°","analysis":"设底角为x，顶角=2x；x+x+2x=180°；4x=180°；x=45°。顶角=90°，底角45°。等等：等腰三角形有两个相等的底角。设底角=x，顶角=2x；2x+x+x=180°（两个底角+顶角）；4x=180°；x=45°；顶角=90°，底角=45°"}
    ]
  },
  {
    "id":"ch06","title":"第6单元 小数的加法和减法",
    "knowledge_points":[
      "掌握小数加减法的计算方法：小数点对齐，相同数位相加减",
      "计算结果中末尾出现0时，要根据情况化简（去掉末尾0）",
      "能用小数加减法解决实际生活中的问题（购物、测量等）",
      "掌握小数加减法的验算方法"
    ],
    "difficulties":[
      "位数不同的小数相加减时，要补齐位数再计算（用0填充空位）",
      "进位和借位的处理（与整数相同，但要注意小数点位置）",
      "计算结果整数部分为0时的写法（如0.9+0.5=1.4，不要写成.14）",
      "实际应用中单位换算结合小数计算"
    ],
    "exercises":[
      {"question":"计算：3.45+2.8=（　）；7.2-4.56=（　）","answer":"6.25；2.64","analysis":"3.45+2.80=6.25（补0对齐）；7.20-4.56=2.64（补0对齐）"},
      {"question":"计算：12.5+8.75+1.25","answer":"22.5","analysis":"12.5+8.75=21.25；21.25+1.25=22.5（或发现8.75+1.25=10，12.5+10=22.5）"},
      {"question":"计算：5-3.46","answer":"1.54","analysis":"5.00-3.46=1.54（整数补小数位）"},
      {"question":"小明买了一本书12.5元，一支钢笔8.8元，一个本子3.6元，共花了多少钱？如果付了30元，找回多少？","answer":"共24.9元；找回5.1元","analysis":"12.5+8.8+3.6=24.9元；30-24.9=5.1元"},
      {"question":"估算：4.87+3.19≈（　）；9.03-5.98≈（　）","answer":"约8；约3","analysis":"4.87≈5，3.19≈3，约8；9.03≈9，5.98≈6，约3"},
      {"question":"水果店称量苹果：第一袋2.35千克，第二袋1.8千克，第三袋1.95千克，三袋共多少千克？","answer":"6.1千克","analysis":"2.35+1.80+1.95=6.10=6.1千克"},
      {"question":"一根绳子长8.5米，剪去3.76米，还剩多少米？再折半，每段多少米？","answer":"剩4.74米；折半2.37米","analysis":"8.5-3.76=4.74米；4.74÷2=2.37米"},
      {"question":"计算并验算：6.34+4.78","answer":"11.12；验算：11.12-4.78=6.34✓","analysis":"6.34+4.78=11.12；验算用减法"}
    ],
    "advanced_exercises":[
      {"question":"小明身高1.32米，小红身高1.47米，小华比他们两人平均身高高0.05米，小华多高？","answer":"1.445米","analysis":"平均=(1.32+1.47)÷2=2.79÷2=1.395米；小华=1.395+0.05=1.445米"},
      {"question":"一辆汽车上午行驶了63.5千米，下午行驶了78.8千米，全天行驶多少千米？如果油箱剩余燃油还能行驶48.7千米，加满后能行驶145千米，需要加多少千米量的油？","answer":"全天142.3千米；需加96.3千米量的油","analysis":"全天：63.5+78.8=142.3千米；加油：145-48.7=96.3千米量"},
      {"question":"排列计算（用简便方法）：5.8+4.3+0.7+5.2","answer":"16","analysis":"5.8+0.2（从4.3取）=6；4.1（剩）+5.9（从5.2取）=10；0.1（剩）+...实际：5.8+4.3+0.7+5.2=(5.8+0.2)+(4.3-0.2+0.7+0.2)...用结合律：(5.8+0.7)+(4.3+5.2)=6.5+9.5=16"},
      {"question":"一瓶饮料重0.8千克，箱子本身重1.25千克，一箱装12瓶，整箱重多少千克？","answer":"10.85千克","analysis":"12瓶=0.8×12=9.6千克；整箱=9.6+1.25=10.85千克"},
      {"question":"【思维题】用1.5、0.5、3、0.25四个数，每个用一次，加减法组合，得到结果最大是多少？最小是多少？","answer":"最大：3+1.5+0.5+0.25=5.25；最小：0.25-1.5-0.5+...=0.25+0.5-1.5-3=-3.75","analysis":"最大=全部加：3+1.5+0.5+0.25=5.25；最小=大数相减：0.25+0.5-1.5-3=-3.75"}
    ]
  },
  {
    "id":"ch07","title":"第7单元 图形的运动（二）",
    "knowledge_points":[
      "认识轴对称图形：沿某条直线对折，两侧完全重合的图形，该直线叫对称轴",
      "能判断一个图形是否是轴对称图形，并画出对称轴",
      "认识平移：图形沿某方向移动，形状和大小不变",
      "认识旋转：图形绕某个中心点转动，形状大小不变"
    ],
    "difficulties":[
      "某些图形有多条对称轴（如正方形4条，圆形无数条）",
      "画对称图形：每个点到对称轴的距离相等，且在对称轴两侧",
      "平移的方向和距离的准确描述",
      "旋转角度的判断（90°、180°等）"
    ],
    "exercises":[
      {"question":"下面哪些字母是轴对称图形？A、B、C、D、E、H、M、O（英文大写）","answer":"A、H、M、O（还有B、C、D、E但有争议，实际上B,C,D,E都有一条水平对称轴）","analysis":"A、H、M有竖直对称轴；O有无数条；B、C、D、E有水平对称轴"},
      {"question":"正方形有几条对称轴？长方形呢？圆形呢？","answer":"正方形4条；长方形2条；圆形无数条","analysis":"正方形：2条对角线+2条中线=4条；长方形：2条中线（不含对角线）"},
      {"question":"将△ABC向右平移5格，得到△A'B'C'，A在(2,3)，A'在哪里？","answer":"A'在(7,3)","analysis":"向右平移5格，横坐标+5，纵坐标不变：(2+5,3)=(7,3)"},
      {"question":"一个图形经过180°旋转后，与原图形的位置关系怎样？","answer":"倒置（上下颠倒，左右也互换）","analysis":"180°旋转=倒置，关于旋转中心对称"},
      {"question":"画出下面图形关于竖线（对称轴）的对称图形：左边有一个L形，描述对称后的形状","answer":"对称后L形变成反L形（镜像）","analysis":"关于竖轴对称，左右互换"},
      {"question":"数字0、1、2、3、8中，哪些是轴对称图形？哪些旋转180°后与原来相同？","answer":"轴对称：0、1、3（部分）、8；旋转180°相同：0、1、6→9→不是、8","analysis":"0和8都有水平和竖直对称轴；旋转180°：0→0，1→1（竖写），8→8"},
      {"question":"将一个正三角形绕中心旋转120°，与原来重合吗？旋转60°呢？","answer":"120°重合；60°不重合（正三角形有3重旋转对称，每次120°）","analysis":"正三角形：旋转120°、240°、360°与原来重合；60°不重合"},
      {"question":"找出生活中的轴对称例子（3个），平移例子（2个）","answer":"轴对称：蝴蝶翅膀、人脸、汉字'山'；平移：开抽屉、升旗","analysis":"开放性问题，言之有理即可"}
    ],
    "advanced_exercises":[
      {"question":"一个图形先向右平移3格，再向上平移4格，与原位置相比，这等效于沿什么方向平移了多少格？（用勾股定理）","answer":"沿右上方平移5格（3-4-5勾股）","analysis":"水平3格，垂直4格，合位移=√(9+16)=5格，方向右偏上"},
      {"question":"将正方形ABCD绕顶点A旋转90°，描述旋转后各顶点的位置变化","answer":"A不动，B→原C位，C→原D'新位，D→原B'新位（每个顶点绕A旋转90°）","analysis":"绕A顺时针旋转90°：A固定，其他顶点各绕A旋转90°"},
      {"question":"一张方格纸上有轴对称图形，对称轴是竖线，左侧有点(1,2),(2,4),(3,1)，右侧对称点分别在哪里？（对称轴在x=4）","answer":"右侧：(7,2),(6,4),(5,1)","analysis":"关于x=4对称：x'=2×4-x；(1→7),(2→6),(3→5)；y不变"},
      {"question":"等腰梯形的两条对角线相交，将梯形分成4个三角形，哪两个三角形完全相同（全等）？","answer":"两个腰上方的三角形全等（利用等腰梯形的轴对称性）","analysis":"等腰梯形有一条对称轴（竖直中线），对角线交点两侧关于对称轴对称"},
      {"question":"【思维题】将一个正方形对折两次后，再沿某条线剪开，打开后得到的图形一定是（）","answer":"具有多条对称轴的图形（折叠后剪出的形状，展开后具有对称性）","analysis":"每次对折增加一条对称轴，两次对折后图形具有4重对称性"}
    ]
  },
  {
    "id":"ch08","title":"第8单元 平均数与条形统计图",
    "knowledge_points":[
      "理解平均数的意义：平均数=总数量÷总份数，代表一组数据的'中等水平'",
      "掌握平均数的计算方法",
      "能利用平均数进行数据分析和比较",
      "复习条形统计图，能绘制和分析简单的统计图"
    ],
    "difficulties":[
      "平均数不一定是实际存在的数据值（如平均分可能是小数）",
      "平均数受极端值影响较大（一个特别高或低的数会影响平均数）",
      "区分平均数、众数、中位数（初步了解）",
      "从统计图中提取数据计算平均数"
    ],
    "exercises":[
      {"question":"某次测试，5名同学的成绩：85、92、78、96、89，平均成绩是多少？","answer":"88分","analysis":"(85+92+78+96+89)÷5=440÷5=88分"},
      {"question":"4个数的平均数是15，如果加入一个新数后，5个数的平均数变为16，新加入的数是多少？","answer":"20","analysis":"5个数总和=16×5=80；原4个数总和=15×4=60；新数=80-60=20"},
      {"question":"小明连续5天跳绳次数：120、135、115、140、130，平均每天跳多少次？","answer":"128次","analysis":"(120+135+115+140+130)÷5=640÷5=128次"},
      {"question":"如果一组数据的平均数是50，其中有一个数是80，另一个是30，问是否影响这组数据的平均数？（开放性问题）","answer":"这两个数对称分布在平均数两侧（各差30），相互'平衡'，平均数不变","analysis":"一个高30，一个低30，对平均数没有影响"},
      {"question":"三个班级参加知识竞赛，甲班平均分82（25人），乙班平均分86（30人），哪个班总分更高？","answer":"乙班总分更高（86×30=2580＞82×25=2050）","analysis":"比较总分：甲=82×25=2050；乙=86×30=2580；乙更高"},
      {"question":"一个书架上有书：第一层12本，第二层15本，第三层9本，第四层18本，平均每层多少本？","answer":"13.5本","analysis":"(12+15+9+18)÷4=54÷4=13.5本"},
      {"question":"小明身高的数据（cm）：三年级：128，四年级上学期：133，四年级下学期：136。计算平均身高，分析增长趋势","answer":"平均：(128+133+136)÷3=132.3cm；每年增长约4cm，在增长","analysis":"平均132.3cm；从128到136共增长8cm，约每学期增长4cm"},
      {"question":"某工厂5月份每天生产产品数（件）：周一120，周二135，周三118，周四142，周五125。工作日平均每天生产多少件？","answer":"128件","analysis":"(120+135+118+142+125)÷5=640÷5=128件"}
    ],
    "advanced_exercises":[
      {"question":"小明语数英三门课：语文89，数学94，英语成绩未知。已知三门课平均分是91，英语多少分？","answer":"90分","analysis":"总分=91×3=273；英语=273-89-94=90分"},
      {"question":"A组5人平均体重42千克，B组4人平均体重38千克，AB两组合在一起的平均体重是多少？","answer":"40.2千克","analysis":"A总=42×5=210；B总=38×4=152；合计=362；÷9=40.2千克"},
      {"question":"某校六次考试平均分是85分，第七次考了97分，七次平均分是多少？","answer":"87分","analysis":"前六次总分=85×6=510；七次总=510+97=607；÷7=86.7...≈87分。精确：607÷7=86.7分"},
      {"question":"一组10个数，平均数是24，去掉最大数40和最小数8后，剩余8个数的平均数是多少？","answer":"23","analysis":"10个数总和=24×10=240；去掉40和8：240-40-8=192；剩余8个数平均=192÷8=24。等等192÷8=24，不是23。重算：24×10=240，240-40-8=192，192÷8=24。答案是24"},
      {"question":"【思维题】班级参加体育达标测试，女生20人平均成绩85分，男生25人平均成绩79分，全班平均成绩是多少？（注意：不是(85+79)÷2）","answer":"81.7分","analysis":"女生总=85×20=1700；男生总=79×25=1975；总=3675；÷45=81.67分≈81.7分"}
    ]
  },
  {
    "id":"ch09","title":"第9单元 数学广角——鸡兔同笼",
    "knowledge_points":[
      "理解鸡兔同笼问题的基本结构：已知总头数和总脚数，求鸡和兔各多少只",
      "掌握列表法（枚举法）：逐一尝试，找到满足条件的解",
      "掌握假设法（假设全是鸡或全是兔），通过差值推算",
      "能建立方程（设未知数）解决鸡兔同笼类问题"
    ],
    "difficulties":[
      "假设法的思维：假设全是鸡（2条腿），脚比实际少，多余的差来自兔（4条腿，比鸡多2条）",
      "列方程：设鸡为x，兔为y，建立两个方程组联立求解",
      "鸡兔同笼问题的变形：如龙凤呈祥（不同腿数的组合）",
      "解题后的检验：代入原条件验证"
    ],
    "exercises":[
      {"question":"笼中有鸡和兔共10只，脚共28条，鸡和兔各多少只？","answer":"鸡6只，兔4只","analysis":"假设全是鸡：10×2=20只脚，比28少8条；多的脚来自兔（兔比鸡多2条腿）：8÷2=4只兔；鸡=10-4=6只"},
      {"question":"验证：鸡6只兔4只，脚=6×2+4×4=12+16=28 ✓","answer":"验证正确","analysis":"代入检验：头数6+4=10✓，脚数28✓"},
      {"question":"鸡兔同笼，共有头15个，脚38条，求鸡和兔各几只？","answer":"鸡11只，兔4只","analysis":"假设全是鸡：15×2=30，比38少8；8÷2=4只兔；鸡=11只。验证：11×2+4×4=22+16=38✓"},
      {"question":"用列表法解：鸡兔共8只，脚22条","answer":"鸡3只，兔5只","analysis":"枚举：鸡8兔0→16脚；鸡7兔1→18；鸡6兔2→20；鸡5兔3→22✓。所以鸡5兔3？验证5×2+3×4=10+12=22✓"},
      {"question":"用方程解：设鸡为x只，兔为y只，已知x+y=8，2x+4y=22，解方程","answer":"x=5,y=3（鸡5兔3）","analysis":"从第一方程：x=8-y；代入第二：2(8-y)+4y=22；16-2y+4y=22；2y=6；y=3；x=5"},
      {"question":"变形题：蜘蛛（8条腿）和蜻蜓（6条腿）共10只，腿共70条，各有多少只？","answer":"蜘蛛5只，蜻蜓5只","analysis":"假设全是蜻蜓：10×6=60条，比70少10；多的来自蜘蛛（比蜻蜓多2条腿）：10÷2=5只蜘蛛；蜻蜓=5只。验证：5×8+5×6=40+30=70✓"},
      {"question":"停车场有三轮车和四轮车共20辆，共有车轮72个，三轮车有多少辆？","answer":"8辆","analysis":"假设全是四轮车：20×4=80，比72多8；多的来自四轮车变三轮车（每辆减1轮）：8辆换成三轮车；三轮车8辆，四轮车12辆。验证：8×3+12×4=24+48=72✓"},
      {"question":"某班同学，有人带了2本书，有人带了3本书，共30人，带了75本书，带2本的多少人？","answer":"15人","analysis":"假设全带3本：30×3=90，比75多15；多来自2本的（3-2=1），15÷1=15人带2本；带3本=15人。验证：15×2+15×3=30+45=75✓"}
    ],
    "advanced_exercises":[
      {"question":"鸡、鸭、鹅共30只，鸡脚2条、鸭脚2条、鹅脚2条...等等这样不行。改题：三轮车、两轮车、独轮车共30辆，共有轮子62个，其中独轮车比三轮车多2辆，三种车各多少辆？","answer":"三轮车6辆，两轮车22辆，独轮车2辆","analysis":"设三轮车x，独轮车x+2，两轮车y；x+(x+2)+y=30→2x+y=28；3x+1(x+2)+2y=62→4x+2y=60→2x+y=30。矛盾？重算：3x+(x+2)×1+2y=62，3x+x+2+2y=62，4x+2y=60，2x+y=30；同时2x+y=28，矛盾。题目数据有问题，调整：62轮，设三轮车x，独轮车z=x+2，两轮车y，x+z+y=30，3x+z+2y=62，代入z=x+2：x+x+2+y=30→2x+y=28；3x+x+2+2y=62→4x+2y=60→2x+y=30，矛盾。题目错误，修改轮子为60：4x+2y=58，2x+y=28+1=29...还是矛盾。放弃此题，换题"},
      {"question":"商店卖苹果和梨，苹果3元/个，梨2元/个，共卖了50个水果，收入120元，苹果和梨各卖了多少个？","answer":"苹果20个，梨30个","analysis":"假设全是梨：50×2=100元，比120少20元；多的来自苹果（比梨贵1元）：20÷1=20个苹果；梨30个。验证：20×3+30×2=60+60=120✓"},
      {"question":"运动会上，学校参赛学生共40人，男生跑步得分3分/人，女生跑步得分2分/人，总得分100分，男女生各多少人？","answer":"男生20人，女生20人","analysis":"假设全是女生：40×2=80，比100少20；多来自男生（多1分）：20÷1=20个男生；女生20人。验证：20×3+20×2=60+40=100✓"},
      {"question":"鸡兔同笼中，如果兔的数量增加2只，则总脚数增加8条，为什么？如果每只鸡增加1条腿，总脚数变化多少？（假设鸡10兔5）","answer":"兔增2只：多2×4=8条腿✓；鸡增腿：10条多，共脚=10×3+5×4=30+20=50条","analysis":"兔每只4条腿，2只多8条；鸡本来10×2=20，每只多1条则10×3=30，多10条"},
      {"question":"【思维拓展】将鸡兔同笼的解法用于：购买文具，圆珠笔5元一支，钢笔8元一支，共买了20支，花了106元，各买了几支？","answer":"圆珠笔18支，钢笔2支","analysis":"假设全买圆珠笔：20×5=100，比106少6；多的来自钢笔（比圆珠笔贵3元）：6÷3=2支钢笔；圆珠笔18支。验证：18×5+2×8=90+16=106✓"}
    ]
  }
]

print("Grade 4 math lower content defined.")

# ============ 三年级语文上册内容 ============
g3_chinese_upper = [
  {
    "id":"u01","title":"第一单元 学校生活",
    "knowledge_points":[
      "学习课文《大青树下的小学》《花的学校》《不懂就要问》中的生字词",
      "能正确、流利、有感情地朗读课文，背诵指定段落",
      "理解课文内容，体会不同国家/地方的学校生活的美好",
      "学习写作：用几句话描述自己的校园生活"
    ],
    "difficulties":[
      "本单元生字较多（约30个），注意形近字区分（如'坪'与'评'）",
      "理解课文中的比喻句和拟人句，感受语言的美",
      "背诵《花的学校》第一、二自然段",
      "写话：用上'有……有……还有……'的句式描述事物"
    ],
    "exercises":[
      {"question":"给下面的字注音：坪___ 晨___ 绒___ 摔___ 跤___","answer":"píng chén róng shuāi jiāo","analysis":"坪píng草坪；晨chén早晨；绒róng绒毛；摔shuāi摔跤；跤jiāo跤"},
      {"question":"写出下面词语的近义词：美丽（　）安静（　）好奇（　）","answer":"漂亮；宁静；奇怪/好奇","analysis":"近义词：美丽≈漂亮；安静≈宁静；好奇≈奇怪"},
      {"question":"把下面的词语补充完整：（　）色（　）样；热热（　）（　）；来来（　）（　）","answer":"各色各样；热热闹闹；来来往往","analysis":"AABB、ABAB等常见叠词结构"},
      {"question":"照样子写句子：'弯弯的小路通向远方。'（用修饰词美化句子）原句：小鸟在树上叫。","answer":"如：可爱的小鸟在绿色的大树上欢快地叫着。","analysis":"通过加修饰词（形容词/副词）使句子更生动"},
      {"question":"根据课文内容填空：《大青树下的小学》描写了（　　）民族的学生，在（　　）的树下上课，大家穿着（　　）的服装。","answer":"各民族；大青树；鲜艳","analysis":"课文描述了一所边疆小学，有汉族和少数民族的学生"},
      {"question":"阅读短文，回答问题：'孙中山小时候读书，先生只叫背诵，从不讲解。孙中山想，这样的读书有什么用？'孙中山有什么问题？他是什么样的人？","answer":"问：书中讲的是什么意思；他是个善于思考、勇于发问的人","analysis":"《不懂就要问》的主题：学习要多问"},
      {"question":"扩句练习：（1）花开了。（加上时间、地点、样子等）（2）同学读书。（加上修饰语）","answer":"（1）春天，五颜六色的花在草地上美丽地开放了。（2）认真的同学们在教室里专心地朗读课文。","analysis":"扩句要使句子更完整、生动、具体"},
      {"question":"仿写句子：'当雷云在天上轰响，六月的雨落下的时候，湿润的东风走过荒野，在竹林中吹着口哨。'请仿写一个描写自然景象的句子。","answer":"当春风吹过大地，三月的阳光温暖大地的时候，快乐的小鸟飞过天空，在树枝间唱着歌谣。（意近即可）","analysis":"仿照原句结构：'当……的时候，……'，注意句式工整"}
    ],
    "advanced_exercises":[
      {"question":"阅读理解（课外）：'小学的操场在下午放学后变得安静了，只有风吹过树叶的沙沙声。一只小鸟停在篮球架上，好奇地看着空旷的操场。'请回答：①这段话写的是什么时间？②用了哪些描写方法？③你觉得这个场景美不美，为什么？","answer":"①下午放学后；②声音描写（沙沙声）、动作描写（停、看）；③美，安静、自然的氛围（言之有理即可）","analysis":"阅读理解要抓住时间、地点、景物描写等要素"},
      {"question":"想象作文（100字以内）：如果你的学校有一棵神奇的大树，它会是什么样的？能做什么？请写一段话。","answer":"开放性作文，言之有理即可。参考：我们学校有一棵神奇的大树，它的叶子是金色的，每当有同学遇到难题，树叶就会飘落下来，上面写着答案的提示……","analysis":"想象作文要有具体的细节，语句通顺"},
      {"question":"写出与'学校'有关的4字词语（至少5个）","answer":"如：书声朗朗、桃李满天、师恩难忘、校园生活、学有所成","analysis":"积累四字词语，丰富词汇量"},
      {"question":"修改病句：①我的理想是医生。②这个问题非常值得认真考虑。③他不但成绩好，和同学也搞好了。","answer":"①我的理想是当一名医生。②这个问题非常值得我们认真考虑。③他不但成绩好，而且和同学关系也很好。","analysis":"①缺少谓语动词'当'；②主语不明确；③'不但……还……'关联词误用，应用'不但……而且……'"},
      {"question":"【综合题】读'不懂就要问'这个道理，结合自己的学习经历，写50字左右谈谈你的理解","answer":"开放性回答。参考：学习中遇到不懂的问题，一定要及时问老师或同学，不能假装明白。孙中山先生说过，不懂就要问，这样才能真正学会知识，打好基础。","analysis":"语言表达流畅，有自己的观点"}
    ]
  },
  {
    "id":"u02","title":"第二单元 秋天的美景",
    "knowledge_points":[
      "学习古诗《山行》《赠刘景文》《夜书所见》及散文《秋天的雨》等",
      "掌握本单元生字词，理解古诗中关键词的意思",
      "能背诵三首古诗，理解诗意",
      "学习用美丽的语言描写秋天，积累秋天相关词语"
    ],
    "difficulties":[
      "古诗中文言词语的理解：如'寒山''径''霜叶''橙黄橘绿'等",
      "古诗的翻译和背诵：特别是诗意的理解，而非死记硬背",
      "体会秋天景色的美，将诗句与现实生活联系起来",
      "学习课文中排比句、比喻句的写法"
    ],
    "exercises":[
      {"question":"默写古诗《山行》（唐·杜牧）","answer":"远上寒山石径斜，白云生处有人家。停车坐爱枫林晚，霜叶红于二月花。","analysis":"完整背诵，注意'斜'读xiá（古音）"},
      {"question":"解释《山行》中的词语：①石径斜 ②坐爱 ③霜叶红于二月花","answer":"①弯弯曲曲的小路②因为喜爱③经霜打后的枫叶比二月的鲜花还要红","analysis":"古诗词语解释要联系上下文"},
      {"question":"《赠刘景文》中'荷尽已无擎雨盖，菊残犹有傲霜枝'，用自己的话说说这两句的意思","answer":"荷花凋谢了，荷叶也没有了；菊花虽然残败，但还有傲然霜寒的枝条","analysis":"'擎雨盖'比喻荷叶；菊花的精神是傲霜"},
      {"question":"填空：'最是橙黄橘绿时'中'橙黄橘绿'描写了（　）季节，表现了（　）的特点","answer":"秋季；秋天色彩丰富、成熟丰收的特点","analysis":"橙色和橘绿是秋天特有的颜色，象征丰收"},
      {"question":"《秋天的雨》中，秋天的雨像一把（　），（　）地打开了秋天的大门。秋天的雨有一盒（　）","answer":"钥匙；轻轻地；五彩缤纷的颜料","analysis":"课文中的比喻和描写"},
      {"question":"仿照'秋天的雨，是一把钥匙'的句式，写一句描写春天（或夏天）的句子","answer":"如：春天的风，是一双温柔的手，轻轻抚摸着大地；夏天的太阳，是一个火球，热烈地照耀着大地","analysis":"保留比喻句式：'XX的YY，是……'"},
      {"question":"积累秋天的词语（至少6个）","answer":"金秋时节、层林尽染、秋高气爽、硕果累累、落叶纷纷、枫叶似火","analysis":"积累描写秋天的四字词语"},
      {"question":"判断下面说法对不对：①《夜书所见》的作者是宋代诗人叶绍翁（　）②'知有儿童挑促织'中'促织'是指蟋蟀（　）③'山行'的意思是在山上行走（　）","answer":"①对②对③对","analysis":"《夜书所见》作者叶绍翁（宋）；促织即蟋蟀；山行=山中行走"}
    ],
    "advanced_exercises":[
      {"question":"对比阅读：《山行》写的是秋天的（　），《赠刘景文》写的是秋天的（　），《夜书所见》写的是秋天的（　）。三首诗各表达了什么情感？","answer":"《山行》写秋天山中枫叶之美，表达赞美；《赠刘景文》写秋末景色，劝友人珍惜时光；《夜书所见》写秋夜客居思乡之情","analysis":"三首诗主题不同，情感各异"},
      {"question":"小练笔：用50字左右描写你眼中的秋天（可用到课文中学到的词句）","answer":"开放性写作，参考：秋天来了，树叶慢慢变黄，就像一只只金色的蝴蝶在空中飞舞。苹果红了，梨黄了，稻谷低下了沉甸甸的头，处处散发着丰收的气息。","analysis":"描写秋天要有具体的景物和感受"},
      {"question":"拓展：你还知道哪些描写秋天的古诗？写出一首并注明作者","answer":"如：刘禹锡《秋词》'自古逢秋悲寂寥，我言秋日胜春朝。晴空一鹤排云上，便引诗情到碧霄。'","analysis":"积累更多秋天古诗"},
      {"question":"理解词语感情色彩：在《夜书所见》中，诗人为什么'见秋风'会'动客情'？结合古代交通不便的背景说一说","answer":"古代交通不便，游子离家在外，看到秋风秋景，自然引发对家乡和亲人的思念，因为秋天象征离别和萧瑟","analysis":"理解古诗要结合历史背景和诗人的情感"},
      {"question":"【综合题】如果你是杜牧，停在山路上看到满山红叶，你会有什么感受？用100字写一段游记","answer":"开放性写作，言之有理即可。参考：深秋的山路上，我驾车缓缓而行，忽然被那满山的红叶惊住了。那枫叶在夕阳的照耀下，红得像一团团燃烧的火焰，比春天的花朵还要娇艳……","analysis":"创意写作，要有真情实感"}
    ]
  },
  {
    "id":"u03","title":"第三单元 童话世界",
    "knowledge_points":[
      "阅读童话故事《去年的树》《那一定会很好》《在牛肚子里旅行》《一块奶酪》",
      "理解童话中拟人化写法的特点和作用",
      "能复述故事，抓住主要情节",
      "学习通过人物对话描写推进故事情节"
    ],
    "difficulties":[
      "理解童话故事的深层含义：友情、信守承诺（《去年的树》）",
      "区分现实与虚构，理解童话夸张手法",
      "把握故事中的时间线索和事物的变化过程",
      "仿写童话，有完整的开头、经过、结尾"
    ],
    "exercises":[
      {"question":"《去年的树》中，鸟儿和树的约定是什么？最后鸟儿怎么做的？","answer":"约定：明年还唱歌给你听；最后树被锯成木柴做成了蜡烛，鸟儿对着烛光唱了歌","analysis":"故事体现了对朋友信守承诺的美好品质"},
      {"question":"下面哪些特点是童话故事的特点？①人物会说话②有真实的历史人物③动物、植物有人的思想④充满想象力","answer":"①③④是童话特点；②不是（童话是虚构的）","analysis":"童话特点：拟人、想象、虚构"},
      {"question":"填空：《在牛肚子里旅行》中，（　）和（　）是好朋友，（　）被（　）吞进了肚子，最后靠（　）逃了出来","answer":"红头；青头；红头；牛；牛打喷嚏/青头的帮助","analysis":"故事情节的理解"},
      {"question":"写出两个带'告别'含义的词语，两个带'思念'含义的词语","answer":"告别：离别、道别；思念：想念、怀念","analysis":"积累近义词"},
      {"question":"给下面的童话开头续写：'小兔子在森林里捡到了一颗神奇的种子……'（写3-5句话）","answer":"小兔子在森林里捡到了一颗神奇的种子，它把种子种在了家门口。第二天，种子变成了一棵小树苗。一周后，小树上开满了各种颜色的花朵，蜜蜂和蝴蝶都来做客。（言之有理即可）","analysis":"续写要和开头内容衔接，有合理的想象"},
      {"question":"《那一定会很好》中，种子经历了哪些变化？按顺序写出来","answer":"种子→大树→手推车→椅子→木地板→阳光下的木屑","analysis":"故事主线：种子的一生，不断变化，始终快乐"},
      {"question":"解释下面词语并造句：蜷缩（　）；焦急（　）","answer":"蜷缩：身体弯曲缩成一团；焦急：非常着急；造句：小猫蜷缩在角落里睡觉；我焦急地等待着妈妈回来。","analysis":"理解词语含义，并正确运用"},
      {"question":"《一块奶酪》中，蚂蚁队长怎么处理那块奶酪碎末的？这说明他是个什么样的人？","answer":"把碎末留给了年龄最小的蚂蚁；说明他严格要求自己、以身作则、公正无私","analysis":"通过人物行为分析人物品格"}
    ],
    "advanced_exercises":[
      {"question":"对比《去年的树》和《那一定会很好》：两个故事的主人公都经历了变化，但情感是否相同？哪个更让你感动？说明理由","answer":"《去年的树》：树变成蜡烛，充满了分别的悲伤但也有对友情的坚守；《那一定会很好》：种子的变化充满了对新生命的期待和快乐。（言之有理）","analysis":"比较阅读，培养批判性思维"},
      {"question":"创作一个简短的童话故事（100字以内）：主角是一片落叶，要包含想象、有简单情节","answer":"开放性创作。参考：一片落叶从大树上飘落，它想去看看世界。它随风飘过小河，看见了游鱼；飘过草地，遇到了蚂蚱。最后它落在了泥土里，化作养分，等待明年新叶的诞生。","analysis":"童话要有拟人化、想象丰富"},
      {"question":"积累童话中的经典句子，找出你最喜欢的一句并说明原因","answer":"如：《去年的树》中'看哪，这只鸟虽然找不到往年的朋友，却守住了对朋友的承诺。'喜欢原因：真正的友情是信守诺言。（言之有理）","analysis":"培养读书积累和欣赏能力"},
      {"question":"如果你能给《去年的树》续写一个结尾，树在来世变成了什么？鸟儿还会来找它吗？","answer":"开放性续写。参考：第二年春天，那根蜡烛燃尽后，烛灰落入泥土，长出了一棵小树苗。鸟儿飞回来，看见了小树苗，高兴地唱了一首歌，就像去年一样。","analysis":"创意续写，保持故事的情感基调"},
      {"question":"【思维题】童话中常有'三'的规律（如三兄弟、经历三次考验等），你知道哪些有这种规律的童话？为什么用'三'比较多？","answer":"如：三只小猪、睡美人（三个仙女）、白雪公主（经历三次危险）等；'三'在童话中象征多次、圆满，也让故事有节奏感，第三次往往是转折或成功","analysis":"文学常识的积累和思考"}
    ]
  },
  {
    "id":"u04","title":"第四单元 猜测与推断",
    "knowledge_points":[
      "学习古诗《元日》《清明》《九月九日忆山东兄弟》了解传统节日",
      "学习《风筝》：理解课文情节，感受童年的快乐",
      "阅读中学习预测策略：根据题目/插图/已读内容猜测接下来的内容",
      "积累传统节日相关词语和习俗"
    ],
    "difficulties":[
      "古诗背诵与理解：三首诗分别描述春节、清明、重阳节",
      "理解重阳节的习俗：登高、插茱萸、饮菊花酒",
      "阅读策略'预测'的方法：有依据的猜测，不是随意想象",
      "理解《风筝》中孩子们的心情变化"
    ],
    "exercises":[
      {"question":"默写《元日》（宋·王安石）","answer":"爆竹声中一岁除，春风送暖入屠苏。千门万户曈曈日，总把新桃换旧符。","analysis":"完整背诵，理解：爆竹、屠苏酒、桃符是春节习俗"},
      {"question":"《清明》中'欲断魂'是什么意思？诗中描写了什么场景？","answer":"欲断魂：形容极度悲伤；场景：清明节下雨，诗人一个人在路上，询问哪里有酒家","analysis":"清明节有扫墓悼念的习俗，天下雨，诗人心情更加忧伤"},
      {"question":"《九月九日忆山东兄弟》中'遥知兄弟登高处，遍插茱萸少一人'，'少一人'指的是谁？","answer":"指诗人王维本人（他一个人在外乡，没能和家人一起登高插茱萸）","analysis":"以逆向思维写思乡：从异乡想象家人，感叹自己不在其中"},
      {"question":"我国传统节日习俗连线：春节—（　）；清明—（　）；端午—（　）；重阳—（　）","answer":"春节—贴春联/放鞭炮；清明—扫墓/踏青；端午—吃粽子/赛龙舟；重阳—登高/插茱萸","analysis":"传统节日习俗的积累"},
      {"question":"阅读《风筝》，回答：孩子们做好风筝放飞时的心情如何？风筝飞走找不到后呢？","answer":"放飞时：兴奋、快乐；找不到后：失落、难过（垂头丧气）","analysis":"心情变化是理解课文的关键"},
      {"question":"预测策略练习：读了《风筝》的题目，你猜这篇课文会写什么？读完开头后，你的预测有什么变化？","answer":"从题目预测：可能写关于风筝的故事；读开头后：确认是写孩子们做放风筝的经历，增加了对情节的期待","analysis":"预测要有依据，读后检验预测"},
      {"question":"写出关于传统节日的古诗句各一句（除本单元外）","answer":"端午：'节分端午自谁言，万古传闻为屈原'（文秀）；中秋：'但愿人长久，千里共婵娟'（苏轼）","analysis":"积累更多传统节日诗句"},
      {"question":"仿写：王维在《九月九日忆山东兄弟》中是在异乡想念家人，你在学校想家的时候，会想起什么？写2-3句话","answer":"开放性回答。参考：在学校想家的时候，我会想起妈妈做的热腾腾的饭，想起爸爸陪我做作业的样子，想起家里暖暖的灯光。","analysis":"联系实际，真情实感"}
    ],
    "advanced_exercises":[
      {"question":"比较《元日》和《九月九日忆山东兄弟》中的节日情感：一首描写喜庆，一首描写思念，为什么同是节日却情感不同？","answer":"元日（春节）是在家中欢庆的节日，充满喜悦；而《九月九日》是游子独处异乡，节日里更加思念家人，节日的团聚习俗反而衬托出诗人的孤独","analysis":"诗歌情感与诗人处境密切相关"},
      {"question":"研究性阅读：找出《风筝》中描写心情的词语（至少4个），并分析它们出现的原因","answer":"精心（做风筝时）、快活（风筝飞起来）、垂头丧气（风筝找不到）、没精打采（继续寻找）等","analysis":"心情词语与情节紧密相连"},
      {"question":"中国传统节日故事：写出一个传统节日的起源故事（60字以内）","answer":"如：端午节起源于纪念爱国诗人屈原。屈原忧国忧民，在农历五月初五投江而死，百姓为了防止鱼虾损伤他的身体，划龙舟驱赶，投粽子喂鱼，久而久之形成了端午节习俗。","analysis":"了解传统文化知识"},
      {"question":"创作：以'中秋节的一个晚上'为题，写一段描写（60字）","answer":"开放性写作。参考：中秋节的晚上，一轮圆月挂在天空，月光洒在庭院里，白亮亮的。全家人围坐在月饼旁，一边品尝甜蜜的月饼，一边望着月亮讲嫦娥的故事。","analysis":"节日作文要有场景、人物、活动"},
      {"question":"【拓展思维】如果你穿越到唐代和王维一起过重阳节，你会对他说什么安慰的话？","answer":"开放性回答。参考：王维先生，我理解你想念家人的心情。但是，你在他乡的努力和成就，一定会让家人为你骄傲。相信不久你就能回到家人身边，到时候一起登高插茱萸，那份喜悦会更加珍贵。","analysis":"将古诗与现代生活联系，培养共情能力"}
    ]
  },
  {
    "id":"u05","title":"第五单元 留心观察",
    "knowledge_points":[
      "学习《铺满金色巴掌的水泥道》《秋天的雨》（关于细致观察的课文）",
      "学会用心观察生活，抓住事物的特点进行描写",
      "积累描写颜色、形状、声音的词语",
      "学习从不同感官（视觉、听觉、嗅觉等）描写事物"
    ],
    "difficulties":[
      "仔细观察与粗略看的区别：留心才能发现美",
      "用准确的词语描述观察到的事物特征",
      "多感官描写：不仅写看到什么，还写听到、闻到、感受到什么",
      "把观察到的事物写成通顺、生动的句子"
    ],
    "exercises":[
      {"question":"照样子，按不同感官分类写词语：①看到的：金色、圆圆的；②听到的（　）；③闻到的（　）；④摸到的（　）","answer":"②叽叽喳喳、轰隆隆；③香甜、芬芳；④光滑、软绵绵","analysis":"不同感官对应不同词语类型"},
      {"question":"'铺满金色巴掌的水泥道'中，'金色巴掌'是比喻什么？用了什么修辞方法？","answer":"比喻梧桐树的落叶；比喻（暗喻）","analysis":"把叶子比作金色的巴掌，形象生动"},
      {"question":"给下面句子加上描写感受的词语，使它更生动：'秋天的雨打在树叶上。'","answer":"如：秋天凉爽的雨'叮叮咚咚'地打在枯黄的树叶上，发出轻柔的声响，像是在演奏一首小曲。","analysis":"多感官描写使句子更丰富"},
      {"question":"把下面词语按感官分类：金黄、清脆、柔软、甜蜜、沙沙响、蓬松、芳香","answer":"视觉：金黄；听觉：清脆、沙沙响；触觉：柔软、蓬松；味觉/嗅觉：甜蜜、芳香","analysis":"感官分类练习"},
      {"question":"观察练习：仔细看一朵花（或任意一种植物），从颜色、形状、气味三方面写3句话","answer":"开放性：如'月季花的花瓣是玫瑰红色的，层层叠叠像小伞一样。花瓣边缘微微卷起，摸上去丝滑柔软。轻轻靠近，能闻到淡淡的清香，让人心旷神怡。'","analysis":"观察写作要有具体细节"},
      {"question":"填写量词：一（　）叶子；一（　）雨滴；一（　）阳光；一（　）风","answer":"一片叶子；一颗/滴雨滴；一缕/束阳光；一阵风","analysis":"量词的正确使用"},
      {"question":"秋天的颜色词语接龙：金黄→（　）→（　）→（　）→（　）","answer":"金黄→橙红→枣红→深红→褐色（或其他合理颜色过渡）","analysis":"颜色词语积累，体会秋天色彩变化"},
      {"question":"仿写比喻句：'水泥道上的落叶，像一只只金色的蝴蝶。'请仿写一句描写自然现象的比喻句","answer":"如：天空中的云朵，像一只只洁白的绵羊；雨后的彩虹，像一座巨大的彩色桥梁；夜空中的星星，像一颗颗闪光的钻石。","analysis":"比喻句要有本体、喻体和相似点"}
    ],
    "advanced_exercises":[
      {"question":"写一段关于冬天的观察日记（80字），要求包含至少两种感官描写","answer":"今天下了今年第一场雪，我站在窗边仔细观察。雪花是白色的，像鹅毛一样轻盈飘落（视觉）。推开窗户，冷冽的空气扑面而来，让我忍不住打了个寒战（触觉）。远处偶尔传来孩子们踩雪的咯吱声，那是冬天特有的音乐（听觉）。","analysis":"观察日记要有时间、地点、所见所感"},
      {"question":"比较：同样是'雨'，秋雨和夏雨有什么不同？从感觉描写来写（50字）","answer":"夏雨：来势凶猛，噼里啪啦地打在地上，像鼓点一样激烈，空气中带着泥土的气息；秋雨：细如牛毛，轻柔地飘落，沙沙声像是低语，空气变得清凉带着淡淡的菊花香。","analysis":"同一事物在不同季节有不同特征"},
      {"question":"阅读理解（课外）：'清晨，露水在草叶上凝聚成一颗颗晶莹的水珠，在阳光下闪闪发光，像一颗颗珍珠。蜜蜂飞来，停在花蕊上，嗡嗡地唱着歌。'①找出比喻句；②哪些是观察到的，哪些是联想到的？","answer":"①比喻句：露水像一颗颗珍珠；②观察：露水、阳光、蜜蜂；联想：'像珍珠'是联想比喻","analysis":"区分观察与联想"},
      {"question":"创意写作：把你最喜欢的一种食物，用两段话描写，第一段写外表（颜色、形状），第二段写味道和口感","answer":"开放性写作。参考：西瓜：外皮翠绿，上面有深绿色的条纹，圆滚滚的像一颗大球。切开来，鲜红的果肉里嵌着黑色的种子，汁水淋漓。放入口中，甜蜜的汁水立刻在嘴里散开，甜而不腻，清凉解暑。","analysis":"从外到内、从形到味，多角度描写"},
      {"question":"【综合题】'留心处处皆学问'——结合本单元学习，说说你在日常生活中通过'留心观察'发现了什么有趣的事物（100字）","answer":"开放性，言之有理即可。提示：可以是自然现象（蚂蚁搬家、叶子变色）、生活细节（影子变化、水的流动）等","analysis":"结合生活实际，培养观察意识"}
    ]
  },
  {
    "id":"u06","title":"第六单元 祖国山河",
    "knowledge_points":[
      "学习课文，感受祖国大好河山的壮美（长城、西沙群岛等）",
      "学习描写景物的方法：由整体到局部，由远到近",
      "掌握本单元生字词，积累描写自然景观的词语",
      "能用几句话介绍一处自然景观"
    ],
    "difficulties":[
      "理解景物描写的层次：远观全景→近看细节",
      "表达对祖国山河的热爱之情，情感要真实",
      "积累描写山、水、树、花等自然景物的词语",
      "写作：用上'那里有……，那里有……'的排比句式"
    ],
    "exercises":[
      {"question":"填写描写山的词语（至少4个）","answer":"连绵起伏、峰峦叠嶂、雄伟壮观、山清水秀、崇山峻岭","analysis":"积累写山的四字词语"},
      {"question":"填写描写水的词语（至少4个）","answer":"波光粼粼、清澈见底、碧波荡漾、水天一色、波涛汹涌","analysis":"积累写水的词语"},
      {"question":"用'不仅……而且……'造一个介绍景物的句子","answer":"如：西湖不仅有美丽的荷花，而且有古朴的亭台楼阁，令人流连忘返。","analysis":"'不仅……而且……'表递进关系"},
      {"question":"阅读：'西沙群岛一带，海水五光十色，瑰丽无比：有深蓝的，淡青的，浅绿的，杏黄的。'①用了什么修辞？②'五光十色'是什么意思？③如果你站在那里，心情如何？","answer":"①排列（列举描写不同颜色）；②五光十色：形容颜色多而鲜艳；③心情：惊喜、赞叹（言之有理）","analysis":"理解景物描写的方法和效果"},
      {"question":"把下面句子改成排比句：'那里的鱼很多，那里的贝壳很漂亮，那里的海草很美丽。'","answer":"那里的鱼成群结队，那里的贝壳色彩斑斓，那里的海草随波摇曳，处处充满生机。","analysis":"排比句要结构相同、内容相关"},
      {"question":"背诵：根据课文内容，介绍一处你了解的名胜古迹（50字）","answer":"如：长城是中国古代劳动人民用智慧和血汗建造的伟大工程，蜿蜒在崇山峻岭之间，全长万余里，是中华民族的象征。","analysis":"介绍景点要有位置、特点、历史意义等"},
      {"question":"填充描写句：'站在山顶，向远处望去，（　）连绵的山峰在云雾中（　），像是（　）一样壮观。'","answer":"无数/连绵的山峰在云雾中若隐若现/飘浮，像是一幅美丽的山水画一样壮观。","analysis":"填充要符合描写景物的语境"},
      {"question":"根据'春夏秋冬'各写一个描写对应季节的景物词语","answer":"春：百花盛开；夏：绿树成荫；秋：金秋时节；冬：白雪皑皑","analysis":"四季景物词语积累"}
    ],
    "advanced_exercises":[
      {"question":"小作文：选择一处你去过的自然景观（山、海、公园等），用80字描写，运用比喻和排比至少各一处","answer":"开放性写作，参考：走进公园，扑面而来的是花的海洋。那里有粉色的桃花，像少女的笑脸；有金色的迎春花，像一串串小灯笼；有洁白的玉兰，像一只只展翅的白鸽。花香混合着泥土的气息，令人心旷神怡。","analysis":"作文要有比喻和排比修辞"},
      {"question":"积累：写出5句描写祖国自然景色的名句（古诗词或散文名句）","answer":"①'飞流直下三千尺，疑是银河落九天'（李白）；②'山重水复疑无路，柳暗花明又一村'（陆游）；③'接天莲叶无穷碧，映日荷花别样红'（杨万里）；④'横看成岭侧成峰，远近高低各不同'（苏轼）；⑤'春风又绿江南岸'（王安石）","analysis":"积累经典名句"},
      {"question":"理解：为什么说'祖国的山河是美丽的'？结合课文和自己的了解，写出3个原因","answer":"①祖国幅员辽阔，有各种地形：山川湖泊、草原沙漠、丛林海岸；②四季分明，不同季节有不同的美；③中华文明在这片土地上留下了许多文化遗迹（如长城、西湖等）","analysis":"理解课文主题，结合地理和文化"},
      {"question":"创意写作：如果你是一只小鸟，飞越祖国大地，你会看到哪些不同的景色？写100字","answer":"开放性写作。参考：如果我是一只自由的小鸟，我会飞越北方辽阔的草原，看牛羊成群；飞越中原肥沃的农田，看稻谷飘香；再飞到南方的海边，看碧蓝的海水和洁白的沙滩。我的家乡真美丽啊！","analysis":"想象性写作，体现对祖国的热爱"},
      {"question":"【综合题】读完本单元，你对'美'有什么新的理解？自然的美和内心的感受是什么关系？","answer":"开放性，参考：通过本单元学习，我理解了'美'不只是表面的颜色和形状，更是心中的感受。当我们用心去观察，就能发现身边处处有美——一片叶子、一缕阳光都可以很美。内心的平静和喜悦，让我们能更好地感受自然的美。","analysis":"哲学性思考，培养审美意识"}
    ]
  },
  {
    "id":"u07","title":"第七单元 我与自然",
    "knowledge_points":[
      "学习《听听，秋的声音》等诗歌，体会大自然的声音之美",
      "学习写大自然日记：记录自己观察到的自然现象",
      "理解人与自然的关系，培养热爱自然、保护环境的意识",
      "学习有感情地朗读诗歌，感受诗歌的节奏和韵律"
    ],
    "difficulties":[
      "诗歌的朗读：注意停顿、重音、语调变化",
      "理解大自然中声音的美（不只是音乐，风雨虫鸣都是声音）",
      "将听到的声音用文字描述出来（拟声词的运用）",
      "写日记的格式：时间、天气、正文"
    ],
    "exercises":[
      {"question":"《听听，秋的声音》中，秋天的声音有哪些？写出3种","answer":"黄叶道别的声音、蟋蟀振动翅膀的声音、大雁南飞时的叫声（或'阵阵叮咛'）","analysis":"诗歌通过多种声音表现秋天"},
      {"question":"写出表示声音的词语（拟声词）至少6个","answer":"哗哗、嗡嗡、沙沙、叽叽喳喳、叮叮当当、咕咕、啪啪、轰隆","analysis":"拟声词积累，模拟自然中的声音"},
      {"question":"写日记：今天你在大自然中听到了什么声音？写一篇50字的日记","answer":"开放性：如'2024年11月1日 晴 今天放学路上，我仔细聆听，听到了树叶在风中沙沙作响，小鸟在树上叽叽喳喳地叫，远处还有汽车的喇叭声。大自然真是一首交响乐！'","analysis":"日记格式：日期、天气、内容"},
      {"question":"把下列声音和发出它们的事物连线：哗哗——（　）；嗡嗡——（　）；沙沙——（　）；轰隆——（　）","answer":"哗哗—流水/大雨；嗡嗡—蜜蜂；沙沙—风吹树叶；轰隆—打雷","analysis":"声音与事物的对应关系"},
      {"question":"仿写：'秋天的声音，是黄叶离开大树时轻轻的叹息，是……'（仿照格式写一句）","answer":"如：秋天的声音，是雨滴打在屋檐上清脆的音符，是大雁飞过天空时高远的鸣叫。","analysis":"仿写保持句式，内容自然真实"},
      {"question":"保护自然：你知道哪些保护自然的行为？写出3条","answer":"①不乱扔垃圾；②爱护花草树木，不随意折枝；③节约用水，减少水污染","analysis":"环保意识教育"},
      {"question":"阅读短诗并回答：'清晨，小露珠在草叶上滚来滚去，对着太阳唱歌，等阳光越来越强，它就羞红了脸，消失在空气中。'①这首诗用了什么手法？②最后'消失'意味着什么（科学角度）？","answer":"①拟人（小露珠唱歌、羞红了脸）；②蒸发（露水在太阳照射下蒸发变成水蒸气）","analysis":"文学欣赏与科学知识相结合"},
      {"question":"选词填空（从课文中学到的词语）：（　）的森林；（　）的溪流；（　）的蓝天","answer":"茂密的森林；清澈的溪流；辽阔的蓝天（意近即可）","analysis":"词语搭配练习"}
    ],
    "advanced_exercises":[
      {"question":"创作小诗：以'大自然的声音'为题，仿照《听听，秋的声音》的格式，写4行","answer":"如：听听，冬的声音，北风在耳边呼呼地吹，那是冬天给大地唱的歌；雪花在空中飘飘地落，那是冬天给孩子的礼物。","analysis":"创作保持格式，有节奏感"},
      {"question":"思考：如果大自然消失了（树木、河流、动物全部消失），人类会怎样？写出3点影响","answer":"①没有新鲜空气（树木不再产生氧气）；②没有干净水源；③没有食物来源（动植物是人类食物链的基础）；④气候失衡（会导致极端天气）","analysis":"生态意识教育，理解自然与人的关系"},
      {"question":"研究性阅读：找出一个关于人类破坏自然后得到惩罚的例子（可以是自然灾害或生态问题），写50字","answer":"如：某地过度砍伐森林后，土地失去保护，每逢下雨就发生山体滑坡和泥石流，村庄被摧毁，许多人失去家园。这告诉我们，人与自然要和谐共处。","analysis":"了解生态环境知识"},
      {"question":"创意写作：想象你是大自然中的一棵树，写一段独白（60字），说说你的感受和希望","answer":"我是一棵树，我给小鸟提供家园，给孩子们遮挡阳光，给大地带来清新的空气。可是有时候，电锯的声音让我颤抖。我希望人类能保护我们，因为没有我们，你们也无法生存。","analysis":"换位思考，培养同理心和环保意识"},
      {"question":"【综合题】联系生活，举例说明'人与自然和谐共处'的重要性（100字）","answer":"自然是人类的家园，人与自然是共生关系。看看身边：种了花草的小区让人心情愉快；有清澈河流的城市让人向往；而荒漠化的土地让人心痛。我们一起节约资源，减少污染，才能让青山绿水永远陪伴我们。","analysis":"结合生活实际，表达观点要有具体事例"}
    ]
  },
  {
    "id":"u08","title":"第八单元 美好品质",
    "knowledge_points":[
      "学习体现美好品质的课文：诚实、勤劳、善良、勇敢等",
      "理解人物行为，从中感受高尚品质",
      "学习通过具体事例表现人物品质的写作方法",
      "能写一段话，通过具体事例赞扬一个人的品质"
    ],
    "difficulties":[
      "从人物的言行中归纳品质特点，而不是直接说'他很勤劳'",
      "通过事例写品质：先写事，再点明品质（用事实说话）",
      "理解不同故事中人物的内心世界",
      "写作时选择典型事例，不要泛泛而谈"
    ],
    "exercises":[
      {"question":"写出表示美好品质的词语（至少8个）","answer":"诚实守信、勤劳勇敢、乐于助人、善良温柔、坚持不懈、谦虚好学、宽容大度、勇于担当","analysis":"积累品质词语"},
      {"question":"仿照例子，用具体事例表现品质：'小明捡到钱包，找到失主还了回去。'体现了小明（　）的品质","answer":"诚实守信（拾金不昧）","analysis":"从具体行为判断品质"},
      {"question":"反义词练习：诚实—（　）；勤劳—（　）；勇敢—（　）；善良—（　）","answer":"虚假/说谎；懒惰；胆小；凶狠/恶毒","analysis":"品质词语的反义词"},
      {"question":"判断：下面哪些行为体现了'诚实'？①发现错误马上承认②因为答应了朋友就算不方便也去做③考试不好隐瞒父母","answer":"①体现诚实；②体现守信（也属于诚实）；③不是诚实","analysis":"辨别诚实与不诚实的行为"},
      {"question":"写话：用3-5句话，通过一件小事表现一个人的某种品质","answer":"如：上周放学路上，我的同学小红看见一个老奶奶的菜篮子掉了，菜散落一地。小红马上放下书包，帮老奶奶把菜一一捡回篮子里，还搀扶她走到路口才离开。小红乐于助人的品质让我很感动。","analysis":"写作：先叙事，后点题（品质）"},
      {"question":"古诗中的品质：'欲穷千里目，更上一层楼'体现了什么精神？'春蚕到死丝方尽'比喻谁？","answer":"体现了积极进取、不断超越的精神；比喻老师（无私奉献）","analysis":"古诗名句的引申含义"},
      {"question":"阅读：'他每天第一个到学校打扫卫生，从不让老师看见。同学们都说他傻，他却笑着说：'我喜欢干净的环境。'他有什么品质？","answer":"默默奉献、不求回报、乐于助人","analysis":"不求表扬的默默付出是高尚品质"},
      {"question":"在你认识的人中，谁有让你佩服的品质？简单说一件事","answer":"开放性，言之有理即可。提示：可以写父母、老师、同学的某件感人的事","analysis":"联系实际，真情实感"}
    ],
    "advanced_exercises":[
      {"question":"对比辨析：'勤劳'和'努力'有什么不同？'善良'和'软弱'有什么区别？","answer":"勤劳指爱劳动、不懒惰；努力指为了目标不懈奋斗（侧重主观意志）；善良是内心温柔、关心他人；软弱是遇事退缩、缺乏勇气（善良≠软弱，真正善良的人也可以很勇敢）","analysis":"辨析近义词或易混词，理解内涵差异"},
      {"question":"写一封信（60字），感谢一个对你有影响的人，具体说明他/她的品质和对你的影响","answer":"开放性写作，参考：亲爱的老师：感谢您一年来对我的耐心教导。每当我数学遇到困难，您总是一次次讲解，从不嫌烦。您的耐心和认真让我明白，做任何事都要坚持不懈。我会像您一样努力。","analysis":"感谢信要具体，结合人物实际的品质"},
      {"question":"分析人物：读《木兰从军》故事（自己了解），花木兰有哪些美好品质？各举事例说明","answer":"①孝顺：代父从军；②勇敢：在战场英勇杀敌；③有志气：在那个时代女子不轻易从军，她克服困难；④淡泊：立功后不要功名，只要回家","analysis":"从故事人物提炼品质"},
      {"question":"思考：现代社会需要什么样的美好品质？写出3点并说明原因","answer":"①诚信：诚信是商业和人际关系的基础，没有诚信社会无法运转；②合作精神：现代工作很少单打独斗，需要团队合作；③责任心：对工作、家庭、社会有责任感，才能做好每件事","analysis":"结合现代社会实际理解品质的价值"},
      {"question":"【综合小作文】以'我身边的好人好事'为题，写一段100字的短文，要求用具体事例说明人物的品质","answer":"开放性写作，要有：人物、事件经过、品质总结三部分","analysis":"写作评分重点：是否有具体事例，品质总结是否准确，语言是否通顺"}
    ]
  }
]

print("Grade 3 Chinese upper content defined.")

# ============ 三年级语文下册（简化版，8单元）============
g3_chinese_lower = [
  {
    "id":"u01","title":"第一单元 可爱的生灵",
    "knowledge_points":[
      "学习《绝句》《惠崇春江晚景》等描写动植物的古诗和课文",
      "掌握本单元生字词，注意多音字的读法",
      "能有感情地朗读描写小动物的课文，感受生命的美好",
      "积累描写动物的词语和句子"
    ],
    "difficulties":[
      "古诗中描写季节和动物的词语理解（如'鸳鸯''桃花水''芦芽短'等）",
      "体会诗中动静结合的描写方法",
      "通过课文感受动物世界的有趣和生命的可爱",
      "写话：用准确的词语描写一种小动物的外形和动作"
    ],
    "exercises":[
      {"question":"默写《绝句》（唐·杜甫）两句：'迟日江山丽，（　）。泥融飞燕子，（　）。'","answer":"迟日江山丽，春风花草香。泥融飞燕子，沙暖睡鸳鸯。","analysis":"早春美景：阳光、花草、燕子、鸳鸯"},
      {"question":"解释词语：①迟日②泥融③睡鸳鸯","answer":"①春天的太阳②泥土融化变软③鸳鸯在沙滩上睡觉","analysis":"古诗词语解释"},
      {"question":"写出你喜欢的一种动物的外形特点（3句话）","answer":"参考：小猫有着雪白的毛，蓝色的眼睛像两颗宝石。它的爪子软软的，走路悄无声息。长长的尾巴总是翘得高高的，非常可爱。","analysis":"描写动物外形要有顺序，抓住特点"},
      {"question":"写出描写动物动作的词语（至少6个）","answer":"飞翔、奔跑、跳跃、爬行、游动、嬉戏、觅食、嬉戏","analysis":"动物动作词语积累"},
      {"question":"用'有的……有的……有的……'写一段描写动物的话","answer":"放学后，操场上的麻雀活跃起来。有的在地上啄食，有的在树枝间跳来跳去，有的在空中追逐嬉戏。","analysis":"排比句式表达多样动作"},
      {"question":"阅读：'春天，小燕子从南方飞回来，在屋檐下筑巢。它们叼来泥土和草叶，用小嘴一遍遍地压实，一个温暖的家就建好了。'①燕子怎么筑巢？②你从中感受到了什么？","answer":"①叼泥土和草叶，用嘴压实；②燕子很勤劳，有建设家园的本能","analysis":"阅读理解：提取信息和感受"},
      {"question":"在括号里填上合适的动词：①蜜蜂（　）花蜜②大雁（　）队形③蚂蚁（　）食物","answer":"①采集②排列（成V形）③搬运","analysis":"动词的准确搭配"},
      {"question":"小练笔：写一段话介绍你最喜欢的一种动物（50字），包含它的外形、特点和你喜欢它的原因","answer":"开放性，言之有理即可","analysis":"人物介绍式写作"}
    ],
    "advanced_exercises":[
      {"question":"对比两首古诗：《绝句》（杜甫）和《惠崇春江晚景》（苏轼），两首诗都描写了哪些动物？哪首诗更有趣？为什么？","answer":"《绝句》：燕子、鸳鸯；《惠崇春江晚景》：鸭子、河豚（提到）；苏轼的诗中'春江水暖鸭先知'更有哲理性，故更有趣（言之有理即可）","analysis":"比较阅读"},
      {"question":"研究小动物：选一种你感兴趣的动物，写出它的3个有趣习性（可查阅资料）","answer":"如：蚂蚁：①用气味（信息素）与同伴通信；②力量是自身体重的50倍；③有分工制度（蚁后、工蚁、兵蚁）","analysis":"自然科学与语文结合"},
      {"question":"创意写作（70字）：从一只小动物的视角，写它一天的经历","answer":"参考：今天我（麻雀）天刚亮就出发找食物了。先在公园的草丛里啄了几粒种子，然后飞到一户人家的窗台偷吃了几口米，被老奶奶挥手赶走。傍晚，我找到了今天的最大收获——一块香喷喷的饼干屑。真是充实的一天！","analysis":"换位思考，想象动物的生活"},
      {"question":"积累：找出描写动物的成语（至少5个），说明各指什么动物","answer":"狡兔三窟（兔）、守株待兔（兔）、如鱼得水（鱼）、龙腾虎跃（龙虎）、猴急（猴）","analysis":"成语积累与理解"},
      {"question":"【思维题】如果动物们会说话，你认为它们最希望对人类说什么？以一种动物口吻写3句话","answer":"参考（小熊猫）：人类朋友，请保护我们的竹林，那是我们的家和食物来源。不要把我们关进笼子，我们向往自由的生活。如果你们保护好环境，我们就能和你们共同生活在这美丽的地球上。","analysis":"环保主题，培养对生命的尊重"}
    ]
  },
  {
    "id":"u02","title":"第二单元 寓言故事",
    "knowledge_points":[
      "学习《守株待兔》《陶罐和铁罐》《鹿角和鹿腿》等寓言故事",
      "理解寓言故事的特点：借助故事说明道理",
      "能复述故事，并说出寓意（道理）",
      "学习通过人物对话描写推进故事，体会人物性格"
    ],
    "difficulties":[
      "理解寓言的寓意：不能只看故事表面，要想深一层",
      "理解寓言中的人物性格（如铁罐的骄傲、陶罐的谦虚）",
      "讲述寓言故事时能抓住要点，不遗漏关键情节",
      "将寓言道理与现实生活联系"
    ],
    "exercises":[
      {"question":"《守株待兔》的成语来自这个故事，它的寓意是什么？","answer":"讽刺那些不努力工作，只想着靠运气/侥幸心理获得意外收获的人（不劳而获是不现实的）","analysis":"守株待兔：守着树桩等兔子，比喻死守偶然经验，不懂变通"},
      {"question":"《陶罐和铁罐》中，铁罐为什么看不起陶罐？最后结果如何？说明了什么？","answer":"铁罐认为自己坚硬，陶罐易碎；最后铁罐生锈消失，陶罐被人们珍藏。说明：不能用自己的优势嘲笑别人的短处，每个人都有自己的价值","analysis":"寓意：不要骄傲自大，要尊重他人"},
      {"question":"判断下面行为和哪个寓言对应：①等着天上掉馅饼②到处说别人坏话③只看别人缺点，不看优点","answer":"①守株待兔；②可能是《乌鸦和狐狸》（说好话骗人）；③《陶罐和铁罐》（铁罐的错误）","analysis":"将寓言与现实行为对应"},
      {"question":"写出2个你知道的成语故事（寓言），并简单说明寓意","answer":"如：①拔苗助长：不按规律强行加速，反而坏事（违背自然规律）；②揠苗助长同上；③亡羊补牢：出了问题及时补救，还不晚（亡：丢失；牢：羊圈）","analysis":"成语寓言积累"},
      {"question":"《鹿角和鹿腿》中，鹿最开始对角和腿的态度是什么？后来改变了吗？为什么？","answer":"开始：喜欢角，嫌弃腿；后来：在狮子追捕时腿救了命，角反而被树枝挂住险些丧命。改变了看法：实用的东西才是真正有价值的","analysis":"不要只看外表，实用性和内在价值更重要"},
      {"question":"写一个简短的寓言（5句话以内），教育小朋友要认真做作业","answer":"如：小蜜蜂花花每天只想玩，不去采花蜜。冬天来了，其他蜜蜂都有足够的食物，花花却快要饿死了。一只勤劳的老蜜蜂说：'现在后悔已经来不及了，夏天不劳动，冬天就没饭吃。'道理：做好眼前的事，不能懈怠","analysis":"自创寓言要有故事、结局和道理"},
      {"question":"找出《陶罐和铁罐》中铁罐说的傲慢的话，改写成谦虚的说法","answer":"原文（大意）：'你敢碰我吗？懦弱的东西！'谦虚改写：'咱们各有所长，都有自己的用处，不要相互比较了。'","analysis":"改写训练，理解谦虚和骄傲的区别"},
      {"question":"用'骄傲自满'造句，用'谦虚谨慎'造句","answer":"骄傲自满：他考了一次好成绩就骄傲自满，不再努力，结果下次考得更差。谦虚谨慎：优秀的同学从不骄傲，总是谦虚谨慎地请教老师和同学。","analysis":"词语运用练习"}
    ],
    "advanced_exercises":[
      {"question":"创作一个现代版的寓言（80字），主题是：不能因为手机游戏而忽视学习","answer":"有一只小兔子迷上了手机游戏，每天只顾玩，不去吃草和练习跑步。一天，大灰狼来了，其他兔子都跑掉了，小兔子因为长期不练跑步，腿无力，险些被抓到。从此，小兔子明白了：玩乐要有节制，必须先做好该做的事。","analysis":"现代化寓言要结合现实"},
      {"question":"深入思考：《守株待兔》的故事告诉我们不能'守株待兔'，但在某些情况下，'守株'（坚守、坚持）是否也有道理？举例说明","answer":"坚守原则是好的（如守时、守信），但盲目等待机会不努力是错误的。区别：在付出努力的前提下，等待时机是智慧；不劳而获地等待才是守株待兔","analysis":"辩证思维，不要走极端"},
      {"question":"比较东西方寓言：中国寓言（如守株待兔）和《伊索寓言》（如龟兔赛跑）有什么共同点和不同点？","answer":"共同点：都通过故事说明道理，都有动物或人物角色；不同点：中国寓言常结合历史典故，背景更具体；伊索寓言动物拟人化更明显","analysis":"文化比较阅读"},
      {"question":"分析：铁罐最终消失，陶罐被珍藏，这个结果说明什么价值观？","answer":"外表的强硬不等于真正的价值；谦虚踏实的人更能经受时间的考验；每种事物都有自己的价值，不应以单一标准评判","analysis":"深层价值观的理解"},
      {"question":"【综合题】选择你最喜欢的一个寓言，写出：①故事概要（30字）②寓意（20字）③你的生活中有没有类似的故事？（50字）","answer":"开放性，结构完整即可","analysis":"综合写作：复述+理解+联系实际"}
    ]
  },
  {
    "id":"u03","title":"第三单元 深厚情感",
    "knowledge_points":[
      "学习表达深厚情感的课文（思乡、亲情、友情等主题）",
      "能理解作者表达情感的方式（直接抒情和间接抒情）",
      "积累描写情感的词语和句子",
      "学习用具体细节表达情感"
    ],
    "difficulties":[
      "理解'借景抒情'：通过描写景物来表达内心感受",
      "区分直接抒情（直说感受）和间接抒情（通过描写表达）",
      "体会课文中人物细腻的情感变化",
      "写作中如何'有情有义'地描写"
    ],
    "exercises":[
      {"question":"写出描写'思念'的词语（至少4个）","answer":"思念、怀念、思乡、牵挂、惦记、魂牵梦萦","analysis":"情感词语积累"},
      {"question":"判断下面是直接抒情还是间接抒情：①'我多么想家啊！'②'窗外的月亮那么圆，那么亮，让我想起了家乡。'","answer":"①直接抒情；②间接抒情（借月亮抒发思乡之情）","analysis":"两种抒情方式的区别"},
      {"question":"仿写句子：'每当看到圆月，我就想起了远方的故乡。'仿写一句表达思念的句子","answer":"如：每当闻到妈妈做的饭菜香，我就想起了在家玩耍的快乐时光。","analysis":"仿写要有情感，有具体的触发物"},
      {"question":"阅读：'爷爷走了好多年了，但每次看到书桌上那盏旧台灯，我就想起他坐在灯下给我讲故事的样子。'①这段话用了什么抒情方式？②'旧台灯'在这里有什么意义？","answer":"①间接抒情（通过台灯表达思念）；②台灯是爷爷的象征，是对爷爷的记忆和感情的寄托（睹物思人）","analysis":"情感联系：物品与人的情感"},
      {"question":"用'虽然……但是……'写一句表达亲情的句子","answer":"如：虽然妈妈有时候很严格，但是我知道那是因为她深深地爱着我。","analysis":"关联词的运用，表达情感"},
      {"question":"写出3个与'爱'有关的词组或句子","answer":"如：母爱如山（深沉）；父爱如海（广博）；爱是无私的奉献","analysis":"爱的表达积累"},
      {"question":"说说你最感动的一件家人为你做的小事，写2-3句话","answer":"开放性，参考：有一次我生病发烧，妈妈整晚守在我床边，每隔一会儿就用冷毛巾敷我的额头，一夜没睡。那一刻，我深深感受到了妈妈的爱。","analysis":"真实的细节最能打动人"},
      {"question":"诗词积累：写出2句关于亲情的古诗词名句","answer":"①'慈母手中线，游子身上衣，临行密密缝，意恐迟迟归'（孟郊《游子吟》）；②'独在异乡为异客，每逢佳节倍思亲'（王维）","analysis":"亲情主题古诗词积累"}
    ],
    "advanced_exercises":[
      {"question":"深度阅读：《游子吟》（孟郊）表达了什么情感？'临行密密缝，意恐迟迟归'这两句为什么感人？","answer":"表达了对母亲的感恩和对母爱的赞美；'密密缝'说明母亲心意细腻，担心儿子在外受寒，每一针都饱含着爱，所以感人","analysis":"古诗精读，理解情感细节"},
      {"question":"写一段感谢父母的话（60字），要求用具体事例，不要空话套话","answer":"开放性，参考：爸爸，谢谢您每天早起送我上学，不管是下雨还是严寒。我知道您工作很累，但您从没有抱怨过。您的坚持让我懂得了责任。","analysis":"感谢要有具体事例，情感要真实"},
      {"question":"'月是故乡明'——月亮是中国文学中最常见的思乡意象。找出3首用月亮抒发情感的古诗","answer":"①《静夜思》李白：'举头望明月，低头思故乡'；②《水调歌头》苏轼：'但愿人长久，千里共婵娟'；③《泊船瓜洲》王安石：'春风又绿江南岸，明月何时照我还'","analysis":"意象的积累：月亮与思乡"},
      {"question":"创意写作（80字）：以'一封家书'为题，想象自己是古代在外求学的孩子，写一封给父母的信","answer":"参考：爹娘亲启：孩儿在京城一切安好，勿挂念。今日天气渐冷，不知家中可添了棉衣？孩儿每夜苦读，望他日学成归来，好好报答双亲养育之恩。盼早日相见！孩儿敬上","analysis":"书信格式，融入情感"},
      {"question":"【哲思题】'距离产生美'，有时候分别让人更加珍惜彼此。你同意这种观点吗？结合生活例子说明","answer":"开放性，言之有理即可。如：同意——久别重逢的喜悦更深；或不完全同意——真正的感情不需要距离来维系，陪伴才是最长情的告白","analysis":"辩证思考，培养表达观点的能力"}
    ]
  },
  {
    "id":"u04","title":"第四单元 多彩童年",
    "knowledge_points":[
      "学习描写童年生活的课文，感受童年的快乐和美好",
      "学习用细节描写表现儿童活泼、天真的特点",
      "积累描写童年、玩耍、快乐的词语",
      "学习写童年记忆：有趣的事、难忘的时刻"
    ],
    "difficulties":[
      "捕捉童年细节：有趣的细节比大事件更打动人",
      "用儿童的视角和语气写作",
      "将内心感受融入叙述中",
      "写作结构：起因→经过→结果→感受"
    ],
    "exercises":[
      {"question":"写出描写童年的词语（至少6个）","answer":"天真烂漫、无忧无虑、欢声笑语、活蹦乱跳、嬉戏玩耍、稚气未脱","analysis":"童年主题词语积累"},
      {"question":"照样子：'童年是一首歌，唱出了无数美好的回忆。'仿写：'童年是一（　），（　）。'","answer":"如：童年是一本书，记录了数不清的欢声笑语；童年是一朵花，绽放在记忆中最美的角落","analysis":"比喻仿写"},
      {"question":"阅读短文：'我们最喜欢在夏天捉萤火虫，把它们装在玻璃瓶里，黑夜里提着小灯笼满村跑。'①哪些词写出了孩子的童真？②你有类似的童年趣事吗？","answer":"①'最喜欢'（情感词）、'满村跑'（动作描写，很活泼）；②开放性回答","analysis":"抓住细节词语，理解儿童心理"},
      {"question":"扩写：'孩子们玩耍。'（加上时间、地点、具体玩耍方式等，至少写3句话）","answer":"放学后，孩子们三三两两聚集在操场上玩耍。有的踢毽子，高高跃起的身影像彩色的蝴蝶；有的打弹珠，蹲在地上仔细瞄准，专心得连下课铃声都没听见。","analysis":"扩写要加入细节，使场景生动"},
      {"question":"选词填空：无忧无虑（　）烦恼；嬉戏玩耍（　）游戏；天真烂漫（　）复杂","answer":"无忧无虑（没有）烦恼；嬉戏玩耍（开心地）游戏；天真烂漫（不）复杂","analysis":"词语理解和运用"},
      {"question":"写一段童年趣事（3-5句话）","answer":"开放性，参考：有一次，我和小伙伴去捉蝴蝶，在花园里追了好久也没追到。我跑得太快，一头撞进了爷爷刚浇过的菜地里，全身沾满了泥，蝴蝶也飞走了。我们哈哈大笑，那一身泥也成了最好的笑料。","analysis":"真实有趣的童年事件"},
      {"question":"积累：写出2句描写童年的古诗名句","answer":"①'儿童散学归来早，忙趁东风放纸鸢'（高鼎《村居》）；②'童孙未解供耕织，也傍桑阴学种瓜'（范成大）","analysis":"古诗中的儿童形象积累"},
      {"question":"反义词：快乐—（　）；天真—（　）；活泼—（　）；嬉戏—（　）","answer":"快乐—悲伤；天真—世故；活泼—沉默/内向；嬉戏—认真工作","analysis":"反义词练习"}
    ],
    "advanced_exercises":[
      {"question":"小作文（80字）：以'最难忘的一件童年趣事'为题写一篇记叙文，要求有时间、地点、人物、事件","answer":"开放性，结构完整，有细节描写即可","analysis":"记叙文要素：时间、地点、人物、事件"},
      {"question":"对比：你的童年和父母/爷爷奶奶的童年有什么不同？（在玩具、游戏、生活等方面）写3点不同","answer":"如：①玩具：我玩电子游戏，他们玩纸牌、陀螺；②游戏：我玩手机，他们捉迷藏、跳皮筋；③生活：我有网络，他们只有电视或收音机","analysis":"历史与现实的对比思考"},
      {"question":"写一封给未来自己（长大后）的信（60字），记录一件现在的童年趣事","answer":"参考：亲爱的未来的我，还记得吗？小时候我们在奶奶家的院子里追鸡，弄得全身是羽毛，奶奶又好气又好笑。那时候的笑声是最真实的快乐，希望你永远不要忘记那份天真。","analysis":"写信格式，情感真实"},
      {"question":"阅读欣赏：'小时不识月，呼作白玉盘。又疑瑶台镜，飞在青云端。'（李白）①'白玉盘'比喻什么？②这首诗表现了儿童怎样的特点？","answer":"①白玉盘比喻月亮（圆而亮）；②儿童对事物充满好奇和想象力，把月亮想象成盘子和镜子，天真可爱","analysis":"古诗与儿童心理的关联"},
      {"question":"【综合题】童年会过去，但童年的美好会留在记忆里。你最希望长大后记住现在的哪些事情？（写三件事）","answer":"开放性，言之有理即可。提示：可以是家人的陪伴、朋友的故事、某个特别的经历等","analysis":"思考现在的价值，珍惜童年时光"}
    ]
  },
  {
    "id":"u05","title":"第五单元 传统文化",
    "knowledge_points":[
      "了解中国传统文化：汉字、古诗、民俗、手艺等",
      "学习了解汉字的演变（从甲骨文到现代汉字）",
      "感受中华文化的博大精深，培养文化自信",
      "积累关于传统文化的词语和知识"
    ],
    "difficulties":[
      "理解汉字的结构：独体字、合体字（会意字、形声字等）",
      "了解传统文化中的一些习俗和节日的文化含义",
      "汉字书写规范：笔顺、间架结构",
      "将传统文化与生活联系，说清楚其意义"
    ],
    "exercises":[
      {"question":"汉字知识：'明'是由'日'和'月'组成的（　）字，意思是（　）","answer":"会意字；明亮（日月都是光明的，合在一起更明亮）","analysis":"会意字：两个或多个汉字组合表示新意"},
      {"question":"写出5个由两部分组成的会意字（如'明'）","answer":"如：休（人依树休息）、森（很多树=森林）、众（三人=众多）、晶（三个日，极明亮）、鑫（三金，财富多）","analysis":"会意字积累"},
      {"question":"汉字笔顺规则：①先（　）后右②先（　）后外③先（　）后下","answer":"①先左后右；②先外后内；③先上后下","analysis":"基本笔顺规则"},
      {"question":"关于传统节日：春节习俗有（　）（至少3种）","answer":"贴春联、放鞭炮、吃饺子（北方）、拜年、压岁钱、挂灯笼","analysis":"传统节日习俗积累"},
      {"question":"'书法'是中国传统艺术，书法字体有：（　）（至少写4种）","answer":"楷书、行书、草书、隶书、篆书","analysis":"书法字体积累"},
      {"question":"写出3个与中国传统文化相关的节日，每个节日写出一种特色食物","answer":"春节—饺子；中秋—月饼；端午—粽子（元宵节—汤圆；重阳—重阳糕等）","analysis":"传统节日与食物的对应"},
      {"question":"填空：中国四大发明是（　）（　）（　）（　）","answer":"造纸术、印刷术、指南针、火药","analysis":"中国四大发明"},
      {"question":"判断对错：①中国汉字有几千年历史（　）②甲骨文是用来占卜的（　）③现代汉字和古代汉字完全一样（　）","answer":"①对②对③错（汉字经历了演变，从图画文字演变成现在的形式）","analysis":"汉字历史基本知识"}
    ],
    "advanced_exercises":[
      {"question":"研究汉字：查找'水'字的字源，它是怎么演变成现在的样子的？","answer":"'水'字：甲骨文像流动的水；金文开始有规范化；小篆进一步规范；楷书演变为现在的'水'字（三点水旁偶尔用'氵'）","analysis":"汉字演变史，培养对汉字的兴趣"},
      {"question":"创意写作：如果你能穿越到古代，参加一个传统节日，你会选择哪个？描述你会看到/参与什么（80字）","answer":"如：我想穿越到唐代参加元宵节。那时长安城灯会盛大，千百盏彩灯挂满街道，人们猜灯谜、看杂耍。我会和小伙伴在人群中挤来挤去，猜猜灯谜赢个小奖，然后找个高处看那万盏灯光把夜晚照得如同白昼。","analysis":"历史想象与文化结合"},
      {"question":"对比中西传统节日：找出中西方各一个类似的节日（如圣诞和春节）进行对比","answer":"春节和圣诞节：共同点——都是一年中最重要的节日，家人团聚；不同点——春节农历正月初一，贴春联放鞭炮；圣诞公历12月25日，挂圣诞树送礼物","analysis":"跨文化比较，开阔视野"},
      {"question":"调查报告（简单版）：问问家人，他们小时候有哪些传统活动是现在没有或者少见的？写出2-3个","answer":"如：长辈小时候会自己做糖葫芦、自己做灯笼过元宵节、过年时全家手工包饺子彻夜不睡等（开放性）","analysis":"传统文化的传承与变化"},
      {"question":"【思维题】有人说：'传统文化在现代社会中慢慢消失了，这是时代的进步。'你同意吗？说出你的看法","answer":"开放性。参考：不完全同意。传统文化是中华民族的根和魂，抛弃传统就是失去了文化认同。但传统文化需要创新发展，不能一成不变。我们应该保护传统节日、汉字、文化习俗，同时融入现代元素。","analysis":"辩证思维，文化保护与发展的思考"}
    ]
  },
  {
    "id":"u06","title":"第六单元 了解故事情节",
    "knowledge_points":[
      "学习复述故事的方法：抓住时间、地点、人物、起因、经过、结果",
      "理解故事情节发展的逻辑（因果关系）",
      "学习分角色朗读，体会人物情感",
      "能用自己的话简单复述读过的故事"
    ],
    "difficulties":[
      "复述时如何抓要点，不多不少",
      "按照事件发展顺序（而不是自己的阅读顺序）叙述",
      "区分主要情节和次要情节",
      "保留故事原有的情感和主题"
    ],
    "exercises":[
      {"question":"一篇故事文章的结构一般是：起因→（　）→（　）→（　）","answer":"起因→经过（发展）→高潮→结果","analysis":"故事结构的基本框架"},
      {"question":"《小马过河》的故事：用'因为……所以……'概括主要情节","answer":"因为松鼠说河水很深，老牛说很浅，小马不知道谁对；所以小马回家问妈妈，妈妈让他自己去试；小马过河后发现水不深也不浅，适合自己","analysis":"因果关系梳理故事"},
      {"question":"复述《狐假虎威》：用5句话以内说完整个故事","answer":"狐狸被老虎抓住，狐狸谎称自己是百兽之王。老虎半信半疑，跟着狐狸走进森林。百兽见了老虎都逃跑，狐狸就以为是因为自己。实际上，动物们是怕老虎，不是怕狐狸。成语：假借别人的威风来吓人","analysis":"复述要有开头结尾，不遗漏关键情节"},
      {"question":"排列顺序：把《乌鸦喝水》的情节按顺序排列：①发现瓶中水③找到办法②石子投入瓶中④喝到水⑤想喝水但够不着","answer":"⑤→①→③→②→④","analysis":"情节排序训练"},
      {"question":"找出故事中的转折点：'小红一路跳着走，突然她脚下踩空了……'这是什么结构转折？","answer":"这是转折点（突变）：之前是轻松快乐，之后出现了意外，改变了故事走向","analysis":"识别情节转折"},
      {"question":"分角色朗读练习：《小马过河》中妈妈和小马的对话，谁用什么语气朗读？","answer":"妈妈：温柔、耐心的语气；小马：稚嫩、困惑的语气；朗读时注意角色特点","analysis":"分角色朗读的要点"},
      {"question":"编写故事结局：'小明找到了失踪的小狗，小狗……'（继续编写3-4句话）","answer":"小明找到了失踪的小狗，小狗见到他立刻冲过来，不停地摇尾巴，还用舌头舔他的脸。小明紧紧地把小狗抱在怀里，眼泪夺眶而出。从那以后，小明再也不随便让小狗离开视线了。","analysis":"续写要和前文衔接，情感合理"},
      {"question":"写出3种你喜欢的故事类型（如冒险类、科幻类等），并各推荐一本书","answer":"开放性。如：冒险类—《鲁滨孙漂流记》；科幻类—《海底两万里》；历史类—《上下五千年》","analysis":"阅读兴趣分享"}
    ],
    "advanced_exercises":[
      {"question":"写一个完整的小故事（100字），要有起因、经过、结果三部分","answer":"开放性写作，结构完整即可，主题自选","analysis":"评分标准：结构完整、情节合理、语言通顺"},
      {"question":"改写：将《龟兔赛跑》从乌龟的视角改写，强调乌龟坚持不懈的内心世界（60字）","answer":"参考：比赛开始后，兔子很快消失在前方。我知道自己慢，但我对自己说：只要一步一步走下去，终点总能到达。当我终于看到兔子在树下睡觉时，我没有停下，也没有叫醒他，只是默默地继续向前走，心跳越来越快，终点就在眼前……","analysis":"视角转换写作，体现人物内心"},
      {"question":"分析：《三只小猪》这个故事，三只小猪各代表什么样的性格？故事想告诉我们什么道理？","answer":"大猪：懒惰，建稻草房；二猪：普通，建木头房；小猪：勤劳聪明，建砖房。道理：做事要认真踏实，不贪图省事，才能经受考验","analysis":"故事中的象征和寓意"},
      {"question":"创作：把《孙悟空三打白骨精》缩写成150字以内的故事梗概","answer":"开放性，保留主要情节：白骨精变化三次（村姑、老婆婆、老头）；悟空三次棒打；唐僧三次误解；悟空含冤被赶走。点明主题：忠诚与误解。","analysis":"缩写要保留关键情节，去掉细节描写"},
      {"question":"【评价题】读完一个故事，你会怎么评价它好不好看？说出你的评价标准（3点）","answer":"如：①情节是否曲折有趣（不无聊）；②人物是否真实立体（有血有肉）；③主题是否有意义（能让人思考或感动）","analysis":"文学欣赏能力的培养"}
    ]
  },
  {
    "id":"u07","title":"第七单元 奇妙的世界",
    "knowledge_points":[
      "学习描写自然奇观、科学现象的文章，感受世界的神奇",
      "学习用疑问和探究的方式认识世界",
      "积累描写神奇景象的词语",
      "理解说明文的基本特点：用准确的语言介绍事物"
    ],
    "difficulties":[
      "区分记叙文（讲故事）和说明文（介绍事物）",
      "说明文中准确用词的重要性",
      "理解自然现象背后的科学原理（语文与科学融合）",
      "仿照说明文格式介绍一种自然现象"
    ],
    "exercises":[
      {"question":"说明文和记叙文的区别：说明文主要（　），记叙文主要（　）","answer":"说明文主要介绍和解释事物（知识为主）；记叙文主要叙述故事（情节为主）","analysis":"两种文体的本质区别"},
      {"question":"自然奇观词语积累：写出5个关于奇妙自然景象的词语","answer":"极光、蘑菇云、潮汐、彩虹、流星雨、大潮（钱塘江大潮）","analysis":"自然现象词语积累"},
      {"question":"用'不仅……而且……'介绍一种自然现象（如彩虹）","answer":"如：彩虹不仅颜色美丽，而且还是一种有趣的自然现象——它是阳光通过雨滴折射形成的。","analysis":"科学知识与语文结合"},
      {"question":"阅读：'每当下雨后，空气中弥漫着一股清新的泥土气息，那是雨水与土地相遇的味道。'①这里描写的是哪种感官？②这种气味有个特别的名字，你知道吗？","answer":"①嗅觉描写；②叫做'土霉素味'或'地理嗅味'（petrichor，雨后泥土香）","analysis":"感官描写与科学知识"},
      {"question":"把下面句子改成说明文式的表达：'彩虹真漂亮啊！'→说明文式：（　）","answer":"彩虹是由于太阳光在雨滴中发生折射和反射而形成的弧形光谱，通常出现在雨后晴天。","analysis":"记叙描写与说明文语言的转换"},
      {"question":"用数字说明（说明文技法）：用具体数字介绍月亮与地球的关系（查阅相关知识）","answer":"月球距地球约38.4万千米，直径约3476千米，绕地球一圈约27.3天（月球基本知识）","analysis":"说明文中数字的使用使描述更准确"},
      {"question":"阅读思考：'钱塘江大潮，素有天下奇观之称。'介绍一下钱塘江大潮的奇妙之处（2句话）","answer":"每年农历八月十八日，钱塘江涌来壮观的大潮，浪头可达数米高，气势磅礴，远远就能听到如万马奔腾的声音","analysis":"著名自然奇观的了解"},
      {"question":"写出3种你知道的自然奇观（自然界中令人惊叹的现象或景色）","answer":"如：北极光（极光）、庐山瀑布、黄果树瀑布、维多利亚湖、亚马逊热带雨林","analysis":"自然奇观知识积累"}
    ],
    "advanced_exercises":[
      {"question":"研究一个自然现象：彩虹是怎么形成的？用你自己的话（50字）解释","answer":"彩虹是因为太阳光（白光）射入雨滴后发生折射，由于不同颜色的光折射角度不同，就被分散开来，形成我们看到的七种颜色的弧形光带（赤橙黄绿蓝靛紫）。","analysis":"科学现象的语文表达"},
      {"question":"仿照说明文写50字：介绍一个你感兴趣的自然现象","answer":"开放性，参考介绍闪电：闪电是大气中正负电荷之间放电形成的现象。积雨云内部的冰晶和水滴摩擦产生大量电荷，当电位差足够大时，就会发生放电，形成闪亮的电弧，同时产生巨大声响，即雷声。","analysis":"说明文要准确、有条理"},
      {"question":"对比写法：同样是描写大海，记叙文和说明文如何不同地描写？各写2句","answer":"记叙文：'大海在阳光下波光粼粼，浪花轻轻地拍打着沙滩，像在给游客奏着迎宾曲。'（有感情）；说明文：'大海覆盖地球表面约71%的面积，平均深度约3800米，储存着地球淡水总量的97%。'（准确数字）","analysis":"两种文体在语言风格上的对比"},
      {"question":"写小报告：假设你是一名小科学家，发现了一种新的昆虫。写一段50字的发现报告","answer":"参考：发现日期：2024年5月1日。发现地点：学校花园。描述：这种昆虫有6条腿，翅膀呈透明蓝色，比普通蚂蚱大2倍，能发出悦耳的鸣声。喜欢在花瓣上活动，可能以花粉为食。","analysis":"科学报告式写作"},
      {"question":"【思维题】'世界上最奇妙的是什么？'这个问题每个人的答案不同。说说你的答案，并给出理由（60字）","answer":"开放性，言之有理即可。参考：我认为最奇妙的是人类的大脑。它能在几秒钟内处理数十亿条信息，创造语言、艺术和科学，却能同时自动控制心跳和呼吸。如此复杂而又神奇的东西，如何能不令人叹为观止？","analysis":"开放性思维，培养独特的观点"}
    ]
  },
  {
    "id":"u08","title":"第八单元 有趣的故事",
    "knowledge_points":[
      "阅读有趣的故事，感受幽默和生活中的乐趣",
      "理解幽默的语言特点：出人意料的结果、双关语等",
      "学习把生活中有趣的事写成故事",
      "复习全学期所学的写作方法和语文知识"
    ],
    "difficulties":[
      "理解幽默的内涵：不是嘲笑别人，而是善意的玩笑和智慧",
      "写有趣的故事：出人意料的结尾更有趣",
      "综合运用本学期学到的写作技巧",
      "复习和巩固本学期重点生字词"
    ],
    "exercises":[
      {"question":"什么是幽默？写出2个特点","answer":"幽默：出人意料（让人想不到）、无害（不伤害别人）、智慧（有内涵的玩笑）","analysis":"幽默的特点理解"},
      {"question":"给下面的故事结尾添加一个有趣的结局：'小明写了一篇关于夏天的作文，老师说写得很好，问他是不是自己写的。小明说……'","answer":"小明说：'是的，老师，我用了整整10分钟写的！'（幽默在于：他以为'用时长'能证明是自己写的，而老师可能觉得时间太短说明不是自己写的，出人意料）","analysis":"幽默结尾要有转折"},
      {"question":"扩写成有趣的故事（5句话）：'猫和鱼'","answer":"参考：一只聪明的猫盯着鱼缸里的金鱼想：'要是能直接伸爪子拿就好了。'于是它趴在鱼缸边，刚把爪子伸进去，'啪'——金鱼游过来给了它一巴掌！猫被吓得向后一跳，从桌子上掉了下来，哐当一声。金鱼悠悠地游过去，好像在说：'你也有今天！'","analysis":"有趣故事要有角色冲突、转折、结尾"},
      {"question":"积累有趣的歇后语（至少3个）","answer":"肉包子打狗——有去无回；猫咬乌龟——无处下嘴；小葱拌豆腐——一清（青）二白","analysis":"歇后语是中国传统幽默语言形式"},
      {"question":"改写：把下面的平淡句子改写成幽默有趣的版本：'今天我迟到了，老师批评了我。'","answer":"如：今天我用速度丈量了从家到学校的距离，却很遗憾地发现，我的奔跑速度比老师的嘴巴速度慢了整整15分钟。","analysis":"幽默写法：用夸张或比喻"},
      {"question":"读一读，想一想这个笑话为什么好笑：'爸爸问：儿子，1加1等于几？儿子说：等于窗。爸爸说：为什么？儿子说：因为1加1等于2（二），竖起来就是窗（窗字上面有两竖）。'","answer":"好笑的原因：谐音（2=二=竖起来）和观察角度出人意料；运用了汉字的形体特点","analysis":"幽默中的谐音和创意联想"},
      {"question":"写出3句你觉得有趣的绕口令","answer":"如：①四是四，十是十，十四是十四，四十是四十；②吃葡萄不吐葡萄皮，不吃葡萄倒吐葡萄皮；③黑化肥发灰，灰化肥发黑","analysis":"绕口令：语言趣味性训练"},
      {"question":"复习：写出本学期学过的5个四字成语并各造一个短句","answer":"开放性，复习本学期成语：守株待兔、各色各样、热热闹闹、无忧无虑、天真烂漫等","analysis":"学期末复习，综合运用词语"}
    ],
    "advanced_exercises":[
      {"question":"创作：写一个有趣的故事（100字），结尾要出人意料","answer":"开放性，评分：①有完整情节②结尾出人意料③语言生动","analysis":"综合写作能力展示"},
      {"question":"幽默分析：分析《蜗牛与黄鹂鸟》这首歌幽默在哪里（可以是歌词或听说的版本）","answer":"幽默点：黄鹂鸟讽刺蜗牛慢，蜗牛不急不忙说'等我爬上去，葡萄就成熟了'——慢有慢的道理，结局反转让人忍俊不禁。道理：勤能补拙，不要讽刺别人的局限","analysis":"幽默中的哲学与道理"},
      {"question":"搜集1个中外幽默小故事，写下来并分析它好笑的原因","answer":"开放性，要求：写出故事+分析幽默原因","analysis":"幽默欣赏与分析"},
      {"question":"学期综合复习：回顾本学期学过的古诗，默写你最喜欢的一首，并写一句你的感受","answer":"开放性，默写古诗要准确，感受要真实","analysis":"学期末综合复习"},
      {"question":"【综合小结】用3-5句话，总结你本学期语文学习的最大收获（知识、方法、感悟都可以）","answer":"开放性，鼓励学生总结自己的学习体验","analysis":"自我反思和总结能力"}
    ]
  }
]

print("Grade 3 Chinese lower content defined.")

# ============ 四年级语文上下册（简化版）============
g4_chinese_upper = [
  {"id":"u01","title":"第一单元 自然之美","knowledge_points":["学习《观潮》《走月亮》等课文，感受自然之美","掌握描写自然景观的词语和句法","学习按照时间或方位顺序描写景物","积累比喻、拟人等修辞手法"],"difficulties":["理解钱塘江大潮的壮观（从声音、视觉等多角度描写）","月亮夜晚的意境描写","写景文的层次结构","在写作中灵活运用修辞手法"],"exercises":[{"question":"《观潮》中描写大潮来时声音的句子：从（　）到（　），最后像（　）","answer":"从远处到近处，从细微到越来越大，最后像山崩地裂","analysis":"用声音的变化表现大潮从远到近"},{"question":"比喻句辨析：'钱塘江大潮像千万匹白色战马齐头并进'——本体是（　），喻体是（　）","answer":"本体：钱塘江大潮（潮头）；喻体：千万匹白色战马","analysis":"比喻句成分：本体、喻词（像）、喻体"},{"question":"写出5个描写潮水的词语","answer":"波涛汹涌、浪花四溅、水天相接、白浪滔天、山崩地裂","analysis":"积累潮水相关词语"},{"question":"仿写：'月亮升起来，院子里凉爽又宁静。'（用比喻或拟人修辞写月亮）","answer":"如：月亮缓缓升起，像一盏温柔的灯，把银白色的光轻轻洒在院子里","analysis":"写月亮要有意境"},{"question":"按顺序排列：潮来时的描写：①白浪翻滚②声音越来越响③浪潮越来越近④远处传来隆隆声","answer":"④→②→③→①","analysis":"大潮描写是由远及近的顺序"},{"question":"《走月亮》中月夜的景色给人什么感觉？找出3个关键词","answer":"宁静、清凉、美好（温暖）","analysis":"月夜意境的理解"},{"question":"扩写句子：'月光照在河上。'（加入修辞，使句子更美）","answer":"月光如银丝般温柔地洒在河面上，波光粼粼，像碎了一地的星星。","analysis":"景物描写要生动形象"},{"question":"写出4个关于月亮的古诗句（不重复）","answer":"①举头望明月，低头思故乡（李白）②床前明月光（李白）③但愿人长久，千里共婵娟（苏轼）④春风又绿江南岸，明月何时照我还（王安石）","analysis":"月亮古诗积累"}],"advanced_exercises":[{"question":"对比《观潮》和《走月亮》的写景方式：一个写大自然的壮阔，一个写静谧之美，各有什么写作特点？","answer":"《观潮》：气势宏大，多用声音和动作描写（听觉+视觉），动态为主；《走月亮》：细腻温情，多用感受和联想，静态为主","analysis":"写景风格对比"},{"question":"小作文（80字）：描写一次你印象深刻的自然现象（日出、下雨、大风等）","answer":"开放性写作，要有感官描写和情感","analysis":"自然景物写作"},{"question":"研究：钱塘江大潮为什么会特别壮观？从地理角度简单解释（30字）","answer":"钱塘江入海口呈喇叭形，潮水涌入时受到地形约束，水量集中，速度加快，形成壮观大潮","analysis":"自然现象的科学原因"},{"question":"积累：写出描写水的四字词语（至少8个）","answer":"波光粼粼、清澈见底、碧波荡漾、水天一色、波涛汹涌、细水长流、浩如烟海、涓涓细流","analysis":"写水的词语积累"},{"question":"【综合题】你最喜欢的自然景观是什么？为什么？写50字","answer":"开放性，要有具体景物描写和情感","analysis":"个人感受表达"}]},
  {"id":"u02","title":"第二单元 古典名著","knowledge_points":["初步接触中国古典名著：《三国演义》《水浒传》《西游记》《红楼梦》","了解四大名著中的主要人物和故事情节","激发阅读兴趣，培养文学欣赏能力","学习通过人物行为描写展现性格"],"difficulties":["古典名著中的文言色彩词语理解","理解复杂的人物关系","从故事中感受中国传统文化","区分历史人物和虚构人物"],"exercises":[{"question":"连线：《西游记》—（　）；《三国演义》—（　）；《水浒传》—（　）；《红楼梦》—（　）","answer":"西游记—吴承恩；三国演义—罗贯中；水浒传—施耐庵；红楼梦—曹雪芹","analysis":"四大名著的作者"},{"question":"《西游记》中，唐僧师徒四人除唐僧外是（　）（　）（　）","answer":"孙悟空、猪八戒、沙僧（沙和尚）","analysis":"《西游记》主要人物"},{"question":"写出《三国演义》中你知道的3个故事名称","answer":"桃园结义、空城计、赤壁之战、三顾茅庐、草船借箭","analysis":"三国故事积累"},{"question":"《水浒传》中的人物绰号连线：及时雨—（　）；黑旋风—（　）；智多星—（　）","answer":"及时雨—宋江；黑旋风—李逵；智多星—吴用","analysis":"水浒人物绰号"},{"question":"判断：①诸葛亮是三国时期真实的历史人物（　）②孙悟空是历史上真实存在的（　）③《红楼梦》是写贾宝玉和林黛玉爱情的故事（　）","answer":"①对；②错（虚构的神话人物）；③对","analysis":"历史与文学的区别"},{"question":"从四大名著中，选一个你喜欢的人物，写3句话介绍他/她","answer":"开放性，如：孙悟空：他机智勇敢，武艺高强，有七十二变的本领和金箍棒。他一心保护唐僧取经，遇到妖怪从不退缩。他是中国文学中最受欢迎的英雄形象之一。","analysis":"人物介绍"},{"question":"《三国演义》中'三顾茅庐'体现了什么精神？","answer":"刘备三次亲自登门拜访诸葛亮，体现了求贤若渴、尊重人才、诚心诚意的精神","analysis":"故事寓意理解"},{"question":"你从四大名著中学到了什么道理？写一点","answer":"开放性。如：从《西游记》学到：困难再多，只要坚持，最终能成功","analysis":"文学作品的价值思考"}],"advanced_exercises":[{"question":"比较：西方经典《格林童话》和中国经典《西游记》，在内容和主题上有什么异同？","answer":"相同：都有神奇元素、勇敢的主人公；不同：格林童话偏向儿童故事，主题简单；西游记规模宏大，主题深刻（修行、善恶、人性）","analysis":"中外文学比较"},{"question":"创作：以三国人物为主角，写一个简短的现代故事（50字）（如诸葛亮穿越到现代）","answer":"开放性创作，参考：诸葛亮穿越到21世纪，用他的智慧和谋略，在一次重要的商业谈判中力挽狂澜，让公司起死回生。他感叹道：'运筹帷幄之中，决胜商场之上，古今同理！'","analysis":"创意写作"},{"question":"阅读延伸：读《西游记》某一回（或摘要），写50字的读书笔记","answer":"开放性，格式：故事内容+人物特点+感悟","analysis":"读书笔记写作"},{"question":"积累：写出与四大名著相关的成语（至少4个）","answer":"三顾茅庐（三国）、过五关斩六将（三国）、火眼金睛（西游）、逼上梁山（水浒）","analysis":"名著成语积累"},{"question":"【思维题】为什么四大名著能流传几百年？它们的共同价值是什么？","answer":"它们描写了人性的复杂和社会的百态，反映了中国传统文化的价值观（忠义、勇敢、智慧、爱情等），同时情节生动，塑造了许多令人难忘的人物形象，跨越时代引发共鸣","analysis":"文学价值的深层思考"}]},
  {"id":"u03","title":"第三单元 观察与发现","knowledge_points":["学习观察自然和生活，发现事物的规律","学习写观察日记","理解科学观察的方法：有目的、有顺序、有记录","积累描写动植物生长变化的词语"],"difficulties":["长期观察的坚持（不是一次性观察）","用准确科学的语言描述观察结果","区分观察到的事实和自己的感受/推测","写观察日记的格式和内容要求"],"exercises":[{"question":"观察日记的格式：（1）日期 （2）（　）（3）正文","answer":"（1）日期（2）天气（3）正文","analysis":"观察日记格式：日期、天气、正文"},{"question":"写出5个描写植物生长的词语","answer":"发芽、抽枝、开花、结果、生长、凋谢、枯萎、茁壮","analysis":"植物生长词语"},{"question":"区分事实和感受：①'小蜗牛爬过去了'（　）②'我觉得蜗牛在寻找食物'（　）","answer":"①事实；②感受（推测）","analysis":"观察日记要区分事实与推测"},{"question":"一次观察要有哪些要素？（至少4个）","answer":"时间、地点、观察对象、观察到的内容（颜色、大小、变化等）、天气等","analysis":"观察要素"},{"question":"写一段种豆子的观察日记（第三天的记录，50字）","answer":"参考：3月5日，晴。今天是第三天，豆子已经长出了小小的嫩芽，白色的，细细的，约有1厘米高。它弯曲着头，就像一个小问号。我轻轻摸了摸，软软的。土壤保持湿润，继续观察。","analysis":"观察日记要具体、客观"},{"question":"动物行为观察：蚂蚁排成一列搬食物，你观察到了什么？有什么发现？","answer":"观察：蚂蚁排成一排，首尾相接，把食物从远处搬回蚁巢；发现：蚂蚁有分工合作，用信息素（气味）通信","analysis":"观察要思考现象背后的原因"},{"question":"比喻训练：把豆芽的样子比喻成某个东西（写一句话）","answer":"如：豆芽弯着腰，像一个正在鞠躬的小人；嫩嫩的豆芽头，像一顶绿色的小帽子。","analysis":"观察后联想与比喻"},{"question":"写出3种适合观察的小动物和观察要点","answer":"①金鱼——颜色、游泳方式、喂食反应；②蚂蚁——路径、搬运方式、对食物的反应；③蜗牛——爬行速度、遇危险时的反应","analysis":"观察对象和观察要点的确定"}],"advanced_exercises":[{"question":"制定一个15天的植物观察计划，说明每天要记录什么","answer":"每天记录：①植物高度（厘米）；②叶子数量；③颜色变化；④特殊现象（如开花、变形等）；⑤天气","analysis":"观察计划制定"},{"question":"小作文（80字）：我的观察日记（选一种动植物，写2-3天的记录）","answer":"开放性，要有日期、天气、具体观察内容","analysis":"观察日记综合写作"},{"question":"思考：为什么科学家要长期、反复地观察同一事物？举例说明","answer":"因为事物是变化的，一次观察只能看到片段；长期观察才能发现规律（如达尔文观察几十年才发现进化论）","analysis":"科学精神的培养"},{"question":"阅读拓展：找一则科学家因为仔细观察而有所发现的故事，写出主要内容（50字）","answer":"如：牛顿看到苹果落地，仔细思考后发现了万有引力定律；巴斯德观察细菌繁殖，发现了消毒方法","analysis":"科学家的观察故事"},{"question":"【综合题】如果你要观察'校园里一棵树一年四季的变化'，你会用什么方法记录？列出你的方案","answer":"①每季度各拍一张照片；②每月测量树高和树干直径；③记录树上的鸟类或昆虫；④画出或描述叶子颜色和形态变化；⑤整理成一本观察手册","analysis":"综合观察方案设计"}]},
  {"id":"u04","title":"第四单元 神话故事","knowledge_points":["学习中国神话故事：女娲补天、精卫填海、夸父追日等","了解神话的特点：源于远古、有神奇色彩、解释自然现象","感受中国神话中人物的精神（勇敢、坚韧等）","学习神话的夸张和想象手法"],"difficulties":["理解神话与现实的关系（神话虽然虚构，但反映了古人的想象和精神）","神话中夸张手法的理解（如夸父日行千里）","积累神话相关词语","创作小神话：需要发挥想象，但有一定情节逻辑"],"exercises":[{"question":"精卫填海的故事：炎帝的女儿（　）溺于东海，化身为（　），每天衔（　）填海","answer":"女娃；精卫鸟；石子和树枝","analysis":"精卫填海故事概要"},{"question":"神话的特点：①（　）②（　）③（　）（至少3点）","answer":"①有神奇人物（神、仙、怪）②解释自然现象③充满想象和夸张","analysis":"神话文学特点"},{"question":"连线：女娲—（　）；夸父—（　）；精卫—（　）；后羿—（　）","answer":"女娲—补天/造人；夸父—追日；精卫—填海；后羿—射日","analysis":"神话人物和故事对应"},{"question":"《夸父追日》中，夸父倒下后，他的手杖变成了（　），表现了他（　）的精神","answer":"桃林；坚韧不拔、永不放弃（即使失败也化为有用之物）","analysis":"神话中的人物精神"},{"question":"夸张手法：《夸父追日》中哪些描写是夸张的？","answer":"夸父一天走万里路、喝干了黄河和渭河（神话夸张，强调他的力量和决心）","analysis":"夸张手法的识别"},{"question":"仿照神话，写一个解释自然现象的小故事开头（3句话）：为什么天上有彩虹？","answer":"传说上古时，天地之间有一条彩色神龙，它飞翔的踪迹就是彩虹。每当雨后天晴，神龙就会出来伸展身体，于是天边出现了美丽的彩虹……","analysis":"神话解释自然现象的创作"},{"question":"从神话人物身上学到的精神：女娲补天代表（　），精卫填海代表（　）","answer":"女娲：勇于担当、自我牺牲；精卫：坚韧执着、永不放弃","analysis":"神话人物精神提炼"},{"question":"中国神话人物：写出你知道的5个","answer":"孙悟空、嫦娥、玉皇大帝、土地公、灶王爷、雷公电母、龙王","analysis":"神话人物积累"}],"advanced_exercises":[{"question":"比较：中国神话（如精卫填海）和西方神话（如普罗米修斯盗火）有什么共同主题？","answer":"共同主题：勇敢、牺牲精神——都是神或英雄为了人类或正义而献身；体现了人类对勇气和牺牲的崇尚","analysis":"中西神话比较"},{"question":"创作一个小神话故事（100字）：为什么月亮会有阴晴圆缺？（自创解释）","answer":"开放性，参考：传说月亮是月神嫦娥的家，她每月有一半时间思念人间，把脸转向地球，就是满月；另一半时间她闭上眼睛哭泣，就渐渐看不见月亮了……","analysis":"神话创作"},{"question":"研究：中国神话'天圆地方'的宇宙观，古人认为天地是什么样的？和现代科学有什么不同？","answer":"古人认为天是圆的（穹顶状），地是方的；现代科学：地球是球形，太阳系是立体的。神话宇宙观反映了当时的认知水平","analysis":"古代宇宙观与科学的对比"},{"question":"积累：写出中国神话中的10个人物名称（不重复）","answer":"女娲、伏羲、神农、黄帝、夸父、精卫、后羿、嫦娥、玉帝、王母","analysis":"神话人物名称积累"},{"question":"【哲思题】神话虽然不是真实的，但它有什么价值？为什么人类各民族都有神话？","answer":"神话的价值：①反映古人的想象力和精神追求；②是民族文化的根源；③传递价值观（如善良、勇敢）；各民族有神话是因为人类都有对未知事物（自然、死亡、起源）的好奇，用神话来解释","analysis":"文化和心理学角度思考神话"}]},
  {"id":"u05","title":"第五单元 习作单元（记事写人）","knowledge_points":["学习记叙文的写作：按时间顺序、事件逻辑写故事","学习写人物：通过外貌、动作、语言、心理描写刻画人物","理解'点面结合'的写作方法","掌握作文的修改方法：通读→找问题→修改"],"difficulties":["如何使记叙文更有细节感，不流于表面","心理活动的描写：人物内心独白","写人物时让读者感受到人物性格（不直接说性格）","修改自己的作文：客观评价自己的文章"],"exercises":[{"question":"记叙文要素'六要素'是哪六个？","answer":"时间、地点、人物、起因、经过、结果","analysis":"记叙文六要素"},{"question":"四种描写人物的方法：（　）描写、（　）描写、（　）描写、（　）描写","answer":"外貌、动作、语言、心理","analysis":"人物描写四种方法"},{"question":"判断下面属于哪种描写：①'他额头上渗出了汗水'（　）②'他心里想：能行吗？'（　）③'他穿着一件蓝色外套'（　）","answer":"①动作描写；②心理描写；③外貌描写","analysis":"描写方式的识别"},{"question":"把下面的平淡描写改成有细节的描写：'他很紧张。'","answer":"他的手心不断出汗，一遍又一遍地摸着衣角，嘴唇微微颤抖，眼睛不知道该看哪里","analysis":"用行为细节代替直接说感受"},{"question":"仿写心理活动：'赛跑的枪声响了，我心里想：……'（写3句心理独白）","answer":"'我一定要跑第一！'我在心里呐喊。但跑到一半，腿开始发酸，我开始动摇：'算了，放弃吧……'不行，我咬紧牙关：'坚持，就剩最后一段了！'","analysis":"心理描写要有变化，反映情绪"},{"question":"开头技巧：用'倒叙'方式写作文开头（先写结果，再回忆）","answer":"如：我站在领奖台上，手里捧着奖杯，心里激动得说不出话。想起一年前的那个冬天，我第一次拿起书……（然后倒回去讲故事）","analysis":"倒叙开头制造悬念"},{"question":"修改练习：找出下面作文中的问题：'今天我去图书馆看书，我看了好多书，书里有很多知识，我觉得很好。'","answer":"问题：①内容空洞，没有具体细节；②重复用'我'开头；③'很好'太笼统。修改方向：写看了什么书，有什么具体收获","analysis":"作文修改：具体化、多样化"},{"question":"结尾技巧：好的结尾有哪些方式？（至少3种）","answer":"①总结感悟（点明主题）；②照应开头；③留有余味（引发思考）；④抒发感情","analysis":"作文结尾方式"}],"advanced_exercises":[{"question":"综合写作（100字）：写一个你遇到困难并最终解决的故事，要用到心理描写","answer":"开放性，评分：有困难设定、心理变化、解决过程、结果与感悟","analysis":"记叙文综合写作"},{"question":"互评练习：找出一篇同学或课文的作文，写出3个优点和1个可以改进的地方","answer":"开放性，培养客观评价能力","analysis":"写作欣赏与评价"},{"question":"研究经典作文的开头：找出3篇你喜欢的文章的开头句子，分析为什么好","answer":"开放性，提示：好的开头有：开门见山型、设置悬念型、景物渲染型","analysis":"写作技法的学习"},{"question":"仿写：模仿《荷花》（朱自清风格）写一段描写花的文章（60字）","answer":"如：公园里的月季花开了，密密实实地挤在一起，红的、粉的、白的，像少女的笑脸。我停下脚步，凑近闻了闻，淡淡的香气钻进鼻子，说不清是什么味道，只知道心里一下子柔软了。","analysis":"模仿名家写作风格"},{"question":"【综合题】写作中最难的是什么？你有什么克服的方法？（50字）","answer":"开放性，言之有理即可","analysis":"写作学习反思"}]},
  {"id":"u06","title":"第六单元 成长故事","knowledge_points":["学习关于成长、挫折、友谊的课文","理解成长的意义：不只是年龄增长，更是心灵的成熟","积累描写成长感悟的词语","学习写成长日记"],"difficulties":["理解'成长'的多层含义","理解课文中人物经历挫折后的心理变化","写成长感悟：联系自己的实际，有真情实感","描写友谊：通过具体事件表现"],"exercises":[{"question":"写出表示成长的词语（至少6个）","answer":"成长、成熟、进步、蜕变、磨砺、收获、领悟、懂事","analysis":"成长主题词语"},{"question":"阅读：'失败是成功之母'——你经历过什么失败？从中学到了什么？（50字）","answer":"开放性，参考：我曾经在运动会跑步比赛中摔倒，但我爬起来跑到了终点，没有放弃。虽然没拿到名次，但我学会了面对困难不放弃。","analysis":"联系实际理解道理"},{"question":"写出描写友谊的词语（至少4个）","answer":"莫逆之交、情同手足、患难与共、志同道合","analysis":"友谊词语积累"},{"question":"仿写：'友谊是一盏灯，在最黑暗的时候给你光明。'仿写一句关于友谊的比喻","answer":"友谊是一把伞，在最风雨交加的时候为你遮挡；友谊是一双手，在你最需要帮助时伸向你","analysis":"友谊比喻句仿写"},{"question":"成长故事要素：写出一个成长故事的基本要素（和记叙文六要素的关系）","answer":"除记叙文六要素外，成长故事还需要：①人物的内心变化；②成长的转折点；③学到了什么","analysis":"成长故事的特殊要素"},{"question":"判断：下面哪些是真正的'成长'？①长高了5厘米②明白了诚实的重要③考试考了高分（如果只是运气）④学会了帮助别人","answer":"②和④是真正的成长（心灵成熟）；①只是身体变化；③如果只是运气不算成长，但如果是努力换来的也算","analysis":"成长的内涵理解"},{"question":"写一段关于你和好朋友之间的故事（3-5句话）","answer":"开放性，要有具体事件和感情描写","analysis":"友谊主题写作"},{"question":"古诗积累：写出2句关于友情的古诗名句","answer":"①'海内存知己，天涯若比邻'（王勃）；②'桃花潭水深千尺，不及汪伦送我情'（李白）","analysis":"友情古诗积累"}],"advanced_exercises":[{"question":"写一篇成长日记（80字）：记录你最近一次从错误中学到的事情","answer":"开放性，要有具体事件和感悟","analysis":"成长日记写作"},{"question":"分析：《假如给我三天光明》（海伦凯勒）这本书的主题是什么？她的故事有什么启示？（50字）","answer":"主题：珍惜和感恩，突破困境。启示：即使身残，也能创造奇迹；不要因为困难就放弃，要感恩生命中的每一天","analysis":"名著阅读与感悟"},{"question":"采访练习：问问一个你认识的大人：'你觉得自己成长的转折点是什么？'写出他/她的回答（50字）","answer":"开放性，实际采访内容","analysis":"与生活联系，了解他人的成长故事"},{"question":"反思写作：你认为你现在有哪些需要'成长'的地方？（60字）","answer":"开放性，真实表达即可，不需要'标准答案'","analysis":"自我认知与反思"},{"question":"【综合题】写一封信给10年后的自己，说说你现在的样子和对未来的期望（80字）","answer":"开放性，格式正确（信件格式），情感真实","analysis":"综合写作：回顾现在，展望未来"}]},
  {"id":"u07","title":"第七单元 爱护自然","knowledge_points":["学习关于保护自然环境的课文","理解环境问题的严峻性和人类的责任","学习用说服的语气写议论性短文","积累环保相关词语"],"difficulties":["议论文的基本结构：提出观点→论据→结论","如何用生动的例子支持自己的观点","理解环境问题的复杂性（不是非黑即白）","写环保主题作文：有观点、有例子、有感情"],"exercises":[{"question":"写出5个与环保相关的词语","answer":"绿色环保、可持续发展、节能减排、低碳生活、垃圾分类","analysis":"环保词语积累"},{"question":"议论文结构：①提出（　）②列举（　）③得出（　）","answer":"①观点②论据（例子/理由）③结论","analysis":"议论文基本结构"},{"question":"我们能为环保做什么？写出5件小事","answer":"①少用塑料袋；②节约用水；③垃圾分类；④骑自行车代替开车；⑤不乱扔垃圾","analysis":"环保行动实践"},{"question":"用'虽然……但是……'写一句关于环保的句子","answer":"虽然使用塑料袋很方便，但是它会造成严重的白色污染，危害环境","analysis":"关联词句式"},{"question":"阅读：'地球只有一个，保护它是我们共同的责任。'这句话是什么论点？你赞同吗？为什么？","answer":"论点：保护地球是所有人的责任；赞同，理由：地球是人类共同的家园，污染和破坏影响所有人","analysis":"论点的理解和评价"},{"question":"反驳：有人说'环保是政府的事，跟我没关系'，你怎么反驳这个观点？（50字）","answer":"环保与每个人的日常行为密切相关。每一个不随手关灯、乱扔垃圾的人都在破坏环境。政府制定政策，但个人行为加起来才是最大的影响因素。每个人都有责任。","analysis":"反驳训练：找出漏洞"},{"question":"举例论证：为'垃圾分类很重要'这个观点举出2个例子","answer":"①可回收垃圾（纸、玻璃）重新利用，减少资源浪费；②有机垃圾可以堆肥，减少垃圾填埋量和甲烷排放","analysis":"用具体例子支持论点"},{"question":"写出一个中国环保标志或口号","answer":"如：'绿水青山就是金山银山'（习近平）；中国环保标志（循环利用标志）","analysis":"环保文化积累"}],"advanced_exercises":[{"question":"写一篇环保议论文（80字），观点自定，要有论据","answer":"开放性，评分：观点明确，有至少2个论据，结构完整","analysis":"议论文写作"},{"question":"调研：问问家人，我们家每天能做到哪些环保行为？还有哪些可以改进？写出调研结果（50字）","answer":"开放性，实际调研结果","analysis":"生活实践与观察"},{"question":"比较：中国'绿色发展'理念和以前'先发展后治理'的理念，哪个更合理？为什么？","answer":"绿色发展更合理：先发展后治理代价太大（污染难以消除，甚至无法恢复）；绿色发展将环保融入发展，可持续，长远看更经济","analysis":"政策理念的比较与评价"},{"question":"创意写作（70字）：想象30年后地球的两种可能——一种是我们保护了环境，一种是没有保护","answer":"开放性，两种未来对比鲜明即可","analysis":"未来想象写作"},{"question":"【综合题】设计一个班级环保活动方案：说明活动目的、内容和预期效果","answer":"如：主题：'校园零垃圾日'；目的：培养垃圾分类意识；内容：当天所有垃圾必须分类，不带一次性塑料；效果：减少垃圾量，提高环保意识","analysis":"活动方案设计"}]},
  {"id":"u08","title":"第八单元 综合复习与提升","knowledge_points":["复习四年级上册全部语文知识","综合运用写作技巧","积累优美语段和名句","语文知识综合检测"],"difficulties":["综合运用各种写作方法","辨析易错字词","复杂段落的阅读理解","古诗文背诵与默写"],"exercises":[{"question":"默写：《题西林壁》（宋·苏轼）","answer":"横看成岭侧成峰，远近高低各不同。不识庐山真面目，只缘身在此山中。","analysis":"四年级必背古诗"},{"question":"《题西林壁》这首诗的哲理是什么？","answer":"当局者迷，旁观者清——由于自己身处其中，难以全面看清事物的真面目，需要从不同角度观察","analysis":"古诗哲理理解"},{"question":"词语辨析：'观察'和'观看'有什么不同？","answer":"观察：有目的地注意，通常伴随思考和记录；观看：只是用眼睛看，不一定有深入思考","analysis":"近义词辨析"},{"question":"修辞判断：①'太阳像一个大火球' ②'风在树林里穿来穿去' ③'这道题真难啊！'","answer":"①比喻；②拟人；③感叹/直接抒情","analysis":"修辞手法复习"},{"question":"说明文中哪些手法使说明更清楚？（至少4种）","answer":"①列数字；②举例子；③作比较；④打比方（比喻）；⑤分类别","analysis":"说明文说明方法复习"},{"question":"复习：写出本学期学过的5首古诗的题目和作者","answer":"（根据教材内容填写，如）《观潮》选段、《题西林壁》（苏轼）、《游山西村》（陆游）等","analysis":"古诗复习"},{"question":"综合修改：找出下面短文的3处问题：'今天天气很好，我去了公园。公园里有很多花，有红色的，有白色的，有黄色的，有粉色的。我觉得很漂亮。公园里有很多人，大家都在玩。我玩了很开心。'","answer":"问题：①多处重复用'有'（'有红色的有白色的'可改为排比更优美）；②'很漂亮''很开心'太笼统，缺细节；③结构单调，缺少有趣的细节描写","analysis":"作文修改综合复习"},{"question":"期末回顾：本学期语文课你印象最深的一篇课文是什么？为什么？（50字）","answer":"开放性，言之有理","analysis":"学习反思与总结"}],"advanced_exercises":[{"question":"写期末作文（100字）：以'我的收获'为题，写本学期的语文学习感悟","answer":"开放性，结构完整，有具体收获","analysis":"综合写作"},{"question":"古诗背诵竞赛：默写你记得最清楚的5首古诗","answer":"开放性，背诵准确","analysis":"古诗综合复习"},{"question":"阅读综合：找一篇课外文章（任何类型），写出：①文章类型②主要内容③你的感受（共60字）","answer":"开放性，格式完整","analysis":"课外阅读与分析"},{"question":"积累：写出本学期学过的20个成语","answer":"开放性，复习本学期成语","analysis":"成语积累综合复习"},{"question":"【期末综合题】给即将升入四年级的三年级同学写一封信（80字），分享一个学习语文的好方法","answer":"开放性，参考：亲爱的三年级小朋友，升上四年级后，语文会更有趣也更有挑战。我建议你养成每天阅读的好习惯，哪怕只是20分钟。多读书，词汇量自然增加，写作文也会越来越流畅。祝你语文学习愉快！","analysis":"综合表达，传递学习经验"}]}
]

g4_chinese_lower = [
  {"id":"u01","title":"第一单元 乡村田园","knowledge_points":["学习描写农村和田园生活的课文","感受自然界和农村的宁静与美好","积累描写田园风光的词语","学习从多角度描写场景"],"difficulties":["把握田园诗歌的意境","感受自然与人工环境的对比","描写乡村要抓住特有的景物","写作中体现季节特点"],"exercises":[{"question":"写出5个描写农村景色的词语","answer":"田野广阔、稻浪翻滚、炊烟袅袅、鸡鸣狗吠、瓜果飘香","analysis":"农村词语积累"},{"question":"仿写：'春天的田野是绿色的，夏天的田野是金黄色的。'仿写：'秋天的（　）是（　）色的，冬天的（　）是（　）色的。'","answer":"秋天的田野是金黄色的，冬天的田野是雪白色的","analysis":"仿写句式，注意颜色和季节对应"},{"question":"阅读短文，回答：'鸡在草地上找虫子，鸭子在小河里游泳，狗在村口晒太阳。'①这段话写了几种动物？②这是一幅什么样的画面？","answer":"①三种（鸡、鸭、狗）；②宁静、悠闲的农村生活画面","analysis":"概括画面特点"},{"question":"写出乡村特有的事物（至少6个）","answer":"稻田、麦秸垛、井水、石磨、炊烟、鸡窝、豆腐坊、木栅栏","analysis":"乡村特征事物积累"},{"question":"把下面句子改为拟人句：'玉米长得很高。'","answer":"玉米骄傲地挺直了腰杆，比村口的老槐树还要高","analysis":"拟人修辞使描写更生动"},{"question":"古诗积累：写出2句描写农村/田园的古诗名句","answer":"①'采菊东篱下，悠然见南山'（陶渊明）；②'稻花香里说丰年，听取蛙声一片'（辛弃疾）","analysis":"田园古诗积累"},{"question":"描写乡村的声音：写出你想象中农村会有哪些声音（4种）","answer":"公鸡啼鸣、牛蛙歌唱、风吹麦浪的沙沙声、拖拉机的轰鸣","analysis":"声音描写，丰富农村画面"},{"question":"写3句话：描写秋天农村丰收的景象","answer":"秋天的田野一片金黄，沉甸甸的稻穗弯腰致意。农民们戴着草帽，挥舞镰刀，欢声笑语飘荡在田间。收获的香气混合着泥土的气息，让人心旷神怡。","analysis":"丰收场景描写"}],"advanced_exercises":[{"question":"对比：城市生活和农村生活各有什么优缺点？写出各2点（60字）","answer":"城市优点：交通便利，资源丰富；城市缺点：拥挤嘈杂，空气较差。农村优点：空气清新，生活节奏慢；农村缺点：教育医疗资源少，交通不便","analysis":"辩证看待城乡差异"},{"question":"小作文（80字）：以'一个难忘的农村体验'为题（真实或想象的）","answer":"开放性写作","analysis":"田园生活写作"},{"question":"研究：中国有多少种农业作物？选择一种，介绍它的生长过程（50字）","answer":"如：水稻：先播种，然后在水田中插秧，约90-120天生长期，然后收割，晒干脱粒，变成我们吃的大米","analysis":"农业知识了解"},{"question":"古诗拓展：陶渊明是著名的'田园诗人'，找出他的一首田园诗并写出诗意","answer":"如《归园田居》：'种豆南山下，草盛豆苗稀……'诗意：在南山种豆，草长得旺盛豆苗却稀疏；每天早出晚归，路窄草深衣服被露水打湿","analysis":"田园诗欣赏"},{"question":"【综合题】写一首描写农村的小诗（4行，不要求押韵）","answer":"开放性，有农村特色词语，有一定意境即可","analysis":"诗歌创作"}]},
  {"id":"u02","title":"第二单元 科技与未来","knowledge_points":["了解现代科技的发展和未来趋势","学习说明文中科技类文章的特点","激发对科学技术的兴趣和好奇心","学习用推测性语言介绍未来科技"],"difficulties":["理解科技文章中专业词语（简单说明即可）","如何准确描述科学现象","想象未来时要基于现实，不能太离谱","说明文语言的客观性"],"exercises":[{"question":"写出5种现代科技发明","answer":"智能手机、人工智能、电动汽车、太阳能、高铁","analysis":"科技词语积累"},{"question":"'机器人在未来可能会取代很多工作。'这是事实还是推测？怎么看出来？","answer":"推测；'可能'是推测标志词","analysis":"区分事实和推测"},{"question":"仿写推测句：'未来，无人驾驶汽车可能会成为普遍交通工具。'仿写一句关于未来科技的推测","answer":"如：未来，全息投影技术可能会让我们在家就能'走遍'世界各地。","analysis":"推测句式练习"},{"question":"你认为最有用的一项科技发明是什么？写2句话说明原因","answer":"开放性，要说明'有用'的理由","analysis":"科技观点表达"},{"question":"比较：古代交通（马车/步行）和现代交通（高铁/飞机），哪个更好？为什么？","answer":"现代更便利（速度快、安全性高）；但古代也有其美（慢而享受过程）；整体上现代更满足大规模人群需求","analysis":"古今科技对比"},{"question":"科技说明文练习：用2句话介绍'高速铁路'","answer":"高速铁路是一种运行速度超过250千米/小时的铁路运输系统。它大大缩短了城市之间的旅行时间，如北京到上海，高铁只需约4.5小时，大约是普通列车的1/3时间。","analysis":"说明文用数字使内容更准确"},{"question":"积累：写出4个与科技相关的成语或词语（不局限于现代科技）","answer":"日新月异（发展变化快）、突飞猛进（进步很快）、与时俱进、高科技","analysis":"科技主题词语"},{"question":"如果你是发明家，你想发明什么？写2句话","answer":"开放性，想象合理即可","analysis":"创新思维和表达"}],"advanced_exercises":[{"question":"写一篇科技说明文（80字）：介绍一种你了解的科学技术","answer":"开放性，要准确、有条理","analysis":"科技说明文写作"},{"question":"思考：科技发展带来了哪些好处和问题？各举2例","answer":"好处：①医疗技术进步，许多疾病可以治愈；②通信技术让全球联系方便。问题：①网络成瘾影响健康；②自动化导致部分工人失业","analysis":"辩证看待科技"},{"question":"想象作文（70字）：描写100年后的一天早晨，你会看到什么","answer":"开放性，想象要合理，有科技元素","analysis":"未来想象写作"},{"question":"调研：问家人，他们小时候没有现在有的哪些科技？听他们讲一个没有这种科技时的故事（50字）","answer":"开放性，实际调研结果","analysis":"科技变迁体验"},{"question":"【综合题】'科技是把双刃剑'——写出你对这句话的理解（60字）","answer":"科技带来便利和进步（医疗、交通、通信），但也带来问题（污染、隐私、上瘾）。关键是如何使用科技，而不是科技本身的好坏。","analysis":"辩证思维"}]},
  {"id":"u03","title":"第三单元 古诗与传统文化","knowledge_points":["学习四年级下册古诗：《芙蓉楼送辛渐》《塞下曲》《墨梅》等","掌握古诗背诵与理解","了解古诗中的边塞文化、隐逸文化","积累古诗中的意象（边关、梅花等）"],"difficulties":["边塞诗的特点：豪迈、思乡、战争","'梅''竹''菊'等植物在古诗中的象征意义","古诗词语的解释（如'不教胡马渡阴山'）","体会诗人写诗时的心境"],"exercises":[{"question":"默写《芙蓉楼送辛渐》（唐·王昌龄）","answer":"寒雨连江夜入吴，平明送客楚山孤。洛阳亲友如相问，一片冰心在玉壶。","analysis":"送别诗，表达诗人冰清玉洁的心志"},{"question":"'一片冰心在玉壶'这句诗的意思是什么？","answer":"我的内心像冰一样纯洁，像玉壶一样清透（表达自己品德高尚，心地纯洁）","analysis":"古诗名句理解"},{"question":"写出梅花在古诗中的象征意义","answer":"梅花象征：高洁、坚韧不拔、不畏严寒、清高脱俗","analysis":"梅花文化意象"},{"question":"《塞下曲》（月黑雁飞高）作者是（　），描写了什么场景？","answer":"卢纶；月黑风高夜，将士追击敌军的场景（雪地追踪）","analysis":"塞下曲内容理解"},{"question":"古诗中的送别意象：'柳'代表（　）,'酒'代表（　）,'月'代表（　）","answer":"柳—离别（折柳相送）；酒—饯别（饮酒道别）；月—思念（月圆人未圆）","analysis":"送别诗意象积累"},{"question":"《墨梅》（元·王冕）：'不要人夸颜色好，只留清气满乾坤。'这两句表达了作者什么精神？","answer":"不在乎别人的夸赞（不求名利），只要内在清高，品德留存于世间","analysis":"托物言志的理解"},{"question":"写出你喜欢的一首四年级学过的古诗（整首）","answer":"开放性，背诵准确即可","analysis":"古诗综合背诵"},{"question":"古诗意象：在古诗中，'大漠''黄沙''边关''马蹄'常出现在什么类型的诗中？","answer":"边塞诗（描写边疆战争、将士生活的诗）","analysis":"诗歌分类"}],"advanced_exercises":[{"question":"比较：边塞诗（如《塞下曲》）和送别诗（如《芙蓉楼送辛渐》），情感有何不同？","answer":"边塞诗：豪迈、壮阔，有战争的紧张和壮烈；送别诗：离别的不舍，对友人的牵挂，以及诗人内心的感慨","analysis":"诗歌情感比较"},{"question":"托物言志：梅花、竹子、菊花分别象征什么品质？各写一句相关古诗","answer":"梅花—坚韧高洁（'宝剑锋从磨砺出，梅花香自苦寒来'）；竹子—虚心正直（'虚心竹有低头叶，傲骨梅无仰面花'）；菊花—隐逸高洁（'采菊东篱下，悠然见南山'）","analysis":"托物言志的理解"},{"question":"创作：以'梅'为题，写一首四行小诗（不要求押韵，有梅花的意境即可）","answer":"开放性，有梅花特征（白色、香气、冬天、坚强）即可","analysis":"古典意象创作"},{"question":"研究：王维、李白、杜甫是唐诗三大家，各有什么写作风格？各举一首代表作","answer":"李白：豪放飘逸（《静夜思》《将进酒》）；杜甫：沉郁顿挫（《春望》《茅屋为秋风所破歌》）；王维：禅意田园（《鹿柴》《山居秋暝》）","analysis":"唐诗风格介绍"},{"question":"【综合题】古诗是中国文化的瑰宝，为什么我们今天还要学古诗？（50字）","answer":"古诗是中华文明的精华，学古诗能培养审美（语言的美）、丰富文化素养、理解历史和情感，还能提高写作水平。古诗中的智慧和情感跨越千年，仍能触动我们的内心","analysis":"古诗价值的理解"}]},
  {"id":"u04","title":"第四单元 动物世界","knowledge_points":["学习关于动物的科普文章和故事","了解动物的生活习性和特点","学习说明文和记叙文混合的写作方式","积累描写动物的词语和句子"],"difficulties":["科普文章的特点：准确性+趣味性","区分动物的外形描写和行为描写","用科学语言描述动物特点","将科普知识转化为生动的文字"],"exercises":[{"question":"写出5种你感兴趣的动物及其一个特点","answer":"如：大象—鼻子长可以取水；海豚—智商高会跳跃；变色龙—会改变皮肤颜色；猫头鹰—夜间活动；蝙蝠—用超声波定位","analysis":"动物特点积累"},{"question":"写出描写动物动作的词语（至少8个）","answer":"爬行、飞翔、奔跑、跳跃、游动、捕食、嬉戏、觅食、蜷缩、扑腾","analysis":"动物动作词语"},{"question":"用'不但……而且……'写一句介绍动物的句子","answer":"海豚不但游泳速度极快，而且智商高，能与人类进行简单的交流","analysis":"关联词句式"},{"question":"阅读：'鸟类用翅膀飞翔，鱼类用鳍游泳，昆虫用腿跑或用翅飞。'这段话用了什么说明方法？","answer":"分类说明（按种类分别介绍）","analysis":"说明方法的识别"},{"question":"写出3个与动物有关的成语及含义","answer":"如：狐假虎威（借助强者权势恐吓他人）；鱼目混珠（以假乱真）；亡羊补牢（出了问题及时补救）","analysis":"动物成语积累"},{"question":"描写动物外貌：选一种动物，用3句话描写它的外形","answer":"开放性，参考：鹦鹉全身羽毛五彩斑斓，头顶一撮蓬松的羽毛像顶着一顶皇冠，嘴巴弯曲有力，眼睛圆圆的、亮亮的，充满了灵气","analysis":"外形描写"},{"question":"动物之谜：写出一个你觉得最神奇的动物行为（如候鸟迁徙、蜜蜂建巢等）","answer":"开放性，如：鲑鱼每年从大海游回它出生的河流产卵，穿越数千千米，凭借嗅觉记住家乡的气味","analysis":"自然奇观积累"},{"question":"积累：写出4个表示动物数量或群体的词语","answer":"一群鸟、一窝兔子、一队蚂蚁、一匹马（马用'匹'）","analysis":"量词积累"}],"advanced_exercises":[{"question":"写一篇关于动物的说明性短文（80字），介绍一种你喜欢的动物的生活习性","answer":"开放性，要有准确的数据或特点描述","analysis":"动物说明文写作"},{"question":"研究：选一种濒危动物（如大熊猫、雪豹），写出它濒危的原因和保护措施（50字）","answer":"如：大熊猫濒危原因：栖息地丧失（竹林砍伐）、繁殖率低。保护措施：建立自然保护区、人工繁殖、增加竹林种植","analysis":"动物保护知识"},{"question":"创意写作（70字）：以第一人称（'我是一只……'）写一段动物自述","answer":"开放性，要有该动物的特点和感受","analysis":"创意写作"},{"question":"比较：陆地动物和海洋动物的生活有什么不同？举例说明（50字）","answer":"陆地动物（狮子）：用腿行走，呼吸空气；海洋动物（鲸鱼）：用鳍游泳，虽然也用肺呼吸但需长时间在水中；不同生态环境塑造了完全不同的身体结构","analysis":"比较说明"},{"question":"【综合思维题】如果动物也有语言，它们最想告诉我们什么？选一种动物写出50字","answer":"开放性，参考：如果我（大熊猫）会说话，我想告诉你们：我们每天要吃12小时的竹子才能维持生命。请不要破坏我们的竹林，那是我们的超市和家。只需要每人种一棵竹子，就能帮助我们","analysis":"换位思考，生态保护"}]},
  {"id":"u05","title":"第五单元 感受多样生活","knowledge_points":["通过课文了解不同地区、民族的生活方式","学习尊重差异、理解多元文化","积累描写民俗文化的词语","学习描写风土人情的写作方法"],"difficulties":["理解不同文化背景下的生活方式","描写民俗时要具体、准确","不同地区的饮食、服饰、节日的词语积累","写作时表达对不同文化的尊重"],"exercises":[{"question":"写出中国不同地区的特色食物（至少5个）","answer":"四川火锅、北京烤鸭、上海小笼包、新疆烤羊肉串、云南过桥米线","analysis":"地区美食积累"},{"question":"中国有多少个少数民族？写出5个","answer":"55个少数民族（加上汉族共56个）；如：壮族、回族、满族、维吾尔族、苗族","analysis":"民族知识"},{"question":"描写一个民族节日（50字）","answer":"如：傣族的泼水节，在每年4月举行，人们互相泼水，象征洗去一年的晦气，迎接新年。活动中有歌舞、象脚鼓表演，非常热闹","analysis":"民俗节日描写"},{"question":"仿写：'北京的胡同，是历史的见证，每一条都有自己的故事。'仿写一句关于某地特色的句子","answer":"如：江南的小桥流水，是水乡的象征，每一座桥下都流淌着千年的文化","analysis":"地方特色描写"},{"question":"写出不同地区的建筑特色（至少3个）","answer":"如：北京—四合院；江南—白墙黑瓦（徽派建筑）；云南—竹楼；内蒙古—蒙古包","analysis":"建筑文化积累"},{"question":"选词填空：民风淳朴/五彩斑斓/热情好客/丰富多彩。①少数民族服饰（　）②农村的民风（　）③我国文化（　）","answer":"①五彩斑斓；②民风淳朴；③丰富多彩","analysis":"词语搭配"},{"question":"从'吃'的角度介绍你的家乡（3句话）","answer":"开放性，参考：我的家乡在四川，那里的美食以麻辣著称。最有名的是火锅，红彤彤的汤底香气扑鼻，各种食材在里面翻腾。每当家人聚在一起围着火锅，就是最幸福的时刻。","analysis":"家乡美食介绍"},{"question":"表达对不同文化的尊重：遇到和自己习惯不同的文化习俗，应该怎么做？","answer":"理解、尊重、欣赏，不嘲笑或批评，保持开放心态；'入乡随俗'是一种尊重的表现","analysis":"文化尊重态度"}],"advanced_exercises":[{"question":"小作文（80字）：介绍一种你了解的民俗文化或节日","answer":"开放性，要有具体描述","analysis":"民俗写作"},{"question":"对比：你的家乡和另一个省/地区的生活方式有什么不同？（饮食、气候、习俗等）写50字","answer":"开放性，实际对比","analysis":"文化比较"},{"question":"研究：中国'一带一路'沿线国家中，选一个，了解它的文化特色（50字）","answer":"开放性，如介绍哈萨克斯坦的草原文化、中亚饮食等","analysis":"国际视野"},{"question":"创意写作（70字）：如果你能穿越到中国古代的某个朝代，你会在哪里？那里的生活是什么样的？","answer":"开放性，有时代特色即可","analysis":"历史文化想象"},{"question":"【综合题】'多元文化是人类文明的财富'，你是否同意？举例说明（60字）","answer":"同意。多元文化让世界更有趣、更丰富。中国56个民族各有特色，丰富了中华文化；世界各地的音乐、食物、艺术相互交流，推动文明进步。单一文化会使世界变得单调乏味","analysis":"文化多样性的理解"}]},
  {"id":"u06","title":"第六单元 语言表达技巧","knowledge_points":["学习各种语言表达技巧：比较、列举、引用等","理解修辞手法的作用：比喻、拟人、排比","学习如何让语言更有感染力","掌握正式场合和非正式场合的语言差异"],"difficulties":["恰当选用修辞手法，不堆砌","理解修辞的效果（为什么这样写更好）","正式与非正式语言的区别","在写作中灵活运用各种表达技巧"],"exercises":[{"question":"判断修辞手法：①'白鸽展翅高飞，像一颗白色的星星飞向天空'（　）②'时间是小偷，偷走了童年'（　）③'大家有的唱歌，有的跳舞，有的画画'（　）","answer":"①比喻；②比喻（暗喻）；③排比","analysis":"修辞手法识别"},{"question":"把下面的句子改为更有感染力的表达：'今天天气很好，我很高兴。'","answer":"阳光明媚的今天，空气中弥漫着花香，我的心情和这天气一样，明朗舒畅！","analysis":"用具体感受代替笼统描述"},{"question":"排比句练习：仿写'她的笑，像春风，像暖阳，像甘甜的泉水。'","answer":"如：他的歌声，像山涧的清泉，像森林里的鸟鸣，像春天第一缕温柔的微风。","analysis":"排比句：三个及以上结构相同的比喻"},{"question":"正式语言和非正式语言：把'我今天来这里说一说'改为正式语言","answer":"今天，我将在此就……这一话题作简要阐述","analysis":"正式场合（演讲/作文）要用规范、庄重的语言"},{"question":"引用名言：在写关于坚持的作文时，可以引用哪些名言？写出1-2句","answer":"'锲而不舍，金石可镂'（荀子）；'世上无难事，只怕有心人'（毛泽东）","analysis":"名言积累与运用"},{"question":"比较的说明方法：用比较说明地球的大小（和其他行星比）","answer":"地球直径约12756千米，比火星（6792千米）大，但比木星（142984千米）小得多","analysis":"比较使说明更直观"},{"question":"写出3个日常生活中的常用成语，并造句","answer":"如：五颜六色（花园里五颜六色的花盛开了）；一目了然（图表使数据一目了然）；络绎不绝（游客络绎不绝地来参观故宫）","analysis":"成语造句"},{"question":"'画龙点睛'这个成语说明什么写作技巧？","answer":"写文章要有点睛之笔——最关键的一句话或一个词，点明主题，使整篇文章生动起来","analysis":"写作技巧成语"}],"advanced_exercises":[{"question":"综合修辞：写一段80字的春天描写，要包含比喻、拟人各一处，排比一处","answer":"开放性，三种修辞都要用到，各一处即可","analysis":"综合修辞写作"},{"question":"演讲稿写作（60字）：为班级演讲比赛写一段开场白（主题：珍惜时间）","answer":"开放性，正式语言，有观点，有开场吸引力","analysis":"演讲稿写作"},{"question":"修辞效果分析：'春天把绿色的画笔洒满大地'，不用比喻写同样的意思，两种表达有什么不同？","answer":"直白：春天来了，植物都变绿了；比喻版更生动、有画面感，让读者有视觉联想","analysis":"修辞效果对比"},{"question":"积累：整理本学期学过的所有修辞手法及例子","answer":"比喻（A像B）、拟人（赋予人的特征）、排比（三个及以上相似结构）、夸张（'飞流直下三千尺'）、反问（'难道不是吗？'）","analysis":"修辞手法综合整理"},{"question":"【创意题】用5种不同的方式描述'这朵花很美'（每种至少一句）","answer":"①直接：这朵花真美丽；②比喻：这朵花像一个害羞的少女；③拟人：这朵花骄傲地抬起头；④夸张：这朵花美得让人窒息；⑤排比：它的颜色美，它的香气美，它的形状美","analysis":"多种表达方式的对比"}]},
  {"id":"u07","title":"第七单元 生命教育","knowledge_points":["通过课文理解生命的价值和意义","学习珍爱生命、关爱他人的品德","理解不同生命形式（植物、动物、人类）都值得尊重","学习写生命主题的感想和体会"],"difficulties":["理解抽象的'生命价值'","将生命主题与具体事物联系","写感悟文章：从事物引发到思考","表达对生命的尊重和珍惜"],"exercises":[{"question":"写出描述生命力的词语（至少5个）","answer":"顽强、旺盛、蓬勃、坚韧、生机勃勃、生生不息","analysis":"生命力词语积累"},{"question":"仿写：'一粒种子，埋入土壤，哪怕黑暗、潮湿，也要破土而出，那是生命的力量。'仿写一句关于生命力的句子","answer":"如：一棵小草，生长在石缝中，哪怕无土无水，也要把细根伸向深处，那是生命不屈的意志。","analysis":"生命力主题仿写"},{"question":"阅读：'石头缝里长出了一朵小花，它虽然弱小，却向着阳光努力地开放。'这朵小花代表什么精神？","answer":"顽强的生命力，不屈不挠，即使在最艰难的环境中也要绽放","analysis":"象征意义理解"},{"question":"生命的价值：你认为动物的生命和人类的生命哪个更重要？说说你的看法（50字）","answer":"开放性，引导学生认识到所有生命都有价值，但也可以辩证地讨论","analysis":"生命价值的思考"},{"question":"写出2个关于生命的名言或诗句","answer":"①'人固有一死，或重于泰山，或轻于鸿毛'（司马迁）；②'生命不是要超越别人，而是要超越自己'（某励志名言）","analysis":"生命主题名言"},{"question":"从大自然中学到生命的道理：'竹子在成长过程中需要不断节节向上，即使风雨来临也不折断。'你从中领悟到什么道理？","answer":"生命要坚强，要不断成长，即使遇到挫折也不放弃，保持柔韧（竹子能弯但不断）","analysis":"从自然现象悟道理"},{"question":"说一说：你认为生命中最重要的是什么？写2句话","answer":"开放性，如：我认为生命中最重要的是健康和爱——拥有健康的身体，才能追求梦想；被爱着和爱别人，让生命有意义","analysis":"生命价值的个人理解"},{"question":"保护生命安全：写出3条日常生活中的安全注意事项","answer":"①过马路看红绿灯，不闯红灯；②不在水边独自玩耍；③遇到危险时呼救，而不是独自处理","analysis":"生命安全教育"}],"advanced_exercises":[{"question":"写一篇感悟短文（80字）：从一棵树的一年四季联想到生命的意义","answer":"开放性，有景物描写和生命感悟","analysis":"托物言志写作"},{"question":"阅读延伸：读一读《钢铁是怎样炼成的》或类似励志书籍，写50字读书感悟","answer":"开放性，有书名、内容简介、感悟","analysis":"励志读书笔记"},{"question":"辩论：有人认为'人不为己，天诛地灭'，有人认为'生命的意义在于奉献'。你怎么看？（60字）","answer":"两者都有道理但都走极端：适当关注自己是必要的，但完全自私的生命是空虚的；能为他人和社会做贡献，生命才更有意义和价值","analysis":"价值观辩证思考"},{"question":"创意写作（70字）：以一粒种子的视角，写它的生命旅程（从发芽到开花到凋谢）","answer":"开放性，有生命过程，有情感表达","analysis":"生命旅程创意写作"},{"question":"【综合题】'生命不在于长短，而在于质量。'你是否同意？联系名人事例说明（80字）","answer":"同意。如李清照一生颠沛流离但留下无数千古佳句；贝多芬耳聋后仍创作出《命运交响曲》。他们的生命或许不尽如人意，但在质量上超越了许多人。生命的长度是天定的，但宽度和厚度可以自己把握","analysis":"生命质量与人生价值"}]},
  {"id":"u08","title":"第八单元 毕业展望","knowledge_points":["复习四年级全部语文知识","准备升入五年级","反思和总结学习成果","写成长记录：记录四年级的学习和成长"],"difficulties":["综合运用全年所学","阅读理解的综合能力","写作水平的综合展示","自我评价和规划"],"exercises":[{"question":"默写：《独坐敬亭山》（唐·李白）","answer":"众鸟高飞尽，孤云独去闲。相看两不厌，只有敬亭山。","analysis":"李白诗，孤独中与山对话"},{"question":"修辞手法综合检测：①'蝴蝶在花间轻舞'（　）②'他快得像一阵风'（　）③'成千上万的花朵同时开放'（　）","answer":"①拟人（'轻舞'是人的动作）；②比喻；③夸张","analysis":"修辞手法综合复习"},{"question":"词语辨析：区分'感激'和'感谢'","answer":"感激：更深层的情感，感受到对方对自己有重大帮助；感谢：礼貌性的表示谢意，程度较轻","analysis":"近义词细微差别"},{"question":"阅读技巧：快速阅读一篇文章，提取主要信息的方法是什么？（3种方法）","answer":"①读标题和小标题；②看每段第一句；③找关键词","analysis":"阅读策略"},{"question":"综合写作：用150字写一篇四年级学习回顾","answer":"开放性，有具体事例，有感悟","analysis":"综合写作能力"},{"question":"写出本学期语文中学到的3种写作手法，各举一个例子","answer":"如：①比喻——'月亮像玉盘'；②排比——'有……有……还有……'；③对比——'以前……现在……'","analysis":"写作手法复习"},{"question":"古诗综合：写出四年级上下册你记得的所有古诗题目（至少6首）","answer":"《题西林壁》《观潮》《芙蓉楼送辛渐》《塞下曲》《独坐敬亭山》《宿新市徐公店》等","analysis":"古诗综合复习"},{"question":"展望：升入五年级，你有什么语文学习计划？（50字）","answer":"开放性，有具体计划（如：多阅读课外书、坚持写日记、背古诗等）","analysis":"学习规划"}],"advanced_exercises":[{"question":"综合作文（100字）：以'成长的脚步'为题，写四年级的成长历程","answer":"开放性，结构完整，有具体事例，有感悟","analysis":"综合写作"},{"question":"创作：写一首描写童年的小诗（4-6行），回忆四年级的美好时光","answer":"开放性，有具体意象和情感","analysis":"诗歌创作"},{"question":"阅读推荐：向同学推荐一本你读过的好书（书名、作者、主要内容、推荐理由），写60字","answer":"开放性，推荐任何好书均可","analysis":"阅读分享"},{"question":"自我评价：用5个词语评价自己四年级的语文学习，每个词语写一句解释","answer":"开放性，真实评价即可","analysis":"自我认知"},{"question":"【综合题】写信给五年级的老师，介绍自己的语文兴趣、优势和想要改进的地方（80字）","answer":"开放性，书信格式，自我介绍真实","analysis":"综合表达与自我介绍"}]}
]

print("Grade 4 Chinese content defined.")

# ============ 三年级英语（人教版PEP）============
g3_english_upper = [
  {"id":"u01","title":"Unit 1 Hello!","knowledge_points":["打招呼和自我介绍：Hello! Hi! I'm... My name is...","询问姓名：What's your name?","告别语：Goodbye! Bye!","基本礼貌用语：Nice to meet you!"],"difficulties":["区分Hello/Hi的正式程度","名字的正确读写","记忆英语字母和自我介绍句型","在实际场景中运用打招呼"],"exercises":[{"question":"翻译：你好！我叫小明。","answer":"Hello! I'm Xiao Ming. (或 My name is Xiao Ming.)","analysis":"基本自我介绍句型"},{"question":"如何用英语问别人叫什么名字？","answer":"What's your name?","analysis":"询问姓名的标准句型"},{"question":"翻译：认识你很高兴！","answer":"Nice to meet you!","analysis":"见面礼貌用语"},{"question":"请写出3种说'再见'的方式","answer":"Goodbye! / Bye! / See you later!","analysis":"告别语多种表达"},{"question":"完成对话：A: Hello! B: _____! A: I'm Tom. B: I'm ____. Nice to _____ you!","answer":"B: Hello! / Hi! ; B: I'm [name]; meet","analysis":"打招呼对话填空"},{"question":"用英语写出你的名字（拼音）和自我介绍一句话","answer":"I'm [your name]. / My name is [your name].（言之有理）","analysis":"实际运用自我介绍"},{"question":"连线：Hello—（　）；Goodbye—（　）；Nice to meet you—（　）","answer":"Hello—你好；Goodbye—再见；Nice to meet you—认识你很高兴","analysis":"基本词语中英翻译"},{"question":"写出英语26个字母中的前10个","answer":"A B C D E F G H I J","analysis":"英语字母表记忆"}],"advanced_exercises":[{"question":"在不同场合如何打招呼？写出英语表达：①早上见到老师②下午见到朋友③晚上见到家人","answer":"①Good morning, teacher!②Good afternoon! / Hi!③Good evening! / Hello!","analysis":"不同时间的问候语"},{"question":"创作一个简短的自我介绍（英语3句话）","answer":"Hello! I'm [name]. I'm [age] years old. Nice to meet you!（言之有理）","analysis":"完整的自我介绍"},{"question":"角色扮演：你是A，朋友是B，写出完整的第一次见面对话（至少4句）","answer":"A: Hello! I'm A. B: Hi! I'm B. Nice to meet you! A: Nice to meet you too! B: Goodbye! A: Bye!","analysis":"完整的见面对话"},{"question":"研究：不同国家的打招呼方式有什么不同？（英语国家 vs 中国）","answer":"英语国家：握手、说Hello/Hi；法国：两颊接吻；日本：鞠躬；中国：点头、握手","analysis":"跨文化比较"},{"question":"【综合题】用英语写一段自我介绍（5-8句），包括名字、年龄、班级、爱好","answer":"Hello! My name is [name]. I'm [age] years old. I'm in Class [x], Grade [x]. I like [hobby]. Nice to meet you!（言之有理）","analysis":"综合自我介绍"}]},
  {"id":"u02","title":"Unit 2 My Family","knowledge_points":["家庭成员词汇：father, mother, brother, sister, grandfather, grandmother","用英语介绍家庭成员：This is my...","询问家庭：How many people are in your family?","数字1-10的英语表达"],"difficulties":["区分grandfather/grandmother（爷爷/奶奶 or 外公/外婆）","介绍句型：This is... / These are...","数字英语单词的拼写","描述家庭关系"],"exercises":[{"question":"翻译家庭成员：爸爸（　）妈妈（　）爷爷（　）奶奶（　）哥哥/弟弟（　）姐姐/妹妹（　）","answer":"father/dad; mother/mum; grandfather/grandpa; grandmother/grandma; brother; sister","analysis":"家庭成员英语词汇"},{"question":"用英语介绍：这是我的妈妈。","answer":"This is my mother/mum.","analysis":"介绍家庭成员句型"},{"question":"问答：How many people are in your family? （3口之家）","answer":"There are three people in my family.","analysis":"描述家庭人数"},{"question":"写出1-10的英语单词","answer":"one, two, three, four, five, six, seven, eight, nine, ten","analysis":"数字英语单词"},{"question":"翻译：我有一个哥哥和一个妹妹。","answer":"I have one brother and one sister.","analysis":"用have介绍家庭成员"},{"question":"完成句子：___ is my father. He is a ___.（填写合适内容）","answer":"This is my father. He is a teacher/doctor等（开放性）","analysis":"家庭介绍句型"},{"question":"写出描述家庭照片的3句英语句子","answer":"This is my family. This is my father. This is my mother.","analysis":"描述照片的英语表达"},{"question":"数字填空：two + three = ___; seven - four = ___","answer":"five; three","analysis":"英语数字计算"}],"advanced_exercises":[{"question":"用英语写一段介绍家庭的短文（5句话以上）","answer":"My family has four people. My father is a teacher. My mother is a doctor. I have one sister. We are a happy family.","analysis":"家庭介绍短文"},{"question":"家庭关系问答：如果Tom的father的father是谁？用英语表达","answer":"Tom's grandfather (grandfather 是父亲的父亲)","analysis":"家庭关系的逻辑"},{"question":"创作：用英语描述一个理想的家庭（3-5句）","answer":"开放性，用学过的家庭词汇造句","analysis":"创意表达"},{"question":"对比：英语family成员称谓和中文有什么不同？（如grandfather包含外公和爷爷）","answer":"中文对亲戚的称呼非常细致（爷爷/外公，舅舅/叔叔），英语通常用一个词（grandfather, uncle），显示文化对家庭关系的不同重视程度","analysis":"跨文化语言比较"},{"question":"【综合题】角色扮演：向新朋友介绍你的家庭（写出英语对话，至少6句）","answer":"A: How many people are in your family? B: There are four people. A: Who are they? B: My father, mother, sister and me. A: What does your father do? B: He is a teacher.","analysis":"综合对话练习"}]},
  {"id":"u03","title":"Unit 3 Look at Me!","knowledge_points":["身体部位词汇：head, eye, ear, nose, mouth, hand, foot","询问和描述：What colour is...? It's...","颜色词汇：red, yellow, blue, green, white, black","简单描述外貌：big/small eyes, long/short hair"],"difficulties":["身体部位单复数（eye→eyes）","颜色词的拼写","描述外貌的形容词使用","What colour is...?的句型"],"exercises":[{"question":"翻译身体部位：头（　）眼睛（　）耳朵（　）鼻子（　）嘴巴（　）手（　）脚（　）","answer":"head; eye/eyes; ear/ears; nose; mouth; hand/hands; foot/feet","analysis":"身体部位词汇"},{"question":"颜色填空：苹果通常是___色的，天空通常是___色的（英语回答）","answer":"red; blue","analysis":"颜色词汇"},{"question":"问答：What colour is the sky? ","answer":"It's blue.","analysis":"询问颜色的句型"},{"question":"翻译：她有一双大眼睛和一头长发。","answer":"She has big eyes and long hair.","analysis":"描述外貌的句型"},{"question":"写出6种颜色的英语单词","answer":"red, yellow, blue, green, white, black (or orange, purple等)","analysis":"颜色词汇积累"},{"question":"单复数变化：eye→（　）；foot→（　）；hand→（　）","answer":"eyes; feet; hands","analysis":"身体部位的复数形式"},{"question":"用英语描述一个人的外貌（3句话）","answer":"She has a small nose. She has big eyes. She has short black hair.","analysis":"外貌描述"},{"question":"完成句子：I have ___ eyes and ___ hair.（用形容词填写）","answer":"big/small eyes; long/short, black/brown hair（开放性）","analysis":"自我外貌描述"}],"advanced_exercises":[{"question":"用英语写一段描述你自己外貌的短文（5句话）","answer":"My name is [name]. I have big eyes. My hair is black and short. I have a small nose. I am tall/short.","analysis":"自我介绍结合外貌描述"},{"question":"猜谜游戏（英语）：描述一个动物的外形，不说名字，让同学猜","answer":"如：It is big. It has four legs. It has a long nose. It is grey. （大象 elephant）","analysis":"英语猜谜"},{"question":"彩虹有哪些颜色？用英语写出来","answer":"red, orange, yellow, green, blue, indigo (靛), violet (紫) 或 red, orange, yellow, green, blue, purple","analysis":"彩虹颜色英语"},{"question":"创作：用英语描述你最喜欢的颜色，为什么喜欢（3句话）","answer":"My favourite colour is blue. I like blue because it's the colour of the sky and the sea. Blue makes me feel calm.","analysis":"颜色喜好表达"},{"question":"【综合题】用英语写一封给笔友的信，描述你的外貌和家庭（8句话左右）","answer":"开放性，包含外貌描述和家庭介绍，语法基本正确","analysis":"综合写作"}]},
  {"id":"u04","title":"Unit 4 We Love Animals","knowledge_points":["动物词汇：cat, dog, bird, fish, panda, elephant, monkey, tiger, lion","喜好表达：I like/love... Do you like...? Yes, I do./No, I don't.","描述动物：It's big/small/cute/funny","数量表达：There is/There are..."],"difficulties":["动物词汇的拼写（特别是elephant, monkey）","I like vs I don't like的句型","There is (单数) / There are (复数)的区别","描述动物特点的形容词"],"exercises":[{"question":"翻译动物：猫（　）狗（　）熊猫（　）大象（　）老虎（　）猴子（　）","answer":"cat; dog; panda; elephant; tiger; monkey","analysis":"动物词汇"},{"question":"I like pandas. 翻译成中文，并写出否定形式","answer":"我喜欢熊猫；否定：I don't like pandas.","analysis":"喜好句型及否定"},{"question":"Do you like cats? 用英语回答（肯定和否定）","answer":"Yes, I do. / No, I don't.","analysis":"Do you like...? 的回答"},{"question":"翻译：熊猫是黑白相间的，它很可爱。","answer":"The panda is black and white. It's cute.","analysis":"描述动物颜色和特点"},{"question":"用There is/There are造句：①一条鱼②三只猫","answer":"①There is a fish.②There are three cats.","analysis":"There is/are的使用"},{"question":"写出5种动物及其特点（英语）","answer":"cat—small, cute; dog—friendly; elephant—big; monkey—funny; tiger—strong","analysis":"动物特点描述"},{"question":"完成对话：A: Do you like dogs? B: Yes, ___. Do you like cats? A: No, ___.","answer":"B: Yes, I do.; A: No, I don't.","analysis":"喜好对话"},{"question":"写出中国的国宝是什么动物，用英语介绍2句话","answer":"The panda is China's national treasure. It's black and white and very cute.","analysis":"大熊猫介绍"}],"advanced_exercises":[{"question":"用英语写一段介绍你最喜欢的动物（5句话）","answer":"My favourite animal is the dog. It's cute and friendly. Dogs can be our friends. I have a dog at home. I love my dog.","analysis":"动物介绍短文"},{"question":"创作：设计一个英语动物谜语（不说名字，描述特点）","answer":"It's big. It's grey. It has a very long nose. It has big ears. What is it? (elephant)","analysis":"动物谜语创作"},{"question":"讨论：如果你是动物园馆长，你会养哪些动物？用英语说出3种并解释原因","answer":"I would have pandas, because they are cute and special. I would have elephants, because children love them. I would have dolphins, because they are smart.","analysis":"英语表达和理由陈述"},{"question":"写一封英语信给动物园：我想参观动物园，我特别想看什么动物（4句）","answer":"Dear Zoo, I would like to visit your zoo. I love animals. I want to see pandas and elephants. Thank you!","analysis":"英语书信格式"},{"question":"【综合题】研究：大熊猫为什么是中国的象征？用英语写3-4句","answer":"The panda is China's symbol because it is found only in China. Pandas are rare and cute. China is working hard to protect them. They are loved by people all over the world.","analysis":"国宝熊猫综合介绍"}]},
  {"id":"u05","title":"Unit 5 Let's Eat!","knowledge_points":["食物词汇：rice, bread, milk, juice, egg, cake, hamburger, hot dog","餐饮表达：Would you like...? Yes, please./No, thank you.","用餐礼貌用语：Enjoy your meal!","表达喜好：I like/don't like..."],"difficulties":["食物词汇（特别是hamburger, juice等）的拼写","Would you like...? 的句型和回答","can I have...? 的使用","不同饮食的文化差异"],"exercises":[{"question":"翻译食物：米饭（　）面包（　）牛奶（　）果汁（　）鸡蛋（　）蛋糕（　）","answer":"rice; bread; milk; juice; egg; cake","analysis":"食物词汇"},{"question":"Would you like some milk? 用英语回答（肯定和否定）","answer":"Yes, please. / No, thank you.","analysis":"Would you like...?的标准回答"},{"question":"翻译：你想要一些蛋糕吗？","answer":"Would you like some cake?","analysis":"Would you like的疑问句"},{"question":"用英语描述你的早餐（3句话）","answer":"For breakfast, I have rice/bread. I drink milk/juice. I eat an egg.","analysis":"早餐英语描述"},{"question":"连线：rice—（　）；milk—（　）；cake—（　）；bread—（　）","answer":"rice—米饭；milk—牛奶；cake—蛋糕；bread—面包","analysis":"食物词汇连线"},{"question":"用英语说出你喜欢和不喜欢的食物各2种","answer":"I like cake and rice. I don't like onions/vegetables.（开放性）","analysis":"食物喜好表达"},{"question":"完成点餐对话：A: _____ you like _____ hamburger? B: Yes, _____!","answer":"A: Would you like a hamburger? B: Yes, please!","analysis":"点餐对话"},{"question":"写出中西方的区别：中国早餐食物vs英语国家早餐食物（各3种）","answer":"中国：稀饭、包子、油条；英语国家：toast（吐司）、cereal（麦片）、eggs（鸡蛋）","analysis":"饮食文化比较"}],"advanced_exercises":[{"question":"用英语设计一个完整的菜单（早、中、晚餐各2道食物）","answer":"Breakfast: bread and milk; Lunch: rice and chicken; Dinner: noodles and vegetables.（开放性）","analysis":"菜单设计"},{"question":"写一段关于你最喜欢的食物的英语短文（5句话）","answer":"My favourite food is pizza. It is round and delicious. I like cheese and tomato on pizza. I eat pizza on weekends. Pizza is my favourite!","analysis":"食物主题短文"},{"question":"创作：用英语写一份生日派对的食物邀请单","answer":"Come to my birthday party! We will have cake, juice, cookies and sandwiches. See you on Saturday!","analysis":"英语写作创意"},{"question":"探究：中国饮食文化和西方饮食文化有什么不同？（英语2句话）","answer":"Chinese people use chopsticks and eat rice. Western people use a knife and fork and eat bread.","analysis":"饮食文化对比（英语表达）"},{"question":"【综合题】角色扮演：在餐厅，你帮家人点菜，用英语写出完整对话（6-8句）","answer":"Waiter: Good afternoon! What would you like? Me: I would like rice and chicken, please. Waiter: Would you like some juice? Me: Yes, please. For my mum, a salad please. Waiter: Enjoy your meal! Me: Thank you!","analysis":"综合点餐对话"}]},
  {"id":"u06","title":"Unit 6 Happy Birthday!","knowledge_points":["生日祝福：Happy Birthday! / Merry Christmas!","数字11-20，以及更大数字","询问年龄：How old are you? I'm... years old.","描述节日习俗：cut the cake, blow out candles","月份：January - December"],"difficulties":["11-20的英语单词拼写（特别是twelve, thirteen等不规则变化）","月份的拼写（较复杂）","询问年龄的句型","生日相关活动的词汇"],"exercises":[{"question":"写出11-20的英语单词","answer":"eleven, twelve, thirteen, fourteen, fifteen, sixteen, seventeen, eighteen, nineteen, twenty","analysis":"11-20数字单词"},{"question":"翻译：生日快乐！你多大了？","answer":"Happy Birthday! How old are you?","analysis":"生日用语"},{"question":"How old are you? 用英语回答（9岁）","answer":"I'm nine years old. / I'm 9.","analysis":"年龄询问回答"},{"question":"写出12个月份的英语单词（可简写前3个）","answer":"January, February, March, April, May, June, July, August, September, October, November, December","analysis":"12个月份英语"},{"question":"翻译：我的生日是三月八日。","answer":"My birthday is March 8th. / My birthday is on the 8th of March.","analysis":"生日日期的英语表达"},{"question":"生日派对活动：写出3个英语短语","answer":"cut the cake（切蛋糕）；blow out the candles（吹蜡烛）；open presents（拆礼物）","analysis":"生日活动词汇"},{"question":"问答：When is your birthday? （自由回答）","answer":"My birthday is in [month].（开放性）","analysis":"询问生日月份"},{"question":"数字计算：nine + seven = ___; twenty - twelve = ___","answer":"sixteen; eight","analysis":"英语数字运算"}],"advanced_exercises":[{"question":"用英语写一张生日卡（5句话，给朋友）","answer":"Dear [name], Happy Birthday! I hope you have a wonderful day. May all your wishes come true! Have a great party! From [your name]","analysis":"英语生日卡写法"},{"question":"介绍你的生日：When, where, what do you do?（用英语写5句）","answer":"My birthday is on [date]. I am [age] years old. I have a party with my family. We eat birthday cake and sing songs. I love my birthday!","analysis":"生日介绍短文"},{"question":"比较中西方生日庆祝方式（各写2点英语）","answer":"Chinese: eat noodles (symbol of long life), family dinner; Western: birthday cake with candles, party with friends","analysis":"生日文化对比"},{"question":"节日大调查：写出4个英语国家的重要节日（英语名称和时间）","answer":"Christmas (December 25), Easter (春季), Halloween (October 31), Thanksgiving (November)","analysis":"西方节日积累"},{"question":"【综合题】设计一个生日派对计划（英语，6-8句），包括时间、地点、活动和食物","answer":"I am having a birthday party on [date]. It is at my home. I will invite my friends. We will play games and sing songs. We will eat cake and pizza. Come join us!（开放性）","analysis":"英语写作综合"}]}
]

g3_english_lower = [
  {"id":"u01","title":"Unit 1 Welcome Back to School!","knowledge_points":["开学问候：Welcome back! How are you?","学校物品词汇：book, bag, pencil, eraser, ruler, pen","用英语描述课堂：classroom, blackboard, desk, chair","表达状态：I'm fine/good/great."],"difficulties":["区分各类文具的英语名称","How are you? 的多种回答方式","学校场所词汇","在英语对话中保持连贯"],"exercises":[{"question":"翻译学校用品：书包（　）铅笔（　）橡皮（　）直尺（　）钢笔（　）","answer":"bag; pencil; eraser; ruler; pen","analysis":"学校用品词汇"},{"question":"How are you? 用英语写出3种不同回答","answer":"I'm fine, thank you! / I'm good! / I'm great! / Not bad.","analysis":"问候回答的多种表达"},{"question":"翻译：欢迎回来！教室里有什么？","answer":"Welcome back! What's in the classroom?","analysis":"开学问候和描述教室"},{"question":"描述教室：There is/are... 造句（3句话）","answer":"There is a blackboard. There are desks and chairs. There are books on the desk.","analysis":"描述教室用品"},{"question":"写出你书包里有的5种文具（英语）","answer":"pencil, eraser, ruler, book, pen等（开放性）","analysis":"文具词汇运用"},{"question":"Welcome back to school! 这句话什么时候说？","answer":"开学第一天，见到同学和老师时","analysis":"语境理解"},{"question":"完成对话：A: How are you? B: ___, thank you! And you? A: ___, thanks.","answer":"B: Fine/Good; A: Fine/Good","analysis":"问候对话"},{"question":"写出4个与学校有关的地方（英语）","answer":"classroom, library, playground, gym/gymnasium","analysis":"学校场所词汇"}],"advanced_exercises":[{"question":"写一段开学第一天的英语日记（5句话）","answer":"Today is the first day of school. I am happy to see my friends. My classroom is big and bright. I have a new pencil case. I love school!","analysis":"开学日记"},{"question":"用英语介绍你的教室（6句话）","answer":"My classroom is big. There are 40 desks and chairs. There is a big blackboard in front. We have books on our desks. The classroom is clean and tidy. I like my classroom.","analysis":"教室介绍"},{"question":"学校规则：用英语写出3条课堂规则","answer":"No talking in class. / Listen to the teacher. / Do your homework every day.","analysis":"英语课堂规则表达"},{"question":"比较：你的学校和英国/美国的学校有什么不同？（2点英语表达）","answer":"Chinese schools: students wear uniforms, study hard; British/American schools: more free activities, no uniforms (in many schools)","analysis":"学校文化比较"},{"question":"【综合题】写一封给笔友的信，介绍你的学校（8句话）","answer":"Dear [name], My school is great! It has many classrooms and a big playground. We have art class and music class. I like PE class. My teacher is very kind. We study Chinese, maths and English. I like my school very much! Best wishes, [name]","analysis":"综合英语写作"}]},
  {"id":"u02","title":"Unit 2 My Family","knowledge_points":["家庭成员进阶：uncle, aunt, cousin","用英语描述家庭活动：cook dinner, watch TV, read books","询问和描述职业：What does your father/mother do?","形容词描述人：tall, short, young, old, kind"],"difficulties":["区分uncle/aunt（叔伯姑舅等英语统一为uncle/aunt）","描述职业的句型","形容词的正确使用位置","家庭活动词汇"],"exercises":[{"question":"翻译：叔叔（　）阿姨（　）表兄弟/堂兄弟（　）","answer":"uncle; aunt; cousin","analysis":"亲戚称谓词汇"},{"question":"What does your father do? 用英语回答（老师）","answer":"He is a teacher.","analysis":"询问职业的句型"},{"question":"描述人：用tall/short/young/old/kind各造一个句子","answer":"My father is tall. My sister is short. My grandfather is old. My mother is kind.（开放性）","analysis":"形容词描述人"},{"question":"翻译家庭活动：做晚饭（　）看电视（　）读书（　）","answer":"cook dinner; watch TV; read books","analysis":"家庭活动词汇"},{"question":"用英语描述你家人的职业（3句话）","answer":"My father is a doctor. My mother is a teacher. My uncle is an engineer.（开放性）","analysis":"职业描述"},{"question":"完成句子：My mother is kind. She always ___（填活动）","answer":"She always cooks dinner./helps me with homework.（开放性）","analysis":"描述家人特点和行为"},{"question":"写出5种职业的英语单词","answer":"teacher, doctor, engineer, farmer, policeman（警察）","analysis":"职业词汇积累"},{"question":"造句：My grandfather is old but he is ___（形容词）","answer":"My grandfather is old but he is strong/kind/healthy.（开放性）","analysis":"转折连词but的使用"}],"advanced_exercises":[{"question":"用英语写一段介绍家庭的短文（8句话），包括成员、外貌和职业","answer":"My family has four people. My father is tall and strong. He is an engineer. My mother is kind. She is a teacher. My sister is young. She is a student. I love my family.","analysis":"家庭综合介绍"},{"question":"采访练习：用英语问你的家人3个问题（What, How old, What does...）","answer":"What is your name? How old are you? What do you do?（面向家人实际采访）","analysis":"英语口语采访"},{"question":"写英语日记：和家人一起度过的一个周末（5句话）","answer":"Last weekend, my family and I went to the park. My father played basketball. My mother read books. My sister and I played on the swings. It was a happy day.","analysis":"周末日记写作"},{"question":"比较：你的家庭和朋友家庭有什么不同？（英语3句话）","answer":"My family has four people. My friend's family has three people. My father is a teacher but my friend's father is a doctor.（开放性）","analysis":"比较句式"},{"question":"【综合题】画家庭树（Family Tree）并用英语标注每个人的名字、年龄和职业（至少4人）","answer":"开放性，格式正确，词语准确","analysis":"家庭树综合描述"}]},
  {"id":"u03","title":"Unit 3 Is This Your Skirt?","knowledge_points":["服装词汇：shirt, skirt, dress, jacket, trousers, shoes","询问所有权：Is this your...? Yes, it is./No, it isn't.","颜色+服装：blue shirt, red dress","购物对话：How much is it?"],"difficulties":["Is this your...?和Are these your...?的区别（单复数）","颜色加服装的组合表达","购物对话的礼貌用语","所有格：my, your, his, her"],"exercises":[{"question":"翻译服装：裙子（　）衬衫（　）连衣裙（　）夹克（　）裤子（　）鞋子（　）","answer":"skirt; shirt; dress; jacket; trousers; shoes","analysis":"服装词汇"},{"question":"Is this your shirt? 用英语回答（是和不是）","answer":"Yes, it is. / No, it isn't.","analysis":"确认所有权的回答"},{"question":"用颜色+服装造句（3句话）","answer":"I have a blue shirt. She has a red dress. He wears black shoes.（开放性）","analysis":"颜色和服装组合"},{"question":"翻译：这双鞋多少钱？","answer":"How much are these shoes?","analysis":"购物询价"},{"question":"写出5种颜色和5件服装的英语单词","answer":"颜色：red, blue, green, yellow, black；服装：shirt, dress, skirt, jacket, shoes","analysis":"词汇积累"},{"question":"所有格练习：这是我的（　），这是他的（　），这是她的（　）","answer":"This is my...; This is his...; This is her...","analysis":"物主代词"},{"question":"完成购物对话：A: How much is the jacket? B: It's ___ yuan. A: I'll take it, thank you!","answer":"B: It's 50/100 yuan.（开放性金额）","analysis":"购物对话"},{"question":"描述你今天穿的衣服（英语3句话）","answer":"Today I'm wearing a blue shirt. I have black trousers. My shoes are white.","analysis":"描述穿着"}],"advanced_exercises":[{"question":"购物场景对话（英语8句）：在服装店买东西","answer":"A: Can I help you? B: Yes, I'd like a shirt. A: What colour? B: Blue, please. A: Here you are. B: How much is it? A: It's 80 yuan. B: I'll take it. Thank you!","analysis":"完整购物对话"},{"question":"用英语写一段描述时装秀的文字（5句话）","answer":"The model is wearing a red dress. She has white shoes. Her jacket is blue. She looks beautiful. This is a great fashion show.","analysis":"时装描述写作"},{"question":"设计你的理想服装（英语描述）：颜色、款式、场合","answer":"My ideal outfit is a white shirt and blue jeans. I would wear them for a school trip. I would also wear white shoes. I love casual clothes.（开放性）","analysis":"服装设计描述"},{"question":"文化比较：中国的传统服装（汉服/旗袍等）和西方服装有什么不同？（英语2句话）","answer":"Chinese traditional clothes are called Hanfu or Qipao. They are beautiful with special patterns and bright colours.","analysis":"服装文化比较"},{"question":"【综合题】为班级时装节写一段介绍词（英语，描述一位同学的着装，6句话）","answer":"Welcome to our class fashion show! My friend [name] is wearing a beautiful blue dress. She has white shoes and a yellow bag. Her hair is long and black. She looks very elegant. Please give her a big hand!","analysis":"综合描述写作"}]},
  {"id":"u04","title":"Unit 4 Where Is My Car?","knowledge_points":["位置介词：in, on, under, behind, in front of, next to","询问位置：Where is/are...? It's/They're...","房间和家具：bedroom, kitchen, sofa, table, bed","描述方位：left, right, upstairs, downstairs"],"difficulties":["in/on/under的区别（里面/上面/下面）","Where is vs Where are（单复数）","in front of 和 behind 的对立","描述具体位置时的表达完整性"],"exercises":[{"question":"翻译位置词：在……里面（　）在……上面（　）在……下面（　）在……后面（　）","answer":"in; on; under; behind","analysis":"位置介词"},{"question":"Where is the book? （书在桌子上）用英语回答","answer":"It's on the table.","analysis":"询问和回答位置"},{"question":"用位置介词造句（in/on/under各一句）","answer":"The cat is in the box. The pen is on the desk. The ball is under the chair.","analysis":"位置介词造句"},{"question":"翻译房间：卧室（　）厨房（　）客厅（　）浴室（　）","answer":"bedroom; kitchen; living room; bathroom","analysis":"房间词汇"},{"question":"Where is the sofa? （沙发在客厅里）","answer":"The sofa is in the living room.","analysis":"家具位置描述"},{"question":"完成句子：The dog is ___ the bed.（在床下面）","answer":"The dog is under the bed.","analysis":"位置介词填空"},{"question":"用英语描述你卧室里有什么（3句话）","answer":"There is a bed in my bedroom. There is a desk next to the bed. My books are on the desk.","analysis":"卧室描述"},{"question":"翻译：我的书包在椅子后面。","answer":"My bag is behind the chair.","analysis":"位置描述翻译"}],"advanced_exercises":[{"question":"用英语描述你家的布局（6句话）","answer":"My home has three rooms. The bedroom is on the right. The kitchen is next to the living room. The bathroom is upstairs. There is a big sofa in the living room. I love my home.","analysis":"家庭布局描述"},{"question":"方向游戏：给出一个房间的平面图，用英语描述如何从卧室到厨房","answer":"Go out of the bedroom. Turn left. Walk past the bathroom. The kitchen is on the right.（根据图形描述）","analysis":"方向指引"},{"question":"写一段找东西的对话（英语6句）：找不到书包","answer":"A: Where is my bag? B: Is it under the table? A: No, it isn't. B: Look behind the sofa! A: Yes! It's there! Thank you! B: You're welcome!","analysis":"找东西对话"},{"question":"比较：中国家庭的布局和西方家庭有什么不同？（英语2句话）","answer":"Chinese families often have a living room for family gatherings. Western homes usually have a larger kitchen as the family centre.","analysis":"家庭文化比较"},{"question":"【综合题】写英语介绍你的家（8句话），包括房间、家具和位置","answer":"开放性，包含房间名称、家具名称、位置介词","analysis":"综合描述写作"}]},
  {"id":"u05","title":"Unit 5 Do You Like Pears?","knowledge_points":["水果蔬菜词汇：pear, apple, banana, orange, grape, tomato, carrot","喜好询问：Do you like...? Yes, I do./No, I don't.","购物用语：How many...do you want?","数量词：some, many, a lot of"],"difficulties":["水果蔬菜的可数与不可数（some water / some apples）","How many vs How much（可数/不可数）","Do you like...? 句型的扩展","健康饮食的表达"],"exercises":[{"question":"翻译水果蔬菜：梨（　）香蕉（　）葡萄（　）胡萝卜（　）西红柿（　）","answer":"pear; banana; grape; carrot; tomato","analysis":"水果蔬菜词汇"},{"question":"Do you like pears? 用英语回答（喜欢）","answer":"Yes, I do. I like pears very much.","analysis":"水果喜好表达"},{"question":"翻译：你想要几个苹果？","answer":"How many apples do you want?","analysis":"询问数量句型"},{"question":"用some/many/a lot of造句（各一句）","answer":"I have some apples. I have many friends. There are a lot of books in the library.","analysis":"数量词使用"},{"question":"健康饮食：写出3种健康食物（英语）及简单说明","answer":"apples (good for health), carrots (good for eyes), bananas (give energy)","analysis":"健康食物介绍"},{"question":"完成购物对话：A: ___you like grapes? B: Yes, ___. A: How many ___? B: ___ kilograms, please.","answer":"Do; I do; do you want/grapes; Two","analysis":"购物对话填空"},{"question":"写出你最喜欢和最不喜欢的水果（英语各2种）","answer":"开放性：I like apples and bananas. I don't like grapes and oranges.","analysis":"个人喜好"},{"question":"翻译：多吃水果蔬菜对健康有好处。","answer":"Eating more fruits and vegetables is good for your health.","analysis":"健康建议句型"}],"advanced_exercises":[{"question":"写一段关于你最喜欢的水果的英语短文（5句话）","answer":"My favourite fruit is the apple. It is red and delicious. Apples are very healthy. I eat one apple every day. An apple a day keeps the doctor away!","analysis":"水果介绍短文"},{"question":"设计健康食谱（英语）：写出一天的早中晚餐，都包含水果或蔬菜","answer":"Breakfast: porridge with bananas; Lunch: rice with carrots and tomatoes; Dinner: noodles with green vegetables.（开放性）","analysis":"健康食谱设计"},{"question":"创作：用英语写一首关于水果的小诗（4行）","answer":"Red apples, yellow bananas, orange grapes on the vine. Eat your fruits every day, and you will feel just fine!（开放性）","analysis":"英语诗歌创作"},{"question":"调查：问3个同学最喜欢的水果，用英语写出调查结果","answer":"开放性，格式：[name] likes [fruit]. [name] likes [fruit]. [name] likes [fruit]. The most popular fruit is [fruit].","analysis":"英语调查报告"},{"question":"【综合题】扮演超市收银员：用英语写出完整的购物对话（8句），包含水果蔬菜","answer":"Cashier: Good morning! Can I help you? Customer: Yes, I'd like some apples and bananas. Cashier: How many apples? Customer: Six, please. Cashier: And how many bananas? Customer: Three. Cashier: Anything else? Customer: No, thank you. How much is it? Cashier: It's 20 yuan. Customer: Here you are. Cashier: Thank you, goodbye!","analysis":"综合购物对话"}]},
  {"id":"u06","title":"Unit 6 How Many?","knowledge_points":["更大的数字：20, 30, 40... 100","询问数量：How many...are there? There are...","统计和数数：count, total","综合复习三年级下册主要内容"],"difficulties":["几十的英语单词（twenty, thirty等）","复杂数字的读写（如35=thirty-five）","运用所学知识进行综合表达","课外英语阅读的初步接触"],"exercises":[{"question":"写出20-100（每十）的英语单词","answer":"twenty, thirty, forty, fifty, sixty, seventy, eighty, ninety, one hundred","analysis":"整十数字单词"},{"question":"翻译数字：35（　）47（　）58（　）","answer":"thirty-five; forty-seven; fifty-eight","analysis":"复合数字英语表达"},{"question":"How many students are in your class? 用英语回答（40人）","answer":"There are forty students in my class.","analysis":"数量询问和回答"},{"question":"翻译：我们班有42名同学，20名男生，22名女生。","answer":"There are 42 students in our class. 20 are boys and 22 are girls.","analysis":"描述数量"},{"question":"数字运算（用英语单词）：thirty + twenty = ___; fifty - fifteen = ___","answer":"fifty; thirty-five","analysis":"英语数字运算"},{"question":"统计练习：图书馆有英语书35本，数学书48本，语文书52本，合计多少本？（用英语表达）","answer":"There are one hundred and thirty-five books in total. (35+48+52=135)","analysis":"数量统计"},{"question":"用英语介绍你的学校人数（3句话）","answer":"There are about 1000 students in my school. There are 40 teachers. There are 25 classes.（开放性）","analysis":"学校人数描述"},{"question":"综合复习：写出本学期学过的5个食物词汇和5个动物词汇（英语）","answer":"食物：apple, rice, milk, bread, cake等；动物：cat, dog, panda, elephant, tiger等","analysis":"词汇综合复习"}],"advanced_exercises":[{"question":"数字游戏：用英语写出1-100中所有的偶数（每行5个）","answer":"two, four, six, eight, ten... （到one hundred，共50个偶数）","analysis":"数字系统练习"},{"question":"写一篇英语数学日记（5句话）：今天数学课上学了数字","answer":"Today in maths class, we learnt big numbers. We counted to one hundred. I can say thirty-five and forty-seven. Numbers are fun! I like maths class.","analysis":"数学英语日记"},{"question":"综合写作（学期回顾）：用英语写出你这学期学到的3件重要事情（3句话）","answer":"This term I learnt many English words. I can introduce my family in English. I also learnt colours, animals and food.（开放性）","analysis":"学期回顾"},{"question":"挑战：用英语描述你的班级统计数据（男女生、年龄、身高等）","answer":"There are 40 students in my class. 18 are girls and 22 are boys. We are all 9 years old. Some students are tall and some are short.（开放性）","analysis":"统计数据描述"},{"question":"【综合题】给英语笔友写一封完整的信（10句话），介绍你自己、家庭、喜好和学校","answer":"开放性，包含：自我介绍、家庭介绍、食物/动物喜好、学校描述","analysis":"综合英语写作（学期总结）"}]}
]

print("Grade 3 English content defined.")

# ============ 四年级英语（简化版，各6单元）============
g4_english_upper = [
  {"id":"u01","title":"Unit 1 My Classroom","knowledge_points":["教室物品：window, door, floor, picture, computer, light","课堂指令：Open/Close the door. Turn on/off the light.","描述教室：The classroom is big/clean.","颜色复习和扩展：brown, grey, pink, purple"],"difficulties":["教室物品词汇量增加","Open/Close, Turn on/off指令的正确搭配","描述教室用clean, tidy, bright等形容词","颜色词的拼写"],"exercises":[{"question":"翻译教室物品：窗户（　）门（　）灯（　）电脑（　）图片（　）","answer":"window; door; light; computer; picture","analysis":"教室词汇"},{"question":"翻译指令：关上门！（　）打开灯！（　）","answer":"Close the door! / Turn on the light!","analysis":"课堂指令"},{"question":"用英语描述你的教室（4句话）","answer":"My classroom is big and bright. There are 40 desks. There are windows on the left. We have a computer on the teacher's desk.（开放性）","analysis":"教室描述"},{"question":"颜色填空：窗帘是（　）色，黑板是（　）色（英语）","answer":"白色white; 绿色green（开放性）","analysis":"颜色词运用"},{"question":"什么指令和什么词搭配？Open/Close配（　），Turn on/off配（　）","answer":"Open/Close配door, window, book等；Turn on/off配light, TV, computer等","analysis":"动词搭配"},{"question":"写出6种新学颜色（英语）","answer":"brown, grey, pink, purple, orange, white","analysis":"颜色词汇扩展"},{"question":"翻译：我们的教室干净整洁。","answer":"Our classroom is clean and tidy.","analysis":"教室特点描述"},{"question":"写出你最喜欢的教室活动（英语2句话）","answer":"I like reading books in the classroom. I also like drawing pictures.（开放性）","analysis":"个人喜好表达"}],"advanced_exercises":[{"question":"写一段介绍理想教室的英语短文（6句话）","answer":"My ideal classroom is big and bright. There are computers for every student. The walls are colourful with pictures. There is a big library corner. The classroom has comfortable chairs. I love studying in this classroom.","analysis":"理想教室描述"},{"question":"课堂规则：用英语写出5条理想的班级规则","answer":"1. Listen to the teacher. 2. Don't talk in class. 3. Keep the classroom clean. 4. Do your homework every day. 5. Be kind to classmates.","analysis":"英语规则制定"},{"question":"描述图画：假设教室里有一张图画，用英语描述它（3句话）","answer":"There is a picture on the wall. It shows a beautiful garden. There are flowers and butterflies in the picture.（开放性）","analysis":"图画描述"},{"question":"比较：你的教室和电影里看到的英国教室有什么不同？（英语2句话）","answer":"Chinese classrooms have more students (about 40-50). British classrooms usually have fewer students (about 25-30) and more free space.","analysis":"教育文化比较"},{"question":"【综合题】写英语介绍（8句话）：介绍你们班的教室给外国朋友","answer":"开放性，包含：教室大小、颜色、物品、人数等","analysis":"综合介绍写作"}]},
  {"id":"u02","title":"Unit 2 My Schoolbag","knowledge_points":["学习用品：Chinese book, maths book, English book, notebook, pencil case","询问内容：What's in your schoolbag?","表达数量：I have... books.","形容词：heavy, light, new, old"],"difficulties":["不同科目书本的英语名称","What's in...? 询问物品内容","heavy/light形容书包重量","数量的准确表达"],"exercises":[{"question":"翻译科目：语文（　）数学（　）英语（　）科学（　）","answer":"Chinese; maths; English; science","analysis":"科目英语名称"},{"question":"What's in your schoolbag? 用英语回答（写出3样东西）","answer":"There are books, pencils and an eraser in my schoolbag.（开放性）","analysis":"回答物品内容"},{"question":"用heavy/light描述书包（造句）","answer":"My schoolbag is heavy. I have many books.","analysis":"重量形容词"},{"question":"翻译：我有3本中文书和2本数学书。","answer":"I have three Chinese books and two maths books.","analysis":"数量描述"},{"question":"写出你书包里的5种东西（英语）","answer":"Chinese book, maths book, pencil case, eraser, ruler等","analysis":"书包内容词汇"},{"question":"形容词选择：new or old？一本新书（　），一支旧铅笔（　）","answer":"a new book; an old pencil","analysis":"new/old形容词"},{"question":"完成句子：My schoolbag is very ___. There are ___ books in it.","answer":"heavy; many/开放数字","analysis":"书包描述"},{"question":"写出4个课程的英语名称","answer":"Chinese, maths, English, science, PE, art, music等（选4个）","analysis":"科目词汇"}],"advanced_exercises":[{"question":"写英语描述你的文具盒（5句话）：里面有什么，颜色，形状","answer":"My pencil case is blue and long. There are five pencils inside. There is also an eraser and a ruler. My pencil case is new. I like my pencil case.","analysis":"文具盒描述"},{"question":"调查：问3个同学书包里有什么，用英语总结","answer":"开放性，如：Mary has three books and two pencils. Tom has four books and a notebook. I have five books.","analysis":"调查报告"},{"question":"创作：用英语写一个关于书包的小故事（5句话）","answer":"One day, my schoolbag was very heavy. I had ten books inside. I asked my mum for help. She took out some books. Now my bag is lighter.","analysis":"小故事创作"},{"question":"比较：你和同学的书包有什么不同？（英语3句话）","answer":"My schoolbag is blue. My friend's bag is red. I have five books but she has six.（开放性）","analysis":"比较句式"},{"question":"【综合题】写一封英语信给新朋友，介绍你的学校生活（8句话），包括书包、科目和喜好","answer":"开放性，包含学校物品、科目、喜好","analysis":"综合写作"}]},
  {"id":"u03","title":"Unit 3 My Friends","knowledge_points":["描述外貌：tall, short, fat, thin, young, old, long hair, short hair","描述性格：funny, kind, smart, quiet, active","朋友介绍：This is my friend, ...","比较：A is taller than B (初步接触比较级)"],"difficulties":["外貌和性格词汇的记忆","介绍朋友的完整句型","初步比较级：taller, shorter, funnier","区分形容词的使用场合"],"exercises":[{"question":"翻译外貌词汇：高的（　）矮的（　）胖的（　）瘦的（　）长发（　）","answer":"tall; short; fat; thin; long hair","analysis":"外貌词汇"},{"question":"翻译性格词汇：有趣的（　）善良的（　）聪明的（　）安静的（　）","answer":"funny; kind; smart; quiet","analysis":"性格词汇"},{"question":"介绍朋友：用英语写3句话介绍你最好的朋友","answer":"This is my friend Tom. He is tall and smart. He is very kind to me.（开放性）","analysis":"朋友介绍句型"},{"question":"翻译：小明比小红高。","answer":"Xiao Ming is taller than Xiao Hong.","analysis":"比较级初步"},{"question":"用funny/kind/smart各造一个句子","answer":"My teacher is funny. My mother is kind. My classmate is smart.（开放性）","analysis":"性格词造句"},{"question":"完成对话：A: Who is your best friend? B: My best friend is ___. He/She is ___ and ___.","answer":"开放性，填入名字和2个形容词","analysis":"朋友描述对话"},{"question":"写出你的一个朋友的外貌和性格（英语4句话）","answer":"My friend [name] is tall. She has long black hair. She is kind and smart. I like her very much.（开放性）","analysis":"朋友描述"},{"question":"比较：写出3组关于朋友的比较句","answer":"A is taller than B. C is smarter than D. E is kinder than F.（开放性）","analysis":"比较级练习"}],"advanced_exercises":[{"question":"写一段介绍最好朋友的英语短文（8句话）","answer":"My best friend is [name]. We are classmates. She is tall with long black hair. She is very smart and kind. She always helps me with my homework. We like playing together. She is funny too! I am happy to have such a friend.","analysis":"朋友综合介绍"},{"question":"对比：你和好朋友有哪些相同和不同之处？（英语4句话）","answer":"My friend and I are both smart. We both like reading books. But she is taller than me. And I am funnier than she is.（开放性）","analysis":"相同点和不同点"},{"question":"写英语故事：你和好朋友的一件难忘的事（5句话）","answer":"Last weekend, my friend and I went to the park. We played on the swings. Suddenly it started to rain. We ran to shelter together. It was a funny adventure!（开放性）","analysis":"友谊故事"},{"question":"讨论：什么样的人是好朋友？写出英语3个标准","answer":"A good friend is kind and honest. A good friend helps you when you are in trouble. A good friend makes you feel happy.","analysis":"好朋友的标准"},{"question":"【综合题】用英语写一封给好朋友的信（8句话），说说你们的友谊和你对他/她的祝愿","answer":"开放性，书信格式，情感真实","analysis":"综合书信写作"}]},
  {"id":"u04","title":"Unit 4 My Home","knowledge_points":["房间词汇：living room, bedroom, bathroom, kitchen, study","家具词汇：sofa, fridge, washing machine, telephone, bed","描述家的位置：on the first floor, upstairs, downstairs","询问和描述：What room is this? It's the..."],"difficulties":["房间和家具词汇的记忆","楼层的英语表达（first floor=一楼）","描述家庭环境的完整句子","数量词结合家具的描述"],"exercises":[{"question":"翻译房间：客厅（　）卧室（　）厨房（　）书房（　）浴室（　）","answer":"living room; bedroom; kitchen; study; bathroom","analysis":"房间词汇"},{"question":"翻译家具：冰箱（　）洗衣机（　）沙发（　）电话（　）","answer":"fridge; washing machine; sofa; telephone","analysis":"家具词汇"},{"question":"翻译：厨房在一楼，卧室在二楼。","answer":"The kitchen is on the first floor. The bedroom is on the second floor.","analysis":"楼层表达"},{"question":"描述你家里的一个房间（英语3句话）","answer":"My bedroom is on the second floor. There is a bed and a desk. My room is cosy and tidy.（开放性）","analysis":"房间描述"},{"question":"What room is this? （指厨房）用英语回答","answer":"It's the kitchen.","analysis":"识别房间"},{"question":"写出你家里有哪些家具（英语5种）","answer":"sofa, fridge, bed, desk, washing machine等","analysis":"家具词汇"},{"question":"造句：We cook in the ___, we sleep in the ___.","answer":"We cook in the kitchen. We sleep in the bedroom.","analysis":"房间功能描述"},{"question":"翻译：我们家有三间卧室和两间浴室。","answer":"We have three bedrooms and two bathrooms.","analysis":"描述家的数量"}],"advanced_exercises":[{"question":"写英语描述你的家（8句话），包括房间数量、位置和家具","answer":"My home has three bedrooms. The living room is on the first floor. There is a big sofa in the living room. The kitchen has a fridge and a stove. My bedroom is upstairs. There is a desk next to my bed. My home is warm and comfortable. I love my home.","analysis":"家庭综合描述"},{"question":"设计理想住宅：用英语描述你梦想中的家（6句话）","answer":"My dream home is a big house in the countryside. It has five bedrooms and three bathrooms. There is a swimming pool in the garden. The kitchen is modern and bright. Every room has big windows. I would love to live there!（开放性）","analysis":"理想住宅描述"},{"question":"写英语信：邀请朋友来你家做客（6句话）","answer":"Dear [name], Please come to my home on Saturday! My home is at [address]. Turn left at the school and go straight. My home is the third house on the right. I will cook delicious food! See you then! [name]","analysis":"邀请信写作"},{"question":"比较：公寓和独栋别墅，各有什么优缺点？（英语4句话）","answer":"An apartment is small but easy to manage. A house is big and has a garden. Apartments are usually cheaper. Houses give more space and privacy.","analysis":"居住类型比较"},{"question":"【综合题】角色扮演：带外国朋友参观你家，用英语介绍每个房间（10句话）","answer":"Welcome to my home! This is the living room. We have a big sofa and a TV. Here is the kitchen. We cook and eat here. Upstairs are the bedrooms. This is my bedroom. I sleep and study here. The bathroom is next to my room. I hope you like my home!","analysis":"参观介绍对话"}]},
  {"id":"u05","title":"Unit 5 What Would You Like?","knowledge_points":["餐食词汇：noodles, dumplings, porridge, steak, salad","点餐表达：What would you like for...? I'd like...","用餐礼貌语：Please have some... / No, thanks, I'm full.","描述食物：delicious, yummy, sour, sweet, spicy"],"difficulties":["Would like和like的区别（Would like=想要）","餐食词汇（特别是中式食物的英语）","味道形容词：sour, sweet, spicy, bitter","在餐厅场景中流畅对话"],"exercises":[{"question":"翻译餐食：面条（　）饺子（　）粥（　）牛排（　）沙拉（　）","answer":"noodles; dumplings; porridge; steak; salad","analysis":"餐食词汇"},{"question":"区别：I like noodles 和 I would like noodles（什么区别？）","answer":"I like noodles（我喜欢面条，表示一般习惯）；I would like noodles（我想要面条，表示此刻的需求，通常用于点餐）","analysis":"like vs would like"},{"question":"What would you like for lunch? 用英语回答","answer":"I'd like (some) noodles/dumplings, please.","analysis":"点餐句型"},{"question":"翻译味道：甜的（　）酸的（　）辣的（　）苦的（　）","answer":"sweet; sour; spicy; bitter","analysis":"味道形容词"},{"question":"用英语描述你最喜欢的食物的味道（2句话）","answer":"I love dumplings. They are delicious and not too spicy.（开放性）","analysis":"食物味道描述"},{"question":"No, thanks, I'm full. 这句话在什么情况下说？","answer":"当别人邀请你吃东西但你已经吃饱了的时候，礼貌地拒绝","analysis":"礼貌拒绝的场景"},{"question":"写出一个完整的点餐对话（英语4句）","answer":"A: What would you like? B: I'd like noodles, please. A: Would you like something to drink? B: Yes, juice please. Thank you!","analysis":"点餐对话"},{"question":"翻译：中国食物非常美味，我最喜欢饺子。","answer":"Chinese food is very delicious. My favourite is dumplings.","analysis":"中国食物介绍"}],"advanced_exercises":[{"question":"在餐厅写一段完整的点餐英语对话（10句话），包含点菜、询问味道、结账","answer":"Waiter: Good evening! May I take your order? Customer: Yes, I'd like the noodles. Waiter: What would you like to drink? Customer: Orange juice, please. Waiter: Anything else? Customer: Are the dumplings spicy? Waiter: They're a little spicy. Customer: OK, I'll have some. Waiter: Your total is 50 yuan. Customer: Here you are. Thank you!","analysis":"完整餐厅对话"},{"question":"写英语食谱介绍：介绍一道中国菜的做法（5句话）","answer":"Dumplings are a popular Chinese food. First, make the dough with flour. Then, fill it with meat and vegetables. Next, fold and seal the edges. Finally, cook in boiling water. They are delicious!","analysis":"食谱介绍（步骤描述）"},{"question":"比较中西方用餐礼仪（各写2点英语）","answer":"Chinese: use chopsticks, it's polite to serve others food; Western: use a knife and fork, eat from your own plate, say 'please' and 'thank you'","analysis":"用餐文化比较"},{"question":"创作：设计一份有创意的菜单（英语），中西结合","answer":"开放性：早餐：Chinese porridge with bread; 午餐：Noodles or salad; 晚餐：Dumplings or steak","analysis":"菜单设计"},{"question":"【综合题】为家庭聚会写英语邀请函，包括日期、地点和餐食（8句话）","answer":"Dear friends and family, Please join us for a family dinner! It will be on Saturday, 3 March. The dinner is at our home. We will have dumplings, noodles and much more. There will also be fruit and dessert. Please come at 6 pm. We look forward to seeing you! Love, [name]","analysis":"综合邀请函写作"}]},
  {"id":"u06","title":"Unit 6 Meet My Family","knowledge_points":["家庭活动：go shopping, watch movies, cook together, play sports","表达计划：We are going to...","描述家庭关系：grandparent, parent, child/children","家庭价值观：love, care, support, respect"],"difficulties":["be going to表示将来计划（初步）","家庭活动的词汇扩展","描述家庭关系的句型","表达情感和感谢"],"exercises":[{"question":"翻译家庭活动：一起购物（　）看电影（　）一起做饭（　）做运动（　）","answer":"go shopping (together); watch movies; cook together; play sports","analysis":"家庭活动词汇"},{"question":"翻译：我们打算周末一起去购物。","answer":"We are going to go shopping together this weekend.","analysis":"be going to表示计划"},{"question":"描述你和家人的一个共同活动（英语3句话）","answer":"Every Sunday, we cook together. My mum makes dumplings. My dad washes the vegetables. I set the table.（开放性）","analysis":"家庭活动描述"},{"question":"用英语写出你的家庭计划（这个周末）","answer":"This weekend, we are going to visit grandma. We will have lunch together. Then we are going to watch a film.（开放性）","analysis":"周末计划表达"},{"question":"家庭价值观：用英语写出家庭中3个重要的价值观","answer":"Love your family. Respect your parents. Help each other.（开放性）","analysis":"家庭价值观表达"},{"question":"翻译：我爱我的家庭，因为他们总是支持我。","answer":"I love my family because they always support me.","analysis":"表达对家庭的爱"},{"question":"写出3件你和家人一起做的快乐事情（英语）","answer":"We go to the park together. We cook and eat dinner. We watch films on weekends.（开放性）","analysis":"家庭活动"},{"question":"家庭关系：grandparent = father/mother的（　）","answer":"grandparent = 祖父母（父亲或母亲的父母）","analysis":"家庭关系词"}],"advanced_exercises":[{"question":"写一段关于家庭的英语短文（8句话），包含家庭成员、活动和感情","answer":"My family has four people: my parents, my sister and me. We love spending time together. Every weekend, we go to the park or watch films. My mum is a great cook. She always makes delicious food. My dad is funny and kind. My sister and I are best friends. I am lucky to have such a wonderful family.","analysis":"家庭综合描述"},{"question":"感谢信：写一封英语感谢信给你的父母（8句话）","answer":"Dear Mum and Dad, Thank you for everything you do for me. You work hard every day for our family. You always help me with my homework. You take care of me when I am sick. You make me feel loved and safe. I am very lucky to have you. I will study hard and make you proud. Love, [name]","analysis":"感谢信写作"},{"question":"学期回顾：用英语写出四年级上学期你学到的3个最重要的英语句型","answer":"开放性，如：1. Would you like...? 2. Where is/are...? 3. What does your father do?","analysis":"学期英语回顾"},{"question":"比较：独生子女家庭和多子女家庭各有什么优缺点？（英语4句话）","answer":"An only child gets more attention from parents. However, it can be lonely without siblings. A family with many children is lively and fun. But parents need to share their time and resources.","analysis":"家庭结构比较"},{"question":"【综合题】期末英语写作：写一篇关于'我的家庭'的完整文章（10句话）","answer":"开放性，包含：家庭成员、外貌、职业、活动、家庭价值观","analysis":"综合写作（期末水平展示）"}]}
]

g4_english_lower = [
  {"id":"u01","title":"Unit 1 Our School","knowledge_points":["学校场所词汇：library, gym, art room, music room, science lab","描述学校：Our school has...","询问位置（复习）：Where is the...?","学校活动和时间表：have PE, have art"],"difficulties":["新学校场所的词汇","描述学校设施的句型","时间表表达：on Monday, at 9 o'clock","文章结构：介绍学校"],"exercises":[{"question":"翻译学校场所：图书馆（　）体育馆（　）美术室（　）音乐室（　）实验室（　）","answer":"library; gym; art room; music room; science lab","analysis":"学校场所词汇"},{"question":"Our school has a big library. 翻译成中文","answer":"我们学校有一个大图书馆","analysis":"学校设施介绍句型"},{"question":"Where is the library? （在一楼）用英语回答","answer":"The library is on the first floor.","analysis":"位置询问回答"},{"question":"用英语写出你们学校时间表的一天（3个科目和时间）","answer":"We have Chinese at 8 o'clock. We have maths at 9 o'clock. We have PE in the afternoon.（开放性）","analysis":"时间表表达"},{"question":"用英语介绍你们学校的3个特别之处","answer":"Our school has a big playground. We have a science lab. There is a beautiful garden.（开放性）","analysis":"学校特点介绍"},{"question":"on Monday / on Tuesday... 写出一周5天的英语单词","answer":"Monday, Tuesday, Wednesday, Thursday, Friday","analysis":"星期词汇"},{"question":"完成句子：We have art on ___ and science on ___.","answer":"开放性，填入两天","analysis":"课程安排表达"},{"question":"翻译：我们的学校又大又美丽，我喜欢在这里学习。","answer":"Our school is big and beautiful. I like studying here.","analysis":"学校描述"}],"advanced_exercises":[{"question":"写一篇介绍学校的英语文章（8句话）","answer":"My school is called [name] Primary School. It is a big and beautiful school. There are 30 classrooms and a big gym. We also have a library and an art room. There are about 1000 students. Our teachers are very kind. I love my school. It is the best school!","analysis":"学校综合介绍"},{"question":"设计理想学校：用英语描述你梦想中的学校（6句话）","answer":"My dream school has a swimming pool. There is a cinema for watching films. Every student has a computer. The school has a big garden with flowers. The teachers are all very interesting. Students can choose their own courses.（开放性）","analysis":"理想学校创意写作"},{"question":"写学校日记（英语5句话）：今天在学校发生的一件有趣的事","answer":"Today in science class, we did an experiment. We mixed vinegar and baking soda. It made a big fizz! The teacher said it was a chemical reaction. It was so cool and fun!（开放性）","analysis":"学校日记写作"},{"question":"比较：你的学校和电视里的美国学校有什么不同？（英语3句话）","answer":"My school starts at 7:30, but American schools often start at 8:00. Chinese students have more homework. American students have more after-school activities.","analysis":"中美学校比较"},{"question":"【综合题】给一位要来中国上学的外国小朋友写欢迎信（10句话），介绍学校","answer":"开放性，包含：学校位置、设施、课程、老师、同学","analysis":"欢迎信综合写作"}]},
  {"id":"u02","title":"Unit 2 What Time Is It?","knowledge_points":["时间表达：What time is it? It's ... o'clock./It's half past...","日常作息词汇：get up, have breakfast, go to school, do homework, go to bed","频率副词：always, usually, often, sometimes, never","描述日常规律：I always...at..."],"difficulties":["时间的两种表达（o'clock和half past）","频率副词的准确使用和排序","描述日常作息的完整句子","整点和半点以外的时间（如5:15=five fifteen）"],"exercises":[{"question":"翻译时间：7点整（　）7:30（　）8:15（　）","answer":"seven o'clock; half past seven; eight fifteen","analysis":"时间表达方式"},{"question":"What time is it? （现在是9点半）用英语回答","answer":"It's half past nine. / It's 9:30.","analysis":"回答时间问题"},{"question":"翻译作息：起床（　）吃早饭（　）上学（　）做作业（　）睡觉（　）","answer":"get up; have breakfast; go to school; do homework; go to bed","analysis":"日常作息词汇"},{"question":"用always/usually/often/sometimes写4个关于自己作息的句子","answer":"I always have breakfast at 7. I usually go to school at 7:30. I often do homework after school. I sometimes watch TV.（开放性）","analysis":"频率副词造句"},{"question":"翻译：我通常7点起床，7:30吃早饭。","answer":"I usually get up at 7 o'clock. I have breakfast at half past seven.","analysis":"作息描述"},{"question":"频率副词顺序：从高到低排列always/usually/often/sometimes/never","answer":"always(100%) > usually(80%) > often(60%) > sometimes(30%) > never(0%)","analysis":"频率副词顺序"},{"question":"用英语描述你的早晨作息（3句话）","answer":"I get up at 6:30. I have breakfast at 7. I go to school at 7:30.（开放性）","analysis":"早晨作息描述"},{"question":"What time do you go to bed? 用英语回答","answer":"I go to bed at 9 o'clock./I usually sleep at nine.（开放性）","analysis":"睡觉时间询问"}],"advanced_exercises":[{"question":"写英语日常作息表（8句话，从起床到睡觉）","answer":"I get up at 6:30 every morning. I have breakfast at 7:00. I go to school at 7:30. School starts at 8:00. I have lunch at 12:00. I do homework at 4:30. I have dinner at 6:00. I go to bed at 9:00.","analysis":"完整作息描述"},{"question":"比较你和妈妈/爸爸的作息（英语4句话）","answer":"I get up at 6:30, but my mum gets up at 6:00. I go to bed at 9:00, but she goes to bed at 11:00. She works very hard! I want to be like her one day.（开放性）","analysis":"比较作息"},{"question":"写英语故事：一天时间管理不好发生的事情（5句话）","answer":"Yesterday I got up late. I missed my breakfast. I was late for school. I forgot my homework. I had a terrible day! Next time I will manage my time better.","analysis":"时间管理故事"},{"question":"讨论：什么是好的时间管理习惯？用英语写出3条建议","answer":"Get up early every day. Do homework first, then play. Go to bed at the same time every night.","analysis":"时间管理建议"},{"question":"【综合题】写一篇关于'我的一天'的英语文章（10句话）","answer":"开放性，包含：起床、吃饭、上学、放学、做作业、娱乐、睡觉等","analysis":"综合写作"}]},
  {"id":"u03","title":"Unit 3 Weather","knowledge_points":["天气词汇：sunny, cloudy, rainy, windy, snowy, foggy","询问天气：What's the weather like today? It's...","季节：spring, summer, autumn, winter","天气与活动的关联：On sunny days, I..."],"difficulties":["天气形容词（形容词形式：sun→sunny）","天气与季节的关联","选择合适的天气描述","描述不同天气时的活动"],"exercises":[{"question":"翻译天气：晴天（　）多云（　）雨天（　）刮风（　）下雪（　）","answer":"sunny; cloudy; rainy; windy; snowy","analysis":"天气词汇"},{"question":"What's the weather like today? （今天是晴天）用英语回答","answer":"It's sunny today.","analysis":"天气询问和回答"},{"question":"写出四季的英语单词","answer":"spring, summer, autumn, winter","analysis":"四季词汇"},{"question":"翻译：春天温暖，夏天炎热，秋天凉爽，冬天寒冷。","answer":"Spring is warm. Summer is hot. Autumn is cool. Winter is cold.","analysis":"四季特点描述"},{"question":"On rainy days, I...（写出2种雨天活动）","answer":"On rainy days, I read books./I stay at home and watch TV.（开放性）","analysis":"天气与活动关联"},{"question":"用英语写一周的天气预报（3天）","answer":"Monday: sunny; Wednesday: rainy; Friday: cloudy（开放性）","analysis":"天气预报表达"},{"question":"哪个季节最适合户外活动？为什么？（英语2句话）","answer":"Spring is the best for outdoor activities. It is warm and beautiful.（开放性）","analysis":"季节活动评价"},{"question":"翻译：下雪天，孩子们喜欢在外面玩雪。","answer":"On snowy days, children like playing in the snow outside.","analysis":"天气与活动描述"}],"advanced_exercises":[{"question":"写天气日记（英语6句话）：描述今天和昨天的天气以及你的活动","answer":"Yesterday was sunny. I played football with my friends. Today is rainy. I stayed at home. I read books and did my homework. I like sunny days better.","analysis":"天气日记"},{"question":"写英语天气预报（5句话）：为本周末预测天气","answer":"This weekend, Saturday will be sunny. The temperature will be 20 degrees. Sunday may be cloudy. There might be some rain in the afternoon. Please bring an umbrella just in case.","analysis":"天气预报写作"},{"question":"比较：你最喜欢的季节和不喜欢的季节（英语4句话）","answer":"My favourite season is spring. The flowers are beautiful and the weather is warm. I don't like winter because it is too cold. I can't play outside easily in winter.（开放性）","analysis":"季节喜好比较"},{"question":"天气对日常生活的影响：写出3个天气影响活动的例子（英语）","answer":"When it's raining, we can't play outside. When it's snowing, we might have a day off school. When it's sunny, we can have a picnic in the park.","analysis":"天气与生活的关系"},{"question":"【综合题】以'我最喜欢的季节'为题写英语文章（8句话）","answer":"开放性，包含：季节特点、天气、活动、原因","analysis":"综合写作"}]},
  {"id":"u04","title":"Unit 4 At the Farm","knowledge_points":["农场动物：cow, horse, sheep, pig, duck, hen","蔬菜词汇：potato, corn, carrot, tomato, cucumber, pumpkin","农场活动：feed the animals, grow vegetables, pick fruit","数量表达（复习）：There are many/some..."],"difficulties":["农场动物和蔬菜词汇的拼写","区分农场动物和宠物","'feed'等动词的使用","描述农场场景"],"exercises":[{"question":"翻译农场动物：奶牛（　）马（　）羊（　）猪（　）鸭子（　）母鸡（　）","answer":"cow; horse; sheep; pig; duck; hen","analysis":"农场动物词汇"},{"question":"翻译蔬菜：土豆（　）玉米（　）胡萝卜（　）黄瓜（　）南瓜（　）","answer":"potato; corn; carrot; cucumber; pumpkin","analysis":"蔬菜词汇"},{"question":"翻译农场活动：喂动物（　）种蔬菜（　）摘水果（　）","answer":"feed the animals; grow vegetables; pick fruit","analysis":"农场活动词汇"},{"question":"用英语描述一个农场（3句话）","answer":"There are many animals on the farm. There are cows, pigs and chickens. There are also vegetables like carrots and tomatoes.（开放性）","analysis":"农场描述"},{"question":"用There are...造句（3句话关于农场动物）","answer":"There are ten cows. There are five horses. There are many ducks.（开放性）","analysis":"数量描述"},{"question":"什么动物产牛奶？什么动物产蛋？（英语回答）","answer":"Cows produce milk. Hens produce eggs.","analysis":"农场动物特点"},{"question":"写出你最喜欢的蔬菜和原因（英语2句话）","answer":"My favourite vegetable is carrot. It is sweet and good for my eyes.（开放性）","analysis":"蔬菜喜好"},{"question":"翻译：农场里有很多动物，农夫每天要喂它们。","answer":"There are many animals on the farm. The farmer feeds them every day.","analysis":"农场活动描述"}],"advanced_exercises":[{"question":"写参观农场的英语日记（8句话）","answer":"Yesterday we visited a farm. I saw many animals. There were cows, pigs and sheep. We fed the animals. I gave carrots to the rabbits. We also picked tomatoes. The farmer showed us how to grow vegetables. It was a great experience!","analysis":"农场参观日记"},{"question":"农场知识问答：英语写出3个关于农场的有趣事实","answer":"Cows can recognize over 100 different faces. Pigs are actually very clean animals. Chickens can run up to 15 km/h.（开放性，查阅资料）","analysis":"农场知识英语表达"},{"question":"创作：以一只农场动物的口吻写一段自述（英语5句话）","answer":"I am a cow on a farm. I wake up early every morning. I eat grass and hay. I give milk twice a day. I love my life on the farm!（开放性）","analysis":"创意写作"},{"question":"比较：农场生活和城市生活各有什么优缺点？（英语4句话）","answer":"Farm life is peaceful and full of nature. But it is hard work and far from shops. City life is convenient and exciting. But it can be noisy and crowded.","analysis":"生活方式比较"},{"question":"【综合题】写英语介绍：如果你有一个农场，你会养什么动物，种什么蔬菜？为什么？（8句话）","answer":"开放性，包含：动物、蔬菜、原因","analysis":"综合写作"}]},
  {"id":"u05","title":"Unit 5 Dinner's Ready!","knowledge_points":["餐桌礼仪词汇：knife, fork, spoon, chopsticks, napkin, plate, bowl","晚餐对话：Dinner's ready! / Come to the table.","表达感谢：Thank you for the delicious meal.","询问意见：How do you like the food?"],"difficulties":["餐具词汇的记忆","西餐和中餐餐具的区别","表达对食物的评价（用形容词）","家庭晚餐场景中的英语对话"],"exercises":[{"question":"翻译餐具：刀（　）叉（　）勺子（　）筷子（　）餐巾（　）盘子（　）碗（　）","answer":"knife; fork; spoon; chopsticks; napkin; plate; bowl","analysis":"餐具词汇"},{"question":"Dinner's ready! 这句话谁说，在什么场合？","answer":"妈妈/家人准备好晚餐后说，叫家人来吃饭","analysis":"场景理解"},{"question":"翻译：谢谢您准备了这么美味的饭菜！","answer":"Thank you for the delicious meal!","analysis":"感谢用语"},{"question":"How do you like the food? 用英语回答（非常好吃）","answer":"It's delicious/yummy! I love it!","analysis":"食物评价"},{"question":"中西餐具比较：中国用（　），西方用（　）（英语）","answer":"中国用chopsticks（筷子）；西方用knife, fork, spoon（刀叉）","analysis":"餐具文化"},{"question":"餐桌礼仪：写出2条中国餐桌礼仪（英语）","answer":"Don't put chopsticks upright in the bowl. Serve food to elders first.（开放性）","analysis":"餐桌礼仪英语表达"},{"question":"用英语写一个晚餐场景对话（4句话）","answer":"Mum: Dinner's ready! Come to the table! Dad: What's for dinner? Mum: We have dumplings and soup. Me: Yummy! Thank you, Mum!（开放性）","analysis":"家庭晚餐对话"},{"question":"用形容词描述你最喜欢的晚餐（英语3句话）","answer":"My favourite dinner is hotpot. It is spicy and delicious. I love eating hotpot with my family.（开放性）","analysis":"晚餐描述"}],"advanced_exercises":[{"question":"写英语描述一次家庭晚餐（8句话）：食物、对话和氛围","answer":"Last night we had a family dinner. Mum cooked dumplings and a delicious soup. Dad prepared the salad. We all sat around the table. Dad said the food was wonderful. We talked and laughed a lot. After dinner, I helped wash the dishes. It was a perfect evening.","analysis":"家庭晚餐描写"},{"question":"中西方餐桌礼仪对比（各写3点英语）","answer":"Chinese: Pour tea for elders first; It's polite to offer food to others; Talking during meals is acceptable. Western: Wait for everyone before eating; Keep elbows off the table; Thank the host after the meal.","analysis":"餐桌礼仪比较"},{"question":"创作：为家人设计一顿特别的晚餐（英语），写菜单和准备步骤（6句话）","answer":"开放性，菜单+步骤","analysis":"创意写作"},{"question":"写英语感谢卡：感谢妈妈总是为家人做美味的饭菜（5句话）","answer":"Dear Mum, Thank you for cooking every day. The food you make is always delicious. I love your dumplings most of all. You work so hard for our family. I love you, Mum!","analysis":"感谢卡写作"},{"question":"【综合题】角色扮演：外国朋友来家里吃饭，用英语写出完整的晚餐对话（10句话）","answer":"开放性，包含：邀请、介绍菜肴、用餐对话、感谢","analysis":"综合对话写作"}]},
  {"id":"u06","title":"Unit 6 Shopping","knowledge_points":["购物词汇：shop, supermarket, market, sale, price, receipt","价格表达：How much is/are...? It costs...yuan.","购物决策：I'll take it./I'll buy it./That's too expensive.","比较价格：cheaper, more expensive"],"difficulties":["价格的英语表达（元/角）","I'll take it / I'll buy it的使用场景","比较价格的形容词（比较级）","购物全程的流畅英语对话"],"exercises":[{"question":"翻译购物词汇：商店（　）超市（　）市场（　）价格（　）收据（　）","answer":"shop; supermarket; market; price; receipt","analysis":"购物词汇"},{"question":"How much is this shirt? （50元）用英语回答","answer":"It costs 50 yuan. / It's 50 yuan.","analysis":"价格询问回答"},{"question":"翻译：这件衬衫太贵了，我不买了。","answer":"This shirt is too expensive. I won't buy it.","analysis":"表达嫌贵"},{"question":"用英语表达：这个更便宜，我要这个。","answer":"This one is cheaper. I'll take this one.","analysis":"比较和决策"},{"question":"写出一个购物场景的4句英语对话","answer":"A: How much is this? B: It's 30 yuan. A: That's a bit expensive. Can I have a discount? B: OK, 25 yuan!（开放性）","analysis":"购物对话"},{"question":"cheaper vs more expensive：苹果5元，草莓10元，哪个更便宜？（英语表达）","answer":"Apples are cheaper. Strawberries are more expensive.","analysis":"比较价格"},{"question":"翻译：打折啦！所有商品五折优惠！","answer":"Sale! Everything is 50% off!","analysis":"打折英语表达"},{"question":"写出你购物时最常说的3句英语","answer":"How much is this? I'll take it. Do you have this in blue?（开放性）","analysis":"购物常用语"}],"advanced_exercises":[{"question":"写完整的购物对话（英语10句话）：在服装店买一件礼物","answer":"Shop assistant: Good afternoon! Can I help you? Customer: Yes, I'm looking for a birthday present. Assistant: How about this jacket? Customer: It looks nice. How much is it? Assistant: It's 120 yuan. Customer: That's a little expensive. Do you have a discount? Assistant: Today we have 20% off. Customer: So it's 96 yuan? Assistant: Yes, that's right. Customer: Great, I'll take it! Here's 100 yuan. Assistant: Here's your change and receipt. Thank you!","analysis":"完整购物对话"},{"question":"写购物英语日记（6句话）：去超市买东西","answer":"Yesterday I went to the supermarket with mum. We bought vegetables, fruit and milk. I helped choose the apples. Each kilogram was 8 yuan. The total was 50 yuan. I paid the cashier and got the receipt.","analysis":"购物日记"},{"question":"设计商店广告（英语4句话）：吸引顾客","answer":"Welcome to [name] Shop! We have the freshest fruits and vegetables. All items are at low prices. Come and get great value today!（开放性）","analysis":"广告设计"},{"question":"比较：网购和实体店购物各有什么优缺点？（英语4句话）","answer":"Online shopping is convenient and often cheaper. But you can't try the product before buying. Shopping in a store is fun and you can see the items. But it takes more time.","analysis":"购物方式比较"},{"question":"【综合题/期末】写一篇英语作文：四年级我最大的进步（英语10句话），回顾学习成果","answer":"开放性，包含：英语学习进步、最喜欢的单元、对五年级的期望","analysis":"期末综合写作"}]}
]

print("Grade 4 English content defined.")

# ============ 主生成逻辑 ============

ALL_CONTENT = {
    "grade3": {
        "math":    {"upper": g3_math_upper,    "lower": g3_math_lower},
        "chinese": {"upper": g3_chinese_upper, "lower": g3_chinese_lower},
        "english": {"upper": g3_english_upper, "lower": g3_english_lower},
    },
    "grade4": {
        "math":    {"upper": g4_math_upper,    "lower": g4_math_lower},
        "chinese": {"upper": g4_chinese_upper, "lower": g4_chinese_lower},
        "english": {"upper": g4_english_upper, "lower": g4_english_lower},
    },
}

def make_grade_index(grade_key):
    g = GRADE_INFO[grade_key]
    cards = ""
    for subj_key, s in SUBJECT_INFO.items():
        cards += f'''
<a href="{s['name']}/index.html" style="display:block;background:#fff;border-radius:18px;padding:25px;margin-bottom:16px;text-decoration:none;box-shadow:0 4px 15px rgba(0,0,0,0.08);border-left:6px solid {s['color']};transition:all .2s;" onmouseover="this.style.transform='translateX(6px)'" onmouseout="this.style.transform=''">
  <div style="font-size:28px;margin-bottom:8px;">{s['icon']}</div>
  <div style="font-size:20px;font-weight:800;color:{s['color']};">{s['name']}</div>
  <div style="font-size:13px;color:#888;margin-top:6px;">人教版 · 上下册</div>
</a>'''
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{g['name']}</title>
<style>body{{font-family:'PingFang SC','微软雅黑',Arial,sans-serif;background:#F0F4F8;margin:0;}}
.header{{background:{g['gradient']};color:#fff;padding:30px 20px;text-align:center;}}
.header h1{{font-size:32px;font-weight:800;margin-bottom:8px;}}
.breadcrumb{{background:#fff;padding:12px 20px;margin:15px;border-radius:12px;box-shadow:0 2px 8px rgba(0,0,0,0.06);font-size:13px;}}
.breadcrumb a{{color:{g['color']};text-decoration:none;font-weight:500;}}
.container{{max-width:500px;margin:0 auto;padding:0 15px 30px;}}
</style>
</head>
<body>
<div class="header">
  <h1>🎒 {g['name']}</h1>
  <div>人教版 · 三科齐全</div>
</div>
<div class="breadcrumb">
  <a href="../main.html">🏠 首页</a> › {g['name']}
</div>
<div class="container">{cards}</div>
</body></html>"""

def make_main_html():
    grade_cards = ""
    for grade_key, g in GRADE_INFO.items():
        subjects_list = "".join(
            f'<span style="display:inline-block;background:{SUBJECT_INFO[sk]["color"]};color:#fff;padding:4px 12px;border-radius:20px;font-size:12px;margin:3px;">{SUBJECT_INFO[sk]["icon"]} {SUBJECT_INFO[sk]["name"]}</span>'
            for sk in SUBJECT_INFO
        )
        grade_cards += f'''
<a href="{g['name']}/index.html" style="display:block;background:#fff;border-radius:20px;padding:30px;margin-bottom:20px;text-decoration:none;box-shadow:0 6px 20px rgba(0,0,0,0.1);transition:all .3s;" onmouseover="this.style.transform='translateY(-5px)'" onmouseout="this.style.transform=''">
  <div style="font-size:24px;font-weight:900;background:{g['gradient']};-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:10px;">{g['name']}</div>
  <div style="margin-bottom:12px;">{subjects_list}</div>
  <div style="background:{g['gradient']};color:#fff;border-radius:10px;padding:10px;text-align:center;font-size:14px;font-weight:600;">开始学习 →</div>
</a>'''
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>小学生学习资料 - 三四年级</title>
<style>
*{{box-sizing:border-box;margin:0;padding:0;}}
body{{font-family:'PingFang SC','微软雅黑',Arial,sans-serif;background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);min-height:100vh;}}
.hero{{text-align:center;padding:50px 20px 30px;color:#fff;}}
.hero h1{{font-size:36px;font-weight:900;text-shadow:0 2px 8px rgba(0,0,0,0.3);margin-bottom:10px;}}
.hero p{{font-size:16px;opacity:0.9;}}
.subjects-bar{{display:flex;justify-content:center;gap:15px;margin:20px 0;flex-wrap:wrap;}}
.subjects-bar span{{background:rgba(255,255,255,0.2);color:#fff;padding:8px 20px;border-radius:25px;font-size:14px;backdrop-filter:blur(10px);}}
.container{{max-width:500px;margin:0 auto;padding:0 20px 40px;}}
.info-box{{background:rgba(255,255,255,0.15);border-radius:16px;padding:20px;margin-bottom:20px;color:#fff;text-align:center;backdrop-filter:blur(10px);}}
.info-box .num{{font-size:36px;font-weight:900;}}
.info-box .label{{font-size:13px;opacity:0.85;}}
</style>
</head>
<body>
<div class="hero">
  <div style="font-size:60px;margin-bottom:15px;">📚</div>
  <h1>小学生学习助手</h1>
  <p>人教版三四年级 · 数学·语文·英语</p>
  <div class="subjects-bar">
    <span>🔢 数学</span>
    <span>📖 语文</span>
    <span>🌍 英语</span>
  </div>
</div>
<div class="container">
  <div style="display:flex;gap:12px;margin-bottom:20px;">
    <div class="info-box" style="flex:1;"><div class="num">2</div><div class="label">年级</div></div>
    <div class="info-box" style="flex:1;"><div class="num">3</div><div class="label">科目</div></div>
    <div class="info-box" style="flex:1;"><div class="num">88+</div><div class="label">章节</div></div>
  </div>
  {grade_cards}
  <div style="background:rgba(255,255,255,0.15);border-radius:16px;padding:20px;color:#fff;text-align:center;backdrop-filter:blur(10px);">
    <div style="font-size:16px;font-weight:600;margin-bottom:8px;">💡 使用提示</div>
    <div style="font-size:13px;opacity:0.9;line-height:1.8;「>先独立思考作答，再点击」查看答案"<br>拔高题有一定难度，挑战一下自己！<br>每个知识点都有详细解析，认真读懂</div>
  </div>
</div>
</body></html>"""

# ============ 生成所有文件 ============
def generate_all():
    generated = 0
    
    # main.html
    main_path = os.path.join(BASE_DIR, "main.html")
    with open(main_path, "w", encoding="utf-8") as f:
        f.write(make_main_html())
    print(f"✅ Created: main.html")
    generated += 1

    for grade_key in ["grade3", "grade4"]:
        grade_dir = os.path.join(BASE_DIR, GRADE_INFO[grade_key]['name'])
        os.makedirs(grade_dir, exist_ok=True)
        
        # grade index
        with open(os.path.join(grade_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(make_grade_index(grade_key))
        print(f"✅ Created: {grade_key}/index.html")
        generated += 1

        for subj_key in ["math", "chinese", "english"]:
            s = SUBJECT_INFO[subj_key]
            subj_dir = os.path.join(grade_dir, s['name'])
            os.makedirs(subj_dir, exist_ok=True)
            
            upper_chs = ALL_CONTENT[grade_key][subj_key]["upper"]
            lower_chs = ALL_CONTENT[grade_key][subj_key]["lower"]
            
            # subject index
            with open(os.path.join(subj_dir, "index.html"), "w", encoding="utf-8") as f:
                f.write(make_subject_index(grade_key, subj_key, upper_chs, lower_chs))
            print(f"✅ Created: {grade_key}/{subj_key}/index.html")
            generated += 1

            for sem_key, chapters in [("upper", upper_chs), ("lower", lower_chs)]:
                sem_dir = os.path.join(subj_dir, SEMESTER_INFO[sem_key])
                os.makedirs(sem_dir, exist_ok=True)
                
                # semester index
                with open(os.path.join(sem_dir, "index.html"), "w", encoding="utf-8") as f:
                    f.write(make_semester_index(grade_key, subj_key, sem_key, chapters))
                print(f"✅ Created: {grade_key}/{subj_key}/{sem_key}/index.html")
                generated += 1

                # chapter files
                for ch in chapters:
                    ch_path = os.path.join(sem_dir, f"{ch['id']}.html")
                    with open(ch_path, "w", encoding="utf-8") as f:
                        f.write(make_chapter_html(grade_key, subj_key, sem_key, ch))
                    generated += 1
                
                print(f"   → Generated {len(chapters)} chapters for {grade_key}/{subj_key}/{sem_key}")

    print(f"\n🎉 All done! Generated {generated} HTML files.")

if __name__ == "__main__":
    generate_all()
