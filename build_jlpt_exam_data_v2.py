import json, re, glob, os, zipfile, unicodedata
from collections import Counter, defaultdict
from bs4 import BeautifulSoup, NavigableString, Tag

ROOT = os.path.dirname(os.path.abspath(__file__))
EPUBS={}
for p in glob.glob('/mnt/data/*.epub'):
    m=re.search(r'\b(N[1-5])\b', os.path.basename(p))
    if m:
        EPUBS[m.group(1)] = p

REQUIRED = ['N1','N2','N3','N4','N5']
missing=[x for x in REQUIRED if x not in EPUBS]
if missing:
    raise SystemExit(f'Missing EPUBs: {missing}')

KANJI_RE = re.compile(r'[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]')

def norm(s):
    s=s.replace('\u3000',' ')
    return re.sub(r'\s+',' ',s).strip()


def iter_ruby_aware(node):
    """Yield plain strings and ruby dicts while ignoring rt text as base text."""
    if isinstance(node, NavigableString):
        yield str(node)
        return
    if not isinstance(node, Tag):
        return
    if node.name in ('rt','rp'):
        return
    if node.name == 'ruby':
        rt=node.find('rt')
        reading=norm(rt.get_text('', strip=True)) if rt else ''
        base_parts=[]
        for child in node.children:
            if isinstance(child, Tag) and child.name in ('rt','rp'):
                continue
            if isinstance(child, NavigableString):
                base_parts.append(str(child))
            elif isinstance(child, Tag):
                base_parts.append(child.get_text('', strip=True))
        base=norm(''.join(base_parts))
        if base:
            if reading:
                yield {'text':base,'reading':reading}
            else:
                yield base
        return
    for child in node.children:
        yield from iter_ruby_aware(child)


def clean_segments(parts):
    out=[]
    for part in parts:
        if isinstance(part, str):
            part=re.sub(r'\s+',' ',part.replace('\u3000',' '))
            if not part:
                continue
            if out and isinstance(out[-1],str):
                out[-1]+=part
            else:
                out.append(part)
        else:
            if out and isinstance(out[-1],str):
                out[-1]=re.sub(r'\s+',' ',out[-1])
            out.append(part)
    # trim only outside whitespace; preserve meaningful spaces inside English text
    if out and isinstance(out[0],str): out[0]=out[0].lstrip()
    if out and isinstance(out[-1],str): out[-1]=out[-1].rstrip()
    return [x for x in out if not (isinstance(x,str) and x=='')]


def para_record(p):
    segments=clean_segments(list(iter_ruby_aware(p)))
    plain=''.join(x if isinstance(x,str) else x['text'] for x in segments)
    return {'text': norm(plain), 'segments': segments}


def get_records(z, part):
    n=f'text/part{part:04d}.html'
    soup=BeautifulSoup(z.read(n),'html.parser')
    out=[]
    for p in soup.find_all('p'):
        rec=para_record(p)
        t=rec['text']
        if t and 'もくじ Table of contents' not in t:
            out.append(rec)
    return out


def get_paras(z, part):
    return [r['text'] for r in get_records(z,part)]


def build_ruby_lexicon(epubs):
    counts=defaultdict(Counter)
    context_counts=defaultdict(Counter)
    for p in epubs.values():
        with zipfile.ZipFile(p) as z:
            for n in z.namelist():
                if not n.endswith('.html'): continue
                soup=BeautifulSoup(z.read(n),'html.parser')
                for para in soup.find_all('p'):
                    segs=clean_segments(list(iter_ruby_aware(para)))
                    for ix,seg in enumerate(segs):
                        if not isinstance(seg,dict) or not seg.get('reading') or not KANJI_RE.search(seg.get('text','')):
                            continue
                        base=seg['text']; reading=seg['reading']
                        counts[base][reading]+=1
                        following=''
                        if ix+1 < len(segs) and isinstance(segs[ix+1],str):
                            following=segs[ix+1]
                        m=re.match(r'([\u3040-\u30ffー]{1,4})',following)
                        if m:
                            kana=m.group(1)
                            for nchar in range(1,len(kana)+1):
                                context_counts[(base,kana[:nchar])][reading]+=1
    lex={}
    for base,c in counts.items():
        top=c.most_common()
        if len(top)==1:
            lex[base]=top[0][0]
        elif len(base)>1 and top[0][1] >= 3*top[1][1]:
            lex[base]=top[0][0]
    context_lex={}
    for key,c in context_counts.items():
        top=c.most_common()
        if len(top)==1 or (len(top)>1 and top[0][1] >= 3*top[1][1]):
            context_lex[key]=top[0][0]
    return lex, context_lex, counts

