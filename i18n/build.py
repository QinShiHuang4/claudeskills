#!/usr/bin/env python3
"""Builds translated copies of the English site in docs/ into docs/<lang>/.
English pages in docs/ are the source. Translations live in i18n/<lang>.json as
{"0": "...", "1": "..."} aligned to i18n/en.json. Run: python3 i18n/build.py"""
import json,re,os,html
from html.parser import HTMLParser
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));DOCS=os.path.join(ROOT,'docs');I=os.path.join(ROOT,'i18n')
PAGES=['index.html','404.html','contact/index.html','delete-account/index.html','privacy/index.html','child-safety/index.html']
ROUTES=['/privacy/','/contact/','/delete-account/','/child-safety/']
ATTR=('alt','aria-label','placeholder','data-ok','data-mail')
JS=["This opens your email app with your request filled in. Just press send.","Your email app should open with the request filled in. If it doesn’t, email","We couldn’t send that. Check your connection and try again, or email","Language"]
SKIP={'Meet Bundle - Dating & Connections','bundle','Bundle','Meet Bundle','App Store','Google Play','support@meetbundle.com','Meet Bundle ·','NCMEC CyberTipline','INHOPE'}
LANGS={ # code: (native name, dir, google fonts family param, head font, body font, og locale)
 'en':('English','ltr','','',"",'en_US'),
 'he':('עברית','rtl','Heebo:wght@400;500;700;800','Heebo','Heebo','he_IL'),
 'ar':('العربية','rtl','Noto+Kufi+Arabic:wght@600;800&family=Noto+Sans+Arabic:wght@400;500;600','Noto Kufi Arabic','Noto Sans Arabic','ar_AR'),
 'ru':('Русский','ltr','Manrope:wght@400;500;600;800','Manrope','Manrope','ru_RU'),
 'uk':('Українська','ltr','Manrope:wght@400;500;600;800','Manrope','Manrope','uk_UA'),
 'de':('Deutsch','ltr','','','','de_DE'),'fr':('Français','ltr','','','','fr_FR'),'es':('Español','ltr','','','','es_ES'),
 'pt':('Português','ltr','','','','pt_BR'),'it':('Italiano','ltr','','','','it_IT'),'nl':('Nederlands','ltr','','','','nl_NL'),
 'zh':('简体中文','ltr','Noto+Sans+SC:wght@400;500;700;900','Noto Sans SC','Noto Sans SC','zh_CN'),
 'ja':('日本語','ltr','Noto+Sans+JP:wght@400;500;700;900','Noto Sans JP','Noto Sans JP','ja_JP'),
 'vi':('Tiếng Việt','ltr','Be+Vietnam+Pro:wght@400;500;600;800','Be Vietnam Pro','Be Vietnam Pro','vi_VN'),
 'th':('ไทย','ltr','Noto+Sans+Thai:wght@400;500;600;800','Noto Sans Thai','Noto Sans Thai','th_TH')}
HREFLANG={'zh':'zh-Hans','pt':'pt'}
FAQ=[('Is Meet Bundle free?',['Yes. Meet Bundle is currently subscription-free, with no payments. You can create a profile, meet people, match and chat without paying.']),
('What is a Spark?',['A Spark is a Like with a short message, so the other person reads your words before they decide.']),
('What’s the difference between a Wink, a Like and a Spark?',['A Wink is a light hello. A Like says you’re interested, and if they like you back, it’s a match. A Spark is a Like with a message.']),
('Is Meet Bundle safe?',['Every photo is reviewed before anyone sees it, new profiles start under review, and you can block or report anyone from their profile or chat.']),
('Who can join Meet Bundle?',['Meet Bundle is for adults 18 and over. Everyone gives a date of birth when they sign up.']),
('Can people see my exact location?',['No. Others see your city and an approximate distance, never your exact location.']),
('How do I delete my account?',['In the app, go to Profile, then Settings, then Account details, and tap Delete account.','You can also request deletion on our website.'])]
def brand(out):
  # Trademark rule: formal brand mentions read 'Meet Bundle'
  fix=lambda t:re.sub(r'(?<!Meet )\bBundle\b','Meet Bundle',t)
  out=re.sub(r'<title>(.*?)</title>',lambda m:'<title>'+fix(m[1])+'</title>',out,count=1)
  out=re.sub(r'(<meta (?:name="description"|property="og:title"|property="og:description"|property="og:site_name"|property="og:image:alt") content=")([^"]*)(")',lambda m:m[1]+fix(m[2])+m[3],out)
  return out
