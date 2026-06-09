#!/usr/bin/env python3
"""encroachment_outreach.py — tailored emails to NGOs, media, government."""
import smtplib, ssl, os, time
from email.message import EmailMessage

HERE      = os.path.dirname(os.path.abspath(__file__))
TOKEN     = os.environ["ZEPTO_TOKEN"]
FROM_ADDR = "olympio.almeida@pressdetective.com"
FROM_NAME = "Olympio Almeida"
EVIDENCE  = os.path.join(HERE, "Evidence_Packet_FULL.pdf")
SENT_LOG  = []
ERROR_LOG = []

def send(subject, to, body, attach_evidence=False):
    m = EmailMessage()
    m["From"]    = f"{FROM_NAME} <{FROM_ADDR}>"
    m["To"]      = to
    m["Subject"] = subject
    m.set_content(body)
    if attach_evidence:
        with open(EVIDENCE, "rb") as f:
            m.add_attachment(f.read(), maintype="application", subtype="pdf",
                             filename="Evidence_Packet_Siolim_Encroachment.pdf")
    ctx = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.zeptomail.in", 465, context=ctx, timeout=300) as s:
        s.ehlo()
        s.login("emailapikey", TOKEN)
        s.send_message(m)

def do(label, subject, to, body, attach_evidence=False):
    print(f"  [{label}] -> {to} ...", end=" ", flush=True)
    try:
        send(subject, to, body, attach_evidence)
        SENT_LOG.append(f"OK  [{label}] {to}")
        print("OK")
    except Exception as e:
        ERROR_LOG.append(f"ERR [{label}] {to}: {e}")
        print(f"ERROR: {e}")
    time.sleep(10)

# ======================================================================
# NGO OUTREACH — warm, personal, invite to property
# ======================================================================

def ngo_body(greeting, org_desc, specific_ask):
    return (
        f"Dear {greeting},\n\n"
        "I hope this message finds you well. My name is Olympio Almeida and I am a "
        "long-time resident of Sodiem, Siolim, Bardez, Goa. I am writing to you today "
        "-- personally, not through any lawyer or agency -- because what has happened "
        "to my land and the trees on it needs a witness and a voice, and I believe "
        f"{org_desc}.\n\n"
        "For decades, my family has cared for a piece of land in Sodiem, Siolim "
        "(Survey No. 197/7, Gaunsawaddo). It is a quiet residential neighbourhood "
        "where trees grew, birds nested, and elderly neighbours could sleep through "
        "the night. That quiet has been destroyed.\n\n"
        'A commercial padel-court business -- calling itself the "Sunday Racquet and '
        'Social Club" -- has moved onto the plot. They built their courts on land they '
        "have no right to occupy. To make space, they cut down trees that had stood "
        "there for years. The courts now run from early morning until midnight, seven "
        "days a week, generating noise of 68 to 75 decibels -- more than ten times the "
        "legal limit for a residential area. My elderly neighbours at La Masseria, "
        "several of them with serious heart conditions, cannot sleep. And I cannot step "
        "onto a portion of my own land.\n\n"
        "What makes this especially painful is that this is not a new fight. Back in "
        "2008, the Village Panchayat itself revoked the construction licence for this "
        "very plot after its own inspection found buildings not as per the approved plan. "
        "I was the one who filed that complaint in 2008. Now, fifteen years later, the "
        "same land has been taken over and the trees cleared, as if that revocation "
        "never happened.\n\n"
        "I filed a detailed noise-pollution complaint with the Goa State Pollution "
        "Control Board in March 2026. Three months passed. No reply. No inspection. "
        "No action. Today, 9 June 2026, I have filed formal complaints simultaneously "
        "with the District Magistrate, TCP, Panchayat, Police and GSPCB, and RTI "
        "applications demanding licence records from all four authorities.\n\n"
        f"{specific_ask}\n\n"
        "I invite you to visit the site and see it for yourself. Come and stand on "
        "Gaunsawaddo, Sodiem, Siolim and look at the stumps where trees once stood. "
        "Meet the elderly residents who have not had an unbroken night's sleep in months. "
        "I am happy to share my full 26-page evidence file, the noise measurements, the "
        "photographs, and every official document.\n\n"
        "Please feel free to call me any time -- I pick up the phone.\n\n"
        "With respect and gratitude,\n"
        "Olympio Almeida\n"
        "Resident, Sodiem, Siolim, Bardez, Goa\n"
        "olympio.almeida@pressdetective.com\n"
        "Mobile: +91 98221 68112"
    )

