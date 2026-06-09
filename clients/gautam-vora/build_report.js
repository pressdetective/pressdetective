const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  Header, Footer, AlignmentType, LevelFormat, HeadingLevel, BorderStyle,
  WidthType, ShadingType, PageNumber, ExternalHyperlink, PageBreak
} = require("docx");

const BLUE = "1F4E79", GREY = "595959", RED = "C00000", GREEN = "538135", AMBER = "BF8F00";
const border = { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" };
const borders = { top: border, bottom: border, left: border, right: border };
const cellMargins = { top: 80, bottom: 80, left: 120, right: 120 };

function h1(t){ return new Paragraph({ heading: HeadingLevel.HEADING_1, children:[new TextRun(t)] }); }
function h2(t){ return new Paragraph({ heading: HeadingLevel.HEADING_2, children:[new TextRun(t)] }); }
function p(t, o={}){ return new Paragraph({ spacing:{after:120}, children:[new TextRun({text:t,...o})] }); }
function bullet(t,l=0){ return new Paragraph({ numbering:{reference:"bullets",level:l}, spacing:{after:60},
  children: Array.isArray(t)?t:[new TextRun(t)] }); }
function num(t){ return new Paragraph({ numbering:{reference:"numbers",level:0}, spacing:{after:80},
  children: Array.isArray(t)?t:[new TextRun(t)] }); }

function hdrCell(t,w){ return new TableCell({ borders, width:{size:w,type:WidthType.DXA}, margins:cellMargins,
  shading:{fill:BLUE,type:ShadingType.CLEAR},
  children:[new Paragraph({children:[new TextRun({text:t,bold:true,color:"FFFFFF",size:18})]})] }); }
function cell(ch,w,fill){ const kids=Array.isArray(ch)?ch:[new Paragraph({children:[new TextRun({text:String(ch),size:18})]})];
  const o={borders,width:{size:w,type:WidthType.DXA},margins:cellMargins,children:kids};
  if(fill)o.shading={fill,type:ShadingType.CLEAR}; return new TableCell(o); }
function tc(t,w,fill,color){ return cell([new Paragraph({children:[new TextRun({text:t,size:18,color})]})],w,fill); }
function sev(s){ return s==="High"?RED:s==="Medium"?AMBER:GREEN; }

const LQ="“", RQ="”";

const invRows=[
  [`Wikipedia — ${LQ}Viveka Babajee${RQ}`,`Names Vora as her boyfriend; quotes the diary line ${LQ}you killed me, Gautam${RQ}. High-authority, permanent, top-ranking.`,"High","High","Very low"],
  [`Grokipedia — ${LQ}Viveka Babajee${RQ}`,"AI-generated encyclopedia entry repeating the relationship and the note. Rising visibility.","High","Medium","Low"],
  [`Yahoo News — ${LQ}…boyfriend arrested in Tikku murder${RQ}`,"Headline fuses both stories: ties the Babajee relationship to a murder arrest. Most damaging framing.","High","Medium","Low"],
  ["DNA India (multiple)",`Mix: ${LQ}clean chit to Gautam Vora${RQ} (favourable); ${LQ}family says she was in a relationship${RQ}; ${LQ}HC grants bail… Tikku murder${RQ}.`,"High","High","Low"],
  [`Business Standard — ${LQ}Court rejects bail of Gautam Vora${RQ}`,"Reports sessions-court bail rejection in the Palande/Tikku harbouring case.","High","Medium","Low"],
  [`Deccan Herald — ${LQ}clean chit to Vora${RQ}`,"Favourable: foul play ruled out, police clean chit (Aug 2010).","Low","Medium","n/a (asset)"],
  ["Indian Express archive (2010)",`${LQ}Viveka was not depressed, had matched kundali with Gautam.${RQ} Archived/premium.`,"Medium","Low","Low"],
  ["Open / Masala / OneIndia","Long-form and aggregator coverage of the suicide naming Vora.","Medium","Low","Low"],
  ["anujtikku.com (victim's family site)","Self-published trial narrative of the Tikku murder; names Vora. Sensitive — family of the deceased.","Medium","Low","Very low"],
  ["Dale Bhagwagar Media Group","PR-agency SEO pages built around both names; rank for the queries.","Medium","Medium","Medium"],
];

const invTable = new Table({ width:{size:9360,type:WidthType.DXA}, columnWidths:[2600,3300,1100,1100,1260],
  rows:[
    new TableRow({tableHeader:true,children:[hdrCell("Source / Property",2600),hdrCell("What it says",3300),hdrCell("Severity",1100),hdrCell("Visibility",1100),hdrCell("Removability",1260)]}),
    ...invRows.map(r=>new TableRow({children:[
      cell([new Paragraph({children:[new TextRun({text:r[0],size:18,bold:true})]})],2600),
      tc(r[1],3300), tc(r[2],1100,undefined,sev(r[2])), tc(r[3],1100), tc(r[4],1260),
    ]}))
  ]
});

const actRows=[
  ["P1",`Stand up an optimized professional identity (personal site + bio, refreshed LinkedIn, verified social handles) under ${LQ}Gautam Vora${RQ} so current, accurate pages exist to rank.`,"Suppression","0–4 weeks","Press Detective"],
  ["P1","Publish steady professional / thought-leadership content (markets, investing) on owned + third-party platforms to build ranking weight.","Suppression","Ongoing","Press Detective"],
  ["P2",`File targeted Google ${LQ}Results about you${RQ} / Right-to-be-Forgotten removal requests on the most damaging URLs, leading with the police clean chit and absence of conviction.`,"Removal","2–8 weeks","Press Detective + client"],
  ["P3","Engage a media lawyer to assess a de-indexing petition (Indian RTBF case law) for the oldest / most prejudicial links, given the clean chit.","Removal","1–3 months","External counsel"],
  ["P3","Approach Dale Bhagwagar Media Group to update or take down their name-built pages.","Removal","2–6 weeks","Press Detective"],
  ["P4","Wikipedia: via the article Talk page, with conflict of interest disclosed, request neutral phrasing and that the clean chit be reflected. Do not edit the article directly.","Correction","1–2 months","Press Detective"],
  ["P4","Grokipedia: use its correction / feedback channel to ensure the clean chit and no-conviction status are present.","Correction","1–2 months","Press Detective"],
  ["—","Set up ongoing monitoring (Google Alerts + monthly SERP audit) and a verification checkpoint at 90 days.","Monitoring","Ongoing","Press Detective"],
];

const actTable = new Table({ width:{size:9360,type:WidthType.DXA}, columnWidths:[900,4400,1560,1300,1200],
  rows:[
    new TableRow({tableHeader:true,children:[hdrCell("Priority",900),hdrCell("Action",4400),hdrCell("Type",1560),hdrCell("Horizon",1300),hdrCell("Lead",1200)]}),
    ...actRows.map(r=>new TableRow({children:[
      cell([new Paragraph({children:[new TextRun({text:r[0],size:18,bold:true})]})],900),
      tc(r[1],4400), tc(r[2],1560), tc(r[3],1300), tc(r[4],1200),
    ]}))
  ]
});

function srcLine(label,url){ return new Paragraph({ numbering:{reference:"numbers",level:0}, spacing:{after:40},
  children:[new TextRun({text:label+" — "}), new ExternalHyperlink({children:[new TextRun({text:url,style:"Hyperlink",size:18})],link:url})] }); }

const sources=[
  ["Wikipedia — Viveka Babajee","https://en.wikipedia.org/wiki/Viveka_Babajee"],
  ["Grokipedia — Viveka Babajee","https://grokipedia.com/page/Viveka_Babajee"],
  ["DNA India — Clean chit to Gautam Vora","https://www.dnaindia.com/lifestyle/report-viveka-babajee-suicide-case-foul-play-ruled-out-clean-chit-to-gautam-vora-1431391"],
  ["DNA India — Family says she was in a relationship with Gautam Vora","https://www.dnaindia.com/mumbai/report-viveka-babajee-case-family-says-she-was-in-relationship-with-gautam-vora-1403940"],
  ["DNA India — HC grants bail to stock broker Gautam Vora (Tikku)","https://www.dnaindia.com/mumbai/report-arun-tikku-murder-hc-grants-bail-to-stock-broker-gautam-vora-1688649/amp"],
  ["Business Standard — Palande case: court rejects bail of Gautam Vora","https://www.business-standard.com/article/pti-stories/palande-case-court-rejects-bail-of-gautam-vora-112050400480_1.html"],
  ["Deccan Herald — Foul play ruled out; clean chit to Vora","https://www.deccanherald.com/content/92844/viveka-suicide-case-foul-play.html"],
  ["Indian Express (archive, 2010)","https://indianexpress.com/article/cities/mumbai/viveka-was-not-depressed-had-matched-kundali-with-gautam-models-family/"],
  ["Yahoo News — Viveka Babajee's boyfriend arrested in Tikku murder","https://www.yahoo.com/news/viveka-babajee-s-boyfriend-arrested-in-tikku-murder.html"],
  ["DNA India — Arun Tikku murder case recap","https://www.dnaindia.com/mumbai/report-arun-tikku-murder-case-recap-1711730"],
  ["Open The Magazine — On the Death of a Supermodel","https://openthemagazine.com/shorts/on-the-death-of-a-supermodel/"],
  ["OneIndia — Viveka Babajee topic page","https://www.oneindia.com/topic/viveka-babajee"],
];

const doc = new Document({
  styles:{ default:{document:{run:{font:"Arial",size:21}}},
    paragraphStyles:[
      {id:"Heading1",name:"Heading 1",basedOn:"Normal",next:"Normal",quickFormat:true,
        run:{size:28,bold:true,font:"Arial",color:BLUE},paragraph:{spacing:{before:280,after:140},outlineLevel:0}},
      {id:"Heading2",name:"Heading 2",basedOn:"Normal",next:"Normal",quickFormat:true,
        run:{size:23,bold:true,font:"Arial",color:GREY},paragraph:{spacing:{before:180,after:100},outlineLevel:1}},
    ]},
  numbering:{config:[
    {reference:"bullets",levels:[
      {level:0,format:LevelFormat.BULLET,text:"•",alignment:AlignmentType.LEFT,style:{paragraph:{indent:{left:540,hanging:280}}}},
      {level:1,format:LevelFormat.BULLET,text:"–",alignment:AlignmentType.LEFT,style:{paragraph:{indent:{left:1080,hanging:280}}}},
    ]},
    {reference:"numbers",levels:[
      {level:0,format:LevelFormat.DECIMAL,text:"%1.",alignment:AlignmentType.LEFT,style:{paragraph:{indent:{left:540,hanging:280}}}},
    ]},
  ]},
  sections:[{
    properties:{page:{size:{width:12240,height:15840},margin:{top:1440,right:1440,bottom:1440,left:1440}}},
    headers:{default:new Header({children:[new Paragraph({
      border:{bottom:{style:BorderStyle.SINGLE,size:6,color:BLUE,space:1}},
      children:[new TextRun({text:"PRESS DETECTIVE  |  Confidential — Client Reputation Audit",size:16,color:GREY})],
    })]})},
    footers:{default:new Footer({children:[new Paragraph({
      alignment:AlignmentType.CENTER,
      children:[new TextRun({text:"Page ",size:16,color:GREY}),new TextRun({children:[PageNumber.CURRENT],size:16,color:GREY})],
    })]})},
    children:[
      new Paragraph({spacing:{after:60},children:[new TextRun({text:"ONLINE REPUTATION AUDIT & ACTION PLAN",bold:true,size:36,color:BLUE})]}),
      new Paragraph({spacing:{after:40},children:[new TextRun({text:"Client: Gautam Vora (stock broker, Mumbai)",size:24,bold:true})]}),
      new Paragraph({spacing:{after:240},children:[
        new TextRun({text:"Prepared by Press Detective   ",size:18,color:GREY}),
        new TextRun({text:"•  9 June 2026  •  Confidential",size:18,color:GREY}),
      ]}),

      h1("1. Executive summary"),
      p("Searches for the client's name are dominated by two unrelated legal episodes from over a decade ago, plus encyclopedia and aggregator pages that keep them permanently visible. The objective is not to deny the record but to ensure the most accurate, current and favourable facts — chief among them a police clean chit and the absence of any conviction — are what people find, and to push the prejudicial coverage off the first page over time."),
      bullet([new TextRun({text:"Storyline A — Viveka Babajee (2010): ",bold:true}),new TextRun("the model's death by suicide; a note named the client. Mumbai police ruled out foul play and gave him a clean chit.")]),
      bullet([new TextRun({text:"Storyline B — Arun Tikku murder (2012): ",bold:true}),new TextRun("the client was arrested for allegedly harbouring the prime accused, Vijay Palande; the Bombay High Court granted bail. This is the more reputationally serious of the two.")]),
      p("Realistic expectation: most of these are accurate news reports of real events and cannot simply be deleted on request. The winning strategy is roughly 70% suppression (building strong, current, accurate properties) and 30% targeted removal / correction where there is genuine leverage. A measurable shift in page-one results typically takes 3–9 months.",{italics:true}),

      h1("2. The two storylines"),
      h2("A. Viveka Babajee (2010)"),
      p(`Viveka Babajee, a Mauritian model (Miss Mauritius World 1993), was found dead at her Bandra, Mumbai residence on 25 June 2010. A diary entry reading ${LQ}you killed me, Gautam${RQ} was recovered. The client, described in coverage as her boyfriend and a stockbroker, was initially under scrutiny for abetment. In August 2010 police closed the investigation: forensic analysis ruled out foul play and a clean chit was issued. No charge was sustained.`),
      h2("B. Arun Tikku murder (2012)"),
      p("In 2012 the client was arrested for allegedly sheltering Vijay Palande — the prime accused in the murders of Arun Tikku and Karan Kakkad — including driving him, helping him check into a hotel and using a credit card to buy clothes. He was booked under sections 212, 202 and 225 of the IPC. A sessions court initially rejected bail; the Bombay High Court subsequently granted it. The final disposition of his role is not clearly documented in public sources."),
      new Paragraph({children:[new TextRun({text:"Action item: confirm with the client the documented final outcome of the Tikku matter (discharge / acquittal / pending). It materially changes what we can claim and request.",italics:true,color:RED,size:18})]}),

      new Paragraph({children:[new PageBreak()]}),
      h1("3. Footprint inventory"),
      p("What currently ranks for the client's name and the linked queries, with a working assessment of severity, search visibility and how removable each item is."),
      invTable,
      new Paragraph({spacing:{before:100},children:[new TextRun({text:`Note: the Deccan Herald and DNA ${LQ}clean chit${RQ} reports are assets, not liabilities — they should be amplified, not buried.`,size:18,italics:true,color:GREEN})]}),

      new Paragraph({children:[new PageBreak()]}),
      h1("4. Strategy"),
      h2("What can realistically be removed"),
      bullet("News archives (DNA, Deccan Herald, Indian Express, Business Standard, Yahoo): publishers very rarely unpublish accurate reporting. Removal is feasible only via a Google de-indexing / Right-to-be-Forgotten request or a court order. India has no RTBF statute, but several High Courts have ordered de-indexing of dated criminal coverage, particularly where the person was acquitted or never convicted."),
      bullet("Wikipedia & Grokipedia: a sourced mention cannot be deleted on request. The achievable goal is accuracy and neutrality — ensuring the clean chit and no-conviction status are present and the tone is not prejudicial. On Wikipedia this must go through the Talk page with the conflict of interest openly disclosed."),
      bullet("anujtikku.com: this is the victim's family's own site. Removal is highly unlikely and any approach would be insensitive. Leave it; out-rank it instead."),
      bullet("PR-agency pages (Dale Bhagwagar): commercially owned — a direct, polite takedown / update request is reasonable and may succeed."),
      h2("What we suppress"),
      p("Suppression means giving Google many strong, current, accurate pages about the client's professional life so the decade-old stories fall to page two or beyond:"),
      bullet("A clean personal website and a tight professional bio at his own name."),
      bullet("A fully built, active LinkedIn profile and verified handles on other major platforms."),
      bullet("Regular professional content — markets / investing commentary, interviews, guest articles — that earns ranking weight legitimately."),
      bullet("Listings in professional directories and any relevant associations."),
      p(`Because the name ${LQ}Gautam Vora${RQ} is shared by many people, a strong, distinct professional identity also helps Google disambiguate him away from the coverage.`),

      h1("5. Prioritized action plan"),
      actTable,

      h1("6. Guardrails"),
      p("These protect the client far more than they constrain him."),
      bullet("No fake reviews, fabricated articles, sock-puppet accounts or impersonation."),
      bullet("No deceptive Wikipedia editing or covert paid edits."),
      bullet(`No ${LQ}guaranteed removal${RQ} vendors or bogus DMCA / copyright claims to force takedowns — these are scams or legal exposure.`),
      bullet("No misrepresenting the record. Everything we publish or request leans on true facts: the police clean chit, the absence of any conviction, and the passage of time."),
      bullet([new TextRun({text:"Streisand-effect caution: ",bold:true}),new TextRun("aggressive or clumsy removal demands can revive dormant stories. We move quietly, lead with suppression, and reserve legal action for a few high-value targets.")]),

      h1("7. Suggested next steps"),
      num("Client confirms the final outcome of the Tikku / Palande matter and supplies any court documents."),
      num("Approve the suppression build (website, bio, LinkedIn, content cadence) so we can start this week."),
      num("Press Detective compiles the de-indexing request package for the top 3–4 most damaging URLs."),
      num("Book a media-law consult to scope a de-indexing petition."),
      num("Stand up monitoring; reconvene at 30 and 90 days to measure SERP movement."),

      new Paragraph({children:[new PageBreak()]}),
      h1("Appendix — sources reviewed"),
      ...sources.map(s=>srcLine(s[0],s[1])),
      new Paragraph({spacing:{before:200},children:[new TextRun({text:"This audit reflects publicly visible search results as of 9 June 2026 and is a strategic plan, not legal advice. Removal of court and news records may require qualified Indian legal counsel.",size:16,italics:true,color:GREY})]}),
      new Paragraph({spacing:{before:120},children:[new TextRun({text:"Note: this matter involves a death by suicide. All outreach should be handled with sensitivity toward the deceased and her family; the goal is accuracy and fair context, not erasure of a tragedy.",size:16,italics:true,color:GREY})]}),
    ],
  }],
});

Packer.toBuffer(doc).then(buf=>{
  fs.writeFileSync("Gautam_Vora_Reputation_Audit.docx",buf);
  console.log("written",buf.length);
});
