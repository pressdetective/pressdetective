const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, AlignmentType, LevelFormat, BorderStyle,
  Table, TableRow, TableCell, WidthType, ShadingType, TabStopType, TabStopPosition, PageNumber, Footer
} = require("docx");

const A4 = { width: 11906, height: 16838 };
const MARGIN = { top: 1440, right: 1440, bottom: 1440, left: 1440 };
const CW = 9026; // content width A4 1" margins

const title=(t)=>new Paragraph({alignment:AlignmentType.CENTER,spacing:{after:60},children:[new TextRun({text:t,bold:true,size:30})]});
const sub=(t)=>new Paragraph({alignment:AlignmentType.CENTER,spacing:{after:160},children:[new TextRun({text:t,size:22,color:"555555"})]});
const rule=()=>new Paragraph({spacing:{after:120,before:60},border:{bottom:{style:BorderStyle.SINGLE,size:6,color:"000000",space:1}},children:[]});
const h1=(t)=>new Paragraph({spacing:{before:300,after:120},border:{bottom:{style:BorderStyle.SINGLE,size:4,color:"2E4A7A",space:2}},children:[new TextRun({text:t,bold:true,size:26,color:"2E4A7A"})]});
const h2=(t)=>new Paragraph({spacing:{before:200,after:100},children:[new TextRun({text:t,bold:true,size:23})]});
const p=(runs,o={})=>{const c=Array.isArray(runs)?runs:[new TextRun({text:runs,size:22})];return new Paragraph({alignment:o.align??AlignmentType.JUSTIFIED,spacing:{after:o.after??140,line:component(o)},children:c});};
function component(o){return o.line??264;}
const bul=(t,ref="bul")=>new Paragraph({numbering:{reference:ref,level:0},alignment:AlignmentType.JUSTIFIED,spacing:{after:90,line:264},children:Array.isArray(t)?t:[new TextRun({text:t,size:22})]});
const numli=(t,ref="steps")=>new Paragraph({numbering:{reference:ref,level:0},alignment:AlignmentType.JUSTIFIED,spacing:{after:90,line:264},children:Array.isArray(t)?t:[new TextRun({text:t,size:22})]});
const bt=(t)=>new TextRun({text:t,size:22});
const bb=(t)=>new TextRun({text:t,size:22,bold:true});

const numberingConfig={config:[
  {reference:"bul",levels:[{level:0,format:LevelFormat.BULLET,text:"•",alignment:AlignmentType.LEFT,style:{paragraph:{indent:{left:560,hanging:280}}}}]},
  {reference:"steps",levels:[{level:0,format:LevelFormat.DECIMAL,text:"%1.",alignment:AlignmentType.LEFT,style:{paragraph:{indent:{left:560,hanging:300}}}}]},
]};

const border={style:BorderStyle.SINGLE,size:1,color:"BBBBBB"};
const borders={top:border,bottom:border,left:border,right:border};
function cell(text,w,opts={}){
  return new TableCell({borders,width:{size:w,type:WidthType.DXA},shading:opts.fill?{fill:opts.fill,type:ShadingType.CLEAR}:undefined,margins:{top:60,bottom:60,left:100,right:100},children:[new Paragraph({children:Array.isArray(text)?text:[new TextRun({text,size:opts.size??20,bold:opts.bold??false,color:opts.color})]})]});
}
function table(headers,rows,widths){
  const headRow=new TableRow({tableHeader:true,children:headers.map((hd,i)=>cell(hd,widths[i],{fill:"2E4A7A",bold:true,color:"FFFFFF",size:20}))});
  const dataRows=rows.map(r=>new TableRow({children:r.map((c,i)=>cell(c,widths[i],{size:20}))}));
  return new Table({width:{size:CW,type:WidthType.DXA},columnWidths:widths,rows:[headRow,...dataRows]});
}

