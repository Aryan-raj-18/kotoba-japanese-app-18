#!/usr/bin/env python3
import json, re
from pathlib import Path
ROOT=Path(__file__).parent
DATA=ROOT/'data'

def load(name): return json.load(open(DATA/name,encoding='utf-8'))
def dump(name,obj):
    with open(DATA/name,'w',encoding='utf-8') as f: json.dump(obj,f,ensure_ascii=False,indent=2)

def norm(s):
    return re.sub(r'[\s（）()「」『』。、・…ー～~]+','',str(s or ''))

freq=load('frequency_words.json')
exam=load('jlpt_exam_questions.json')
roadmap=load('roadmap.json')

GRAMMAR_POS={'p','p. case','p. conj','p. disc','p conj','p disc','p case','aux','aux, cp','cp','conj'}

# Approximate learning levels for common structures. These are Kotoba study tiers,
# not claims of official JLPT ownership; exact exam-source matches below override them.
LEVEL_HINTS={
'N5': {'の','に','は','た','を','だ','が','て','と','ます','も','で','ている','です','ない','か','から','よ','へ','たい','より','まで(迄)','ね','ので','でも','たり'},
'N4': {'れる','せる','けれど','よう','んだ','のだ','ば','し','ながら','ても','てくる','だけ','くらい','ぐらい','ではない','ていく','てみる','かもしれない','てもらう','ておく','ことがある','なければいけない','なければならない','らしい','のに'},
'N3': {'として','について','それで','など','によって','ほど','しかし','なんか','まま','しか','にとって','ばかり','ことが出来る','ことになる','に対して','に対する','それでも','一方','さえ','に関して','に関する','こそ','しかも','ずつ'},
'N2': {'において','における','による','により','である','のである','べし','及び','のみ','だが','つつ','したがって','だけでなく','どころか'},
'N1': set(),
}
HINT_BY_PATTERN={p:lvl for lvl,ps in LEVEL_HINTS.items() for p in ps}
level_order={'N5':0,'N4':1,'N3':2,'N2':3,'N1':4}

# Index exact correct-answer patterns from the uploaded exam-prep datasets.
answer_matches={}
for lvl,qs in exam.items():
    for q in qs:
        ans=str(q.get('answer_label') or q.get('answer') or '').strip()
        if not ans: continue
        answer_matches.setdefault(norm(ans),[]).append((lvl,q))

def fallback_level(rank):
    if rank <= 300: return 'N5'
    if rank <= 700: return 'N4'
    if rank <= 1150: return 'N3'
    if rank <= 1600: return 'N2'
    return 'N1'

def pos_label(pos):
    if 'conj' in pos: return 'Conjunction'
    if pos.startswith('p') or pos=='p': return 'Particle'
    if 'aux' in pos: return 'Auxiliary'
    if pos=='cp': return 'Grammar pattern'
    return 'Grammar'

grammar=[]
seen=set()
for e in freq:
    pos=e.get('part_of_speech','')
    if pos not in GRAMMAR_POS: continue
    pattern=e['word'].strip(); key=norm(pattern)
    if not key or key in seen: continue
    seen.add(key)
    lvl=HINT_BY_PATTERN.get(pattern) or fallback_level(e['rank'])
    source_examples=[]
    # Exact-match exam source is strong evidence for a study level. We only
    # match multi-character patterns to avoid a single particle like に being
    # "promoted" by appearing inside an unrelated N1 answer.
    if len(key)>=2 and key in answer_matches:
        matches=answer_matches[key]
        # If a pattern is explicitly the right answer in more than one source,
        # keep the easiest level it is directly practiced at.
        source_lvl=min((m[0] for m in matches), key=lambda x: level_order.get(x,9))
        # Never promote a common/basic form merely because the same surface
        # string appears as an answer in a harder exam question. Ambiguous
        # strings such as それ or よう occur across many functions. Keep the
        # easier of the curated/frequency study tier and the direct source.
        lvl=min((lvl, source_lvl), key=lambda x: level_order.get(x,9))
        for mlvl,q in matches[:2]:
            source_examples.append({
                'level':mlvl,
                'sentence':q.get('explanation') or q.get('prompt',''),
                'blocks':q.get('explanation_blocks', []),
                'question_id':q.get('id',''),
            })
    grammar.append({
        'id':f'g-{len(grammar)+1:03d}',
        'pattern':pattern,
        'reading':e.get('reading',''),
        'romaji':e.get('romaji',''),
        'meaning':e.get('meaning',''),
        'level':lvl,
        'level_source':('curated' if pattern in HINT_BY_PATTERN else 'frequency'),
        'type':pos_label(pos),
        'part_of_speech':pos,
        'frequency_rank':e.get('rank'),
        'example_ja':e.get('example_ja',''),
        'example_en':e.get('example_en',''),
        'source_examples':source_examples,
    })