NGOS = [
    ("Goa Foundation", "goafoundation@gmail.com",
     "Encroachment + Tree Cutting on My Land in Siolim -- Can Goa Foundation Help?",
     "the Goa Foundation team",
     "you have stood up for Goa's land and its people in more courtrooms than almost anyone else",
     "You have filed hundreds of PILs and know these corridors of power better than anyone. "
     "I need your guidance. The National Green Tribunal is one option. If you believe this "
     "case deserves support -- a PIL, an intervention, a letter, advice on the right advocate "
     "-- I would be deeply grateful. I am not asking for charity. I am asking for justice "
     "for a piece of Goa's land that is being destroyed in plain sight."),

    ("Konkan Dev Society", "directorexec.pdo@sdbpanjim.org",
     "Help Needed -- Encroachment & Tree Cutting on Residential Land in Siolim, Goa",
     "the Director",
     "the Konkan Development Society has long cared for this coast and its communities",
     "I would be grateful for any support you can offer -- documentation assistance, help "
     "navigating the authorities, connecting me with the right people, or simply lending "
     "your organisation's voice to this complaint. Knowing that a respected organisation "
     "is watching changes how officials respond."),

    ("CEE Goa", "ceegoa@ceeindia.org",
     "Trees Cut, Land Encroached in Siolim -- Requesting CEE Goa's Attention",
     "the CEE Goa team",
     "the Centre for Environmental Education has shaped how Goa understands and defends its natural heritage",
     "I am hoping you might be willing to document this case -- the before and after, the "
     "stumps where trees stood, the noise readings, the paper trail -- and perhaps amplify "
     "it through your network. Environmental education works best when it is grounded in "
     "real stories. This is as real as it gets."),

    ("WWF Goa", "wwfgso@sancharnet.in",
     "Wildlife Habitat & Trees Destroyed for Illegal Padel Courts -- Sodiem, Siolim, Goa",
     "the WWF Goa team",
     "WWF has consistently defended the habitats and natural cover that make Goa worth living in",
     "I am asking whether WWF Goa might be willing to document the tree loss or bring it to "
     "the attention of the Forest Department. Trees felled for this commercial venture were "
     "not just property -- they were habitat, shade, and part of the living fabric of this "
     "neighbourhood. I would welcome guidance on the legal process for the unauthorised "
     "tree felling under the Goa Preservation of Trees Act, 1984."),

    ("Nirmal Vishwa", "greenarc@sancharnet.in",
     "Appeal for Support -- Encroachment, Tree Cutting & Noise Pollution, Siolim, Goa",
     "the Nirmal Vishwa team",
     "Nirmal Vishwa has been a quiet, steady guardian of Goa's green spaces",
     "I am hoping you might be willing to visit the site, lend your voice to the complaint, "
     "or help connect this matter with the right authorities. Even a letter of support from "
     "a known environmental organisation makes a difference when approaching the GSPCB or "
     "the Collector's office."),

    ("Green Ray Foundation", "greenray@goenkar.com",
     "Illegal Tree Felling & Land Encroachment in Siolim -- Seeking Your Support",
     "the Green Ray Foundation",
     "Green Ray Foundation has worked to protect Goa's environment from precisely this kind of quiet destruction",
     "I am reaching out to ask whether you would be willing to visit and document the site, "
     "or to lend your voice as we push the GSPCB and the District Magistrate to act. "
     "Formal complaints were filed today. What we need now is witnesses who care."),

    ("Peaceful Society", "peaceful@goatelecom.com",
     "Plea for Help -- Commercial Club Encroaches on My Land, Fells Trees, Mapusa Area, Goa",
     "the Peaceful Society",
     "the Peaceful Society has worked at the grassroots to protect communities and their rights",
     "What I need most right now is for people who care about Goa's communities to know what "
     "is happening here. If you are able to visit, document, or help amplify this case -- "
     "through your networks, your contacts in the Panchayat, or your experience with similar "
     "matters in Mapusa and Bardez -- I would be deeply grateful."),

    ("Swami Vivekanand Env Brigade", "rpkerkar@yahoo.com",
     "Environmental Violation in Siolim -- Encroachment & Tree Cutting -- Your Support Needed",
     "Professor Kerkar",
     "your environmental awareness work has inspired many in Goa to stand up and speak",
     "I am writing to you as someone who has dedicated years to making Goa's people aware of "
     "what is being lost. I would value your guidance on how to approach this -- through the "
     "Forest Department, the Tree Authority, the GSPCB or the NGT. And if you are willing "
     "to lend your voice to the complaint, it would mean more than I can say."),

    ("Bailancho Manch", "bailanchomanch@gmail.com",
     "Land Encroachment & Tree Cutting in Siolim -- Requesting Bailancho Manch's Support",
     "the Bailancho Manch team",
     "Bailancho Manch has fought for land rights and justice for communities across Goa, especially for those who have no other voice",
     "My neighbours at La Masseria include elderly women who are unable to sleep and afraid "
     "to speak up alone. The operator of the club is well-connected locally. Your experience "
     "in land rights and your willingness to stand alongside communities is why I am writing. "
     "Please consider visiting and adding your voice."),
]