RUBY_LEXICON, RUBY_CONTEXT, RUBY_COUNTS = build_ruby_lexicon(EPUBS)
RUBY_KEYS = sorted(RUBY_COUNTS, key=len, reverse=True)

# A few N3 answer summaries omit ruby in the source answer page. These contextual
# readings are standard readings for the exact answer contexts that remain after
# source-ruby matching. They are intentionally context-scoped, not global.
SPECIAL_CONTEXT_READINGS = {
    ('数','が'): 'かず',
    ('皆','、'): 'みな',
    ('主','を'): 'ぬし',
    ('張','った'): 'は',
}


def annotate_text(text):
    """Add source-derived furigana to plain text using the EPUB ruby lexicon."""
    text=norm(text)
    if not text: return []
    out=[]; i=0
    while i < len(text):
        match=None; reading=None
        # Match longest source-backed ruby base beginning here. Prefer an unambiguous
        # base reading, then a source-observed base+okurigana context reading.
        for key in RUBY_KEYS:
            if len(key) > len(text)-i or not text.startswith(key,i):
                continue
            if key in RUBY_LEXICON:
                match=key; reading=RUBY_LEXICON[key]; break
            tail=text[i+len(key):]
            km=re.match(r'([\u3040-\u30ffー]{1,4})',tail)
            if km:
                kana=km.group(1)
                for nchar in range(min(4,len(kana)),0,-1):
                    r=RUBY_CONTEXT.get((key,kana[:nchar]))
                    if r:
                        match=key; reading=r; break
            if match: break
        if not match:
            # Exact-context fallback for the few answer-summary kanji not ruby-tagged
            # anywhere unambiguously enough for the source lexicon.
            for (base,suffix),r in SPECIAL_CONTEXT_READINGS.items():
                if text.startswith(base+suffix,i):
                    match=base; reading=r; break
        if match and reading:
            out.append({'text':match,'reading':reading}); i+=len(match)
        else:
            ch=text[i]
            if out and isinstance(out[-1],str): out[-1]+=ch
            else: out.append(ch)
            i+=1
    return clean_segments(out)


def ensure_furigana(blocks):
    """Fill any plain Japanese block with source-derived ruby; preserve exact source ruby where present."""
    fixed=[]
    for block in blocks:
        if not block: continue
        if any(isinstance(x,dict) and x.get('reading') for x in block):
            # Annotate remaining plain spans too, so answer pages with partial ruby still read well.
            merged=[]
            for x in block:
                if isinstance(x,dict): merged.append(x)
                else: merged.extend(annotate_text(x))
            fixed.append(clean_segments(merged))
        else:
            plain=''.join(x if isinstance(x,str) else x['text'] for x in block)
            fixed.append(annotate_text(plain))
    return fixed

OPT_PATTERNS=[
    re.compile(r'^\((\d)\)\s*(.*)$'),
    re.compile(r'^([1-4])[\.．]\s*(.*)$'),
    re.compile(r'^([①②③④])\s*(.*)$'),
]
CIRC={'①':1,'②':2,'③':3,'④':4}

def parse_opt(s):
    for p in OPT_PATTERNS:
        m=p.match(s)
        if m:
            key=m.group(1)
            num=CIRC.get(key,int(key) if key.isdigit() else None)
            return num,norm(m.group(2))
    return None

def strip_qnum(s):
    s=re.sub(r'^\s*\d+\s*[\.．]\s*','',s)
    s=re.sub(r'^\s*\d+\s+','',s)
    return norm(s)

