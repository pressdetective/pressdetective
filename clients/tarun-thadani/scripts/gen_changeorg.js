const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, AlignmentType, LevelFormat, BorderStyle,
  Table, TableRow, TableCell, WidthType, ShadingType, TabStopType, TabStopPosition, PageNumber, Footer
} = require("docx");

const A4 = { width: 11906, height: 16838 };
const MARGIN = { top: 1440, right: 1440, bottom: 1440, left: 1440 };
const CW = 9026;

const title=(t)=>new Paragraph({alignment:AlignmentType.CENTER,spacing:{after:60},children:[new TextRun({text:t,bold:true,size:30})]});
const sub=(t)=>new Paragraph({alignment:AlignmentType.CENTER,spacing:{after:160},children:[new TextRun({text:t,size:22,color:"555555"})]});
const rule=()=>new Paragraph({spacing:{after:120,before:60},border:{bottom:{style:BorderStyle.SINGLE,size:6,color:"000000",space:1}},children:[]});
const h1=(t)=>new Paragraph({spacing:{before:300,after:120},border:{bottom:{style:BorderStyle.SINGLE,size:4,color:"C0392B",space:2}},children:[new TextRun({text:t,bold:true,size:26,color:"C0392B"})]});
const h2=(t)=>new Paragraph({spacing:{before:200,after:100},children:[new TextRun({text:t,bold:true,size:23})]});
const p=(runs,o={})=>{const c=Array.isArray(runs)?runs:[new TextRun({text:runs,size:22})];return new Paragraph({alignment:o.align??AlignmentType.JUSTIFIED,spacing:{after:o.after??140,line:o.line??264},children:c});};
const bul=(t,ref="bul")=>new Paragraph({numbering:{reference:ref,level:0},alignment:AlignmentType.JUSTIFIED,spacing:{after:90,line:264},children:Array.isArray(t)?t:[new TextRun({text:t,size:22})]});
const numli=(t,ref="steps")=>new Paragraph({numbering:{reference:ref,level:0},alignment:AlignmentType.JUSTIFIED,spacing:{after:90,line:264},children:Array.isArray(t)?t:[new TextRun({text:t,size:22})]});
const bt=(t)=>new TextRun({text:t,size:22});
const bb=(t)=>new TextRun({text:t,size:22,bold:true});
const box=(label,text)=>new Paragraph({shading:{type:"clear",fill:"F4F6F8"},spacing:{after:120,before:40},border:{left:{style:BorderStyle.SINGLE,size:18,color:"C0392B",space:8}},children:[new TextRun({text:label+"  ",bold:true,size:21}),new TextRun({text:text,size:21})]});

const numberingConfig={config:[
  {reference:"bul",levels:[{level:0,format:LevelFormat.BULLET,text:"•",alignment:AlignmentType.LEFT,style:{paragraph:{indent:{left:560,hanging:280}}}}]},
  {reference:"steps",levels:[{level:0,format:LevelFormat.DECIMAL,text:"%1.",alignment:AlignmentType.LEFT,style:{paragraph:{indent:{left:560,hanging:300}}}}]},
  {reference:"asks",levels:[{level:0,format:LevelFormat.DECIMAL,text:"%1.",alignment:AlignmentType.LEFT,style:{paragraph:{indent:{left:560,hanging:300}}}}]},
]};