def send_ngos():
    print("\n=== NGO OUTREACH ===")
    for label, to, subject, greeting, org_desc, specific_ask in NGOS:
        body = ngo_body(greeting, org_desc, specific_ask)
        do(label, subject, to, body, attach_evidence=True)

# ======================================================================
# MEDIA OUTREACH — story pitch, invite to property
# ======================================================================

def media_body(salutation, outlet_desc, outlet_reason, outlet_name, specific_close):
    return (
        f"{salutation},\n\n"
        "STORY TIP: Illegal Padel Courts, Tree Felling & Encroachment in Siolim --\n"
        "Elderly Cardiac Patients Cannot Sleep. Authorities Silent for 3 Months.\n\n"
        f"My name is Olympio Almeida. I am a resident of Sodiem, Siolim, Bardez, Goa, "
        f"and I am writing to {outlet_desc} with a story that I believe {outlet_reason}.\n\n"
        "THE FACTS\n"
        '- A commercial padel-court business -- "Sunday Racquet and Social Club" -- has\n'
        "  occupied land in Gaunsawaddo, Sodiem, Siolim (Survey No. 197/7), including a\n"
        "  portion of my land, to which they have no right or title.\n"
        "- To build the courts, trees growing on the land were felled without any Tree\n"
        "  Authority permission under the Goa Preservation of Trees Act, 1984.\n"
        "- The courts run from approx. 7:00 a.m. until midnight, seven days a week,\n"
        "  generating 68-75 dB(A). The residential limit is 55 dB(A).\n"
        "- Senior citizens at adjacent La Masseria villas -- several with coronary artery\n"
        "  disease and multiple cardiac stents -- cannot sleep.\n"
        "- The plot had its construction licence revoked by the Village Panchayat in 2008\n"
        "  (Order V.P.S.S./2008-09/977) for unauthorised construction -- on my own complaint.\n\n"
        "THREE MONTHS OF OFFICIAL SILENCE\n"
        "A 26-page complaint with noise measurements, photographs and official documents was\n"
        "filed with the GSPCB on 9 March 2026. Three months. Not a single acknowledgement.\n\n"
        "TODAY'S ESCALATION (9 June 2026)\n"
        "- District Magistrate, North Goa: Section 152 BNSS application for immediate stop order\n"
        "- TCP Department, Mapusa: unauthorised commercial use in residential zone\n"
        "- Village Panchayat Siolim-Sodiem: violation of their own 2008 revocation order\n"
        "- Coastal Police Station, Siolim: noise nuisance + FIR for trespass/encroachment\n"
        "- GSPCB: re-filing with warning of NGT proceedings\n"
        "- RTI applications filed with all four authorities\n\n"
        f"INVITATION TO VISIT\n"
        f"I invite {outlet_name} to come to Sodiem, Siolim and see the site for yourself --\n"
        "the tree stumps, the courts that back onto people's homes, the elderly residents\n"
        "who have not had a peaceful night in months. I am available for interview at any time.\n"
        "The full 26-page evidence packet, noise measurements and photographs are ready to share.\n\n"
        f"{specific_close}\n\n"
        "Olympio Almeida\n"
        "Resident, Sodiem, Siolim, Bardez, Goa\n"
        "olympio.almeida@pressdetective.com\n"
        "Mobile: +91 98221 68112 (please call any time)"
    )