def jsonld(code,M,desc):
  t=lambda x:M.get(x,x)
  home='https://meetbundle.com'+('/' if code=='en' else '/'+code+'/')
  lang=HREFLANG.get(code,code)
  g=[{'@type':'Organization','@id':'https://meetbundle.com/#org','name':'Meet Bundle','url':'https://meetbundle.com/','logo':'https://meetbundle.com/icon-512.png','email':'support@meetbundle.com','contactPoint':{'@type':'ContactPoint','contactType':'customer support','email':'support@meetbundle.com'}},
   {'@type':'WebSite','@id':'https://meetbundle.com/#website','name':'Meet Bundle','alternateName':'Bundle','url':'https://meetbundle.com/','publisher':{'@id':'https://meetbundle.com/#org'},'inLanguage':[HREFLANG.get(c,c) for c in LANGS]},
   {'@type':'MobileApplication','name':'Meet Bundle','alternateName':'Bundle - Dating & Connections','operatingSystem':'Android, iOS','applicationCategory':'LifestyleApplication','applicationSubCategory':'Dating','description':re.sub(r'(?<!Meet )\bBundle\b','Meet Bundle',desc),'url':home,'inLanguage':lang,'image':'https://meetbundle.com/og.png','publisher':{'@id':'https://meetbundle.com/#org'},'offers':{'@type':'Offer','price':'0','priceCurrency':'USD'}},
   {'@type':'FAQPage','inLanguage':lang,'mainEntity':[{'@type':'Question','name':t(q),'acceptedAnswer':{'@type':'Answer','text':' '.join(t(a) for a in ans)}} for q,ans in FAQ]}]
  return '<script type="application/ld+json">'+json.dumps({'@context':'https://schema.org','@graph':g},ensure_ascii=False).replace('</','<\\/')+'</script>'
SW=('<!--i18n--><label class="langsw"><span class="sr">%LABEL%</span>'
 '<svg width="18" height="18" viewBox="0 0 24 24" aria-hidden="true"><g fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.5 2.7 3.8 5.7 3.8 9s-1.3 6.3-3.8 9c-2.5-2.7-3.8-5.7-3.8-9S9.5 5.7 12 3Z"/></g></svg>'
 '<select onchange="bundleLang(this.value)">%OPTS%</select></label>'
 '<script>function bundleLang(v){try{localStorage.setItem(\'bundle-lang\',v)}catch(e){}var p=location.pathname.replace(/^\\/(%RE%)(?=\\/)/,\'\');location.href=(v===\'en\'?\'\':\'/\'+v)+p+location.hash}</script>'
 '<style>.langsw{position:relative;display:inline-flex;align-items:center;gap:6px;color:inherit;min-height:44px;padding:0 8px}.langsw select{background:transparent;color:inherit;border:1px solid currentColor;border-radius:999px;padding:6px 10px;font:inherit;font-size:14px;min-height:36px;opacity:.85}.langsw select option{color:#000}.sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}</style><!--/i18n-->')
class X(HTMLParser):
  def __init__(s):super().__init__();s.skip=0;s.out=[]
  def handle_starttag(s,t,a):
    if t in('script','style','svg'):s.skip+=1
    d=dict(a)
    for k in ATTR:
      if d.get(k) and re.search('[A-Za-z]',d[k]):s.out.append(d[k])
    if t=='meta' and (d.get('name')=='description' or d.get('property') in('og:title','og:description','og:image:alt')):s.out.append(d['content'])
  def handle_endtag(s,t):
    if t in('script','style','svg'):s.skip-=1
  def handle_data(s,d):
    if not s.skip and d.strip() and re.search('[A-Za-z]',d):s.out.append(d.strip())
