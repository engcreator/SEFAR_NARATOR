import json
from pathlib import Path
import re
import streamlit as st


st.set_page_config(page_title="SEFAR NARATOR V1.1", page_icon="🌿", layout="wide")
st.markdown('''<style>
.stApp{background:linear-gradient(180deg,#f8fbf5,#fff 60%,#f0f7ef)}
.block-container{max-width:1360px;padding-top:1.2rem}
.hero,.card,.result{background:#fff;border:1px solid #dce8da;border-radius:20px;padding:22px;box-shadow:0 7px 24px rgba(25,60,40,.06);margin-bottom:16px}
.hero{background:linear-gradient(120deg,#fff,#eaf5e5)}
.storypanel{border-left:6px solid #9b7848}.sciencepanel{border-left:6px solid #2a9d8f}.activitypanel{border-left:6px solid #e76f51}.audio{background:#f2efff;border-left:5px solid #8064b5;border-radius:10px;padding:13px 15px;margin:10px 0}
@media(max-width:700px){.block-container{padding:.7rem}.hero,.card,.result{padding:15px}}
.title{font-size:clamp(2rem,4vw,3rem);font-weight:850;color:#193329}.tagline{color:#356744;font-weight:650;margin-top:7px}.version{color:#718077;font-size:.85rem}
.section{font-size:1.3rem;font-weight:800;color:#285d3c;margin:16px 0 10px}.small{color:#6d7d72;font-size:.9rem}
.badge{display:inline-block;background:#e7f3e2;color:#356744;border-radius:999px;padding:5px 10px;margin:2px 4px 6px 0;font-size:.78rem;font-weight:750}
.story{white-space:pre-line;font-size:1.06rem;line-height:1.8;color:#26382d}.fact{background:#eff8ec;border-left:5px solid #4f8f45;border-radius:10px;padding:13px 15px;margin:10px 0}.lesson{background:#fbf4e8;border-left:5px solid #9b7848;border-radius:10px;padding:13px 15px;margin:10px 0}
.flow{display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin:8px 0 18px}.step{background:#edf6e9;color:#285d3c;border:1px solid #d4e6cf;border-radius:999px;padding:7px 12px;font-size:.82rem;font-weight:750}
.note{background:#eef5ff;border-left:5px solid #5c8fd8;border-radius:10px;padding:13px 15px;margin:10px 0}
.rtl{direction:rtl;text-align:right}.choicebox{background:#fff;border:1px solid #d9e8d5;border-radius:14px;padding:14px;margin:10px 0}.choicebox b{color:#285d3c}.langbox{background:#eef5ff;border-left:5px solid #5c8fd8;border-radius:10px;padding:12px 15px;margin:8px 0}

/* V1.0 structured colored compartments */
.compartment-title{display:flex;align-items:center;gap:9px;border-radius:12px;padding:10px 13px;margin:-2px 0 12px;font-weight:900;letter-spacing:.01em}
.compartment-title .num{display:grid;place-items:center;width:28px;height:28px;border-radius:50%;background:rgba(255,255,255,.78);font-size:.8rem}
.compartment-hint{font-size:.82rem;color:#56665c;margin:-5px 0 10px}
.compartment-audience{background:#eef8ee;border:2px solid #79ad70}
.compartment-explore{background:#fff3e5;border:2px solid #e2a45c}
.compartment-experience{background:#eef5ff;border:2px solid #719ddd}
.compartment-language{background:#f0edff;border:2px solid #8a76c8}
.compartment-create{background:#fff7df;border:2px solid #d5a83d}
.compartment-profile{background:#eef8f7;border:2px solid #55a59b}
.compartment-actions{background:#fff0ec;border:2px solid #df806b}
/* Strong visual separation for Streamlit bordered containers */
div[data-testid="stVerticalBlockBorderWrapper"]{border-radius:18px!important;box-shadow:0 5px 18px rgba(30,55,40,.055)!important;background:rgba(255,255,255,.72)}

/* V0.9 responsive/accessibility layer */
:focus-visible{outline:3px solid #2f6f45!important;outline-offset:2px}
button,.stButton>button{min-height:44px}
.stSelectbox label,.stRadio label,.stTextInput label{font-weight:700}
@media(max-width:900px){.block-container{padding-left:.8rem;padding-right:.8rem}.hero{border-radius:16px}.story{font-size:1rem;line-height:1.7}}
@media(max-width:700px){.block-container{padding:.55rem}.hero,.card,.result{padding:14px;border-radius:14px}.title{font-size:2rem}.section{font-size:1.15rem}.flow{gap:5px}.step{font-size:.74rem;padding:6px 9px}.story{font-size:.98rem;line-height:1.65}.badge{font-size:.72rem}}
@media print{.stSidebar,.stButton,.stSelectbox,.stRadio,.stTextInput{display:none!important}.block-container{max-width:none}.hero,.card,.result{box-shadow:none;border:1px solid #bbb}.story{font-size:12pt}}

/* V0.9.5 adaptive storytelling visual system */
.story-experience{--accent:#4f8f45;--accent2:#dfeeda;--deep:#244c38;--surface:#fff;--glow:#eef8ea;position:relative;overflow:hidden;border-radius:28px;padding:28px;margin:24px 0 18px;background:linear-gradient(135deg,var(--surface),var(--glow));border:1px solid var(--accent2);box-shadow:0 16px 45px rgba(20,45,30,.10)}
.story-experience:before,.story-experience:after{content:"";position:absolute;border-radius:50%;pointer-events:none;opacity:.28}.story-experience:before{width:220px;height:220px;right:-70px;top:-90px;background:var(--accent2)}.story-experience:after{width:150px;height:150px;left:-60px;bottom:-75px;background:var(--accent)}
.story-hero{position:relative;z-index:1;display:flex;align-items:center;gap:18px;padding:6px 4px 20px}.subject-orb{width:92px;height:92px;min-width:92px;border-radius:50%;display:grid;place-items:center;font-size:3.25rem;background:linear-gradient(145deg,#fff,var(--accent2));box-shadow:inset 0 0 0 6px rgba(255,255,255,.75),0 12px 28px rgba(20,45,30,.12)}
.story-kicker{font-size:.78rem;text-transform:uppercase;letter-spacing:.12em;font-weight:800;color:var(--accent)}.story-title{font-size:clamp(1.9rem,3.6vw,2.85rem);line-height:1.05;color:var(--deep);font-weight:900;margin:5px 0 8px}.story-subtitle{color:#52665a;font-size:1rem;margin:0;max-width:800px}.story-nav{position:relative;z-index:1;display:flex;gap:8px;flex-wrap:wrap;margin-bottom:8px}.story-chip{display:inline-block;border-radius:999px;padding:6px 11px;background:rgba(255,255,255,.82);border:1px solid var(--accent2);color:var(--deep);font-size:.78rem;font-weight:800}
.adaptive-card{position:relative;border-radius:20px;padding:22px;margin:14px 0;background:rgba(255,255,255,.95);border:1px solid var(--accent2);box-shadow:0 8px 25px rgba(20,45,30,.06)}.adaptive-card h2,.adaptive-card h3{color:var(--deep)}.adaptive-story{border-top:5px solid var(--accent)}.adaptive-science{border-top:5px solid #2a9d8f}.adaptive-activity{border-top:5px solid #e76f51}.visual-caption{text-align:center;color:#66766d;font-size:.85rem;margin-top:8px}
@media(max-width:700px){.story-experience{padding:18px;border-radius:20px}.story-hero{gap:14px;padding-bottom:18px}.subject-orb{width:78px;height:78px;min-width:78px;font-size:2.8rem}.story-title{font-size:2rem}.adaptive-card{padding:16px;border-radius:16px}}

/* Restored V1.0 Storybook proportions: compact characters, readable story width, and controlled paragraph size */
.storybook-layout{display:grid;grid-template-columns:minmax(0,1fr) 270px;gap:18px;align-items:start;margin:16px 0 20px}
.storybook-main{background:#fffdf8;border:1px solid #eadfce;border-radius:20px;padding:26px 30px 22px;box-shadow:0 10px 28px rgba(80,60,35,.07);border-top:5px solid var(--accent)}
.storybook-main h2{font-family:Georgia,'Times New Roman',serif;font-size:1.7rem;line-height:1.2;margin:0 0 20px;color:#3f513f}
.story-text{font-family:Georgia,'Times New Roman',serif;font-size:1.08rem;line-height:1.78;color:#344238}
.story-text p{max-width:58ch;margin:0 auto 1.05em}
.story-text p:first-child:first-letter{font-size:2.5em;float:left;line-height:.82;padding-right:7px;padding-top:4px;font-weight:700;color:var(--accent)}
.storybook-note{margin:16px auto 0;max-width:58ch;padding:11px 13px;border-left:4px solid var(--accent);background:#f6f1e7;border-radius:8px;color:#687267;font-size:.82rem;line-height:1.5}
.storybook-result{position:sticky;top:14px;background:#f3f8f0;border:1px solid #d7e5d1;border-radius:18px;padding:18px 16px;box-shadow:0 8px 22px rgba(45,80,45,.06)}
.storybook-result h3{font-family:Georgia,'Times New Roman',serif;font-size:1.05rem;line-height:1.3;color:#31563a;margin:0 0 13px}
.result-item{padding:9px 0;border-bottom:1px solid #dce7d8}.result-item:last-child{border-bottom:0}.result-label{display:block;font-size:.68rem;text-transform:uppercase;letter-spacing:.08em;color:#718071;font-weight:800}.result-value{display:block;font-size:.86rem;color:#304735;font-weight:700;margin-top:2px}
@media(max-width:900px){.storybook-layout{grid-template-columns:1fr}.storybook-result{position:static;order:-1}.storybook-main{padding:22px 24px}.story-text{font-size:1.05rem}.story-text p{max-width:56ch}}
@media(max-width:700px){.storybook-main{padding:18px 17px}.storybook-main h2{font-size:1.45rem}.story-text{font-size:1rem;line-height:1.7}.story-text p{max-width:100%;margin-bottom:1em}.storybook-result{padding:15px}.storybook-note{max-width:100%}}

/* V1.1 Public Launch landing page */
.landing-shell{max-width:1240px;margin:0 auto;padding:8px 0 42px}
.landing-topbar{display:flex;align-items:center;justify-content:space-between;padding:5px 6px 18px;color:#315b43}.landing-brand{font-family:Georgia,'Times New Roman',serif;font-size:1.05rem;font-weight:900;letter-spacing:.04em}.landing-brand span{color:#b07b1c}.landing-topnote{font-size:.78rem;font-weight:750;color:#718077}
.landing-hero{position:relative;overflow:hidden;border-radius:34px;padding:58px 56px 50px;background:linear-gradient(118deg,#143d2a 0%,#286342 47%,#a77922 128%);box-shadow:0 24px 65px rgba(23,63,44,.20);color:white;margin-bottom:18px;min-height:455px}
.landing-hero:before{content:"";position:absolute;width:520px;height:520px;border-radius:50%;right:-155px;top:-205px;background:rgba(255,255,255,.10)}.landing-hero:after{content:"";position:absolute;width:360px;height:360px;border-radius:50%;left:-165px;bottom:-205px;background:rgba(255,255,255,.065)}
.landing-content{position:relative;z-index:3;max-width:720px}.landing-kicker{display:inline-flex;align-items:center;gap:7px;padding:7px 12px;border:1px solid rgba(255,255,255,.35);border-radius:999px;background:rgba(255,255,255,.10);font-size:.75rem;font-weight:850;letter-spacing:.11em;text-transform:uppercase}
.landing-title{font-family:Georgia,'Times New Roman',serif;font-size:clamp(3.15rem,6.3vw,5.8rem);line-height:.91;margin:20px 0 18px;font-weight:900;letter-spacing:-.045em}.landing-title span{color:#ffd878}.landing-lead{font-size:clamp(1.05rem,2vw,1.32rem);line-height:1.62;color:rgba(255,255,255,.93);max-width:700px;margin-bottom:19px}.landing-sublead{font-size:.91rem;color:rgba(255,255,255,.73);max-width:610px;line-height:1.55}
.landing-promise{display:flex;gap:8px;flex-wrap:wrap;margin:19px 0 0}.landing-pill{padding:8px 11px;border-radius:999px;background:rgba(255,255,255,.13);border:1px solid rgba(255,255,255,.22);font-size:.8rem;font-weight:750}
.landing-art{position:absolute;right:25px;bottom:10px;width:min(41%,465px);height:355px;display:grid;place-items:center;opacity:.99;z-index:2}.landing-art .book{font-size:7.4rem;filter:drop-shadow(0 14px 18px rgba(0,0,0,.23));position:relative;z-index:2}.landing-art .bee{position:absolute;right:14%;top:10%;font-size:4.1rem}.landing-art .owl{position:absolute;left:7%;top:18%;font-size:4.35rem}.landing-art .fox{position:absolute;right:2%;bottom:6%;font-size:4.9rem}.landing-art .tree{position:absolute;left:2%;bottom:-2px;font-size:7.3rem;opacity:.92}
.landing-micro{display:flex;justify-content:center;gap:18px;flex-wrap:wrap;color:#66766d;font-size:.78rem;font-weight:700;margin:13px 0 26px}.landing-micro span{display:inline-flex;align-items:center;gap:5px}
.landing-section-title{font-family:Georgia,'Times New Roman',serif;text-align:center;font-size:2.05rem;color:#244c38;margin:35px 0 7px}.landing-section-lead{text-align:center;color:#627267;max-width:780px;margin:0 auto 20px;line-height:1.55}
.landing-feature{height:100%;background:#fff;border:1px solid #dce8da;border-radius:20px;padding:23px;box-shadow:0 8px 26px rgba(25,60,40,.06);transition:transform .15s ease}.landing-feature .icon{font-size:2rem}.landing-feature h3{color:#285d3c;margin:10px 0 7px}.landing-feature p{color:#607066;line-height:1.6;margin:0}
.landing-sample{background:linear-gradient(135deg,#fffdf7,#f0f7ef);border:1px solid #dce8da;border-radius:26px;padding:26px;box-shadow:0 10px 32px rgba(25,60,40,.06);margin-top:22px}.sample-kicker{text-transform:uppercase;letter-spacing:.12em;font-size:.72rem;font-weight:850;color:#6d7d72}.sample-title{font-family:Georgia,'Times New Roman',serif;font-size:1.8rem;font-weight:900;color:#285d3c;margin:6px 0}.sample-story{font-family:Georgia,'Times New Roman',serif;font-size:1.02rem;line-height:1.68;color:#34463b;max-width:60ch;margin-left:auto;margin-right:auto}.sample-fact{background:#eff8ec;border-left:5px solid #4f8f45;border-radius:10px;padding:12px 14px;color:#496056;font-size:.92rem;line-height:1.55}.sample-tags{display:flex;gap:7px;flex-wrap:wrap;margin-top:13px}.sample-tag{background:#fff;border:1px solid #dce8da;border-radius:999px;padding:6px 10px;font-size:.76rem;font-weight:800;color:#45634f}
.landing-flow{display:grid;grid-template-columns:repeat(5,1fr);gap:10px;margin:18px 0 10px}.landing-flow-step{background:#f7faf5;border:1px solid #dce8da;border-radius:16px;padding:15px 12px;text-align:center}.landing-flow-step b{display:block;color:#285d3c;margin-bottom:4px}.landing-flow-step span{font-size:.82rem;color:#718077}
.landing-vision{margin-top:26px;background:#173f2c;color:white;border-radius:25px;padding:28px 30px;text-align:center;box-shadow:0 12px 35px rgba(23,63,44,.12)}.landing-vision h3{font-family:Georgia,'Times New Roman',serif;font-size:1.7rem;margin:0 0 7px}.landing-vision p{color:rgba(255,255,255,.82);max-width:820px;margin:0 auto;line-height:1.65}.landing-bottom{margin-top:18px;background:linear-gradient(120deg,#f0f7ef,#fff8e8);border:1px solid #dce8da;border-radius:24px;padding:26px;text-align:center}.landing-bottom h3{font-family:Georgia,'Times New Roman',serif;color:#285d3c;font-size:1.55rem;margin:0 0 7px}.landing-bottom p{color:#65756a;margin:0 auto 16px;max-width:760px}
@media(max-width:900px){.landing-hero{padding:42px 30px;min-height:0}.landing-art{position:relative;right:auto;bottom:auto;width:100%;height:190px;margin:12px auto -8px}.landing-art .book{font-size:5rem}.landing-art .tree{font-size:5rem}.landing-art .owl{font-size:3rem}.landing-art .fox{font-size:3.4rem}.landing-art .bee{font-size:2.8rem}.landing-flow{grid-template-columns:1fr 1fr}}
@media(max-width:600px){.landing-topbar{padding-bottom:11px}.landing-topnote{display:none}.landing-hero{padding:32px 22px;border-radius:22px}.landing-title{font-size:2.85rem}.landing-lead{font-size:1rem}.landing-flow{grid-template-columns:1fr}.landing-section-title{font-size:1.6rem}.landing-sample{padding:20px;border-radius:20px}.landing-vision{padding:23px 18px}}

</style>''', unsafe_allow_html=True)