# Add advanced correct-answer forms from the N2/N1 exam books when they are
# not already represented by a frequency-list grammar entry. These entries
# deliberately keep source-language rationale instead of inventing a gloss.
N2_GLOSSES = {
    'からいうと':'from the standpoint of; judging from',
    'からして':'judging from; starting with',
    '次第で':'depending on; according to',
    'において':'in; at; on (formal context)',
    'に限り':'only; limited to',
    'にかけては':'when it comes to; regarding skill in',
    'にこたえて':'in response to',
    'にそって':'along; in accordance with',
    'にとっての':'for; from the point of view of',
    'に反して':'contrary to; against',
    'による':'by; due to; based on',
    'によっては':'depending on; in some cases',
    'にわたって':'over; across; throughout',
    'はともかく':'leaving aside; regardless of',
    'めぐって':'concerning; over; surrounding',
    'もとでは':'under; under the conditions of',
    'をもとにして':'based on; using as a basis',
    'はもとより':'not only; to say nothing of',
    'をきっかけに':'triggered by; taking the opportunity of',
    'を契機に':'on the occasion of; as a turning point',
    'をこめて':'with; putting feeling or meaning into',
    'を通じて':'through; via; throughout',
    'を問わず':'regardless of; irrespective of',
    'に対しての':'toward; regarding',
    'につき':'due to; because of; per',
    'にほかならない':'nothing other than; precisely',
    'にかかわらず':'regardless of; irrespective of',
    'に際して':'on the occasion of; when',
    'に先立ち':'prior to; before',
    'よう':'it seems that; apparently',
    'ことに':'to one’s …; notably',
    'こと':'should; must (instruction/rule)',
    'ことなく':'without doing',
    'ことだから':'because it is characteristic of',
    'ことは':'there is no need to … (in 〜ことはない)',
    'わけにはいかない':'cannot reasonably; cannot afford to',
    'ものがあります':'there is something that; has a certain quality',
    'うえ':'after; upon doing',
    'うえは':'now that; since',
    'うえに':'in addition to; moreover',
    'ことか':'how …!; what a …! (emphasis)',
    'ことから':'because; from the fact that',
    'もの':'you know; because (explanatory ending)',
    'もん':'colloquial もの; because / you know',
    'ものなら':'if one could; if it were possible',
    'もんか':'no way; absolutely not',
    'ものの':'although; even though',
    'わけでもない':'it is not that; not necessarily',
    'あげく':'after much …, ending in (often negative)',
    '末':'after; at the end of a process',
    'だけあって':'as expected of; precisely because',
    'だけに':'precisely because; all the more because',
    'とともに':'together with; as',
    'につれて':'as; in proportion as',
    'にともなって':'along with; as a result of',
    'にしたら':'from the standpoint of',
    'にしても':'even if; even for',
    'にしては':'for; considering',
}

N1_CURATED = {
    '機に': ('〜を機に', 'taking the opportunity or occasion of'),
    'でもしたら': ('〜でもしたら', 'if something like that were to happen'),
    '最中に': ('〜最中に', 'in the middle of; while in the midst of'),
    'のみならず': ('〜のみならず', 'not only … but also'),
    '話すともなく': ('〜ともなく', 'without any particular intention or target'),
    'しまつだ': ('〜始末だ', 'to end up in an undesirable state or result'),
    'なりに': ('〜なりに', 'in one’s own way; appropriate to'),
    'じゃあるまいし': ('〜じゃあるまいし', 'it is not as if …'),
    'にひきかえ': ('〜にひきかえ', 'in contrast to; compared with'),
    '反面': ('〜反面', 'on the other hand; while'),
    'ちなみに': ('ちなみに', 'incidentally; by the way'),
    'ってとこ': ('〜ってとこ', 'roughly speaking; about'),
    'ともなると': ('〜ともなると', 'when it comes to; once it reaches'),
    'とあれば': ('〜とあれば', 'if it is the case that; if for the sake of'),
}

for lvl in ('N2','N1'):
    for q in exam.get(lvl,[]):
        raw_pat=str(q.get('answer_label') or q.get('answer') or '').strip()
        if lvl == 'N1' and raw_pat not in N1_CURATED:
            continue
        pat = N1_CURATED.get(raw_pat, (raw_pat, ''))[0]
        key=norm(pat)
        if not key or key in seen or len(pat)>28: continue
        if not re.search(r'[ぁ-んァ-ヶ一-龯]',pat): continue
        seen.add(key)
        expl=q.get('explanation','')
        source_note=''
        # Many N1 source explanations include a rationale after the completed sentence.
        if '。 ' in expl:
            source_note=expl.split('。 ',1)[1].strip()
        grammar.append({
            'id':f'g-{len(grammar)+1:03d}',
            'pattern':pat,
            'reading':'',
            'romaji':'',
            'meaning':(N1_CURATED.get(raw_pat, ('',''))[1] if lvl=='N1'
                       else N2_GLOSSES.get(raw_pat, 'advanced source-backed grammar pattern')),
            'level':lvl,
            'level_source':'exam',
            'type':'Exam grammar pattern',
            'part_of_speech':'exam',
            'frequency_rank':None,
            'example_ja':expl.split('。',1)[0]+'。' if expl else q.get('prompt',''),
            'example_en':'',
            'source_note':source_note,
            'answer_form': raw_pat,
            'source_blocks': q.get('explanation_blocks', []),
            'source_examples':[{'level':lvl,'sentence':expl or q.get('prompt',''),'blocks':q.get('explanation_blocks', []),'question_id':q.get('id','')}],
        })