MEDIA = [
    ("Herald Editor", "editor@heraldgoa.in",
     "Story Tip: Illegal Padel Courts + Tree Felling + Encroachment in Siolim -- Elderly Cannot Sleep",
     "Dear Editor, O Heraldo",
     "Goa's oldest and most trusted newspaper",
     "belongs on the front page",
     "O Heraldo",
     "O Heraldo has been the voice of civic accountability in Goa for over a century. This "
     "story has everything -- encroachment, tree felling, official inaction, elderly residents "
     "in distress, and a 2008 precedent that was simply ignored. I trust you will find it "
     "worth investigating."),

    ("Herald News Desk", "news@heraldgoa.in",
     "News Tip: Illegal Padel Courts Encroach on Land, Fell Trees, Silence Elderly -- Siolim",
     "Dear News Desk, O Heraldo",
     "O Heraldo's news team",
     "is exactly the kind of story your readers expect you to pursue",
     "your reporter",
     "I am happy to meet your reporter at the site at a time that suits you."),

    ("The Goan Editor", "editor@thegoan.net",
     "Story for The Goan: Illegal Padel Club Encroaches, Fells Trees, Runs Until Midnight in Residential Siolim",
     "Dear Editor, The Goan",
     "The Goan -- which has described itself as a fierce watchdog on development versus environment",
     "is exactly the intersection of development, environment and civic failure that The Goan was founded to cover",
     "The Goan",
     "This is the kind of story The Goan was built for. A commercial operation on illegally-occupied "
     "land, trees felled without permission, official silence for three months, and elderly residents "
     "with heart conditions who cannot sleep. I am available for a full briefing."),

    ("The Goan Desk", "desk@thegoan.net",
     "Story Tip -- Encroachment, Tree Felling, Noise Pollution: Illegal Padel Club in Siolim Unchecked",
     "Dear News Desk, The Goan",
     "The Goan's news desk",
     "will want to follow up on today's formal complaints to five different authorities",
     "your team",
     "Today, formal complaints were filed simultaneously with the District Magistrate, TCP, "
     "Panchayat, Police and GSPCB. RTI applications are also running. This story is actively "
     "moving -- I can brief your reporter in full."),

    ("Goa Chronicle", "editor@goachronicle.com",
     "Investigative Tip -- Padel Club Encroaches, Fells Trees in Siolim: 3 Months of Official Silence",
     "Dear Editor, Goa Chronicle",
     "Goa Chronicle's investigative desk",
     "is exactly the kind of exposé Goa Chronicle does best",
     "Goa Chronicle",
     "Goa Chronicle has broken important stories on encroachment and official negligence before. "
     "This case has documentary evidence going back to 2008 -- a Panchayat revocation order that "
     "was ignored, a GSPCB complaint that received no reply, and a commercial operation running "
     "without any visible licence from any authority. The full document trail is available."),

    ("Prudent Media TV", "info@prudentmedia.in",
     "TV Story -- Illegal Padel Courts, Tree Felling & Encroachment in Siolim; Elderly Cannot Sleep",
     "Dear Prudent Media",
     "Prudent Media -- Goa's most-watched news channel",
     "has the kind of visual impact that makes officials act when words alone have not",
     "Prudent Media's cameras",
     "Come and film the tree stumps. Come at night when the courts are running at full volume "
     "at 11:00 p.m. and record it. That footage -- from Goa's most-watched channel -- will "
     "do more in 24 hours than three months of written complaints. I will be at the site "
     "whenever you wish to come."),

    ("Scroll.in", "tips@scroll.in",
     "Tip: Goa -- Illegal Padel Club Occupies Residential Land, Fells Trees, Runs Until Midnight",
     "Dear Scroll.in team",
     "Scroll.in",
     "has the national reach to make this a story about how environmental and land laws are not enforced in coastal India",
     "Scroll.in",
     "Scroll.in's environment coverage has the national reach to turn this into a conversation "
     "about how India's noise pollution rules, tree protection laws and land revenue codes are "
     "routinely ignored in tourist-economy coastal zones. I am happy to provide a full briefing."),

    ("The Wire", "editor@thewire.in",
     "Tip for The Wire -- Goa: Commercial Club Encroaches, Fells Trees; 3 Months of GSPCB Silence",
     "Dear The Wire Editorial Team",
     "The Wire",
     "matters precisely because it covers the slow failure of institutions to protect individuals against powerful commercial interests",
     "The Wire",
     "The Wire has covered institutional failure and environmental injustice in India with the "
     "depth this story deserves. This case has documented evidence going back to 2008, a clear "
     "timeline of official inaction, vulnerable elderly residents, and a traceable paper trail. "
     "I am available for a full interview."),

    ("Down To Earth", "dtedit@cse.org.in",
     "Story Pitch: Goa -- Noise Pollution, Tree Felling & Encroachment; GSPCB Silent for 3 Months",
     "Dear Down To Earth editorial team",
     "Down To Earth -- India's leading environment magazine",
     "is precisely the kind of on-the-ground violation of India's noise and tree-protection laws that Down To Earth documents",
     "Down To Earth",
     "The noise readings (68-75 dB against 55 dB residential limit), the felled trees, the "
     "GSPCB complaint with no reply -- this is a textbook case of how India's environmental "
     "protection framework fails at the last mile of enforcement. Down To Earth's coverage "
     "and the Centre for Science and Environment's voice would be enormously powerful here."),

    ("All India Radio Goa", "airgoa@gmail.com",
     "Story Suggestion for AIR Goa -- Noise Pollution, Encroachment & Tree Felling in Siolim",
     "Dear All India Radio Goa",
     "All India Radio Goa",
     "reaches every corner of Goa, especially the interior communities that other media does not",
     "AIR Goa",
     "A story on noise pollution and environmental violations affecting senior citizens in a "
     "residential neighbourhood of Siolim -- with 68-75 decibel measurements and trees that "
     "were felled -- would resonate with listeners across Bardez and beyond. I am available "
     "for a phone interview or an in-person recording at the site."),
]