def extract():
  out=[]
  for f in PAGES:
    p=X();p.feed(re.sub(r'<!--i18n-->.*?<!--/i18n-->','',open(os.path.join(DOCS,f)).read(),flags=re.S));out+=p.out
  u=[x for x in dict.fromkeys(out+JS) if x not in SKIP]
  return u
def url(code,path):return path if code=='en' else '/'+code+path
def translate(src,M):
  parts=re.split(r'(<script\b.*?</script>|<style\b.*?</style>|<svg\b.*?</svg>)',src,flags=re.S)
  for i in range(0,len(parts),2):
    p=parts[i]
    p=re.sub(r'(^|>)(\s*)([^<]+?)(\s*)(?=<|$)',lambda m:m[1]+m[2]+(html.escape(M[html.unescape(m[3])],quote=False) if html.unescape(m[3]) in M else m[3])+m[4],p)
    p=re.sub(r'\b(alt|aria-label|placeholder|data-ok|data-mail|content)="([^"]*)"',lambda m:m[1]+'="'+(html.escape(M[html.unescape(m[2])]) if html.unescape(m[2]) in M else m[2])+'"',p)
    parts[i]=p
  return ''.join(parts)
def page_path(f):return '/' if f=='index.html' else ('/404.html' if f=='404.html' else '/'+f[:-len('index.html')])
def build():
  cur=extract();ef=os.path.join(I,'en.json')
  prev=json.load(open(ef)) if os.path.exists(ef) else []
  en=prev+[x for x in cur if x not in prev]  # stable order: new strings are appended
  json.dump(en,open(ef,'w'),ensure_ascii=False,indent=0)
  avail=['en']+[c for c in LANGS if c!='en' and os.path.exists(os.path.join(I,c+'.json'))]
  opts=''.join(f'<option value="{c}">{LANGS[c][0]}</option>' for c in avail)
  for code in avail:
    if code!='en':
      T=json.load(open(os.path.join(I,code+'.json')))
      if isinstance(T,list):
        fx=lambda t:re.sub(r'(?<!Meet )\bBundle\b','Meet Bundle',t)
        for i in range(len(T),len(en)):  # auto-derive trademark variants of existing strings
          j=next((j for j in range(len(T)) if fx(en[j])==en[i] and en[j]!=en[i]),None)
          if j is None:break
          T.append(fx(T[j]))
        assert len(T)==len(en),(code,len(T),len(en));T={str(i):v for i,v in enumerate(T)}
      M={e:T[str(k)] for k,e in enumerate(en) if str(k) in T and T[str(k)].strip()}
      miss=[k for k in range(len(en)) if str(k) not in T];
      if miss:print(code,'missing',len(miss),miss[:10])
    for f in PAGES:
      src=open(os.path.join(DOCS,f)).read()
      src=re.sub(r'\n?<!--i18n-->.*?<!--/i18n-->','',src,flags=re.S)  # strip previous injections on en
      pp=page_path(f)
      name,d,fam,hf,bf,loc=LANGS[code]
      alt='' if f=='404.html' else ''.join(f'<link rel="alternate" hreflang="{HREFLANG.get(c,c)}" href="https://meetbundle.com{url(c,pp)}">' for c in avail)+f'<link rel="alternate" hreflang="x-default" href="https://meetbundle.com{pp}">'
      det='' if code!='en' else '<script>(function(){try{var s=localStorage.getItem("bundle-lang");if(s)return}catch(e){}var A=%s,L=(navigator.languages||[navigator.language||""]);for(var i=0;i<L.length;i++){var l=(L[i]||"").toLowerCase(),c=l.split("-")[0];if(c==="iw")c="he";if(c==="en")return;if(A.indexOf(c)>-1){location.replace("/"+c+location.pathname+location.search+location.hash);return}}})();</script>'%json.dumps([c for c in avail if c!='en'])
      font=''
      if fam:font=f'<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family={fam}&display=swap"><style>:root{{--head:"{hf}",system-ui,sans-serif!important;--body:"{bf}",system-ui,sans-serif!important}}body,h1,h2,h3,.hd h1,.eyebrow,.btn,input,select,textarea{{font-family:var(--body)}}h1,h2,h3{{font-family:var(--head)}}</style>'
      rtl='<style>[dir=rtl] .phone,[dir=rtl] .shot-img{direction:ltr}[dir=rtl] ol.steps,[dir=rtl] ul{padding-inline-start:20px;padding-left:0}[dir=rtl] #prev svg{transform:scaleX(-1)}[dir=rtl] #next svg{transform:none!important}[dir=rtl] .h2,[dir=rtl] h1,[dir=rtl] h2{letter-spacing:0}</style>' if d=='rtl' else ''
      i18njs='' if code=='en' else '<script>window.I18N=%s</script>'%json.dumps({k:M.get(k,k) for k in JS},ensure_ascii=False)
      ld='' if f!='index.html' else jsonld(code,({} if code=='en' else M),(M.get(en[1],en[1]) if code!='en' else en[1]))
      head_inj=f'\n<!--i18n-->{alt}{det}{font}{rtl}{i18njs}{ld}<!--/i18n-->'
      sel=opts.replace('value="%s"'%code,'value="%s" selected'%code)
      langre='|'.join(c for c in avail if c!='en')
      label='Language' if code=='en' else M.get('Language','Language')
      sw=SW.replace('%LABEL%',label).replace('%RE%',langre).replace('%OPTS%',sel)
      out=src
      if code!='en':
        out=translate(out,M)
        out=out.replace('<html lang="en">',f'<html lang="{HREFLANG.get(code,code)}" dir="{d}">')
        if '<html' not in out[:200]:out=out
        for r in ROUTES:out=out.replace(f'href="{r}"',f'href="/{code}{r}"').replace(f'href="https://meetbundle.com{r}"',f'href="https://meetbundle.com/{code}{r}"')
        out=out.replace('href="/"',f'href="/{code}/"').replace('href="/#',f'href="/{code}/#').replace('href="#download"','href="#download"')
        out=out.replace('<link rel="canonical" href="https://meetbundle.com/">',f'<link rel="canonical" href="https://meetbundle.com/{code}/">').replace('content="https://meetbundle.com/"',f'content="https://meetbundle.com/{code}/"')
        out=re.sub(r'<meta property="og:url" content="https://meetbundle.com(/[^"]*)">',lambda m:f'<meta property="og:url" content="https://meetbundle.com{m[1] if m[1].startswith("/"+code+"/") else "/"+code+m[1]}">',out)
        out=out.replace('<meta property="og:type"',f'<meta property="og:locale" content="{loc}">\n<meta property="og:type"',1)
        out=out.replace('<meta name="robots" content="noindex">','<meta name="robots" content="noindex">')
      out=brand(out.replace('<meta property="og:site_name" content="Bundle">','<meta property="og:site_name" content="Meet Bundle">'))
      if f=='index.html':out=re.sub(r'<title>.*?</title>','<title>Meet Bundle - Dating &amp; Connections</title>',out,count=1)
      if f=='404.html':out=re.sub(r'<link rel="canonical"[^>]*>\n?','',out)
      # inject head + switcher
      out=out.replace('</head>',head_inj+'\n</head>',1) if '</head>' in out else out.replace('</title>','</title>'+head_inj,1)
      out=re.sub(r'(<footer>.*?)(</div></footer>)',lambda m:m[1]+sw+m[2],out,count=1,flags=re.S)
      dst=os.path.join(DOCS,f) if code=='en' else os.path.join(DOCS,code,f)
      os.makedirs(os.path.dirname(dst),exist_ok=True)
      if code=='en':open(dst,'w').write(out)
      else:open(dst,'w').write(out)
  # sitemap
  sm=['<?xml version="1.0" encoding="UTF-8"?>','<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
  for pp in ['/']+ROUTES:
    for c in avail:
      sm.append(f'  <url><loc>https://meetbundle.com{url(c,pp)}</loc>'+''.join(f'<xhtml:link rel="alternate" hreflang="{HREFLANG.get(o,o)}" href="https://meetbundle.com{url(o,pp)}"/>' for o in avail)+'</url>')
  sm.append('</urlset>');open(os.path.join(DOCS,'sitemap.xml'),'w').write('\n'.join(sm)+'\n')
  print('built',avail,len(en),'strings')
if __name__=='__main__':build()