stories=json.loads((Path(__file__).parent/'data'/'stories.json').read_text(encoding='utf-8'))
by_subject={s['subject']:s for s in stories}
AGES={
 '4–6 years':('Little explorers','Simple language, short sections, pictures, audio, and playful discovery.'),
 '7–12 years':('Curious minds','Imaginative stories, nature facts, questions, and exploration.'),
 '13–16 years':('Growing together','Deeper narratives, ethics, science, relationships, and reflection.'),
 '17–20 years':('Building tomorrow','Science, society, sustainability, and independent exploration.'),
 '20+ years':('Lifelong learning','Detailed stories, documentaries, scientific context, and perspectives.'),
 'Group / Classroom':('Shared discovery','Facilitator-led stories, activities, discussion, and assessment.')}
PROFILES=['Parent','Teacher','Educator','Student','Individual visitor','Researcher / Professional','Other']
LANGUAGES=['English','Français','العربية']

# V0.8 multilingual content layer. English remains the reference version in stories.json;
# French and Arabic provide real localized story content instead of translating only the interface.
LOCALIZED={
'Français':{
'Honey Bee':("Le jardin qui avait besoin des abeilles","Dans le jardin de Lina, les abeilles butinent les fleurs en transportant involontairement du pollen d'une fleur à l'autre. Lina comprend peu à peu que les fruits, les fleurs, les insectes, le sol et les personnes forment un réseau vivant.",
["Les abeilles domestiques récoltent le nectar comme source d'énergie et le pollen comme ressource nutritive.","La pollinisation aide de nombreuses plantes à produire des graines et des fruits.","Les abeilles ouvrières sont des femelles qui butinent et entretiennent la colonie."],"Les pollinisateurs relient les plantes, les animaux et les humains. Protéger leur habitat aide tout l'écosystème.",["Pourquoi la pollinisation est-elle importante ?","Comment un jardin peut-il aider les pollinisateurs ?","Quelle différence y a-t-il entre l'histoire imaginaire et les faits scientifiques ?"]),
'Eurasian Jay':("Le geai et les secrets de la forêt","Un geai des chênes explore la forêt, cache des graines et revient parfois vers les endroits qu'il a mémorisés. Son comportement montre comment un oiseau peut participer à la dispersion des graines et à la dynamique de la forêt.",["Le geai des chênes appartient à la famille des corvidés.","Il consomme notamment des glands et peut transporter ou cacher des graines.","Les graines oubliées peuvent contribuer à la régénération de la végétation."],"Un animal peut influencer son environnement tout en dépendant de celui-ci.",["Quel rôle le geai peut-il jouer dans la dispersion des graines ?","Pourquoi les corvidés sont-ils intéressants à observer ?"]),
'Oak Tree':("Le vieux chêne et la forêt vivante","Un vieux chêne semble immobile, mais ses branches, ses feuilles, ses racines et son écorce abritent une multitude d'organismes. Au fil des saisons, il devient un véritable habitat vivant.",["Les chênes fournissent nourriture et abri à de nombreuses espèces.","Leurs glands sont consommés par plusieurs animaux.","Les arbres participent aux cycles du carbone, de l'eau et des nutriments."],"Un arbre est aussi une infrastructure écologique : il crée des ressources pour de nombreuses espèces.",["Quelles espèces peuvent dépendre d'un chêne ?","Pourquoi un arbre âgé peut-il avoir une grande valeur écologique ?"]),
'Barn Owl':("La chouette qui chasse dans la nuit","À la tombée de la nuit, une chouette effraie quitte son refuge. Elle vole silencieusement au-dessus des champs et écoute attentivement les petits mouvements au sol avant de plonger.",["La chouette effraie est un rapace nocturne.","Son vol est particulièrement silencieux grâce à la structure de ses plumes.","Elle se nourrit principalement de petits mammifères dans de nombreuses régions."],"Les adaptations d'un animal correspondent souvent aux défis de son environnement.",["Pourquoi le silence est-il utile à une chouette nocturne ?","Comment ses sens l'aident-ils à chasser ?"]),
'Red Fox':("Le renard et la frontière de la ville","À la tombée de la nuit, un renard roux traverse discrètement un paysage où se rencontrent champs, jardins et habitations. Il adapte ses déplacements aux ressources et aux risques de cet environnement partagé.",["Le renard roux est un mammifère très adaptable.","Son régime alimentaire est varié et peut changer selon les ressources disponibles.","Il peut vivre dans des paysages ruraux, forestiers et parfois urbains."],"La coexistence avec la faune sauvage demande de comprendre les besoins des animaux et les effets de nos aménagements.",["Pourquoi le renard est-il considéré comme adaptable ?","Quels risques une ville peut-elle créer pour la faune ?"]),
'African Elephant':("La mémoire de la savane","Dans la savane, un groupe d'éléphants avance vers une zone où l'eau est disponible. Les plus expérimentés semblent guider le déplacement du groupe, tandis que les jeunes restent proches des adultes.",["Les éléphants d'Afrique vivent en groupes sociaux complexes.","Les femelles adultes jouent un rôle important dans la cohésion du groupe.","Les éléphants modifient aussi leur environnement en consommant et en déplaçant de la végétation."],"Les relations sociales et la connaissance du paysage peuvent être essentielles à la survie d'une espèce.",["Pourquoi les groupes d'éléphants sont-ils importants ?","Comment les éléphants transforment-ils leur habitat ?"]),
'Bottlenose Dolphin':("Les dauphins de la baie","Sous la surface, un groupe de grands dauphins se déplace ensemble. Ils utilisent des sons et des signaux corporels pour communiquer et coordonner leurs activités.",["Les grands dauphins utilisent l'écholocation pour explorer leur environnement.","Ils vivent souvent en groupes sociaux variables.","Leurs comportements comprennent la coopération et des interactions sociales complexes."],"La communication permet à de nombreux animaux sociaux de coordonner leurs comportements.",["À quoi sert l'écholocation ?","Pourquoi la vie en groupe peut-elle être avantageuse ?"]),
'Green Sea Turtle':("Le long voyage de la tortue verte","Une tortue verte nage dans l'océan puis revient vers une zone côtière favorable à la reproduction. Son cycle de vie relie les écosystèmes marins et côtiers.",["Les tortues vertes sont des reptiles marins.","Elles utilisent plusieurs habitats au cours de leur vie.","La perte des plages et les activités humaines en mer peuvent affecter leurs populations."],"Protéger une espèce migratrice signifie protéger plusieurs habitats connectés.",["Pourquoi une tortue a-t-elle besoin de plusieurs habitats ?","Quels dangers peuvent affecter les tortues marines ?"]),
'Monarch Butterfly':("Le voyage du monarque","Un papillon monarque commence un long déplacement saisonnier. Son voyage relie plusieurs régions et dépend de plantes hôtes, de fleurs et de conditions météorologiques favorables.",["Les chenilles monarques se nourrissent principalement de plantes du genre Asclepias.","Certaines populations effectuent de longues migrations saisonnières.","La disponibilité des plantes et la qualité des habitats influencent leur cycle de vie."],"Une petite espèce peut dépendre d'un réseau d'habitats très vaste.",["Pourquoi les plantes hôtes sont-elles importantes ?","Comment la migration relie-t-elle différents écosystèmes ?"]),
},
'العربية':{
'Honey Bee':("الحديقة التي احتاجت إلى النحل","في حديقة لينا، تزور نحلات العسل الأزهار وتنقل حبوب اللقاح من زهرة إلى أخرى دون قصد. تكتشف لينا أن الثمار والأزهار والحشرات والتربة والإنسان تشكل شبكة حية مترابطة.",["يجمع نحل العسل الرحيق كمصدر للطاقة وحبوب اللقاح كمصدر للعناصر الغذائية.","يساعد التلقيح كثيراً من النباتات على إنتاج البذور والثمار.","العاملات إناث تجمع الغذاء وتعتني بالخلية."],"يربط الملقحات بين النباتات والحيوانات والإنسان. وحماية موائلها تساعد النظام البيئي كله.",["لماذا يعد التلقيح مهماً؟","كيف يمكن للحديقة أن تساعد الملقحات؟","ما الفرق بين أحداث القصة والحقائق العلمية؟"]),
'Eurasian Jay':("القيق الأوراسي وأسرار الغابة","يتنقل طائر القيق الأوروبي بين أشجار الغابة، ويخزن بعض البذور ثم يعود أحياناً إلى الأماكن التي يتذكرها. يوضح سلوكه كيف يمكن لطائر واحد أن يساهم في انتشار البذور وتجدد الغابة.",["ينتمي القيق الأوروبي إلى فصيلة الغرابيات.","يتغذى على الجوز وموارد غذائية أخرى، وقد ينقل البذور أو يخزنها.","يمكن للبذور التي لا يستعيدها الطائر أن تساهم في تجدد الغطاء النباتي."],"يمكن للحيوان أن يؤثر في بيئته، وفي الوقت نفسه يعتمد عليها.",["ما دور القيق في انتشار البذور؟","لماذا تستحق الغرابيات المراقبة والدراسة؟"]),
'Oak Tree':("البلوط العجوز والغابة الحية","يبدو البلوط العجوز ثابتاً، لكن أغصانه وأوراقه وجذوره ولحاؤه توفر موارد وملاجئ لكائنات كثيرة. ومع تعاقب الفصول يصبح الشجرة موطناً حياً متكاملاً.",["توفر أشجار البلوط الغذاء والمأوى لعدد كبير من الأنواع.","تتغذى حيوانات عديدة على ثمار البلوط.","تشارك الأشجار في دورات الكربون والماء والعناصر الغذائية."],"الشجرة ليست مجرد نبات؛ إنها بنية بيئية توفر موارد لأنواع كثيرة.",["ما الأنواع التي يمكن أن تعتمد على شجرة بلوط؟","لماذا قد تكون الشجرة القديمة ذات قيمة بيئية كبيرة؟"]),
'Barn Owl':("البومة التي تصطاد في الليل","مع حلول الليل تخرج بومة الحظائر من مخبئها. تحلق فوق الحقول بهدوء شديد، وتصغي إلى الحركات الصغيرة على الأرض قبل أن تهبط بسرعة.",["بومة الحظائر طائر جارح ليلي.","يساعدها تركيب ريشها على الطيران بهدوء.","تتغذى في مناطق كثيرة أساساً على الثدييات الصغيرة."],"تتوافق تكيفات الحيوان غالباً مع التحديات التي يفرضها موطنه.",["لماذا يفيد الهدوء البومة أثناء الصيد؟","كيف تساعدها حواسها على العثور على الفريسة؟"]),
'Red Fox':("الثعلب وحدود المدينة","مع حلول المساء يتحرك الثعلب الأحمر بحذر في منطقة تلتقي فيها الحقول والحدائق والمساكن. يغير مساراته وفق الموارد المتاحة والمخاطر في البيئة التي يشاركها مع الإنسان.",["الثعلب الأحمر من الثدييات القادرة على التكيف مع بيئات مختلفة.","غذاؤه متنوع ويمكن أن يتغير حسب الموارد المتاحة.","يمكن أن يعيش في المناطق الريفية والغابات وأحياناً في البيئات الحضرية."],"يتطلب التعايش مع الحياة البرية فهم احتياجات الحيوانات وتأثيرات أنشطتنا وتخطيطنا للبيئة.",["لماذا يعد الثعلب حيواناً متكيفاً؟","ما المخاطر التي قد تسببها المدن للحياة البرية؟"]),
'African Elephant':("ذاكرة السافانا","في السافانا تتحرك مجموعة من الفيلة نحو منطقة يتوفر فيها الماء. يبدو أن الأفراد الأكثر خبرة تساعد في توجيه المجموعة، بينما تبقى الصغار قريبة من البالغين.",["تعيش الفيلة الإفريقية في مجموعات اجتماعية معقدة.","تلعب الإناث البالغة دوراً مهماً في تماسك المجموعة.","تؤثر الفيلة في موطنها من خلال استهلاك ونقل النباتات."],"يمكن للعلاقات الاجتماعية ومعرفة المكان أن تكونا أساسيتين لبقاء النوع.",["لماذا تعد المجموعة مهمة للفيلة؟","كيف تغير الفيلة موطنها؟"]),
'Bottlenose Dolphin':("الدلافين في الخليج","تتحرك مجموعة من الدلافين قارورية الأنف معاً تحت سطح الماء. تستخدم الأصوات والإشارات الجسدية للتواصل وتنسيق سلوكها.",["تستخدم الدلافين قارورية الأنف تحديد الموقع بالصدى لاستكشاف البيئة.","تعيش غالباً في مجموعات اجتماعية متغيرة.","تشمل سلوكياتها التعاون والتفاعلات الاجتماعية المعقدة."],"يسمح التواصل لكثير من الحيوانات الاجتماعية بتنسيق سلوكها.",["ما فائدة تحديد الموقع بالصدى؟","لماذا قد تكون الحياة في مجموعة مفيدة؟"]),
'Green Sea Turtle':("رحلة السلحفاة الخضراء الطويلة","تسبح السلحفاة الخضراء في المحيط ثم تعود إلى منطقة ساحلية مناسبة للتكاثر. ويربط أسلوب حياتها بين الأنظمة البيئية البحرية والساحلية.",["السلاحف الخضراء زواحف بحرية.","تستخدم عدة موائل خلال مراحل حياتها.","يمكن لفقدان الشواطئ والأنشطة البشرية في البحر أن يؤثر في أعدادها."],"حماية نوع مهاجر تعني حماية عدة موائل مترابطة.",["لماذا تحتاج السلحفاة إلى أكثر من موطن؟","ما الأخطار التي تهدد السلاحف البحرية؟"]),
'Monarch Butterfly':("رحلة فراشة الملك","تبدأ فراشة الملك رحلة موسمية طويلة. ويربط سفرها بين مناطق مختلفة، ويعتمد على النباتات المضيفة والأزهار والظروف الجوية المناسبة.",["تتغذى يرقات فراشة الملك أساساً على نباتات الصقلاب.","تقوم بعض الجماعات بهجرات موسمية طويلة.","يؤثر توفر النباتات وجودة الموائل في دورة حياتها."],"قد يعتمد كائن صغير على شبكة واسعة من الموائل المتصلة.",["لماذا تعد النباتات المضيفة مهمة؟","كيف تربط الهجرة بين الأنظمة البيئية؟"]),
}}

