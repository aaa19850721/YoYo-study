# -*- coding: utf-8 -*-
"""生成 grammar.html：蓝色主题语法卡片页（仿 words.html 结构）"""
import json,collections,re

BASE=r'D:\YoYo\YoYo-study\YoYo-study'
topics=json.load(open(BASE+r'\_grammar\topics.json',encoding='utf-8'))

# 合并例句
exs={}
for i in range(1,4):
    try:
        d=json.load(open(BASE+r'\_grammar\out\out_%02d.json'%i,encoding='utf-8'))
        exs.update(d)
    except FileNotFoundError:
        print('缺 out_%02d'%i)
missing=[t['name'] for t in topics if t['name'] not in exs]
if missing:
    print('缺例句的卡片:',missing); raise SystemExit(1)

# 组内排序（按 count 降序）→ 卡片按组别聚合排列
groups=collections.OrderedDict()
for t in sorted(topics,key=lambda x:-x['count']):
    groups.setdefault(t['group'],[]).append(t)
cards=[]
for g,ts in groups.items():
    cards.extend(ts)

def esc(s): return s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;').replace('"','&quot;')
def es(s): return json.dumps(s,ensure_ascii=False)

def summary(t):
    ds=[d for d in t['descs'] if d]
    return '；'.join(ds[:2]) if ds else ''

WORDS=[{
  'name':t['name'],'group':t['group'],'count':t['count'],
  'summary':summary(t),'exs':exs[t['name']],
} for t in cards]