def qnum_from(s):
    m=re.match(r'^\s*(\d+)\s*(?:[\.．]|\s)',s)
    return int(m.group(1)) if m else None

def parse_mcq_questions(records):
    paras=[r['text'] for r in records]
    start=0
    for i,p in enumerate(paras):
        if '【問題】' in p:
            start=i+1; break
    qs=[]; last=start; i=start
    while i+3 < len(paras):
        group=[parse_opt(paras[i+j]) for j in range(4)]
        if all(group[j] and group[j][0]==j+1 for j in range(4)):
            qblock=[p for p in paras[last:i] if not p.startswith(('問題 ', 'もんだい ')) and '【問題】' not in p]
            qi=None
            for k,p in enumerate(qblock):
                if qnum_from(p) is not None:
                    qi=k; break
            if qi is None:
                i+=1; continue
            qblock=qblock[qi:]
            qnum=qnum_from(qblock[0])
            qblock[0]=strip_qnum(qblock[0])
            prompt=norm(' '.join(qblock))
            opts=[x[1] for x in group]
            if prompt and all(opts): qs.append({'num':qnum,'prompt':prompt,'options':opts})
            last=i+4; i+=4
        else:
            i+=1
    return qs

ANSWER_RE=[
    re.compile(r'^(\d+)\s*[-−]\s*\((\d)\)\s*(.*)$'),
    re.compile(r'^(\d+)\s*[\.．]\s*\((\d)\)\s*(.*)$'),
    re.compile(r'^(\d+)\s*[-−]\s*([1-4])\s*[\.．]\s*(.*)$'),
    re.compile(r'^(\d+)\s*[-−]\s*([①②③④])\s*(.*)$'),
]
def parse_ans_marker(s):
    for p in ANSWER_RE:
        m=p.match(s)
        if m:
            key=m.group(2); idx=CIRC.get(key,int(key) if key.isdigit() else None)
            return int(m.group(1)),idx,norm(m.group(3))
    return None

def mostly_english(s):
    latin=sum(c.isascii() and c.isalpha() for c in s)
    jp=sum(('\u3040'<=c<='\u30ff') or ('\u3400'<=c<='\u9fff') for c in s)
    return latin>jp*2 and latin>15

def parse_answers(records):
    markers=[]
    for i,r in enumerate(records):
        m=parse_ans_marker(r['text'])
        if m: markers.append((i,m))
    ans={}
    for pos,(i,(num,idx,label)) in enumerate(markers):
        j=markers[pos+1][0] if pos+1<len(markers) else len(records)
        completed=[]; rationale=[]
        for r in records[i+1:j]:
            s=r['text']
            if mostly_english(s): break
            if s.startswith(('【','−−','※')) or 'Table of contents' in s: continue
            # Source books place the completed sentence/dialogue first. Detailed
            # option-analysis lines then begin with brackets/quotes or ∴. Keep those
            # separate so we never show a rejected-option note as the sentence itself.
            is_analysis = s.startswith(('（','(','「','∴')) or '∴★' in s
            if is_analysis and completed:
                rationale.append(r)
            elif not rationale:
                completed.append(r)
            else:
                rationale.append(r)

        # Keep the completed answer sentence/dialogue concise (usually 1-2 lines).
        blocks=[r['segments'] for r in completed[:2]]
        plain_notes=[r['text'] for r in completed[:2]]

        # If the source provides an explicit correct-choice reason, add that reason.
        correct_reason=next((r for r in rationale if '○' in r['text']), None)
        if correct_reason is None:
            correct_reason=next((r for r in rationale if '∴★' in r['text']), None)
        if correct_reason is not None:
            blocks.append(correct_reason['segments'])
            plain_notes.append(correct_reason['text'])

        blocks=ensure_furigana(blocks)
        ans[num]={
            'answer_index':idx-1,
            'answer_label':label,
            'explanation':norm(' '.join(plain_notes)),
            'explanation_blocks':blocks,
        }
    return ans