# V1.0 localized addition for the Golden Eagle subject.
LOCALIZED['Français']['Golden Eagle']=(
    "L’aigle au-dessus des montagnes",
    "Un aigle royal plane au-dessus d’une vallée montagneuse. Il utilise les courants d’air ascendants pour gagner de l’altitude et observer le paysage. La scène narrative reste imaginaire, tandis que les informations scientifiques sont présentées séparément.",
    ["L’aigle royal est un grand rapace de la famille des Accipitridés.","Ses larges ailes lui permettent d’utiliser les courants ascendants pour planer efficacement.","Son alimentation comprend différents mammifères et autres animaux selon les régions et les ressources disponibles."],
    "Un prédateur appartient à un système écologique plus vaste : son habitat, ses proies et ses sites de nidification sont liés.",
    ["Comment le vol plané aide-t-il un grand rapace ?","Quels éléments du paysage peuvent être importants pour un aigle ?","Comment un prédateur dépend-il des autres espèces ?"]
)
LOCALIZED['العربية']['Golden Eagle']=(
    "النسر فوق الجبال",
    "يحلق النسر الذهبي فوق وادٍ جبلي، ويستفيد من تيارات الهواء الصاعدة ليرتفع ويستكشف المناظر الطبيعية من الأعلى. يبقى المشهد القصصي خيالياً، بينما تُعرض المعلومات العلمية بشكل منفصل.",
    ["النسر الذهبي من الطيور الجارحة الكبيرة وينتمي إلى فصيلة البازيات.","تساعده أجنحته العريضة على استخدام تيارات الهواء الصاعدة والتحليق بكفاءة.","يشمل غذاؤه ثدييات وحيوانات أخرى تختلف حسب المنطقة وتوفر الموارد."],
    "المفترس جزء من نظام بيئي أوسع؛ فموطنه وفرائسه ومواقع تعشيشه ترتبط ببقية عناصر البيئة.",
    ["كيف يساعد التحليق طائراً جارحاً كبيراً؟","ما عناصر الموطن المهمة للنسر؟","كيف يعتمد المفترس على الأنواع الأخرى؟"]
)