def send_media():
    print("\n=== MEDIA OUTREACH ===")
    for label, to, subject, salutation, outlet_desc, outlet_reason, outlet_name, specific_close in MEDIA:
        body = media_body(salutation, outlet_desc, outlet_reason, outlet_name, specific_close)
        do(label, subject, to, body, attach_evidence=True)

# ======================================================================
# GOVERNMENT — newly-contacted bodies
# ======================================================================

def g_cm_grievance():
    body = (
        "To,\nThe Chief Minister's Grievance Cell,\nGovernment of Goa.\n\n"
        "Subject: URGENT GRIEVANCE -- Encroachment on Residential Land, Illegal Tree\n"
        "Felling and Noise Pollution -- Sunday Racquet and Social Club, Gaunsawaddo,\n"
        "Sodiem, Siolim, Bardez, North Goa -- Three Months of Institutional Inaction.\n\n"
        "Respected Sir / Madam,\n\n"
        "I, Olympio Almeida, resident of Sodiem, Siolim, Bardez, Goa, am writing to the\n"
        "Hon'ble Chief Minister's Grievance Cell as a last resort after three months of\n"
        "silence from the Goa State Pollution Control Board.\n\n"
        "THE CORE GRIEVANCE\n"
        "1. A commercial padel-court operation called Sunday Racquet and Social Club has\n"
        "   encroached upon my land at Survey No. 197/7, Gaunsawaddo, Sodiem, Siolim.\n"
        "2. Trees growing on the plot were felled without any Tree Authority permission\n"
        "   under the Goa Preservation of Trees Act, 1984.\n"
        "3. The operation runs from 7:00 a.m. until midnight daily, generating 68-75\n"
        "   dB(A) -- more than double the 55 dB(A) residential limit.\n"
        "4. Senior citizens at adjacent La Masseria villas, several with coronary artery\n"
        "   disease and multiple cardiac stents, cannot sleep.\n"
        "5. The same plot had its construction licence revoked by Village Panchayat\n"
        "   Siolim-Sodiem in 2008 (Order Ref. V.P.S.S./2008-09/977, 24.09.2008)\n"
        "   for unauthorised construction -- on my own complaint.\n\n"
        "INSTITUTIONAL INACTION\n"
        "A 26-page complaint with noise measurements and documentary evidence was filed\n"
        "with the GSPCB on 9 March 2026. As of 9 June 2026: no acknowledgement,\n"
        "no inspection, no action. Today, formal complaints were filed with the District\n"
        "Magistrate (u/s 152 BNSS), TCP, Panchayat, Police and GSPCB. RTI applications\n"
        "filed with all four authorities.\n\n"
        "RELIEF REQUESTED\n"
        "(a) Direct GSPCB to respond to the 9 March 2026 complaint within 7 days\n"
        "(b) Direct the District Magistrate, North Goa, to act on the S.152 BNSS application\n"
        "(c) Ensure a joint inspection by TCP, Panchayat and GSPCB officials\n"
        "(d) Protect the rights of an ordinary Goan resident against an unlicensed\n"
        "    commercial operation on his own land\n\n"
        "I would be grateful for an acknowledgement and a reference number.\n\n"
        "Yours faithfully,\n"
        "Olympio Almeida, Resident, Sodiem, Siolim, Bardez, Goa\n"
        "olympio.almeida@pressdetective.com | +91 98221 68112"
    )
    do("CM Grievance",
       "Urgent Grievance -- Encroachment, Tree Felling & Noise Pollution, Siolim -- 3 Months of GSPCB Silence",
       "cmgoa.grievance@gov.in", body, attach_evidence=True)