html=f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>红火箭分级阅读语法表 · 语法卡片</title>
<style>
  :root{{
    --bg:#e7eefb;
    --ink:#2f3555; --sub:#7d8698;
    --accent:#3f6bd9; --accent2:#2f52ab;
    --card-face:#ffffff;
    --shadow:0 2px 6px rgba(47,82,171,.10),0 8px 24px rgba(47,82,171,.12);
    --shadow-lift:0 4px 10px rgba(47,82,171,.14),0 18px 40px rgba(47,82,171,.20);
  }}
  *{{box-sizing:border-box;margin:0;padding:0}}
  body{{
    font-family:"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif;
    color:var(--ink);
    background:var(--bg);
    min-height:100vh;
    padding:32px 24px 60px;
  }}
  .wrap{{max-width:1080px;margin:0 auto}}

  /* ===== 顶部固定栏 ===== */
  .topbar{{
    position:sticky;top:0;z-index:50;
    background:var(--bg);
    padding:8px 0 14px;
    margin-bottom:10px;
    box-shadow:0 2px 8px rgba(47,82,171,.08);
  }}
  header{{text-align:center;margin-bottom:26px}}
  header h1{{margin-top:6px}}
  h1{{font-size:34px;font-weight:800;letter-spacing:1px;color:var(--accent2)}}
  .subtitle{{margin-top:6px;color:var(--sub);font-size:13px;letter-spacing:2px}}

  /* ===== 搜索框 ===== */
  .searchbar{{display:flex;justify-content:center;margin-bottom:8px}}
  .searchbox{{position:relative;width:420px;max-width:100%}}
  .searchbox input{{
    width:100%;height:46px;border:none;outline:none;
    border-radius:23px;padding:0 46px 0 46px;font-size:15px;color:var(--ink);
    background:var(--card-face);
    box-shadow:var(--shadow), inset 0 -2px 0 rgba(43,58,85,.06);
    transition:box-shadow .2s, transform .2s;
  }}
  .searchbox input:focus{{
    box-shadow:var(--shadow-lift), inset 0 -2px 0 rgba(63,107,217,.25);
    transform:translateY(-1px);
  }}
  .searchbox .icon{{position:absolute;left:16px;top:50%;transform:translateY(-50%);font-size:17px;color:var(--sub);pointer-events:none}}
  .searchbox .clear{{
    position:absolute;right:14px;top:50%;transform:translateY(-50%);
    width:22px;height:22px;border-radius:50%;border:none;cursor:pointer;
    background:#dce3f0;color:var(--sub);font-size:12px;line-height:1;display:none;
  }}
  .searchbox .clear:hover{{background:#c9d2e4}}
  .count{{text-align:center;color:var(--sub);font-size:12.5px;margin:8px 0 6px}}

  /* ===== 瀑布流 ===== */
  .grid{{display:flex;gap:22px;align-items:flex-start}}
  .col{{flex:1;min-width:0;display:flex;flex-direction:column}}
  @media (max-width:980px){{.grid{{gap:16px}}}}
  @media (max-width:640px){{.grid{{gap:14px}}}}
  .scene{{margin-bottom:22px;perspective:1400px;height:400px}}

  .card{{
    position:relative;width:100%;height:100%;
    transform-style:preserve-3d;
    transition:transform .65s cubic-bezier(.2,.75,.3,1.1);
    cursor:pointer;
  }}
  .card.flipped{{transform:rotateY(180deg)}}
  .face{{
    position:absolute;inset:0;border-radius:18px;
    backface-visibility:hidden;-webkit-backface-visibility:hidden;
    box-shadow:var(--shadow);
    overflow:hidden;
    background:rgba(63,107,217,.12);
    backdrop-filter:blur(20px) saturate(1.3);
    -webkit-backdrop-filter:blur(20px) saturate(1.3);
    border:1px solid rgba(63,107,217,.5);
  }}
  @supports not ((backdrop-filter:blur(1px)) or (-webkit-backdrop-filter:blur(1px))){{
    .face{{background:rgba(255,255,255,.88)}}
  }}
  .scene:hover .card:not(.flipped){{transform:translateY(-8px) rotateX(4deg)}}
  .scene:hover .card{{box-shadow:var(--shadow-lift)}}

  /* ---- 正面 ---- */
  .front{{display:flex;flex-direction:column;align-items:center;justify-content:center;padding:20px;text-align:center}}
  .grp{{
    padding:4px 16px;border-radius:14px;margin-bottom:16px;
    background:var(--accent);color:#fff;font-size:13px;font-weight:700;letter-spacing:2px;
    box-shadow:0 4px 10px rgba(47,82,171,.30);
  }}
  .gname{{
    font-size:26px;font-weight:800;color:var(--accent2);
    max-width:260px;word-break:break-word;line-height:1.35;
  }}
  .gsum{{margin-top:14px;font-size:15px;color:var(--sub);line-height:1.6;max-height:96px;overflow:hidden}}
  .gcount{{margin-top:10px;font-size:13px;color:#9aa6c0}}
  .hint{{position:absolute;bottom:14px;left:0;right:0;color:#9db0c8;font-size:11.5px;letter-spacing:1px}}

  /* ---- 记忆度按钮：会了 / 半熟 / 忘了 ---- */
  .memo{{margin-top:14px;display:flex;gap:10px;user-select:none}}
  .m{{
    padding:6px 14px;border-radius:16px;cursor:pointer;
    font-size:13px;font-weight:600;letter-spacing:.5px;
    border:1px solid #cfd8ea;background:rgba(255,255,255,.75);
    color:#5f6a80;transition:all .15s;
  }}
  .m:hover{{transform:translateY(-1px);border-color:#8fa4d0}}
  .m.on-know{{background:#3f9d6b;border-color:#3f9d6b;color:#fff;box-shadow:0 3px 8px rgba(47,125,85,.30)}}
  .m.on-half{{background:#d19a3d;border-color:#d19a3d;color:#fff;box-shadow:0 3px 8px rgba(160,110,30,.30)}}
  .m.on-forget{{background:#c2685c;border-color:#c2685c;color:#fff;box-shadow:0 3px 8px rgba(150,70,60,.30)}}

  /* ---- 背面 ---- */
  .back{{transform:rotateY(180deg);display:flex;flex-direction:column}}
  .back::before{{content:"";position:absolute;left:0;right:0;top:0;height:6px;background:var(--accent)}}
  .back-inner{{flex:1;overflow-y:scroll;padding:18px 18px 14px}}
  .back-inner::-webkit-scrollbar{{width:8px}}
  .back-inner::-webkit-scrollbar-track{{background:#eef2fa;border-radius:4px}}
  .back-inner::-webkit-scrollbar-thumb{{background:#a9bce0;border-radius:4px}}
  .back-inner::-webkit-scrollbar-thumb:hover{{background:#8fa4d0}}
  .bhead{{text-align:center;padding-bottom:10px;border-bottom:1px dashed #d7dfef;margin-bottom:10px}}
  .bword{{font-size:22px;font-weight:800;color:var(--accent2)}}
  .bgrp{{color:var(--accent);font-size:14px;margin-top:3px;font-weight:600}}
  .ex{{display:block;color:#54608a;margin-top:8px;font-size:16.5px;line-height:1.65;padding-left:2px}}
  .ex b{{color:var(--accent);font-weight:600}}
  .flipback{{text-align:center;color:#a9b3c8;font-size:12px;padding:7px 0 9px;border-top:1px dashed #d7dfef;letter-spacing:1px}}
  .noresult{{text-align:center;color:var(--sub);font-size:15px;padding:60px 0;display:none}}

  /* 排序按钮 */
  .searchbar{{display:flex;justify-content:center;align-items:center;gap:14px;margin-bottom:8px}}
  .sortbtns{{display:flex;gap:8px;flex-shrink:0}}
  .sbtn{{
    height:40px;padding:0 16px;border-radius:20px;cursor:pointer;
    border:1px solid #cfd8ea;background:rgba(255,255,255,.85);
    color:#5f6a80;font-size:13.5px;font-weight:600;letter-spacing:.5px;
    transition:all .15s;user-select:none;
  }}
  .sbtn:hover{{transform:translateY(-1px);border-color:#8fa4d0;color:var(--accent2)}}
  .sbtn.active{{background:var(--accent);border-color:var(--accent);color:#fff;box-shadow:0 3px 8px rgba(47,82,171,.30)}}
</style>
</head>
<body>
<div class="wrap">
  <div class="topbar">
    <header>
      <h1>红火箭分级阅读语法表</h1>
      <div class="subtitle">RED ROCKET READERS · 语法卡片</div>
    </header>
    <div class="searchbar">
      <div class="searchbox">
        <span class="icon">🔍</span>
        <input id="q" type="text" placeholder="模糊搜索语法，如 复数 / can / 时态 …" autocomplete="off">
        <button class="clear" id="clear" title="清空">×</button>
      </div>
      <div class="sortbtns">
        <button id="btnRandom" class="sbtn" title="点击随机打乱卡片顺序">🔀 随机排序</button>
      </div>
    </div>
    <div class="count" id="count"></div>
  </div>

  <div class="grid" id="grid"></div>
  <div class="noresult" id="noresult">没有找到匹配的语法卡片 🐾</div>
</div>

<script>
const WORDS = [
__DATA__
];

function esc(s){{return s.replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;")}}

function buildCard(w){{
  const exHtml = w.exs.map((e,i)=>`<span class="ex"><b>${{i+1}}、</b>${{esc(e)}}</span>`).join("");
  return `
    <div class="card">
      <div class="face front">
        <div class="grp">${{esc(w.group)}}</div>
        <div class="gname">${{esc(w.name)}}</div>
        <div class="gsum">${{esc(w.summary)}}</div>
        <div class="gcount">涵盖 ${{w.count}} 个课堂语法要点</div>
        <div class="memo" data-word="${{esc(w.name)}}">
          <span class="m" data-m="know">会了</span>
          <span class="m" data-m="half">半熟</span>
          <span class="m" data-m="forget">忘了</span>
        </div>
        <div class="hint">— 点击卡片看例句 —</div>
      </div>
      <div class="face back">
        <div class="back-inner">
          <div class="bhead">
            <div class="bword">${{esc(w.name)}}</div>
            <div class="bgrp">${{esc(w.group)}} · 典型例句</div>
          </div>
          ${{exHtml}}
        </div>
        <div class="flipback">— 点击返回 —</div>
      </div>
    </div>`;
}}

/* 懒加载：空壳占位，滚近了才填内容 */
const grid=document.getElementById("grid");
const scenes=WORDS.map((w,i)=>{{
  const s=document.createElement("div");
  s.className="scene";
  s.dataset.idx=i;
  s.dataset.key=w.name+"|"+w.group+"|"+w.summary;
  return s;
}});
function fillScene(s){{
  if(s.dataset.filled) return;
  s.dataset.filled="1";
  s.innerHTML=buildCard(WORDS[+s.dataset.idx]);
  applyMemo(WORDS[+s.dataset.idx].name,s);
}}
const io=new IntersectionObserver(entries=>{{
  entries.forEach(e=>{{
    if(e.isIntersecting){{ fillScene(e.target); io.unobserve(e.target); }}
  }});
}},{{rootMargin:"900px 0px"}});
scenes.forEach(s=>io.observe(s));

/* 瀑布流分栏 */
let cols=[];
let order=WORDS.map((_,i)=>i);
function colCount(){{
  const w=window.innerWidth;
  return w<=640?1:(w<=980?2:3);
}}
function distribute(){{
  const n=colCount();
  if(n===cols.length) return;
  grid.innerHTML="";
  cols=[];
  for(let i=0;i<n;i++){{
    const c=document.createElement("div");
    c.className="col";
    grid.appendChild(c); cols.push(c);
  }}
  order.forEach((idx,i)=>cols[i%n].appendChild(scenes[idx]));
}}

/* 翻转 + 记忆度选择 */
grid.addEventListener("click",e=>{{
  const mb=e.target.closest(".m");
  if(mb){{ setMemo(mb.parentElement.dataset.word, mb.dataset.m); return; }} /* 记忆度按钮不触发翻面 */
  const card=e.target.closest(".card");
  if(card) card.classList.toggle("flipped");
}});

/* 记忆度：会了/半熟/忘了，单选，localStorage 持久保存 */
const MEMO_KEY="rocket_grammar_memo";
let memo={{}};
try{{ memo=JSON.parse(localStorage.getItem(MEMO_KEY)||"{{}}"); }}catch(_){{ memo={{}}; }}
const ON={{know:"on-know",half:"on-half",forget:"on-forget"}};
const WORD_IDX=new Map(WORDS.map((w,i)=>[w.name,i]));
function applyMemo(name,scene){{
  scene = scene || scenes[WORD_IDX.get(name)];
  if(!scene || !scene.dataset.filled) return;
  const cur=memo[name];
  scene.querySelectorAll(".m").forEach(el=>{{
    el.className="m"+(cur&&ON[cur]===ON[el.dataset.m]?" "+ON[el.dataset.m]:"");
  }});
}}
function setMemo(name,val){{
  /* 再点一次已选项 = 取消选择 */
  memo[name] = (memo[name]===val) ? undefined : val;
  if(!memo[name]) delete memo[name];
  try{{ localStorage.setItem(MEMO_KEY,JSON.stringify(memo)); }}catch(_){{}}
  applyMemo(name);
  update();   /* 顶部统计随选择实时刷新 */
}}
function memoStats(){{
  let know=0,half=0,forget=0;
  for(const v of Object.values(memo)){{
    if(v==="know") know++;
    else if(v==="half") half++;
    else if(v==="forget") forget++;
  }}
  return `（其中会了 ${{know}} 个，半熟 ${{half}} 个，忘了 ${{forget}} 个）`;
}}

/* 随机排序 */
const btnRandom=document.getElementById("btnRandom");
btnRandom.addEventListener("click",()=>{{
  order=WORDS.map((_,i)=>i);
  for(let i=order.length-1;i>0;i--){{
    const j=Math.floor(Math.random()*(i+1));
    [order[i],order[j]]=[order[j],order[i]];
  }}
  btnRandom.classList.add("active");
  cols.forEach(c=>c.innerHTML="");
  const n=colCount();
  order.forEach((idx,i)=>cols[i%n].appendChild(scenes[idx]));
  update();
}});

/* 搜索：匹配 语法名 + 分类 + 要点 */
const q=document.getElementById("q"), clear=document.getElementById("clear");
const count=document.getElementById("count"), noresult=document.getElementById("noresult");
function update(){{
  const raw=q.value.trim().toLowerCase();
  clear.style.display=raw?"block":"none";
  const visible=[];
  for(const idx of order){{
    const s=scenes[idx];
    const key=s.dataset.key.toLowerCase();
    if(!raw || key.includes(raw)) visible.push(s);
  }}
  const n=colCount();
  cols.forEach(c=>c.innerHTML="");
  visible.forEach((s,i)=>cols[i%n].appendChild(s));
  count.textContent = (raw ? `匹配到 ${{visible.length}} 张卡片` : `共 ${{WORDS.length}} 张卡片`) + memoStats();
  noresult.style.display=visible.length?"none":"block";
}}
q.addEventListener("input",update);
clear.addEventListener("click",()=>{{q.value="";update();q.focus()}});
distribute();
update();
let lastCols=colCount();
window.addEventListener("resize",()=>{{
  const n=colCount();
  if(n!==lastCols){{ lastCols=n; distribute(); update(); }}
}});
</script>
</body>
</html>
'''

data='\n'.join('  '+json.dumps(w,ensure_ascii=False)+',' for w in WORDS)
html=html.replace('__DATA__',data)
open(BASE+r'\grammar.html','w',encoding='utf-8').write(html)
print('grammar.html 已生成：',len(WORDS),'张卡片,',len(html.encode('utf-8')),'bytes')