UI={
'English':{'audience':'Who is this experience for?','explore':'What do you want to explore?','experience':'How would you like to experience it?','language':'Language','start':'🌿 START EXPLORING','story':'Story','facts':'Nature & Science','discover':'What we discover','questions':'Questions & Activity','related':'Related discoveries','audio':'🔊 Audio-ready narration','prev':'← Previous chapter','next':'Next chapter →','create':'Create your age-specific experience','adapted':'Your adapted experience','category':'Category','subject':'Nature subject','mode':'Experience mode','format':'Format','depth':'Narrative depth','objective':'Educational or personal objective','reset':'Reset','save':'💾 Save this experience','activity':'Observation activity','activity_intro':'Choose the steps you want to complete after the story.','checks':['Observe the habitat or surroundings','Identify one relationship between living things','Write one scientific fact you learned','Separate one fictional element from one scientific fact']},
'Français':{'audience':'Pour qui cette expérience est-elle destinée ?','explore':'Que voulez-vous explorer ?','experience':'Comment souhaitez-vous vivre cette expérience ?','language':'Langue','start':'🌿 COMMENCER L’EXPLORATION','story':'Histoire','facts':'Nature et science','discover':'Ce que nous découvrons','questions':'Questions et activité','related':'Découvertes associées','audio':'🔊 Narration prête pour l’audio','prev':'← Chapitre précédent','next':'Chapitre suivant →','create':'Créer votre expérience adaptée à l’âge','adapted':'Votre expérience adaptée','category':'Catégorie','subject':'Sujet nature','mode':'Mode d’expérience','format':'Format','depth':'Profondeur narrative','objective':'Objectif éducatif ou personnel','reset':'Réinitialiser','save':'💾 Enregistrer cette expérience','activity':'Activité d’observation','activity_intro':'Choisissez les étapes que vous souhaitez réaliser après l’histoire.','checks':['Observer l’habitat ou les alentours','Identifier une relation entre des êtres vivants','Écrire un fait scientifique appris','Séparer un élément imaginaire d’un fait scientifique']},
'العربية':{'audience':'لمن هذه التجربة؟','explore':'ماذا تريد أن تستكشف؟','experience':'كيف تريد أن تعيش هذه التجربة؟','language':'اللغة','start':'🌿 ابدأ الاستكشاف','story':'القصة','facts':'الطبيعة والعلوم','discover':'ماذا نكتشف؟','questions':'أسئلة ونشاط','related':'اكتشافات مرتبطة','audio':'🔊 السرد جاهز للصوت','prev':'→ الفصل السابق','next':'الفصل التالي ←','create':'أنشئ تجربتك الملائمة للعمر','adapted':'تجربتك المكيّفة','category':'الفئة','subject':'موضوع الطبيعة','mode':'نمط التجربة','format':'الشكل','depth':'عمق السرد','objective':'الهدف التعليمي أو الشخصي','reset':'إعادة ضبط','save':'💾 حفظ هذه التجربة','activity':'نشاط الملاحظة','activity_intro':'اختر الخطوات التي تريد تنفيذها بعد القصة.','checks':['ملاحظة الموطن أو البيئة المحيطة','تحديد علاقة بين كائنات حية','كتابة حقيقة علمية تعلمتها','تمييز عنصر خيالي عن حقيقة علمية']}}