# Stable order: level then source frequency, then pattern.
grammar.sort(key=lambda g:(level_order.get(g['level'],9), g['frequency_rank'] or 99999, g['pattern']))
# Re-number after sorting.
for i,g in enumerate(grammar,1): g['id']=f'g-{i:03d}'
dump('grammar.json',grammar)

# ---------------------------- advanced roadmap ----------------------------
# Remove prior generated sections if this script is re-run.
new_ids={'upper-intermediate','advanced-grammar','n1-mastery'}
roadmap=[s for s in roadmap if s.get('id') not in new_ids]

def split_chunks(items,n): return [items[i:i+n] for i in range(0,len(items),n)]

def make_chapter(level, idx, items, section_id):
    cid=f'{level.lower()}-grammar-{idx:02d}'
    vocab=[]; sentences=[]; points=[]
    for g in items:
        reading=g.get('reading') or ''
        romaji=g.get('romaji') or ''
        vocab.append({'jp':g['pattern'],'reading':reading,'romaji':romaji,'meaning':g['meaning']})
        ex=g.get('example_ja') or ''
        answer_form=g.get('answer_form') or g['pattern'].lstrip('〜')
        if ex and answer_form in ex:
            sentences.append({
                'jp':ex.replace(answer_form,'___',1),
                'reading':ex.replace(answer_form,'___',1),
                'romaji':'',
                'english':g.get('example_en') or g['meaning'],
                'blank':g['pattern'],
            })
        points.append({'pattern':g['pattern'], 'note':g['meaning'], 'jp':ex, 'en':g.get('example_en','')})
    title=f'{level} Grammar Patterns {idx}'
    return {
        'id':cid,'title':title,'icon':'文','kind':'lesson',
        'guide':{
            'intro':f'Build control of {level}-level grammar patterns. Read the sourced example first, then compare the function and sentence context.',
            'points':points[:8],
        },
        'vocab':vocab,
        'sentences':sentences,
    }

def make_section(sec_id,title,blurb,level,limit_chapters):
    items=[g for g in grammar if g['level']==level and g.get('example_ja')]
    # Roadmap lessons need especially clean, level-representative material.
    # N2 prioritizes patterns directly practiced by the uploaded N2 source;
    # N1 is intentionally limited to the curated grammar-form questions, not
    # sentence-building answer fragments such as ordinary nouns or numbers.
    if level == 'N2':
        direct=[g for g in items if g.get('level_source')=='exam' or any(x.get('level')=='N2' for x in g.get('source_examples',[]))]
        rest=[g for g in items if g not in direct]
        items=direct+rest
    elif level == 'N1':
        items=[g for g in items if g.get('level_source')=='exam']
    elif level == 'N3':
        curated=[g for g in items if g.get('pattern') in LEVEL_HINTS['N3']]
        rest=[g for g in items if g not in curated]
        items=curated+rest
    chunks=split_chunks(items[:limit_chapters*8],8)
    chapters=[make_chapter(level,i+1,ch,sec_id) for i,ch in enumerate(chunks)]
    chapters.append({
        'id':f'{sec_id}-review','title':f'{title} — Section Review','icon':'✓','kind':'review',
        'review_section':sec_id,'vocab':[],'sentences':[]
    })
    return {'id':sec_id,'title':title,'blurb':blurb,'chapters':chapters}

roadmap.extend([
    make_section('upper-intermediate','Upper Intermediate','Move from everyday grammar into denser N3-style structures.','N3',5),
    make_section('advanced-grammar','Advanced Grammar','Practice formal and nuanced N2-style patterns in context.','N2',5),
    make_section('n1-mastery','N1 Mastery','Work through advanced source-backed forms and sentence nuance.','N1',5),
])
# Keep Grand Review last if it existed earlier; it was before the appended sections.
grand=[s for s in roadmap if s.get('id')=='grand-review']
roadmap=[s for s in roadmap if s.get('id')!='grand-review']+grand
# Actually put grand review last after advanced sections.
if grand:
    gr=roadmap.pop(-1)
    roadmap.append(gr)
dump('roadmap.json',roadmap)
print('grammar entries',len(grammar))
print('roadmap sections',[(s['id'],len(s['chapters'])) for s in roadmap])
