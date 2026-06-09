const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, AlignmentType,
  LevelFormat, BorderStyle, TabStopType, TabStopPosition, PageNumber,
  Footer
} = require("docx");

const A4 = { width: 11906, height: 16838 };
const MARGIN = { top: 1440, right: 1440, bottom: 1440, left: 1440 };

function center(text, opts = {}) {
  return new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: opts.after ?? 120, before: opts.before ?? 0 },
    children: [new TextRun({ text, bold: opts.bold ?? false, size: opts.size ?? 24, allCaps: opts.caps ?? false, underline: opts.underline ? {} : undefined })]
  });
}
function rule() {
  return new Paragraph({ spacing: { after: 120, before: 60 }, border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: "000000", space: 1 } }, children: [] });
}
function h(text) {
  return new Paragraph({ spacing: { before: 240, after: 120 }, children: [new TextRun({ text, bold: true, size: 24, underline: {} })] });
}
function p(runs, opts = {}) {
  const children = Array.isArray(runs) ? runs : [new TextRun({ text: runs, size: 24 })];
  return new Paragraph({ alignment: opts.align ?? AlignmentType.JUSTIFIED, spacing: { after: opts.after ?? 160, line: 276 }, indent: opts.indent, children });
}
function num(text, ref) {
  return new Paragraph({ numbering: { reference: ref, level: 0 }, alignment: AlignmentType.JUSTIFIED, spacing: { after: 140, line: 276 }, children: [new TextRun({ text, size: 24 })] });
}
function blank() { return new Paragraph({ children: [], spacing: { after: 120 } }); }
function bt(text){ return new TextRun({ text, size:24 }); }
function bb(text){ return new TextRun({ text, size:24, bold:true }); }