def localized_content(subject, language, audience):
    if language == 'English':
        v=by_subject[subject]['versions'][audience]
        return v['title'],v['story'],v['facts'],v['lesson'],v['questions']

    localized = LOCALIZED.get(language, {}).get(subject)
    if not localized:
        # Safe fallback: never replace the selected subject when a translation is absent.
        v = by_subject[subject]['versions'][audience]
        return v['title'], v['story'], v['facts'], v['lesson'], v['questions']
    title, base_story, facts, lesson, questions = localized
    # V0.8.1 content-parity layer: localized stories are adapted to the selected
    # audience instead of using one short text for every age group.
    if language == 'Français':
        adaptations = {
            '4–6 years': (
                "Imagine que tu accompagnes le personnage principal pendant une petite exploration. Observe les couleurs, les sons et les mouvements de la nature. Dans cette histoire, certains éléments sont imaginés pour raconter une aventure, tandis que les faits scientifiques restent réels.",
                "À la fin, demande-toi ce que tu as vu dans son habitat et comment tu pourrais protéger cet endroit."),
            '7–12 years': (
                "Au fil de l'exploration, le lecteur peut observer plusieurs indices sur la manière dont cet animal ou cette plante vit, se nourrit et interagit avec son environnement. L'histoire utilise l'imagination pour donner du mouvement aux personnages, mais les informations naturalistes sont présentées séparément afin de distinguer le récit des connaissances scientifiques.",
                "Cette découverte peut être prolongée par une observation de la nature près de chez toi : cherche un indice de présence, un habitat ou une interaction entre deux espèces."),
            '13–16 years': (
                "L'aventure permet aussi d'examiner les relations entre comportement, habitat et adaptation. Les intentions et les dialogues des personnages appartiennent à la fiction ; en revanche, les comportements biologiques mentionnés dans la partie scientifique correspondent aux connaissances naturalistes. Cette distinction aide à apprécier l'histoire sans confondre imagination et science.",
                "Réfléchis ensuite à la façon dont les changements de l'habitat, les activités humaines ou le climat pourraient modifier cette relation écologique."),
            '17–20 years': (
                "Cette version approfondit la lecture en reliant le récit à des notions d'écologie, d'adaptation et de coexistence. Le lecteur est invité à considérer l'animal ou la plante comme un élément d'un système plus vaste : ressources, prédateurs, partenaires, saisonnalité et activités humaines peuvent modifier les conditions de vie. Les éléments narratifs restent volontairement imaginaires.",
                "Pour aller plus loin, compare cette relation avec un autre écosystème et identifie les facteurs qui favorisent ou fragilisent sa stabilité."),
            '20+ years': (
                "Pour un lecteur adulte, le récit peut être lu comme une porte d'entrée vers une réflexion plus large sur les systèmes vivants. L'espèce présentée n'existe pas isolément : son comportement, son habitat et ses ressources s'inscrivent dans des interactions écologiques et, de plus en plus souvent, dans un environnement transformé par les activités humaines. La fiction sert ici à rendre ces relations concrètes sans remplacer l'information scientifique.",
                "Une lecture approfondie peut consister à rechercher une interaction réelle comparable, à examiner ses facteurs écologiques et à considérer les mesures de conservation ou de gestion qui pourraient la préserver."),
            'Group / Classroom': (
                "Cette histoire peut être utilisée comme point de départ pour une activité collective. Le groupe peut repérer les passages imaginaires, relever les informations scientifiques, puis discuter de la relation entre l'espèce, son habitat et les autres êtres vivants. Cette méthode permet de travailler à la fois la compréhension, l'esprit critique et l'observation du vivant.",
                "Pour conclure, chaque participant peut proposer une action simple permettant d'observer ou de protéger la biodiversité locale."),
        }
    else:
        adaptations = {
            '4–6 years': (
                "تخيّل أنك ترافق الشخصية الرئيسية في جولة صغيرة في الطبيعة. لاحظ الألوان والأصوات والحركات من حولها. بعض عناصر هذه الحكاية خيالية من أجل المتعة، بينما تبقى المعلومات العلمية واقعية وواضحة.",
                "في النهاية، حاول أن تتذكر موطن الكائن وفكّر في طريقة بسيطة لحماية هذا المكان."),
            '7–12 years': (
                "أثناء الاستكشاف، يمكن للقارئ ملاحظة دلائل مختلفة على طريقة عيش الكائن، وغذائه، وعلاقته بالبيئة المحيطة. تستخدم القصة الخيال لإعطاء الشخصيات صوتاً وحركة، لكن المعلومات الطبيعية والعلمية تُعرض بشكل منفصل حتى يبقى الفرق بين الحكاية والمعرفة واضحاً.",
                "يمكن متابعة الاكتشاف بمراقبة الطبيعة من حولك والبحث عن أثر لكائن حي أو موطن أو علاقة بين نوعين."),
            '13–16 years': (
                "تسمح هذه المغامرة أيضاً بفهم العلاقة بين السلوك والموطن والتكيف. أما الحوارات والنوايا المنسوبة إلى الشخصيات فهي جزء من الخيال، بينما تستند المعلومات البيولوجية في القسم العلمي إلى المعرفة الطبيعية. يساعد هذا الفصل على الاستمتاع بالقصة من دون الخلط بين الخيال والعلم.",
                "فكّر بعد ذلك في كيفية تأثير تغير الموطن أو الأنشطة البشرية أو المناخ في هذه العلاقة البيئية."),
            '17–20 years': (
                "تقدم هذه النسخة قراءة أعمق تربط الحكاية بمفاهيم علم البيئة والتكيف والتعايش. ويمكن النظر إلى الكائن باعتباره جزءاً من نظام أوسع تؤثر فيه الموارد والمفترسات والشركاء والفصول والأنشطة البشرية. وتبقى العناصر القصصية الخيالية واضحة ومقصودة.",
                "وللتوسع، قارن هذه العلاقة بعلاقة أخرى في نظام بيئي مختلف وحدد العوامل التي تساعدها على الاستمرار أو تجعلها أكثر هشاشة."),
            '20+ years': (
                "يمكن للقارئ البالغ أن ينظر إلى الحكاية بوصفها مدخلاً إلى فهم أوسع للأنظمة الحية. فالكائن لا يعيش بمعزل عن محيطه؛ إذ يرتبط سلوكه وموطنه وموارده بتفاعلات بيئية متعددة، وببيئات تتغير أيضاً بفعل الأنشطة البشرية. ويُستخدم الخيال هنا لجعل هذه العلاقات أكثر قرباً من القارئ من دون أن يحل محل المعرفة العلمية.",
                "وللتعمق، يمكن البحث عن علاقة حقيقية مشابهة ودراسة عواملها البيئية والتفكير في وسائل الحفاظ عليها."),
            'Group / Classroom': (
                "يمكن استخدام هذه القصة كنقطة انطلاق لنشاط جماعي. يستطيع المتعلمون تحديد الأجزاء الخيالية، واستخراج المعلومات العلمية، ثم مناقشة علاقة الكائن بموطنه وبالكائنات الأخرى. ويساعد ذلك على تنمية الفهم والتفكير النقدي وملاحظة الطبيعة.",
                "وفي الختام، يمكن لكل مشارك اقتراح عمل بسيط يساعد على مراقبة التنوع الحيوي المحلي أو حمايته."),
        }
    before, after = adaptations[audience]
    story = base_story.strip() + "\n\n" + before + "\n\n" + after
    return title, story, facts, lesson, questions