def build_pairs(level, pairs):
    rows=[]
    with zipfile.ZipFile(EPUBS[level]) as z:
        for qpart,apart,category in pairs:
            qrec=get_records(z,qpart); arec=get_records(z,apart)
            qs=parse_mcq_questions(qrec); aa=parse_answers(arec)
            for q in qs:
                a=aa.get(q['num'])
                if not a or not (0<=a['answer_index']<len(q['options'])): continue
                q.update(a); q.update({'category':category,'source_part':qpart})
                rows.append(q)
    return rows

# Same source-backed sets as v3.1.0.
N5_pairs=[]
for q in [11,13,15,17,19,21,23,25]: N5_pairs.append((q,q+1,'Vocabulary'))
for q in [91,93,95]: N5_pairs.append((q,q+1,'Particles'))
for q in [112,114,117,129,131,136,141,148,150,158,160,162,164,166]: N5_pairs.append((q,q+1,'Grammar'))
for q in [215,217,219,221,223,225]: N5_pairs.append((q,q+1,'Expressions'))
for q in [239,241]: N5_pairs.append((q,q+1,'Conversation'))

N4_pairs=[]
for q in range(108,126,2): N4_pairs.append((q,q+1,'Grammar'))
for q in [146,148,150]: N4_pairs.append((q,q+1,'Usage & Grammar'))

N2_pairs=[]
for q in [71,73,75,77,79,81]: N2_pairs.append((q,q+1,'Grammar: noun patterns'))
for q in [118,120,122,124]: N2_pairs.append((q,q+1,'Grammar: formal nouns'))
for q in [148,150]: N2_pairs.append((q,q+1,'Grammar: paired expressions'))

# N1: include book examples plus the dedicated practice sets.
N1_pairs=[
    (22,23,'Grammar: form choice'),
    (24,25,'Grammar: sentence building'),
    (143,144,'Grammar: form choice'),
    (145,146,'Grammar: form choice'),
    (147,148,'Grammar: form choice'),
    (149,150,'Grammar: sentence building'),
    (151,152,'Grammar: sentence building'),
    (153,154,'Grammar: sentence building'),
]

DATA={
    'N5':build_pairs('N5',N5_pairs),
    'N4':build_pairs('N4',N4_pairs),
    'N2':build_pairs('N2',N2_pairs),
    'N1':build_pairs('N1',N1_pairs),
}

# N3 reading helpers.
def parse_n3_short(z,qpart,apart):
    ps=get_paras(z,qpart)
    problem_idx=next((i for i,p in enumerate(ps) if p.startswith('問題')),None)
    if problem_idx is None: return None
    passage=[]
    for p in ps:
        if p.startswith(('内容理解','つぎの')) or re.fullmatch(r'\d+',p): continue
        if p.startswith('問題'): break
        passage.append(p)
    prompt=re.sub(r'^問題\s*','',ps[problem_idx]).strip()
    opts=[]
    for p in ps[problem_idx+1:]:
        m=re.match(r'^([1-4])\s+(.+)$',p)
        if m: opts.append(norm(m.group(2)))

    arecs=get_records(z,apart)
    answer_rec=next((r for r in arecs if re.match(r'^[1-4]\s+.+',r['text'])),None)
    if len(opts)!=4 or not answer_rec: return None
    m=re.match(r'^([1-4])\s+(.+)$',answer_rec['text'])
    idx=int(m.group(1))-1; label=norm(m.group(2))
    blocks=ensure_furigana([annotate_text(label)])
    return {'category':'Reading: short','passage':norm(' '.join(passage)),'prompt':prompt,
            'options':opts,'answer_index':idx,'answer_label':label,'explanation':label,
            'explanation_blocks':blocks,'source_part':qpart}


