const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, AlignmentType,
  LevelFormat, BorderStyle, TabStopType, TabStopPosition, PageNumber, Footer
} = require("docx");

const A4 = { width: 11906, height: 16838 };
const MARGIN = { top: 1440, right: 1440, bottom: 1440, left: 1440 };

const center=(t,o={})=>new Paragraph({alignment:AlignmentType.CENTER,spacing:{after:o.after??120,before:o.before??0},children:[new TextRun({text:t,bold:o.bold??false,size:o.size??24,allCaps:o.caps??false})]});
const rule=()=>new Paragraph({spacing:{after:120,before:60},border:{bottom:{style:BorderStyle.SINGLE,size:6,color:"000000",space:1}},children:[]});
const h=(t)=>new Paragraph({spacing:{before:240,after:120},children:[new TextRun({text:t,bold:true,size:24,underline:{}})]});
const p=(runs,o={})=>{const c=Array.isArray(runs)?runs:[new TextRun({text:runs,size:24})];return new Paragraph({alignment:o.align??AlignmentType.JUSTIFIED,spacing:{after:o.after??160,line:276},children:c});};
const num=(t,ref)=>new Paragraph({numbering:{reference:ref,level:0},alignment:AlignmentType.JUSTIFIED,spacing:{after:140,line:276},children:[new TextRun({text:t,size:24})]});
const blank=()=>new Paragraph({children:[],spacing:{after:120}});
const bt=(t)=>new TextRun({text:t,size:24});
const bb=(t)=>new TextRun({text:t,size:24,bold:true});

const numberingConfig={config:[
  {reference:"grounds",levels:[{level:0,format:LevelFormat.UPPER_LETTER,text:"%1.",alignment:AlignmentType.LEFT,style:{paragraph:{indent:{left:720,hanging:360}}}}]},
  {reference:"facts",levels:[{level:0,format:LevelFormat.DECIMAL,text:"%1.",alignment:AlignmentType.LEFT,style:{paragraph:{indent:{left:720,hanging:360}}}}]},
  {reference:"prayer",levels:[{level:0,format:LevelFormat.LOWER_LETTER,text:"(%1)",alignment:AlignmentType.LEFT,style:{paragraph:{indent:{left:720,hanging:420}}}}]},
]};

const disclaimer=[
  rule(),
  new Paragraph({shading:{type:"clear",fill:"F2F2F2"},spacing:{after:80,before:80},children:[new TextRun({text:"DRAFT FOR REVIEW BY ADVOCATE ON RECORD — NOT LEGAL ADVICE",bold:true,size:20})]}),
  p([new TextRun({text:"This is an AI-generated working draft prepared from the case materials supplied. It must be reviewed, verified and settled by the Advocate on Record (Adv. Sujata Shirasi) before filing. Items in [square brackets] are placeholders to be confirmed against certified copies. The FIR predates 01 July 2024, so the Code of Criminal Procedure, 1973 and the Indian Penal Code, 1860 continue to apply (saved by Section 531 BNSS); the BNSS equivalent of Section 482 CrPC is Section 528 BNSS — verify at filing. A petition to quash and a revision against refusal of discharge are alternative/parallel remedies; counsel should decide which to press, and avoid pursuing both on identical grounds simultaneously without disclosure to the Court.",size:20,italics:true})],{after:120}),
  rule(),
];