def apply_depth(story, facts, lesson, questions, depth, language):
    """Adjust presentation depth without deleting the core educational content."""
    if depth in ("Essential", "Essentielle", "أساسي"):
        # Keep the complete story, but present a compact fact/question set.
        return story, facts[:3], lesson, questions[:2]
    if depth in ("Exploring", "Exploration", "استكشافي"):
        return story, facts, lesson, questions
    # Detailed and Advanced retain all available content in this release.
    return story, facts, lesson, questions

def direction(language):
    return 'rtl' if language=='العربية' else 'ltr'

def validate_content():
    required = ['subject','scientific_name','category','versions','related_subjects']
    problems=[]
    for item in stories:
        missing=[k for k in required if k not in item]
        if missing:
            problems.append(f"{item.get('subject','Unknown')}: missing {', '.join(missing)}")
            continue
        for age in AGES:
            v=item['versions'].get(age)
            if not v or not all(v.get(k) for k in ['title','story','facts','lesson','questions']):
                problems.append(f"{item['subject']}: incomplete English {age} version")
        for lang in ['Français','العربية']:
            if item['subject'] not in LOCALIZED.get(lang, {}):
                problems.append(f"{item['subject']}: missing {lang} localization")
    return problems

SUBJECT_THEMES={
 'Honey Bee':('#D99A16','#FFF0B8','#FFF9E8','🐝🌼','Pollination · gardens · cooperation'),
 'Eurasian Jay':('#2D6A73','#CDE9E6','#EFF9F7','🐦🌳','Woodland · seeds · memory'),
 'Oak Tree':('#557A3E','#DCE8C8','#F4F8EF','🌳🍂','Forest · seasons · habitat'),
 'Barn Owl':('#5A567A','#DCD9F1','#F4F2FB','🦉🌙','Night · adaptation · senses'),
 'Red Fox':('#B85C38','#F3D2B7','#FFF3EC','🦊🌲','Forest edge · adaptation · coexistence'),
 'African Elephant':('#8A6A4A','#E7D8C5','#FAF4EC','🐘🌾','Savanna · society · landscape'),
 'Bottlenose Dolphin':('#237C9B','#C7EAF3','#EFFAFF','🐬🌊','Ocean · communication · cooperation'),
 'Green Sea Turtle':('#2E7D65','#CBE8D8','#EFFAF4','🐢🌊','Ocean · coast · migration'),
 'Monarch Butterfly':('#C66A1B','#F6D3A8','#FFF5E9','🦋🌼','Migration · flowers · life cycles')
}

if 'show_story' not in st.session_state: st.session_state.show_story=False
if 'saved' not in st.session_state: st.session_state.saved=False
if 'show_app' not in st.session_state: st.session_state.show_app=False

# Public product landing page: the commercial identity comes before the configuration interface.
if not st.session_state.show_app:
 st.markdown('''<div class="landing-shell">
   <div class="landing-topbar"><div class="landing-brand">SEFAR <span>NARATOR</span></div><div class="landing-topnote">Nature · Story · Discovery · Learning</div></div>
   <section class="landing-hero">
     <div class="landing-content">
       <div class="landing-kicker">🌿 A new way to explore the living world</div>
       <div class="landing-title">Stories that<br><span>bring nature alive.</span></div>
       <div class="landing-lead">Create illustrated and educational stories about animals, plants, habitats and the relationships that connect life.</div>
       <div class="landing-sublead">Choose the audience, subject and experience. Then enter a story world where imagination and nature knowledge meet.</div>
       <div class="landing-promise"><span class="landing-pill">📖 Story</span><span class="landing-pill">🎨 Illustration</span><span class="landing-pill">🔬 Discovery</span><span class="landing-pill">🧭 Learning</span></div>
     </div>
     <div class="landing-art"><div class="tree">🌳</div><div class="owl">🦉</div><div class="bee">🐝</div><div class="fox">🦊</div><div class="book">📖</div></div>
   </section>
   <div class="landing-micro"><span>✓ Multilingual</span><span>✓ Age-adapted</span><span>✓ Fiction + science clearly separated</span><span>✓ Designed for the web</span></div>
 </div>''',unsafe_allow_html=True)

 cta1, cta2 = st.columns([1.2,1])
 with cta1:
  if st.button('🌱 Start exploring nature', type='primary', use_container_width=True, key='landing_start'):
   st.session_state.show_app=True
   st.rerun()
 with cta2:
  if st.button('✨ Discover how SEFAR NARATOR works', use_container_width=True, key='landing_how'):
   st.session_state.landing_more = True

 st.markdown('''<div class="landing-section-title">More than a story generator</div><div class="landing-section-lead">SEFAR NARATOR is designed as a complete nature-learning experience: a story gives the subject a voice, discovery gives it context, and learning turns curiosity into understanding.</div>''',unsafe_allow_html=True)
 f1,f2,f3,f4 = st.columns(4)
 features=[('📖','Story','Follow an engaging narrative shaped around a living subject and the audience you choose.'),('🎨','Illustration','Enter a visual world that can evolve with the story, its habitat and its characters.'),('🔬','Discovery','Explore real nature knowledge while keeping fictional storytelling clearly distinct from science.'),('🧭','Learning','Continue with facts, questions, observations and activities that extend the experience.')]
 for col,(icon,title,desc) in zip((f1,f2,f3,f4),features):
  with col:
   st.markdown(f'<div class="landing-feature"><div class="icon">{icon}</div><h3>{title}</h3><p>{desc}</p></div>',unsafe_allow_html=True)

 st.markdown('<div class="landing-section-title">A first SEFAR NARATOR story</div><div class="landing-section-lead">One subject can become many experiences. Here is the kind of journey the platform is designed to create.</div>',unsafe_allow_html=True)
 st.markdown('''<div class="landing-sample">
   <div class="sample-kicker">Sample experience · Honey Bee</div>
   <div class="sample-title">🐝 The Garden That Needed Bees</div>
   <div class="sample-story">A small garden is full of flowers, but something is missing. A honey bee arrives, follows the scent of blossoms and begins a journey through the living garden. The story invites the reader to imagine the bee's world — then step back into science to discover pollination and the relationship between bees and flowering plants.</div>
   <div class="sample-fact"><b>Nature & science:</b> Honey bees visit flowers to collect resources such as nectar and pollen. During these visits, pollen can be transferred between flowers, contributing to pollination.</div>
   <div class="sample-tags"><span class="sample-tag">📖 Story</span><span class="sample-tag">🌼 Pollination</span><span class="sample-tag">🔬 Nature & Science</span><span class="sample-tag">❓ Questions</span></div>
 </div>''',unsafe_allow_html=True)

 st.markdown('<div class="landing-section-title">One subject. Many experiences.</div><div class="landing-section-lead">The structure remains simple for the visitor while allowing the experience to become deeper and more personalized.</div>',unsafe_allow_html=True)
 st.markdown('''<div class="landing-flow"><div class="landing-flow-step"><b>1 · Audience</b><span>Who is this for?</span></div><div class="landing-flow-step"><b>2 · Explore</b><span>World & subject</span></div><div class="landing-flow-step"><b>3 · Experience</b><span>Mode & format</span></div><div class="landing-flow-step"><b>4 · Language</b><span>Choose your language</span></div><div class="landing-flow-step"><b>5 · Create</b><span>Story + science + discovery</span></div></div>''',unsafe_allow_html=True)

 st.markdown('''<div class="landing-vision"><h3>Built for today. Ready for tomorrow.</h3><p>V1.0 establishes the stable story and learning foundation. The future can add AI-assisted story enrichment, adaptive illustrations, synchronized narration and richer interactive discovery — without losing the clear distinction between imagination and factual nature knowledge.</p></div>''',unsafe_allow_html=True)

 if st.session_state.get('landing_more'):
  st.markdown('''<div class="landing-bottom"><h3>Now enter the experience</h3><p>Choose an audience, explore the living world, select a subject and create your first SEFAR NARATOR story.</p></div>''',unsafe_allow_html=True)
  if st.button('🌿 Enter SEFAR NARATOR', type='primary', use_container_width=True, key='landing_enter_bottom'):
   st.session_state.show_app=True
   st.rerun()
 st.caption('SEFAR NARATOR V1.1 · Public Launch Edition · V1.0 story platform underneath')
 st.stop()