const children=[
  title("PLAN OF ACTION"),
  sub("Defence Strategy & Roadmap — False Case against Mr. Tarun Thadani (Founder, Dharte)"),
  rule(),
  new Paragraph({shading:{type:"clear",fill:"FFF4E5"},spacing:{after:120,before:60},children:[new TextRun({text:"Prepared from supplied case materials for internal strategic use. This is not legal advice. All litigation steps must be settled and executed by the Advocate on Record (Adv. Sujata Shirasi). Items in [brackets] need verification.",italics:true,size:19})]}),

  h1("1. Case Snapshot"),
  table(
    ["Item","Detail"],
    [
      ["Client / Accused","Mr. Tarun Thadani — entrepreneur, founder of Dharte (dharte.com)"],
      ["FIR / C.R.","No. 0654 of 2022, Dadar Police Station, Mumbai (registered ~12–13 Aug 2022)"],
      ["Offences alleged","Assault + ₹1 crore extortion — IPC s.384/385/387, 506 r/w 34 [confirm exact sections]"],
      ["Complainant","Mr. Abhishek Badriprasad Saraf (Esplanade House, Mumbai 400001)"],
      ["Co-accused","Mr. Ali Asgar Merchant"],
      ["Incident","Private event, restaurant in Worli, 02–03 June 2022"],
      ["Client's role","Sent invitations only; NOT present at the venue"],
      ["Status","Charge-sheeted; discharge REFUSED by Sessions Court on 31 March 2024"],
      ["Counsel","Adv. Sujata Shirasi (+91 93216 13691)"],
    ],
    [2600,6426]
  ),

  h1("2. The Core Defence (One Line)"),
  p([bt("Mr. Thadani was "),bb("not present"),bt(" at the incident and did "),bb("nothing beyond sending invitations"),bt("; the "),bb("extortion allegation was absent"),bt(" from the original complaint of 04 June 2022 and was "),bb("manufactured ~2 months later"),bt("; and the FIR was registered "),bb("without examining any accused or verifying any evidence"),bt(". The prosecution against him cannot survive even prima facie scrutiny.")]),

  h1("3. The Five Pillars of Innocence"),
  numli([bb("Absence: "),bt("Client was not at the venue at the relevant time — to be established by location/CCTV/itinerary/witness evidence.")]),
  numli([bb("No role: "),bt("Sole act was sending invitations — innocuous and non-criminal; cannot attract s.384/385/387 or s.34 IPC.")]),
  numli([bb("Delayed, altered complaint: "),bt("Original 04.06.2022 complaint = assault only; extortion of ₹1 cr introduced ~2 months later. The improvement is the heart of the false-implication case.")]),
  numli([bb("Procedural illegality: "),bt("No accused summoned/examined; no call records, messages or bank trails verified before FIR.")]),
  numli([bb("Complainant's antecedents: "),bt("Saraf is independently linked to fraud/forgery/PoA-misuse allegations (Esplanade House / Martin Burn Ltd / Fatehpuria family) — shows propensity to misuse process. Use subject to relevance & admissibility.")]),

  h1("4. Litigation Tracks"),
  h2("Track A — Criminal (primary)"),
  table(
    ["Step","Forum","Purpose","Priority"],
    [
      ["Criminal Revision Application (s.397/401 CrPC)","Bombay High Court","Set aside the 31.03.2024 refusal of discharge; seek discharge + stay","HIGH"],
      ["Quashing Petition (s.482 CrPC)","Bombay High Court","Quash FIR 0654/2022 & charge-sheet qua client; alternative/parallel remedy","HIGH"],
      ["Application for stay of trial","With the above","Halt Sessions trial against client pending hearing","HIGH"],
    ],
    [2900,1900,3000,1226]
  ),
  p([bb("Note: "),bt("Revision and quashing are alternative remedies. Counsel should decide which to lead with (or file the revision and keep s.482 in reserve), and must disclose the pendency of one to the Court when filing the other. Pressing both on identical grounds without disclosure should be avoided.")],{after:120}),

  h2("Track B — Defamation / media correction"),
  bul([bb("Status: "),bt("Legal notice already issued (29.07.2025) by Adv. Sujata Shirasi to The Times of India re articles dated 22.06.2023 and 31.03.2024.")]),
  bul([bb("Next: "),bt("If no correction/apology, file civil defamation suit (damages + injunction) and/or criminal defamation complaint (s.499/500 IPC / s.356 BNS). Track the limitation period for each article.")]),
  bul([bb("Goal: "),bt("Public correction naming the actual complainant; removal of defamatory content from print & digital archives; protect reputation/brand of Dharte.")]),

  h2("Track C — Anti-Corruption Bureau (ACB) / procedural misconduct"),
  bul([bb("Status: "),bt("Representations on record (Santosh Sakpal complaints to ACB Maharashtra) alleging bribe to Inspector Mahesh Narayan Mugutra (PBMH76505) for filing the false FIR.")]),
  bul([bb("Next: "),bt("Pursue/renew written representation to ADGP, ACB Maharashtra seeking inquiry into alteration of complaint and registration of FIR without examination of accused; obtain acknowledgement and inquiry number.")]),
  bul([bb("Caution: "),bt("Keep bribery allegations factual and supportable; in court pleadings, frame procedural irregularity carefully and avoid unprovable scandalous assertions.")]),

  h2("Track D — Counter-action against false complainant (optional, advised by counsel)"),
  bul("Consider complaint/relief for false implication and giving false information (e.g. IPC s.182/211 / BNS equivalents), pursued strategically — usually after a favourable order in Track A."),
  bul("Consolidate evidence of Saraf's antecedents (Esplanade House dispute, court records) as corroboration of motive/propensity."),

  h1("5. Evidence To Assemble (Defence Brief)"),
  bul("Certified copies: FIR 0654/2022, full charge-sheet, all s.161 CrPC statements, and the impugned order dated 31.03.2024."),
  bul("The original online complaint dated 04.06.2022 (proving extortion was absent) — the single most important document."),
  bul("Proof of client's absence: phone location/CDR, CCTV, travel/itinerary, calendar, third-party witnesses."),
  bul("The invitation(s) sent by client — to show the limited, innocuous role."),
  bul("Timeline chart: 02.06.2022 incident → 04.06.2022 complaint (assault only) → ~Aug 2022 altered version (extortion) → 12/13.08.2022 FIR → charge-sheet → 31.03.2024 refusal."),
  bul("ACB representations & any acknowledgements; Santosh Sakpal material."),
  bul("Records re Saraf's antecedents (Martin Burn Ltd v. Abhishek Saraf; Esplanade House)."),

  h1("6. Indicative Timeline & Owners"),
  table(
    ["Phase","Action","Owner","Target"],
    [
      ["Immediate","Obtain all certified copies; build timeline & evidence index","Counsel + Client","Week 1–2"],
      ["Filing","Finalise & file Revision + s.482 with stay applications","Adv. Shirasi","Week 2–4"],
      ["Interim","Press for stay of Sessions trial qua client","Adv. Shirasi","At admission"],
      ["Parallel","Defamation follow-up; ACB representation","Adv. Shirasi","Week 2–6"],
      ["Hearing","Arguments on discharge/quashing","Adv. Shirasi","Per HC roster"],
      ["Contingency","If relief refused: SLP / further remedies as advised","Senior counsel","As needed"],
    ],
    [1700,3700,1900,1726]
  ),

  h1("7. Key Risks & Watch-points"),
  bul("Confirm which court passed the 31.03.2024 order and the exact IPC sections — these drive forum and framing."),
  bul("Limitation for the revision (and for defamation) — file promptly or seek condonation with reasons."),
  bul("Avoid duplicative/contradictory pleadings across revision and s.482; disclose parallel proceedings."),
  bul("Keep all public statements measured while matters are sub judice."),
  bul("Bribery/forgery allegations must be evidence-backed before being pleaded in court."),

  h1("8. Immediate Next 5 Steps"),
  numli("Confirm court, accused number and exact charge-sheet sections; fill all [brackets] in the two draft petitions."),
  numli("Secure the certified copy of the 31.03.2024 order and the original 04.06.2022 complaint."),
  numli("Settle and file the Criminal Revision Application (+ stay) — lead remedy."),
  numli("Keep the s.482 quashing petition ready as alternative/parallel relief."),
  numli("Advance the defamation and ACB tracks in parallel; diarise all limitation dates."),

  new Paragraph({spacing:{before:240},children:[new TextRun({text:"Prepared for: Mr. Tarun Thadani  |  Counsel: Adv. Sujata Shirasi (+91 93216 13691)  |  Mumbai, 2026",size:18,color:"777777"})]}),
  rule(),
  new Paragraph({children:[new TextRun({text:"Disclaimer: AI-generated strategic draft for internal use; not legal advice. All steps to be vetted and executed by the Advocate on Record.",italics:true,size:18,color:"777777"})]}),
];

const doc=new Document({numbering:numberingConfig,styles:{default:{document:{run:{font:"Calibri",size:22}}}},
  sections:[{properties:{page:{size:A4,margin:MARGIN}},
    footers:{default:new Footer({children:[new Paragraph({border:{top:{style:BorderStyle.SINGLE,size:4,color:"CCCCCC",space:1}},tabStops:[{type:TabStopType.RIGHT,position:TabStopPosition.MAX}],children:[new TextRun({text:"Plan of Action — Tarun Thadani (DRAFT, not legal advice)",size:16,color:"888888"}),new TextRun({text:"\tPage ",size:16,color:"888888"}),new TextRun({children:[PageNumber.CURRENT],size:16,color:"888888"}),new TextRun({text:" of ",size:16,color:"888888"}),new TextRun({children:[PageNumber.TOTAL_PAGES],size:16,color:"888888"})]})]})},
    children}]});
Packer.toBuffer(doc).then(b=>{fs.writeFileSync("03_Plan_of_Action_Tarun_Thadani.docx",b);console.log("Doc 3 written");});