const children=[
  center("IN THE HIGH COURT OF JUDICATURE AT BOMBAY",{bold:true,caps:true,size:26,after:40}),
  center("ORDINARY ORIGINAL CRIMINAL JURISDICTION",{bold:true,size:22,after:60}),
  center("CRIMINAL APPLICATION (QUASHING) NO. ________ OF 2026",{bold:true,size:24,after:40}),
  center("(Under Section 482 of the Code of Criminal Procedure, 1973 — alternatively Article 226/227 of the Constitution of India)",{size:20,after:120}),
  rule(),
  p([bb("IN THE MATTER OF FIR / C.R. No. 0654 of 2022 registered at Dadar Police Station, Mumbai, and the charge-sheet filed pursuant thereto, in so far as they relate to the Applicant;")],{after:120}),
  p([bb("AND IN THE MATTER OF Sections 384, 385, 387, 506 read with 34 of the Indian Penal Code, 1860 [confirm against charge-sheet];")],{after:160}),
  p([bb("Mr. Tarun Thadani"),bt(", aged about ____ years, Indian inhabitant, founder of Dharte (dharte.com), residing at [address], Mumbai – [PIN].")],{after:20}),
  new Paragraph({alignment:AlignmentType.RIGHT,spacing:{after:40},children:[new TextRun({text:"… APPLICANT",bold:true,size:24})]}),
  new Paragraph({alignment:AlignmentType.RIGHT,spacing:{after:160},children:[new TextRun({text:"(Original Accused No. ____)",size:20})]}),
  center("VERSUS",{bold:true,size:22,after:120}),
  num("The State of Maharashtra (through Dadar Police Station, Mumbai), through the Office of the Public Prosecutor, High Court of Bombay.","facts"),
  num("Mr. Abhishek Badriprasad Saraf, aged about ____ years, residing at 3rd Floor, Esplanade House, 29, Hazarimal Somani Marg, Mumbai – 400001 (Original First Informant / Complainant).","facts"),
  new Paragraph({alignment:AlignmentType.RIGHT,spacing:{after:160},children:[new TextRun({text:"… RESPONDENTS",bold:true,size:24})]}),
  rule(),
  center("TO,",{size:22,after:20}),
  p([bt("THE HON’BLE THE CHIEF JUSTICE AND THE OTHER HON’BLE PUISNE JUDGES OF THE HIGH COURT OF JUDICATURE AT BOMBAY.")],{after:120}),
  p([bb("THE HUMBLE APPLICATION OF THE APPLICANT ABOVENAMED MOST RESPECTFULLY SHEWETH:")],{after:160}),

  h("I. NATURE AND PRAYER OF THE APPLICATION"),
  p([bt("By this Application the Applicant seeks the quashing of FIR No. 0654 of 2022 registered at Dadar Police Station, and of all consequent proceedings including the charge-sheet, in so far as they relate to the Applicant, on the ground that the said proceedings constitute a gross abuse of the process of law and that even taking the prosecution case at its highest, no offence whatsoever is disclosed against the Applicant.")],{after:160}),

  h("II. FACTS"),
  num("The Applicant is a law-abiding entrepreneur and the founder of Dharte (dharte.com), with an unblemished record and standing in society.","facts"),
  num("On 02 June 2022 a private social event was organised at a restaurant in Worli, Mumbai. The Applicant’s involvement was confined solely to sending invitations to the event. The Applicant was not present at the venue at any time material to the alleged incident.","facts"),
  num("During the event, a personal altercation is alleged to have occurred between Mr. Ali Asgar Merchant and Respondent No. 2. The Applicant had no part in it.","facts"),
  num("On 04 June 2022, Respondent No. 2 lodged an online complaint alleging only assault. The complaint contained no allegation of extortion, monetary demand or threat, and ascribed no role to the Applicant. A copy of the said complaint is annexed and marked Exhibit ‘A’.","facts"),
  num("No FIR was registered on the original complaint. After an unexplained delay of nearly two months, Respondent No. 2 materially altered his version and, for the first time, levelled a false allegation of extortion of ₹1 crore.","facts"),
  num("On the strength of this altered version, FIR No. 0654 of 2022 was registered on or about 12/13 August 2022 implicating, inter alia, the Applicant. A copy of the FIR is annexed and marked Exhibit ‘B’. No accused was summoned or examined and no call records, messages or financial transactions were verified prior to registration.","facts"),
  num("It is pertinent that Respondent No. 2 is himself the subject of independent allegations of fraud, forgery and misuse of a power of attorney concerning the heritage property ‘Esplanade House’ (Martin Burn Ltd. / Fatehpuria family), reflecting a pattern of misuse of legal process. [Subject to relevance and admissibility.]","facts"),
  num("A charge-sheet has since been filed and the Applicant’s application for discharge was rejected by the learned Sessions Court by order dated 31 March 2024. [Where a revision against the said order is also preferred, the same be disclosed to this Hon’ble Court.]","facts"),

  h("III. GROUNDS FOR QUASHING"),
  p([bt("The Applicant submits that the present case falls squarely within the parameters laid down by the Hon’ble Supreme Court in State of Haryana v. Bhajan Lal, 1992 Supp (1) SCC 335, for the exercise of the power to quash, and urges the following grounds:")],{after:120}),
  num("BECAUSE even accepting the allegations in the FIR and charge-sheet in their entirety and at face value, they do not prima facie constitute any offence against the Applicant or make out a case against him.","grounds"),
  num("BECAUSE the allegations are absurd and inherently improbable, the Applicant having admittedly not been present at the venue and his role being limited to sending invitations — facts on which no reasonable person could conclude that an offence is made out against him.","grounds"),
  num("BECAUSE the introduction of the ₹1 crore extortion allegation for the first time after a delay of nearly two months, when it was conspicuously absent from the original complaint, demonstrates that the proceeding is manifestly attended with mala fides and has been instituted with an ulterior motive to wreak vengeance and to falsely implicate the Applicant.","grounds"),
  num("BECAUSE Section 34 IPC cannot be pressed into service against the Applicant absent any prima facie material of common intention or participation; presence and a shared intention are sine qua non, both of which are wholly absent.","grounds"),
  num("BECAUSE the registration of the FIR is vitiated by patent procedural illegality — no accused was examined, and no verification of evidence was undertaken — which, coupled with the antecedents of the first informant, renders the prosecution against the Applicant an abuse of process.","grounds"),
  num("BECAUSE the continuation of criminal proceedings against the Applicant, who is demonstrably innocent, would result in serious miscarriage of justice and cause grave and irreparable prejudice to his reputation, profession and family, particularly given the prejudicial media reporting already occasioned.","grounds"),
  num("BECAUSE no useful purpose will be served by subjecting the Applicant to the ordeal of a full trial when the proceedings against him are doomed to end in acquittal on the existing material, and the inherent powers of this Hon’ble Court ought to be exercised to prevent abuse of process and to secure the ends of justice.","grounds"),

  h("IV. INTERIM RELIEF"),
  p([bt("Pending the hearing and final disposal of this Application, the Applicant prays that all further proceedings arising out of FIR No. 0654 of 2022, in so far as they relate to the Applicant, be stayed, the Applicant having made out a strong prima facie case, the balance of convenience being in his favour, and grave and irreparable harm being likely to ensue if interim protection is not granted.")],{after:120}),

  h("V. PRAYER"),
  p([bt("The Applicant therefore most respectfully prays that this Hon’ble Court may be pleased to:")],{after:120}),
  num("quash and set aside FIR No. 0654 of 2022 registered at Dadar Police Station, Mumbai, together with the charge-sheet and all proceedings consequent thereto, in so far as they relate to the Applicant;","prayer"),
  num("pending the hearing and final disposal of this Application, stay all further proceedings against the Applicant arising out of the said FIR and charge-sheet;","prayer"),
  num("grant such other and further reliefs as this Hon’ble Court may deem fit and proper in the interest of justice.","prayer"),
  blank(),
  p([bb("AND FOR THIS ACT OF KINDNESS, THE APPLICANT, AS IN DUTY BOUND, SHALL EVER PRAY.")],{after:240}),

  new Paragraph({children:[new TextRun({text:"Place: Mumbai",size:24})],spacing:{after:40}}),
  new Paragraph({children:[new TextRun({text:"Dated this ____ day of __________ 2026.",size:24})],spacing:{after:240}}),
  new Paragraph({alignment:AlignmentType.RIGHT,children:[new TextRun({text:"__________________________",size:24})],spacing:{after:10}}),
  new Paragraph({alignment:AlignmentType.RIGHT,children:[new TextRun({text:"Advocate for the Applicant",size:24})],spacing:{after:10}}),
  new Paragraph({alignment:AlignmentType.RIGHT,children:[new TextRun({text:"Adv. Sujata Shirasi  |  Mob: +91 93216 13691",size:22})],spacing:{after:240}}),
  new Paragraph({alignment:AlignmentType.RIGHT,children:[new TextRun({text:"__________________________",size:24})],spacing:{after:10}}),
  new Paragraph({alignment:AlignmentType.RIGHT,children:[new TextRun({text:"Applicant — Tarun Thadani",size:24})],spacing:{after:240}}),

  h("VERIFICATION"),
  p([bt("I, Tarun Thadani, the Applicant abovenamed, do hereby state and declare that the contents of the foregoing paragraphs are true and correct to the best of my knowledge, information and belief, and that I believe the same to be true. Solemnly affirmed at Mumbai on this ____ day of __________ 2026.")],{after:240}),
  new Paragraph({alignment:AlignmentType.RIGHT,children:[new TextRun({text:"__________________________",size:24})],spacing:{after:10}}),
  new Paragraph({alignment:AlignmentType.RIGHT,children:[new TextRun({text:"Tarun Thadani (Applicant / Deponent)",size:24})],spacing:{after:200}}),

  ...disclaimer,
];

function buildDoc(children,footerTitle){
  return new Document({numbering:numberingConfig,styles:{default:{document:{run:{font:"Times New Roman",size:24}}}},
    sections:[{properties:{page:{size:A4,margin:MARGIN}},
      footers:{default:new Footer({children:[new Paragraph({border:{top:{style:BorderStyle.SINGLE,size:4,color:"999999",space:1}},tabStops:[{type:TabStopType.RIGHT,position:TabStopPosition.MAX}],children:[new TextRun({text:footerTitle,size:16,color:"666666"}),new TextRun({text:"\tPage ",size:16,color:"666666"}),new TextRun({children:[PageNumber.CURRENT],size:16,color:"666666"}),new TextRun({text:" of ",size:16,color:"666666"}),new TextRun({children:[PageNumber.TOTAL_PAGES],size:16,color:"666666"})]})]})},
      children}]});
}
Packer.toBuffer(buildDoc(children,"Sec.482 Quashing Petition — Tarun Thadani — DRAFT")).then(b=>{fs.writeFileSync("02_Section_482_Quashing_Petition_Tarun_Thadani.docx",b);console.log("Doc 2 written");});