st.markdown('''<div class="hero"><div class="title">🌿 SEFAR NARATOR</div><div class="tagline">Stories that bring nature alive</div><div class="version">V1.0 — First stable release · multilingual storytelling, nature learning, responsive experience</div></div>''',unsafe_allow_html=True)
st.markdown('<div class="flow"><span class="step">1. Audience</span>→<span class="step">2. Explore</span>→<span class="step">3. Experience</span>→<span class="step">4. Language</span>→<span class="step">5. Create</span>→<span class="step">✨ Story + learning</span></div>',unsafe_allow_html=True)

st.markdown('<div class="visitor-guide"><b>Your exploration path</b><span>Choose one step at a time. Your final story reflects your choices and opens further discoveries.</span></div>',unsafe_allow_html=True)

with st.sidebar:
 st.header('👤 My Profile')
 st.caption('Profile manages the account; Audience controls the current experience.')
 account=st.radio('Account status',['Continue as guest','Use a profile'])
 profile='Guest'
 if account=='Use a profile':
  profile=st.selectbox('Profile type',PROFILES)
  st.text_input('Display name (optional)')
  st.success('Profile settings are active for this session. Persistent accounts are outside V1.0.')
 else:
  st.info('Explore without an account.')
 st.divider()
 st.header('🧪 V1.0 release check')
 problems=validate_content()
 if problems:
  st.error(f'{len(problems)} content issue(s) detected')
  with st.expander('Details'):
   for p in problems: st.write('• '+p)
 else:
  st.success('Content integrity: OK')
 st.caption(f'{len(stories)} subjects · {len(AGES)} audience profiles · 3 languages')
 st.divider()
 st.header('Current session')
 st.write('**Profile:**',profile)
 if profile!='Guest':
  st.selectbox('Membership preview',['Free visitor','Individual member','Family member','Teacher / Classroom','Institution'])

st.info('V1.0 stable release: responsive, multilingual, age-adapted nature storytelling with clearly separated fiction and science. AI generation is intentionally outside this release.')

# Audience and Language share the same row, matching the Explore / Experience layout.
c1,c2=st.columns(2)
with c1:
 with st.container(border=True):
  st.markdown('<div class="compartment-title compartment-audience"><span class="num">1</span> 👥 AUDIENCE</div><div class="compartment-hint">Who is this experience designed for?</div>',unsafe_allow_html=True)
  audience=st.selectbox('Audience',list(AGES),format_func=lambda x:f'{x} — {AGES[x][0]}', key='audience')
  st.markdown(f'<div class="choicebox"><b>{audience}</b><br><span class="small">{AGES[audience][1]}</span></div>',unsafe_allow_html=True)
with c2:
 with st.container(border=True):
  st.markdown('<div class="compartment-title compartment-language"><span class="num">4</span> 🌐 LANGUAGE</div><div class="compartment-hint">Select the language of the complete experience.</div>',unsafe_allow_html=True)
  language=st.selectbox(UI['English']['language'],LANGUAGES, key='language')
  rtl = direction(language)

c1,c2=st.columns(2)
with c1:
 with st.container(border=True):
  st.markdown('<div class="compartment-title compartment-explore"><span class="num">2</span> 🌿 EXPLORE</div><div class="compartment-hint">Choose the nature world and subject.</div>',unsafe_allow_html=True)
  categories=['All categories']+sorted({s['category'] for s in stories})
  category=st.selectbox(UI.get(language,UI['English'])['category'],categories, key='category')
  options=[s['subject'] for s in stories if category=='All categories' or s['category']==category]
  if st.session_state.get('subject') not in options:
   st.session_state['subject'] = options[0]
  subject=st.selectbox(UI.get(language,UI['English'])['subject'],options, key='subject')
  mode=st.selectbox(UI.get(language,UI['English'])['mode'],['Story','Discovery','Documentary','Fantasy'], key='mode')
with c2:
 with st.container(border=True):
  st.markdown('<div class="compartment-title compartment-experience"><span class="num">3</span> ✨ EXPERIENCE</div><div class="compartment-hint">Define how the story should be presented.</div>',unsafe_allow_html=True)
  fmt=st.selectbox(UI.get(language,UI['English'])['format'],['Long-form story','Story + scientific facts','Story + questions','Classroom activity'], key='format')
  depth_options={'English':['Essential','Exploring','Detailed','Advanced'],'Français':['Essentielle','Exploration','Détaillée','Avancée'],'العربية':['أساسي','استكشافي','مفصل','متقدم']}
  length=st.selectbox(UI.get(language,UI['English'])['depth'],depth_options[language], key='depth')
  objective=st.text_input(UI.get(language,UI['English'])['objective'],'Understand a relationship in nature', key='objective')

if language!='English':
 st.markdown(f'<div class="langbox"><b>✓ {language} localization active</b><br>Stories, scientific facts, discovery lesson and questions are displayed in the selected language. The English version remains available as the reference edition.</div>',unsafe_allow_html=True)

st.markdown(f'<div class="section">{UI[language]["create"]}</div>',unsafe_allow_html=True)
with st.container(border=True):
 st.markdown('<div class="compartment-title compartment-create"><span class="num">5</span> 🎨 CREATE & LAUNCH</div><div class="compartment-hint">Review the complete selection before starting the experience.</div>',unsafe_allow_html=True)
 st.markdown(f'''<div class="choicebox compartment-create {'rtl' if language=='العربية' else ''}"><b>{'Your selection' if language=='English' else 'Votre sélection' if language=='Français' else 'اختياراتك'}</b><br><span class="badge">{audience}</span><span class="badge">{category}</span><span class="badge">{subject}</span><span class="badge">{language}</span><span class="badge">{length}</span><span class="badge">{mode}</span></div>''',unsafe_allow_html=True)
 a,b=st.columns([3,1])
 with a:
  if st.button(UI[language]['start'],type='primary',use_container_width=True): st.session_state.show_story=True; st.session_state.saved=False
 with b:
  if st.button(UI[language]['reset'],use_container_width=True):
   st.session_state.show_story=False
   st.session_state.saved=False
   st.session_state.chapter=0
   for _key in ['audience','language','format','depth','objective','category','subject','mode']:
    st.session_state.pop(_key, None)
   st.rerun()