def g_dslr():
    body = (
        "To,\nThe Director,\nDirectorate of Settlement and Land Records (DSLR),\nGoa.\n\n"
        "Subject: COMPLAINT -- Encroachment on Survey No. 197/7, Gaunsawaddo (Sodiem),\n"
        "Siolim, Bardez, North Goa -- Request for Boundary Demarcation Survey.\n\n"
        "Sir / Madam,\n\n"
        "I, Olympio Almeida, resident of Sodiem, Siolim, Bardez, Goa, am the owner of\n"
        "land in Sodiem, Siolim. I am writing to report an encroachment and to request\n"
        "a formal boundary demarcation survey.\n\n"
        "THE ENCROACHMENT\n"
        'A commercial padel-court business operating as "Sunday Racquet and Social Club"\n'
        "at House No. 47/3, Gaunsawaddo, Sodiem, Siolim (Survey No. 197/7) has encroached\n"
        "upon a portion of my land without any right, title or consent. Trees growing on\n"
        "the encroached portion were felled to make way for the padel courts, without any\n"
        "Tree Authority permission under the Goa Preservation of Trees Act, 1984.\n\n"
        "HISTORY\n"
        "Village Panchayat Siolim-Sodiem issued Revocation Order V.P.S.S./2008-09/977\n"
        "(24.09.2008) revoking the construction licence for a structure at Survey No. 197/7\n"
        "for unauthorised construction -- on a complaint I filed in 2008. Despite that\n"
        "revocation, structures and now a commercial operation have continued on this land.\n\n"
        "REQUEST\n"
        "(a) Conduct a boundary demarcation survey to precisely establish the boundaries\n"
        "    of Survey No. 197/7 and adjacent plots including any land in my name in Sodiem\n"
        "(b) Issue a survey report usable as evidence before the District Magistrate and\n"
        "    if necessary the Bombay High Court, Goa Bench\n"
        "(c) If any government or comunidade land has also been encroached upon in this\n"
        "    area, initiate appropriate revenue encroachment proceedings\n\n"
        "I am available to meet at any time and will provide all relevant title documents.\n\n"
        "Yours faithfully,\n"
        "Olympio Almeida, Resident, Sodiem, Siolim, Bardez, Goa\n"
        "olympio.almeida@pressdetective.com | +91 98221 68112"
    )
    do("DSLR",
       "Complaint & Request for Boundary Demarcation -- Encroachment at Sy. 197/7, Gaunsawaddo, Sodiem, Siolim",
       "dir-land.goa@nic.in", body, attach_evidence=True)

def g_info_publicity():
    body = (
        "To,\nThe Director,\nDepartment of Information and Publicity,\nGovernment of Goa.\n\n"
        "Subject: For Public Record -- Encroachment on Residential Land, Tree Felling and\n"
        "Noise Pollution in Siolim -- Ordinary Resident Seeks Justice.\n\n"
        "Sir / Madam,\n\n"
        "My name is Olympio Almeida. I am a resident of Sodiem, Siolim, Bardez, Goa. I am\n"
        "writing to this Department not to make a political complaint but to place on official\n"
        "public record the situation that I and my neighbours are living through.\n\n"
        "WHAT HAS HAPPENED\n"
        'A commercial padel-court business has occupied and built upon land at Survey No.\n'
        "197/7, Gaunsawaddo, Sodiem, Siolim, including a portion of my land. Trees that grew\n"
        "on this land were cut down without any Tree Authority permission under the Goa\n"
        "Preservation of Trees Act, 1984. The operation runs from 7:00 a.m. until midnight\n"
        "daily at 68-75 dB(A), while the legal residential limit is 55 dB(A). Elderly\n"
        "residents with heart conditions cannot sleep.\n\n"
        "THREE MONTHS OF SILENCE FROM GSPCB\n"
        "A detailed, 26-page complaint was filed with the GSPCB on 9 March 2026. Not a\n"
        "single acknowledgement in three months. Formal escalation was filed today to the\n"
        "District Magistrate, TCP, Panchayat, Police and GSPCB itself.\n\n"
        "WHY I AM WRITING HERE\n"
        "The Goa Government has repeatedly promised to be responsive to ordinary residents.\n"
        "I am one of those residents. I am not a developer, not a litigant by choice. I am\n"
        "a man who is asking for his land back and for the trees that were cut on it to be\n"
        "acknowledged. I hope that by writing to this Department, at minimum, there is a\n"
        "formal record that this matter is known to the Government of Goa.\n\n"
        "If the Department of Information and Publicity believes the public should know about\n"
        "this matter, I am available to speak to any journalist or publication the Department\n"
        "might direct toward this story.\n\n"
        "Yours faithfully,\n"
        "Olympio Almeida, Resident, Sodiem, Siolim, Bardez, Goa\n"
        "olympio.almeida@pressdetective.com | +91 98221 68112"
    )
    do("Dept Info & Publicity",
       "For Public Record -- Encroachment, Tree Felling & Noise Pollution in Siolim -- Resident Seeks Justice",
       "dipgoa@gmail.com", body, attach_evidence=False)