const children=[
  title("CHANGE.ORG CAMPAIGN — READY-TO-PUBLISH PACKAGE"),
  sub("Justice for Tarun Thadani (Founder, Dharte) — Stop the Misuse of a False Criminal Case"),
  rule(),
  new Paragraph({shading:{type:"clear",fill:"FFF4E5"},spacing:{after:120,before:60},children:[new TextRun({text:"Publish only after review by Adv. Sujata Shirasi. The case is sub judice. Third-party conduct is stated as “alleged” throughout to reduce defamation/contempt risk. Do not add unproven criminal accusations against named individuals before legal sign-off.",italics:true,size:19})]}),

  h1("1. Petition Title (pick one)"),
  bul([bb("Recommended: "),bt("“Justice for an Innocent Man: Drop the False Case Against Tarun Thadani”")]),
  bul("“He Only Sent Invitations — Yet He’s an ‘Accused’. Demand a Fair Inquiry for Tarun Thadani.”"),
  bul("“Stop the Abuse of Process: Protect Innocent Citizens from Fabricated FIRs”"),
  box("Tip:","Change.org titles work best under ~80 characters, name the person, and state one clear ask. Keep it human, not legalistic."),

  h1("2. Petition To (Decision-makers / Targets)"),
  bul("Commissioner of Police, Mumbai"),
  bul("ADGP, Anti-Corruption Bureau (ACB), Maharashtra"),
  bul("Joint Commissioner of Police (Crime), Mumbai"),
  bul("The Senior Inspector, Dadar Police Station / Anti-Extortion Cell"),
  bul("[Optional] Hon’ble Home Minister, Government of Maharashtra"),
  box("Note:","On Change.org these go in the “Decision Maker” field. Do not name the trial court or sitting judges as targets while the matter is sub judice."),

  h1("3. Short Summary (the “blurb” under the title)"),
  p([bt("Tarun Thadani, an entrepreneur and founder of Dharte, has been dragged into a criminal case for an incident he was not even present at. His only role was sending invitations to a private event. Worse, the ₹1 crore “extortion” charge did not exist in the original complaint — it appeared nearly two months later. Sign to demand a fair, evidence-based inquiry and an end to the misuse of process.")],{after:120}),

  h1("4. Full Petition Text (main body — copy/paste)"),
  p([bb("This petition asks the authorities to ensure a fair, transparent and evidence-based review of a criminal case in which an innocent man has been falsely implicated.")]),
  h2("What happened"),
  p([bt("On 2 June 2022, a private social event was held at a restaurant in Worli, Mumbai. Mr. Tarun Thadani’s involvement was limited to sending invitations. "),bb("He was not present at the venue"),bt(" when an altercation is said to have taken place between two other individuals.")]),
  p([bt("On 4 June 2022, a complaint was filed alleging "),bb("only assault"),bt(". It contained no allegation of extortion, no monetary demand, and no role attributed to Mr. Thadani.")]),
  p([bt("When no FIR was registered, the complaint was "),bb("materially changed nearly two months later"),bt(", and a new and serious allegation of ₹1 crore extortion was introduced for the first time. On the basis of this altered version, an FIR (No. 0654/2022, Dadar Police Station) was registered — naming Mr. Thadani, who was never present and had no role beyond invitations.")]),
  h2("Why this is wrong"),
  bul("None of the accused were summoned or examined before the FIR was registered."),
  bul("No call records, messages, or financial transactions were verified."),
  bul("A grave charge surfaced only after a long, unexplained delay and a change in the complaint."),
  bul("An innocent person’s name, reputation, profession and family have been damaged — including through one-sided media coverage."),
  p([bt("If a complaint can be quietly altered later and used to brand an innocent person a criminal — without due process — then "),bb("any citizen is at risk."),bt(" This is not about one person; it is about whether due process means anything.")]),
  h2("What we are asking for"),
  numli("A fair, transparent and impartial inquiry into how the complaint was altered and how the FIR came to be registered without examining the accused.","asks"),
  numli("Accountability for any procedural irregularity or misuse of authority in the registration and investigation, in accordance with law.","asks"),
  numli("Protection for innocent citizens from fabricated or improved complaints used to settle scores.","asks"),
  numli("That the authorities act strictly on verified evidence — not on belated, altered allegations.","asks"),
  p([bb("Please sign and share. Your voice can help ensure that due process protects the innocent.")],{after:120}),
  box("Sub judice safeguard:","This petition seeks a fair inquiry and due process. It does not ask anyone to pre-judge guilt and makes no unproven criminal accusation against any named individual."),

  h1("5. Social Sharing Copy"),
  h2("WhatsApp / general"),
  p([bt("He only sent invitations to an event he didn’t even attend — yet Tarun Thadani is an “accused” in a case where the ₹1 crore extortion charge appeared 2 months AFTER the original complaint. Demand a fair inquiry. Sign & share 👉 [LINK]")],{after:100}),
  h2("X / Twitter (under 280 chars)"),
  p([bt("An innocent man named in an FIR for an incident he wasn’t present at. The ₹1cr “extortion” charge wasn’t even in the original complaint — it was added 2 months later. Due process must protect the innocent. Sign: [LINK] #Justice #DueProcess")],{after:100}),
  h2("Instagram / Facebook caption"),
  p([bt("What if a complaint against you could be quietly rewritten months later — and suddenly you’re a criminal “accused”? That’s what Tarun Thadani is facing. His only role was sending invitations to a private event he didn’t attend. We’re asking for one thing: a fair, evidence-based inquiry. Link in bio to sign. 🔗 [LINK]")],{after:100}),
  h2("LinkedIn (professional)"),
  p([bt("Due process is the difference between justice and persecution. An entrepreneur I’m supporting has been named in a criminal case for an incident he was not present at — with a serious charge added to the complaint months after the fact. This petition simply asks the authorities for a fair, transparent, evidence-based inquiry. Please consider signing and sharing: [LINK]")],{after:120}),

  h1("6. Campaign Updates Plan (post on Change.org to keep momentum)"),
  undefined,
  h1("7. Launch Checklist"),
  numli("Get Adv. Sujata Shirasi’s sign-off on the title, body and asks.","steps"),
  numli("Create the petition on Change.org; paste Title, Decision-maker(s), Summary, and Full Petition Text.","steps"),
  numli("Add a strong image (Tarun’s professional photo or a ‘due process’ graphic). Avoid graphic/defamatory imagery.","steps"),
  numli("Set the goal to a realistic first milestone (e.g., 500 signatures), then raise it as you grow.","steps"),
  numli("Seed first 25–50 signatures privately (family, friends, colleagues) before public sharing.","steps"),
  numli("Share via WhatsApp first (highest conversion), then X, Instagram, Facebook, LinkedIn.","steps"),
  numli("Post a campaign update every time you hit a milestone or there’s a development.","steps"),
  numli("Keep every public statement measured and factual while the case is sub judice.","steps"),

  rule(),
  new Paragraph({children:[new TextRun({text:"Disclaimer: AI-generated campaign draft for review by counsel. Not legal advice. Publish only after legal sign-off. Replace [LINK] with the live Change.org URL after creation.",italics:true,size:18,color:"777777"})]}),
];