const numberingConfig = {
  config: [
    { reference: "grounds", levels: [{ level: 0, format: LevelFormat.UPPER_LETTER, text: "%1.", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
    { reference: "facts", levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
    { reference: "prayer", levels: [{ level: 0, format: LevelFormat.LOWER_LETTER, text: "(%1)", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 720, hanging: 420 } } } }] },
    { reference: "bul", levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
  ]
};

const disclaimer = [
  rule(),
  new Paragraph({ shading: { type: "clear", fill: "F2F2F2" }, spacing: { after: 80, before: 80 }, children: [new TextRun({ text: "DRAFT FOR REVIEW BY ADVOCATE ON RECORD — NOT LEGAL ADVICE", bold: true, size: 20 })] }),
  p([new TextRun({ text: "This is an AI-generated working draft prepared from the case materials supplied. It must be reviewed, verified and settled by the Advocate on Record (Adv. Sujata Shirasi) before filing. All items in [square brackets] are placeholders requiring confirmation against the certified copies of the FIR, charge-sheet and the impugned order. Section references follow the Code of Criminal Procedure, 1973 (CrPC) and the Indian Penal Code, 1860 (IPC), which continue to govern this matter as the FIR predates 01 July 2024 (saved by Section 531 BNSS / Section 358 BNS). The BNSS equivalents (revision – s.438/442; inherent powers – s.528) should be cross-checked at filing.", size: 20, italics: true })], { after: 120 }),
  rule(),
];

const doc1Children = [
  center("IN THE HIGH COURT OF JUDICATURE AT BOMBAY", { bold: true, caps: true, size: 26, after: 40 }),
  center("ORDINARY ORIGINAL CRIMINAL JURISDICTION", { bold: true, size: 22, after: 60 }),
  center("CRIMINAL REVISION APPLICATION NO. ________ OF 2026", { bold: true, size: 24, after: 40 }),
  center("(Under Sections 397 read with 401 of the Code of Criminal Procedure, 1973)", { size: 20, after: 120 }),
  rule(),
  p([bb("IN THE MATTER OF the order dated 31 March 2024 passed by the learned Additional Sessions Judge, Greater Bombay, at [Sessions Court — confirm], below the application for discharge (Exh. ____) in Sessions Case No. ______ of 20____, arising out of C.R. / FIR No. 0654 of 2022 registered at Dadar Police Station, Mumbai;")], { after: 120 }),
  p([bb("AND IN THE MATTER OF Sections 384, 385, 387, 506 read with 34 of the Indian Penal Code, 1860 [and such other sections as appear in the charge-sheet — confirm];")], { after: 160 }),
  p([bb("Mr. Tarun Thadani"), bt(", aged about ____ years, Indian inhabitant, founder of Dharte (dharte.com), residing at [address], Mumbai – [PIN].")], { after: 20 }),
  new Paragraph({ alignment: AlignmentType.RIGHT, spacing: { after: 40 }, children: [new TextRun({ text: "… APPLICANT", bold: true, size: 24 })] }),
  new Paragraph({ alignment: AlignmentType.RIGHT, spacing: { after: 160 }, children: [new TextRun({ text: "(Original Accused No. ____)", size: 20 })] }),
  center("VERSUS", { bold: true, size: 22, after: 120 }),
  num("The State of Maharashtra (through Dadar Police Station, Mumbai), to be served through the Office of the Public Prosecutor, High Court of Bombay.", "facts"),
  num("Mr. Abhishek Badriprasad Saraf, aged about ____ years, residing at 3rd Floor, Esplanade House, 29, Hazarimal Somani Marg, Mumbai – 400001 (Original First Informant / Complainant).", "facts"),
  new Paragraph({ alignment: AlignmentType.RIGHT, spacing: { after: 160 }, children: [new TextRun({ text: "… RESPONDENTS", bold: true, size: 24 })] }),
  rule(),
  center("TO,", { size: 22, after: 20 }),
  p([bt("THE HON’BLE THE CHIEF JUSTICE AND THE OTHER HON’BLE PUISNE JUDGES OF THE HIGH COURT OF JUDICATURE AT BOMBAY.")], { after: 120 }),
  p([bb("THE HUMBLE REVISION APPLICATION OF THE APPLICANT ABOVENAMED MOST RESPECTFULLY SHEWETH:")], { after: 160 }),

  h("I. SYNOPSIS"),
  p([bt("The Applicant, an entrepreneur with no connection to the alleged offence, has been falsely arraigned as an accused in a fabricated case of assault and extortion. His only role was to send invitations to a private social event; he was admittedly "), bb("not present"), bt(" at the venue when the alleged altercation took place between two other persons. Critically, the allegation of ₹1 crore extortion was "), bb("wholly absent"), bt(" from the first informant’s original online complaint dated 04 June 2022 and surfaced only after a deliberate delay of nearly two months, when the version was materially altered. No accused was summoned or examined, and no call records, messages or financial transactions were verified before the FIR was registered. Despite there being no material whatsoever to connect the Applicant with any offence, the learned Sessions Court, by the impugned order dated 31 March 2024, declined to discharge him. The present Revision Application is preferred against that erroneous order.")], { after: 160 }),

  h("II. FACTS GIVING RISE TO THE APPLICATION"),
  num("That a private social event was organised on 02 June 2022 at a restaurant in Worli, Mumbai. The Applicant’s involvement in the said event was strictly and solely limited to sending out invitations. The Applicant was not present at the venue at any time relevant to the alleged incident.", "facts"),
  num("That during the said event, a purely personal altercation is alleged to have taken place between Mr. Ali Asgar Merchant and Respondent No. 2 (Mr. Abhishek Badriprasad Saraf). The Applicant neither participated in, nor witnessed, nor facilitated the said altercation, being absent from the venue.", "facts"),
  num("That on 04 June 2022, Respondent No. 2 lodged an online police complaint. The said complaint alleged only assault. It contained no allegation whatsoever of extortion, monetary demand, threat or blackmail, and did not attribute any role to the Applicant.", "facts"),
  num("That as no FIR came to be registered on the basis of the original complaint, Respondent No. 2, after an unexplained delay of nearly two months, materially altered his version and, for the first time, introduced a wholly new and false allegation of extortion of ₹1 crore.", "facts"),
  num("That on the basis of this belatedly improved and altered version, FIR No. 0654 of 2022 came to be registered at Dadar Police Station on or about 12/13 August 2022, implicating, inter alia, the Applicant. It is the Applicant’s case that the FIR was registered without any application of mind and contrary to settled procedure, in that: (i) none of the accused, including the Applicant, were summoned or examined prior to registration; (ii) no verification of call data records, messages or financial transactions was undertaken; and (iii) no independent material was gathered to support the extortion allegation.", "facts"),
  num("That the bona fides of Respondent No. 2 are gravely in doubt. He is independently the subject of serious allegations of fraud, forgery and misuse of a power of attorney in relation to the heritage property ‘Esplanade House’ (Martin Burn Ltd. / Fatehpuria family), demonstrating a propensity to misuse legal and quasi-legal processes. [To be substantiated through the relevant records, subject to relevance and admissibility.]", "facts"),
  num("That upon completion of investigation, a charge-sheet came to be filed and the matter was committed to the Court of Sessions, being Sessions Case No. ______ of 20____.", "facts"),
  num("That the Applicant preferred an application for discharge under Section 227 of the CrPC, contending that there existed no material on record to even prima facie connect him with the alleged offence.", "facts"),
  num("That by the impugned order dated 31 March 2024, the learned Additional Sessions Judge was pleased to reject the Applicant’s discharge application. Being aggrieved, the Applicant approaches this Hon’ble Court. The certified copy of the impugned order is annexed hereto and marked Exhibit ‘A’.", "facts"),

  h("III. GROUNDS"),
  p([bt("Being aggrieved by the impugned order dated 31 March 2024, the Applicant craves leave to urge the following grounds, without prejudice to one another:")], { after: 120 }),
  num("BECAUSE the learned Sessions Court failed to appreciate that there is no material on record, whether in the FIR, the statements under Section 161 CrPC, or the charge-sheet, that even prima facie connects the Applicant with the commission of any offence.", "grounds"),
  num("BECAUSE on the prosecution’s own showing the Applicant was not present at the venue and his role was limited to sending invitations — conduct that is wholly innocuous and incapable of constituting any offence under Sections 384/385/387 or 506 IPC, whether read with Section 34 or otherwise.", "grounds"),
  num("BECAUSE the learned Court ignored the most telling circumstance, namely that the allegation of extortion was entirely absent from the original complaint dated 04 June 2022 and was introduced for the first time after a deliberate delay of nearly two months. Such a material improvement, unexplained and uncorroborated, ought to have been treated as a strong circumstance pointing to false implication.", "grounds"),
  num("BECAUSE invocation of Section 34 IPC requires a prima facie case of common intention and participation; mere sending of invitations, in the absence of presence or any overt act, cannot in law sustain a charge with the aid of Section 34.", "grounds"),
  num("BECAUSE the registration of the FIR was vitiated by procedural impropriety — no accused was summoned or examined, and no verification of call records, messages or financial transactions was undertaken — rendering the very foundation of the prosecution against the Applicant suspect.", "grounds"),
  num("BECAUSE at the stage of charge the Court is required to sift and weigh the material to ascertain whether a prima facie case exists, and where the material does not disclose grave suspicion against the accused, the accused is entitled to be discharged. The learned Court applied the wrong test and proceeded on conjecture.", "grounds"),
  num("BECAUSE the impugned order is a non-speaking order to the extent that it does not deal with the Applicant’s specific and distinct case (absence from the venue; limited role; absence of the extortion allegation in the original complaint), and instead rejects the application on a generalised footing common to all accused.", "grounds"),
  num("BECAUSE continuation of the prosecution against the Applicant amounts to an abuse of the process of the Court and will cause grave and irreparable harm to his reputation, profession and personal life, as is already evident from the prejudicial press reporting that has ensued.", "grounds"),
  num("BECAUSE an order rejecting a discharge application is not a purely interlocutory order within the meaning of Section 397(2) CrPC but an intermediate / quasi-final order, and is therefore amenable to the revisional jurisdiction of this Hon’ble Court.", "grounds"),

  h("IV. MAINTAINABILITY AND LIMITATION"),
  p([bt("The present Revision Application is maintainable under Sections 397 read with 401 of the CrPC, the impugned order being an intermediate order affecting the rights of the Applicant. The Application is filed within limitation; to the extent of any delay occasioned by [obtaining the certified copy / bona fide reasons], the Applicant craves leave to file an appropriate application for condonation of delay. No other Revision Application on the same cause of action has been filed by the Applicant before this Hon’ble Court or the Court of Sessions.")], { after: 120 }),

  h("V. INTERIM RELIEF"),
  p([bt("Pending the hearing and final disposal of this Revision Application, the Applicant prays that further proceedings in Sessions Case No. ______ of 20____ pending before the learned Sessions Court, in so far as they relate to the Applicant, be stayed, as the Applicant has a strong prima facie case and the balance of convenience lies entirely in his favour.")], { after: 120 }),

  h("VI. PRAYER"),
  p([bt("The Applicant therefore most respectfully prays that this Hon’ble Court may be pleased to:")], { after: 120 }),
  num("call for the records and proceedings of Sessions Case No. ______ of 20____ and of the discharge application decided by the impugned order dated 31 March 2024;", "prayer"),
  num("quash and set aside the impugned order dated 31 March 2024 passed by the learned Additional Sessions Judge, Greater Bombay, in so far as it rejects the Applicant’s discharge application, and consequently discharge the Applicant from Sessions Case No. ______ of 20____ arising out of FIR No. 0654 of 2022, Dadar Police Station;", "prayer"),
  num("pending the hearing and final disposal of this Application, stay the further proceedings against the Applicant in the said Sessions Case;", "prayer"),
  num("grant such other and further reliefs as this Hon’ble Court may deem fit and proper in the facts and circumstances of the case and in the interest of justice.", "prayer"),
  blank(),
  p([bb("AND FOR THIS ACT OF KINDNESS, THE APPLICANT, AS IN DUTY BOUND, SHALL EVER PRAY.")], { after: 240 }),

  new Paragraph({ children: [new TextRun({ text: "Place: Mumbai", size: 24 })], spacing: { after: 40 } }),
  new Paragraph({ children: [new TextRun({ text: "Dated this ____ day of __________ 2026.", size: 24 })], spacing: { after: 240 } }),
  new Paragraph({ alignment: AlignmentType.RIGHT, children: [new TextRun({ text: "__________________________", size: 24 })], spacing: { after: 10 } }),
  new Paragraph({ alignment: AlignmentType.RIGHT, children: [new TextRun({ text: "Advocate for the Applicant", size: 24 })], spacing: { after: 10 } }),
  new Paragraph({ alignment: AlignmentType.RIGHT, children: [new TextRun({ text: "Adv. Sujata Shirasi  |  Mob: +91 93216 13691", size: 22 })], spacing: { after: 240 } }),
  new Paragraph({ alignment: AlignmentType.RIGHT, children: [new TextRun({ text: "__________________________", size: 24 })], spacing: { after: 10 } }),
  new Paragraph({ alignment: AlignmentType.RIGHT, children: [new TextRun({ text: "Applicant — Tarun Thadani", size: 24 })], spacing: { after: 240 } }),

  h("VERIFICATION"),
  p([bt("I, Tarun Thadani, the Applicant abovenamed, do hereby state and declare that what is stated in the foregoing paragraphs is true and correct to the best of my knowledge, information and belief, and that I believe the same to be true. Solemnly affirmed at Mumbai on this ____ day of __________ 2026.")], { after: 240 }),
  new Paragraph({ alignment: AlignmentType.RIGHT, children: [new TextRun({ text: "__________________________", size: 24 })], spacing: { after: 10 } }),
  new Paragraph({ alignment: AlignmentType.RIGHT, children: [new TextRun({ text: "Tarun Thadani (Applicant / Deponent)", size: 24 })], spacing: { after: 200 } }),

  ...disclaimer,
];

function buildDoc(children, footerTitle) {
  return new Document({
    numbering: numberingConfig,
    styles: { default: { document: { run: { font: "Times New Roman", size: 24 } } } },
    sections: [{
      properties: { page: { size: A4, margin: MARGIN } },
      footers: { default: new Footer({ children: [ new Paragraph({ border: { top: { style: BorderStyle.SINGLE, size: 4, color: "999999", space: 1 } }, tabStops: [{ type: TabStopType.RIGHT, position: TabStopPosition.MAX }], children: [ new TextRun({ text: footerTitle, size: 16, color: "666666" }), new TextRun({ text: "\tPage ", size: 16, color: "666666" }), new TextRun({ children: [PageNumber.CURRENT], size: 16, color: "666666" }), new TextRun({ text: " of ", size: 16, color: "666666" }), new TextRun({ children: [PageNumber.TOTAL_PAGES], size: 16, color: "666666" }) ] }) ] }) },
      children
    }]
  });
}

Packer.toBuffer(buildDoc(doc1Children, "Criminal Revision Application — Tarun Thadani — DRAFT")).then(b => {
  fs.writeFileSync("01_Criminal_Revision_Application_Tarun_Thadani.docx", b);
  console.log("Doc 1 written");
});