def g_ngt():
    body = (
        "To,\nThe Registrar,\nNational Green Tribunal (Western Zone Bench),\nPune.\n\n"
        "Subject: NOTICE OF INTENTION TO FILE APPLICATION -- Noise Pollution, Illegal Tree\n"
        "Felling and Encroachment -- Sunday Racquet and Social Club, Survey No. 197/7,\n"
        "Gaunsawaddo, Sodiem, Siolim, Bardez, North Goa -- GSPCB Inaction for Three Months.\n\n"
        "Sir / Madam,\n\n"
        "I, Olympio Almeida, resident of Sodiem, Siolim, Bardez, Goa, am writing to this\n"
        "Hon'ble Tribunal to place on record the violations occurring in my neighbourhood and\n"
        "my intention to file a formal Application if the statutory authorities fail to act.\n\n"
        "THE ENVIRONMENTAL VIOLATIONS\n"
        "1. NOISE POLLUTION -- Sunday Racquet and Social Club operates outdoor padel courts\n"
        "   at Survey No. 197/7, Gaunsawaddo, Sodiem, Siolim from 7:00 a.m. until midnight\n"
        "   daily, generating 68-75 dB(A). This exceeds the Noise Pollution (Regulation and\n"
        "   Control) Rules, 2000 residential daytime limit (55 dB) by 13-20 dB, and the\n"
        "   night-time limit (45 dB) by 23-30 dB. Amplified music continues past 10:00 p.m.\n"
        "   in violation of the loudspeaker prohibition.\n\n"
        "2. ILLEGAL TREE FELLING -- Trees growing on the plot were felled to construct the\n"
        "   padel courts without any Tree Authority permission under the Goa Preservation of\n"
        "   Trees Act, 1984. This is an offence under that Act and an environmental violation\n"
        "   within this Hon'ble Tribunal's jurisdiction.\n\n"
        "3. ENCROACHMENT -- The operator has occupied a portion of my land (Survey No. 197/7,\n"
        "   Gaunsawaddo, Sodiem) without title or consent. The same plot had its construction\n"
        "   licence revoked by Village Panchayat Siolim-Sodiem in 2008 (V.P.S.S./2008-09/977).\n\n"
        "GSPCB INACTION -- THREE MONTHS\n"
        "A 26-page complaint with noise measurements and photographic evidence was filed with\n"
        "the GSPCB on 9 March 2026. As of 9 June 2026 -- 92 days -- no acknowledgement, no\n"
        "inspection, no action. This constitutes dereliction of statutory duty.\n\n"
        "TODAY'S ESCALATION (9 June 2026)\n"
        "Formal complaints filed with: District Magistrate (u/s 152 BNSS), TCP Mapusa,\n"
        "Panchayat Siolim-Sodiem, Coastal PS Siolim, GSPCB (re-filing). RTI applications\n"
        "filed with GSPCB, TCP, Panchayat and Collectorate.\n\n"
        "INTENTION TO FILE\n"
        "If the above authorities do not act within 30 days, I intend to file a formal\n"
        "Application before this Hon'ble Tribunal under Section 18 of the National Green\n"
        "Tribunal Act, 2010, seeking:\n"
        "(a) Directions to GSPCB to immediately inspect and suspend the illegal operation\n"
        "(b) Directions to the Tree Authority to inquire into the illegal tree felling and\n"
        "    order restoration or compensation\n"
        "(c) Directions to the District Magistrate to act under S.152 BNSS\n"
        "(d) Compensation for the environmental damage and loss of tree cover\n\n"
        "I respectfully request guidance from this Registry on the correct procedure for\n"
        "filing in the Western Zone and the documents to be compiled.\n\n"
        "The 26-page Evidence Packet is attached for the Registry's reference.\n\n"
        "Yours faithfully,\n"
        "Olympio Almeida, Resident, Sodiem, Siolim, Bardez, Goa\n"
        "olympio.almeida@pressdetective.com | +91 98221 68112"
    )
    do("NGT Western Zone",
       "Notice of Intention to File NGT Application -- Noise Pollution, Tree Felling, Encroachment -- Siolim, Goa",
       "ngtwz@nic.in", body, attach_evidence=True)

def send_government():
    print("\n=== GOVERNMENT (NEW BODIES) ===")
    g_cm_grievance()
    g_dslr()
    g_info_publicity()
    g_ngt()

# ======================================================================
# FINAL REPORT
# ======================================================================