// build updates table separately and splice
function updatesTable(){
  const border={style:BorderStyle.SINGLE,size:1,color:"BBBBBB"};
  const borders={top:border,bottom:border,left:border,right:border};
  const cell=(text,w,opts={})=>new TableCell({borders,width:{size:w,type:WidthType.DXA},shading:opts.fill?{fill:opts.fill,type:ShadingType.CLEAR}:undefined,margins:{top:60,bottom:60,left:100,right:100},children:[new Paragraph({children:[new TextRun({text,size:opts.size??20,bold:opts.bold??false,color:opts.color})]})]});
  const widths=[2200,6826];
  const head=new TableRow({tableHeader:true,children:[cell("When",widths[0],{fill:"C0392B",bold:true,color:"FFFFFF"}),cell("Update to post",widths[1],{fill:"C0392B",bold:true,color:"FFFFFF"})]});
  const rows=[
    ["At launch","“We’ve started this petition. Here’s the story — please sign and share.”"],
    ["100 signatures","“Thank you! 100 voices for due process. Keep sharing.”"],
    ["Any milestone","Share the new number + one fresh fact (timeline, the altered complaint)."],
    ["Legal development","Plain-language update on filings/hearings (no commentary on the merits while sub judice)."],
    ["Media correction","If/when a correction or apology is published, share it as a win."],
  ].map(r=>new TableRow({children:[cell(r[0],widths[0]),cell(r[1],widths[1])]}));
  return new Table({width:{size:CW,type:WidthType.DXA},columnWidths:widths,rows:[head,...rows]});
}
// replace placeholder table() call
const finalChildren=[];
for(const c of children){ if(c && c.__isPlaceholder){ finalChildren.push(updatesTable()); } else { finalChildren.push(c);} }
// Since table() returned undefined above, fix: rebuild by replacing undefined entries
const cleaned=children.map(c=>c===undefined?updatesTable():c);

const doc=new Document({numbering:numberingConfig,styles:{default:{document:{run:{font:"Calibri",size:22}}}},
  sections:[{properties:{page:{size:A4,margin:MARGIN}},
    footers:{default:new Footer({children:[new Paragraph({border:{top:{style:BorderStyle.SINGLE,size:4,color:"CCCCCC",space:1}},tabStops:[{type:TabStopType.RIGHT,position:TabStopPosition.MAX}],children:[new TextRun({text:"Change.org Campaign — Tarun Thadani (DRAFT, review before publishing)",size:16,color:"888888"}),new TextRun({text:"\tPage ",size:16,color:"888888"}),new TextRun({children:[PageNumber.CURRENT],size:16,color:"888888"}),new TextRun({text:" of ",size:16,color:"888888"}),new TextRun({children:[PageNumber.TOTAL_PAGES],size:16,color:"888888"})]})]})},
    children:cleaned}]});
Packer.toBuffer(doc).then(b=>{fs.writeFileSync("04_ChangeOrg_Campaign_Tarun_Thadani.docx",b);console.log("Doc 4 written");})