if st.session_state.show_story:
 labels = {'English': {'scientific_subject':'Scientific subject','objective':'Objective','illustration_note':'Illustration placeholder; visual assets will be added progressively.','creative':'Creative activity','audio_note':'Narration scripts are prepared for future audio integration. Real audio files and voice selection are not yet connected.'}, 'Français': {'scientific_subject':'Sujet scientifique','objective':'Objectif','illustration_note':'Illustration provisoire ; les ressources visuelles seront ajoutées progressivement.','creative':'Activité créative','audio_note':'Les scripts de narration sont préparés pour une future intégration audio. Les fichiers audio et le choix de la voix ne sont pas encore connectés.'}, 'العربية': {'scientific_subject':'الموضوع العلمي','objective':'الهدف','illustration_note':'رسم توضيحي مؤقت؛ ستتم إضافة الموارد البصرية تدريجياً.','creative':'نشاط إبداعي','audio_note':'تم إعداد نصوص السرد لدمج الصوت مستقبلاً. لم يتم ربط الملفات الصوتية واختيار الصوت بعد.'}}[language]
 s=by_subject.get(subject)
 if not s:
  st.error('The selected subject is unavailable. Please reset the experience.')
  st.stop()
 try:
  title,story,facts,lesson,questions=localized_content(subject,language,audience)
  story,facts,lesson,questions=apply_depth(story,facts,lesson,questions,length,language)
 except (KeyError, TypeError) as exc:
  st.error(f'Content error for {subject} / {language} / {audience}: {exc}')
  st.stop()
 direction_class='rtl' if rtl=='rtl' else ''
 theme=SUBJECT_THEMES.get(s['subject'],('#4F8F45','#DFEEDA','#F4FAF1','🌿','Nature · discovery · life'))
 accent,accent2,glow,emoji,theme_words=theme
 localized_intro=("Version localisée en français." if language=='Français' else "نسخة مترجمة ومهيأة باللغة العربية." if language=='العربية' else "Age-specific reference edition.")
 st.markdown(f'<div class="section">{UI[language]["adapted"]}</div>',unsafe_allow_html=True)
 st.markdown(f'<div class="story-experience {direction_class}" style="--accent:{accent};--accent2:{accent2};--glow:{glow}"><div class="story-hero"><div class="subject-orb">{emoji}</div><div><div class="story-kicker">SEFAR NARATOR · {s["category"]}</div><div class="story-title">{title}</div><p class="story-subtitle">{theme_words} · {s["scientific_name"]}</p></div></div><div class="story-nav"><span class="story-chip">{audience}</span><span class="story-chip">{mode}</span><span class="story-chip">{language}</span><span class="story-chip">{length}</span></div><div class="story-subtitle"><b>{labels["scientific_subject"]}:</b> {s["subject"]} · <b>{labels["objective"]}:</b> {objective} · {localized_intro}</div></div>',unsafe_allow_html=True)
 paragraphs=[x.strip() for x in re.split(r"\n\s*\n", story) if x.strip()]
 if not paragraphs: paragraphs=[story]
 visual_note=("The visual atmosphere follows the selected nature subject. Illustration assets can be connected here later." if language=='English' else "L’atmosphère visuelle suit le sujet nature sélectionné. Des illustrations pourront être intégrées ici." if language=='Français' else "يتبع الجو البصري موضوع الطبيعة المختار. يمكن دمج الرسوم التوضيحية هنا لاحقًا.")
 visual_title=("Visual world" if language=='English' else "Univers visuel" if language=='Français' else "العالم البصري")
 st.markdown(f'<div class="adaptive-card {direction_class}" style="--accent:{accent};--accent2:{accent2}"><h2>🖼️ {visual_title}</h2><div style="font-size:3.8rem;text-align:center;line-height:1.05">{emoji}</div><p class="visual-caption">{visual_note}</p></div>',unsafe_allow_html=True)
 # V1.0 Storybook presentation: continuous story, generous serif typography, controlled reading width, and a compact result panel.
 story_html=''.join(f'<p>{p}</p>' for p in paragraphs)
 result_labels = {
  'English': [('Audience', audience),('Category', category),('Subject', subject),('Mode', mode),('Language', language),('Depth', length),('Objective', objective)],
  'Français': [('Public', audience),('Catégorie', category),('Sujet', subject),('Mode', mode),('Langue', language),('Profondeur', length),('Objectif', objective)],
  'العربية': [('الجمهور', audience),('الفئة', category),('الموضوع', subject),('النمط', mode),('اللغة', language),('العمق', length),('الهدف', objective)]
 }[language]
 result_html=''.join(f'<div class="result-item"><span class="result-label">{lab}</span><span class="result-value">{val}</span></div>' for lab,val in result_labels)
 result_title = 'Your SEFAR NARATOR experience' if language=='English' else 'Votre expérience SEFAR NARATOR' if language=='Français' else 'تجربتك في SEFAR NARATOR'
 storybook_note = ('The story is continuous. Fictional storytelling and scientific information remain clearly separated below.' if language=='English' else 'L’histoire est continue. Le récit imaginaire et les informations scientifiques restent clairement séparés ci-dessous.' if language=='Français' else 'القصة متواصلة. يبقى السرد الخيالي والمعلومات العلمية منفصلين بوضوح أدناه.')
 st.markdown(f"""<div class=\"storybook-layout {direction_class}\">
   <div class=\"storybook-main\" style=\"--accent:{accent}\">
     <h2>📖 {UI[language]['story']}</h2>
     <div class=\"story-text\">{story_html}</div>
     <div class=\"storybook-note\" style=\"--accent:{accent}\">{storybook_note}</div>
   </div>
   <aside class=\"storybook-result\">
     <h3>🌿 {result_title}</h3>
     {result_html}
   </aside>
 </div>""",unsafe_allow_html=True)
 st.markdown(f'<div class="card sciencepanel {"rtl" if rtl=="rtl" else ""}><h2>🔬 {UI[language]["facts"]}</h2>'+''.join(f'<div class="fact">{f}</div>' for f in facts)+'</div>',unsafe_allow_html=True)
 st.markdown(f'<div class="card sciencepanel {"rtl" if rtl=="rtl" else ""}><h2>💡 {UI[language]["discover"]}</h2><div class="lesson">{lesson}</div></div>',unsafe_allow_html=True)
 st.markdown(f'<div class="card activitypanel {"rtl" if rtl=="rtl" else ""}><h2>❓ {UI[language]["questions"]}</h2>'+''.join(f'<p>• {q}</p>' for q in questions)+'<hr><b>Creative activity:</b> Draw the habitat, make an observation list, or explain one relationship between the subject and another species.</div>',unsafe_allow_html=True)
 st.markdown(f'<div class="adaptive-card adaptive-activity {"rtl" if rtl=="rtl" else ""}"><h3>📝 {UI[language]["activity"]}</h3><p>{UI[language]["activity_intro"]}</p></div>',unsafe_allow_html=True)
 for idx, check in enumerate(UI[language]['checks']):
  st.checkbox(check, key=f'activity_{language}_{idx}')
 st.markdown(f'<div class="audio {"rtl" if rtl=="rtl" else ""}"><b>{UI[language]["audio"]}</b><br><span class="small">Narration scripts are prepared for future audio integration. Real audio files and voice selection are not yet connected.</span></div>',unsafe_allow_html=True)
 related = s.get('related_subjects', []) if isinstance(s, dict) else []
 st.markdown(f'<div class="card {"rtl" if rtl=="rtl" else ""}><h2>🧭 {UI[language]["related"]}</h2>'+''.join(f'<span class="badge">{r}</span>' for r in related)+'</div>',unsafe_allow_html=True)
 if audience=='Group / Classroom': st.markdown(f'<div class="note {"rtl" if rtl=="rtl" else ""}"><b>{"Suggestion pour l’animateur" if language=="Français" else "اقتراح للميسّر" if language=="العربية" else "Facilitator suggestion"}:</b> {"Demandez aux apprenants de distinguer les éléments imaginaires des informations scientifiques, puis de créer un dessin, une fiche d’observation ou une courte présentation." if language=="Français" else "اطلب من المتعلمين التمييز بين العناصر الخيالية والمعلومات العلمية، ثم إعداد رسم أو ورقة ملاحظة أو عرض قصير." if language=="العربية" else "Invite learners to separate fictional elements from scientific claims, then create a drawing, observation sheet, or short group presentation."}</div>',unsafe_allow_html=True)
 if st.button(UI[language]['save']):
  st.session_state.saved=True
 if st.session_state.saved: st.success('Expérience enregistrée pour cette session.' if language=='Français' else 'تم حفظ التجربة لهذه الجلسة.' if language=='العربية' else 'Experience saved for this session. Persistent profile storage is planned for a future account-enabled release.')

st.markdown('<div style="text-align:center;color:#7b857d;font-size:.8rem;margin-top:28px">SEFAR NARATOR V1.0 · Multilingual storytelling with clearly separated scientific information.</div>',unsafe_allow_html=True)