def send_report():
    sent_text = "\n".join("  " + s for s in SENT_LOG) if SENT_LOG else "  none"
    err_text  = "\n".join("  " + e for e in ERROR_LOG) if ERROR_LOG else "  None."
    total     = len(SENT_LOG) + len(ERROR_LOG)
    body = f"""Gautam,

Encroachment resources outreach campaign completed -- {len(SENT_LOG)}/{total} sent.

Every email was personally tailored for the recipient: their expertise, their
audience, their angle. Every one invites them to visit the property in Sodiem,
Siolim, and gives Olympio's mobile number (+91 98221 68112).

==============================================================
NGOs CONTACTED (9)
==============================================================
1. Goa Foundation (goafoundation@gmail.com) -- asked for PIL/NGT guidance
2. Konkan Dev Society (directorexec.pdo@sdbpanjim.org) -- documentation + navigation
3. CEE Goa (ceegoa@ceeindia.org) -- document and amplify the case
4. WWF Goa (wwfgso@sancharnet.in) -- document tree loss; engage Forest Dept
5. Nirmal Vishwa (greenarc@sancharnet.in) -- site visit + letter of support
6. Green Ray Foundation (greenray@goenkar.com) -- document and lend voice
7. Peaceful Society (peaceful@goatelecom.com) -- amplify through Mapusa/Bardez networks
8. Swami Vivekanand Env. Brigade (rpkerkar@yahoo.com) -- guidance on Tree Authority/NGT
9. Bailancho Manch (bailanchomanch@gmail.com) -- stand with elderly women residents

==============================================================
MEDIA PITCHED (10 outlets)
==============================================================
1. O Heraldo Editor (editor@heraldgoa.in) -- front-page story, century of accountability
2. O Heraldo News Desk (news@heraldgoa.in) -- reporter site visit
3. The Goan Editor (editor@thegoan.net) -- development vs environment watchdog angle
4. The Goan Desk (desk@thegoan.net) -- following today's 5 authority complaints
5. Goa Chronicle (editor@goachronicle.com) -- 2008 paper trail; investigative exposé
6. Prudent Media TV (info@prudentmedia.in) -- film stumps + 11pm noise; visual impact
7. Scroll.in (tips@scroll.in) -- national coastal enforcement failure angle
8. The Wire (editor@thewire.in) -- institutional failure + vulnerable elderly residents
9. Down To Earth (dtedit@cse.org.in) -- noise data + tree felling; CSE voice
10. All India Radio Goa (airgoa@gmail.com) -- broadcast story; interior Bardez reach

==============================================================
GOVERNMENT (4 new bodies)
==============================================================
1. CM Grievance Cell (cmgoa.grievance@gov.in) -- direct GSPCB/DM to act within 7 days
2. DSLR (dir-land.goa@nic.in) -- formal boundary demarcation survey requested
3. Dept of Info & Publicity (dipgoa@gmail.com) -- placed on official public record
4. NGT Western Zone Pune (ngtwz@nic.in) -- notice of intention to file; asked for procedure

==============================================================
DELIVERY STATUS
==============================================================
{sent_text}

Errors:
{err_text}

==============================================================
THE PLAYBOOK THAT WORKS IN GOA
==============================================================
Complaint + Media + NGO Backing = Government action.

You now have all three in motion:
- 5 formal complaints to authorities (filed this morning)
- 4 RTI applications (30-day clock running)
- 9 NGOs contacted with invitation to visit
- 10 media outlets pitched with evidence
- 4 new government bodies added (CM, DSLR, Info Dept, NGT)

If even ONE Goa outlet (O Heraldo, The Goan, Prudent Media TV) runs a story,
officials at GSPCB, TCP and the Panchayat will respond within days.

If Goa Foundation or Bailancho Manch engage, an NGT application can be filed
within 2 weeks with their support.

Keep every reply -- a WhatsApp from a journalist, an acknowledgement from the
CM Grievance Cell, an email from an NGO saying they are coming to visit -- and
forward it to info@pressdetective.com.

PressDetective | 9 June 2026
olympio.almeida@pressdetective.com"""

    print("\n=== FINAL REPORT ===")
    print("  [Report -> gavora + info] ...", end=" ", flush=True)
    try:
        m = EmailMessage()
        m["From"]    = f"{FROM_NAME} <{FROM_ADDR}>"
        m["To"]      = "gavora@gmail.com"
        m["Cc"]      = "info@pressdetective.com"
        m["Subject"] = f"[PressDetective] Encroachment Campaign -- {len(SENT_LOG)}/{total} Sent -- NGOs + Media + Govt"
        m.set_content(body)
        ctx = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.zeptomail.in", 465, context=ctx, timeout=300) as s:
            s.ehlo()
            s.login("emailapikey", TOKEN)
            s.send_message(m)
        print("OK")
    except Exception as e:
        print(f"ERROR: {e}")

# ======================================================================
def main():
    send_ngos()
    send_media()
    send_government()
    send_report()
    ok  = len(SENT_LOG)
    err = len(ERROR_LOG)
    print(f"\n{'='*55}")
    print(f"All done. {ok} sent, {err} errors.")
    if ERROR_LOG:
        for e in ERROR_LOG: print(f"  {e}")

if __name__ == "__main__":
    main()