def parse_n3_question_page(z, passage_part, qpart, apart, category):
    passage_ps=get_paras(z,passage_part)
    passage=[]
    for p in passage_ps:
        if p.startswith(('内容理解','つぎの','情報検索')) or re.fullmatch(r'\d+',p): continue
        if p.startswith('問'): break
        passage.append(p)
    passage=norm(' '.join(passage))
    ps=get_paras(z,qpart)
    qs=[]; i=0
    while i<len(ps):
        m=re.match(r'^問\s*([０-９0-9]+)\s*(.*)$',ps[i])
        if not m:
            i+=1; continue
        num=int(unicodedata.normalize('NFKC',m.group(1)))
        prompt=norm(m.group(2)); i+=1; opts=[]
        while i<len(ps) and len(opts)<4:
            om=re.match(r'^[１２３４1-4][\.．]?\s*(.+)$',ps[i])
            if om: opts.append(norm(om.group(1)))
            elif prompt and not ps[i].startswith('問'): prompt=norm(prompt+' '+ps[i])
            i+=1
        if len(opts)==4:
            qs.append({'num':num,'category':category,'passage':passage,'prompt':prompt,'options':opts,'source_part':qpart})

    amap={}
    for r in get_records(z,apart):
        m=re.match(r'^問\s*([０-９0-9]+)\s*[-−]\s*([１２３４1-4])\s*(.*)$',r['text'])
        if not m: continue
        num=int(unicodedata.normalize('NFKC',m.group(1)))
        idx=int(unicodedata.normalize('NFKC',m.group(2)))-1
        label=norm(m.group(3))
        amap[num]=(idx,label,ensure_furigana([annotate_text(label)]))
    for q in qs:
        if q['num'] in amap:
            q['answer_index'],q['answer_label'],q['explanation_blocks']=amap[q['num']]
            q['explanation']=q['answer_label']
    return [q for q in qs if 'answer_index' in q]

n3=[]
with zipfile.ZipFile(EPUBS['N3']) as z:
    for qp,ap in [(82,83),(87,88),(92,93),(97,98),(102,103),(107,108),(112,113)]:
        x=parse_n3_short(z,qp,ap)
        if x:n3.append(x)
    for pp,qp,ap,cat in [
        (117,118,119,'Reading: medium'),(123,124,125,'Reading: medium'),(130,131,132,'Reading: medium'),
        (137,138,139,'Reading: medium'),(144,145,146,'Reading: medium'),(151,152,153,'Reading: medium'),
        (157,158,159,'Reading: long'),(164,165,166,'Reading: long'),(171,172,173,'Reading: long'),
    ]:
        n3.extend(parse_n3_question_page(z,pp,qp,ap,cat))
DATA['N3']=n3

# Final cleanup, IDs, and guaranteed feedback block.
for level,rows in DATA.items():
    seen=set(); clean=[]
    for q in rows:
        if len(q.get('options',[]))!=4: continue
        idx=q['answer_index']
        if not 0<=idx<4: continue
        q['answer']=q['options'][idx]
        q.pop('num',None)
        key=(q.get('passage',''),q['prompt'],tuple(q['options']))
        if key in seen: continue
        seen.add(key)
        blocks=q.get('explanation_blocks') or []
        if not blocks:
            fallback=q.get('explanation') or q.get('answer_label') or q['answer']
            blocks=[annotate_text(fallback)]
        q['explanation_blocks']=ensure_furigana(blocks)
        clean.append(q)
    for i,q in enumerate(clean,1):
        q['id']=f'{level.lower()}-exam-{i:03d}'
    DATA[level]=clean

out=os.path.join(ROOT,'data','jlpt_exam_questions.json')
with open(out,'w',encoding='utf-8') as f:
    json.dump(DATA,f,ensure_ascii=False,indent=2)
print('WROTE',out)
print('ruby lexicon entries:',len(RUBY_LEXICON),'context entries:',len(RUBY_CONTEXT))
for level in ['N5','N4','N3','N2','N1']:
    rows=DATA[level]
    cats={c:sum(1 for q in rows if q['category']==c) for c in sorted(set(q['category'] for q in rows))}
    print(level,len(rows),cats)
    for q in rows[:2]:
        print(' ',q['id'],q['category'],q['prompt'][:75],'=>',q['answer'])
        print('   blocks',q['explanation_blocks'][:1])
