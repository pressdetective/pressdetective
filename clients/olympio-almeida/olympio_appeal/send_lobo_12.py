import smtplib, ssl, time, os
from email.message import EmailMessage

PW   = "FzspzmcI-DE4s1JIp7HU3A"
FROM = "Olympio Almeida <olympio.almeida@pressdetective.com>"
ADDR = "olympio.almeida@pressdetective.com"

def bridge_send(msg):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False; ctx.verify_mode = ssl.CERT_NONE
    with smtplib.SMTP("127.0.0.1", 1025, timeout=120) as s:
        s.ehlo(); s.starttls(context=ctx)
        s.login(ADDR, PW)
        s.send_message(msg)

def zepto_send(msg):
    token = os.environ.get("ZEPTO_TOKEN", "")
    if not token:
        raise RuntimeError("ZEPTO_TOKEN not set")
    ctx = ssl.create_default_context()
    with smtplib.SMTP("smtp.zeptomail.in", 587, timeout=30) as s:
        s.ehlo(); s.starttls(context=ctx)
        s.login("emailapikey", token)
        s.send_message(msg)

def send_with_fallback(msg):
    try:
        bridge_send(msg); return "bridge"
    except Exception as be:
        if "2011" in str(be) or "frozen" in str(be).lower() or "limit" in str(be).lower():
            print(f"\n  [Bridge frozen, trying ZeptoMail...]", end=" ", flush=True)
            zepto_send(msg); return "zepto"
        raise

# Delilah Lobo direct constituency office
TO_LOBO = "Delilah Lobo MLA Siolim <mlasil.gvs@gov.in>"

# Full CC -- MLAs (unique addresses), all departments, press, PressDetective
CC = ", ".join([
    # Assembly Secretariat (covers Speaker + several MLAs sharing this address)
    "sec-assembly.goa@nic.in",
    # CM
    "mla.sanquelim.gvs@gov.in",
    # MLAs with individual emails
    "yugjit.33@gmail.com",
    "pravinarlekar4pernem@gmail.com",
    "mlashetye03bicholim@gmail.com",
    "mla.tivim.gvs@gov.in",
    "mla.mapusa.gvs@gov.in",
    "mla.calangute.gvs@gov.in",
    "kedarnaikoffcebetim@gmail.com",
    "atanasiomonserrate10@gmail.com",
    "rudolf.fernandes2707@gmail.com",
    "borkarviresh@gmail.com",
    "premendra@mailvenus.com",
    "drdeviyarane.mla.poriem@gmail.com",
    "mla.poriem.gvs@gov.in",
    "govindforgoa@gmail.com",
    "mla.dabolim.gvs@gov.in",
    "vasantonio1661@yahoo.com",
    "mla.nuvem.gvs@gov.in",
    "mla.margao.gvs@gov.in",
    "venzy4aapbenaulim@gmail.com",
    "dajisalkar@gmail.com",
    "mla.marcaim.gvs@gov.in",
    "mla.curchorem.gvs@gov.in",
    "ganeshgaonkar5909@gmail.com",
    # Siolim Panchayats
    "vp-siolimsodiem.goa@gov.in",
    "sec-siolimsodiem.goa@gov.in",
    "vp-siolimmarna.goa@gov.in",
    "sec-siolimmarna.goa@gov.in",
    "ddp-north.goa@nic.in",
    "panch-vig.goa@nic.in",
    # Administration
    "coll-north.goa@nic.in",
    "addcoll1-north.goa@nic.in",
    "sdm-mapusa.goa@nic.in",
    "mam-bardez.goa@nic.in",
    "stp-mapusa.goa@nic.in",
    "tcp-squad.goa@nic.in",
    "dir-land.goa@nic.in",
    "bdo-bardez1.goa@gov.in",
    "cmgoa.grievance@gov.in",
    # Pollution / Environment / Forest
    "chairperson-gspcb.goa@nic.in",
    "ms-gspcb.goa@nic.in",
    "dir-env.goa@nic.in",
    "dcfnorth-forest.goa@nic.in",
    "ms-gczma.goa@gov.in",
    "ngtwz@nic.in",
    # Police
    "pi-anjuna.goa@nic.in",
    "sdpo-mapusa.goa@nic.in",
    "spnorth@goapolice.gov.in",
    # Press
    "editor@goachronicle.com",
    "info@prudentmedia.in",
    "editor@thegoan.net",
    "desk@thegoan.net",
    "airgoa@gmail.com",
    # PressDetective
    "info@pressdetective.com",
])

FACTS = """CASE FACTS FOR REFERENCE:
- Property: Survey No. 197/7, Gaunsawaddo, Sodiem, Siolim, Bardez, Goa
- Illegal establishment: "Sunday Racquet and Social Club", House No. 47/3
- Panchayat Revocation Order: Ref V.P.S.S./2008-09/977, dated 24 Sep 2008 --
  issued on my own complaint, never enforced in 18 years
- Noise: 68-75 dB(A) measured on my property every Sunday
  (statutory limit: 55 dB(A) day / 45 dB(A) night)
- Trees felled on my land without Tree Authority permission
  (Goa Preservation of Trees Act 1984)
- Encroachment on my private land, Survey No. 197/7
- MLA Delilah Lobo publicly inaugurated this establishment"""

FOOTER = """
I remain respectfully yours,

Olympio Almeida
Resident, Sodiem, Siolim, Bardez, Goa
olympio.almeida@pressdetective.com

Represented by PressDetective (pressdetective.com)

---
This is a formal civic communication. All parties on copy are being kept
informed as witnesses to this appeal for justice. If you have received this
in error or wish to be removed from future correspondence, please reply with
UNSUBSCRIBE in the subject line."""

emails = [

    # ── 1 ── Personal Plea
    {
        "subject": "Respected MLA Delilah Lobo -- I Have Been Trying to Reach You -- Please Respond to a Suffering Constituent",
        "body": f"""Respected MLA Delilah Lobo,

I am Olympio Almeida, a resident of Sodiem, Siolim -- your constituency.
I am writing to you with great humility and with a heavy heart.

I have been trying to reach you by phone and by message for many days.
I have not received any response. I do not know if my calls have been
seen. I do not know if you are aware of my situation. I am giving you
the benefit of the doubt and writing again today.

The Sunday Racquet and Social Club, an establishment operating on my land
at Survey No. 197/7, Gaunsawaddo, Sodiem, Siolim, has been causing
severe noise pollution, encroaching on my property, and felling trees on
my land without any legal permission -- for years.

What troubles me most, Respected MLA, is this: the Siolim-Sodiem
Panchayat itself issued a Revocation Order (Ref V.P.S.S./2008-09/977)
against this establishment on 24 September 2008 -- eighteen years ago --
on my very own complaint. That order was never enforced.

And yet, I have seen photographs of you inaugurating this same
establishment. I say this not to embarrass you, but because I am confused
and I need your help. Were you aware at the time that it was built on
encroached land? Were you told it had a valid licence?

I am not an educated man in legal matters. I am simply a resident asking
his elected representative for help.

To the press and all officials on this correspondence: I humbly request
that you note my attempts to reach MLA Lobo and help ensure that she is
able to respond to this matter, which is entirely within her constituency
and directly concerns a constituent's home, land, and health.

To all MLAs copied: I appeal to you as fellow elected representatives of
the people of Goa -- please encourage your colleague to respond.

{FACTS}
{FOOTER}""",
    },

    # ── 2 ── The Inauguration Question
    {
        "subject": "MLA Delilah Lobo -- A Respectful Question: How Did You Come to Inaugurate an Establishment Built on Encroached Land?",
        "body": f"""Respected MLA Delilah Lobo,

I write to you once again, as I have been unable to reach you by phone or
message. I write with respect, and I write only with the truth.

A matter of public record: you have inaugurated the "Sunday Racquet and
Social Club" located at House No. 47/3, Gaunsawaddo, Sodiem, Siolim.

Another matter of public record: the Siolim-Sodiem Village Panchayat
issued Revocation Order Ref V.P.S.S./2008-09/977 on 24 September 2008
against this very plot, on my complaint. The establishment on this land
is illegal. The encroachment on my property (Survey No. 197/7) has never
been legally resolved.

I do not accuse you of knowing this at the time. You may have been misled
by those who invited you to inaugurate it. You may have been assured that
all paperwork was in order. I am asking -- with full respect -- for your
version of events.

Respected MLA, an elected representative's presence at the inauguration
of a venue carries the implied endorsement of that representative. When
that venue turns out to be built on someone's encroached private land,
that representative deserves an opportunity to clarify their position.

I am offering you that opportunity now, publicly, in the presence of your
colleagues in the Assembly, the administration, and the press.

To the press and officials on this correspondence: I ask you to note this
question and, if you are able, to seek a response from MLA Lobo on this
specific point. The people of Siolim deserve to understand how an
establishment operating in violation of a Panchayat order received the
honour of an MLA inauguration.

To the Goa Legislative Assembly Secretariat: I request that this
correspondence be placed on record as a constituent's formal communication
to their elected representative.

{FACTS}
{FOOTER}""",
    },

    # ── 3 ── The 2008 Order
    {
        "subject": "18 Years of Non-Enforcement: Panchayat Order Ref V.P.S.S./2008-09/977 -- MLA Delilah Lobo, Why Has No One Acted?",
        "body": f"""Respected MLA Delilah Lobo,

Today I write about a single document: Panchayat Revocation Order
Ref V.P.S.S./2008-09/977, issued on 24 September 2008.

This order was issued by the Siolim-Sodiem Village Panchayat on the basis
of my own complaint. It ordered that the licence of the establishment
operating at Survey No. 197/7, Gaunsawaddo, Sodiem, Siolim, be revoked.

That was eighteen years ago.

The establishment is still operating. The noise continues every Sunday.
The encroachment on my land has not been reversed. The trees that were
felled on my property without Tree Authority permission have not been
replanted. Nobody has been held to account.

MLA Lobo, you are the elected representative for this constituency. You
have a relationship with the Panchayat. You have spoken at village
functions. You have the power to ask: why has a Panchayat order from
2008 not been enforced?

To the Director of Panchayats (North Goa): I ask you to review why
Order Ref V.P.S.S./2008-09/977 has not been enforced, and to report on
what action will now be taken.

To the Panchayat Vigilance Officer (North Zone): I ask you to audit the
Siolim-Sodiem Panchayat's handling of this order over 18 years.

To the District Collector, North Goa: I ask for your office's
intervention to ensure this historic order is finally given effect.

To the press: This order exists. It is a matter of Panchayat record.
Eighteen years of non-enforcement of a Panchayat's own order is a story
the people of Goa deserve to know about.

I continue to wait -- humbly and respectfully -- for MLA Lobo's response.

{FACTS}
{FOOTER}""",
    },

    # ── 4 ── Noise and Health
    {
        "subject": "68-75 dB(A) Every Sunday in a Residential Zone -- Health Hazard -- MLA Lobo, This Is Your Constituency",
        "body": f"""Respected MLA Delilah Lobo,

Every Sunday, the padel tennis courts and social club operating illegally
on my land at Survey No. 197/7, Sodiem, Siolim produce noise levels of
68 to 75 decibels (dB(A)) as measured at my property boundary.

The statutory limit for a residential zone is 55 dB(A) during the day
and 45 dB(A) at night.

The club routinely exceeds this by 13 to 30 dB(A). In acoustic terms,
every 3 dB represents a doubling of sound energy. The noise at my
property is therefore 16 to 1,000 times the legally permitted level.

I am not a young man. Sustained exposure to noise at these levels causes
documented harm: elevated blood pressure, cardiovascular stress, sleep
disruption, anxiety. My family and the neighbouring residents endure this
every weekend.

Respected MLA, this is your constituency. These are your constituents.
The health impact is real and it is measurable.

To the Goa State Pollution Control Board (GSPCB Chairman and Member
Secretary, both copied): I formally request a noise measurement inspection
at Survey No. 197/7, Gaunsawaddo, Sodiem, Siolim, on any Sunday morning.
I will be present. I invite you to witness what I hear every week.

To the Siolim Primary Health Centre and the Directorate of Health
Services: I ask for your assessment of the health implications of
sustained noise at 68-75 dB(A) for residential neighbours.

To the North Goa District Flying Squad (Nodal Magistrate): I ask for a
field visit to this address on any Sunday between 9 AM and 4 PM.

To MLA Lobo: Please, I ask you simply to acknowledge this. Your
constituents are suffering a documented health hazard. Will you help?

{FACTS}
{FOOTER}""",
    },

    # ── 5 ── Tree Felling
    {
        "subject": "Trees Felled on My Land Without Tree Authority Permission -- Goa Preservation of Trees Act 1984 Violated -- Siolim",
        "body": f"""Respected MLA Delilah Lobo,

I wish to draw your attention and the attention of all officials and
press on this correspondence to a specific environmental crime.

Multiple trees on my private land at Survey No. 197/7, Gaunsawaddo,
Sodiem, Siolim were felled by those operating the Sunday Racquet and
Social Club -- without any permission from the Tree Authority, and
without any notice to me as the land owner.

This is a clear violation of the Goa Preservation of Trees Act, 1984.
Under this Act, it is an offence to fell, cut, damage, or destroy any
tree without obtaining prior permission from the designated Tree Authority.
No such permission was sought. No such permission was granted.

The trees were cleared to make way for padel tennis courts built on
land encroached from me -- land that the Panchayat ordered vacated in
2008. The destruction of these trees is therefore doubly illegal: the
establishment is itself illegal, and the tree felling to build it was
done without legal sanction.

To the Deputy Conservator of Forests, North Goa: I formally draw your
attention to this violation under the Goa Preservation of Trees Act 1984
and ask that your office investigate, record, and act upon it.

To the Directorate of Environment and Climate Change: I ask that this
be noted as an environmental violation in a residential area of the
Siolim constituency.

To the NGO representatives and the press on copy: The felling of trees
on private land without permission, to build an illegal commercial
establishment, is an environmental story as well as a legal one.

To MLA Delilah Lobo: You inaugurated an establishment that was built,
in part, by destroying my trees without permission. I ask you only to
look into this and to help me find the truth.

{FACTS}
{FOOTER}""",
    },

    # ── 6 ── Land Encroachment
    {
        "subject": "My Land Has Been Encroached -- Survey No. 197/7 Sodiem Siolim -- I Ask MLA Lobo and All Authorities for Help",
        "body": f"""Respected MLA Delilah Lobo,

At the heart of this matter is a simple fact: the Sunday Racquet and
Social Club is operating on my land.

Survey No. 197/7, Gaunsawaddo, Sodiem, Siolim, Bardez, Goa is my private
property. I have title to it. I have the documents. The establishment
at House No. 47/3 on this survey number is built on land that belongs to
me, and has been built there in contravention of the Panchayat Revocation
Order of 2008 which demanded that this encroachment be undone.

I have not sold this land. I have not leased it. I have not given any
permission for a commercial padel tennis court and social club to be
operated on it. Yet here we are, eighteen years after the Panchayat
itself recognised the encroachment, and nothing has changed.

To the Collectorate of North Goa (Collector Dr. Sneha Gitte, IAS, and
both Additional Collectors): I formally ask for the intervention of
your office in ensuring that my land rights are protected.

To the Bardez Mamlatdar (Revenue Office): I ask for a revenue
investigation into the current physical possession and usage of
Survey No. 197/7 and for a boundary inspection to be ordered.

To the Senior Town Planner and TCP Flying Squad: I ask whether any
building permission, conversion or development order was ever issued
for the construction of commercial courts on this residential plot.

To MLA Delilah Lobo: You know this constituency. You know these
villages. I ask you simply: will you help a constituent recover his land?

{FACTS}
{FOOTER}""",
    },

    # ── 7 ── Press Intervention
    {
        "subject": "Appeal to the Goa Press -- MLA Lobo Has Not Responded in Days -- Please Investigate and Report -- Siolim Encroachment",
        "body": f"""Respected MLA Delilah Lobo,

I am writing this letter, as I have written many others, because I have
been unable to reach you by phone or message. I am a humble person. I do
not have political connections. I have only my rights as a citizen and a
constituent.

Today I write directly to the press who have received this correspondence,
and I ask them for their help.

Dear editors and journalists of Goa Chronicle, Prudent Media, The Goan,
and All India Radio Goa:

A constituent of MLA Siolim (Delilah Lobo) has been suffering noise
pollution, land encroachment, and illegal tree felling on his property
for years. The Village Panchayat issued a Revocation Order in 2008. It
has never been enforced. The MLA whose constituency this falls in publicly
inaugurated this illegal establishment.

I have been calling and messaging MLA Lobo for days. I have written to
her formally. I have sent evidence. I have appealed to all authorities.
There has been no response from her office.

I ask you, as representatives of the free press, to:
1. Reach out to MLA Delilah Lobo for her comments on this matter
2. Investigate the non-enforcement of Panchayat Order V.P.S.S./2008-09/977
3. Look into whether an elected representative's inauguration of an
   illegal establishment has a straightforward explanation
4. Report on the story of a Siolim resident who has been fighting this
   for years with no governmental response

I am available for an interview at any time. I will share my evidence
dossier, my noise measurements, and all my correspondence with the
authorities. I have nothing to hide. I ask only for justice.

To MLA Lobo: the press are now looking at this matter. I pray that you
will find it in your heart to respond to your constituent.

{FACTS}
{FOOTER}""",
    },

    # ── 8 ── Fellow MLAs
    {
        "subject": "To All Goa MLAs -- Your Colleague from Siolim Has Not Responded -- A Constituent Appeals for Your Help",
        "body": f"""Respected MLA Delilah Lobo,

I am writing to you in the presence of your colleagues -- the elected
representatives of every constituency in Goa -- because I do not know
how else to reach you.

I have called. I have messaged. I have written formal letters. I have
sent my evidence. I have appealed to the authorities. My MLA -- you --
has not responded.

I am not angry. I understand that elected representatives are busy, that
many people approach them, that a single constituent's letter may not
rise to the top of a large inbox. But the matter I write about is
significant. It involves my home, my land, my health, and the safety of
my neighbourhood.

To all the Honourable MLAs of the Goa Legislative Assembly who have
received this correspondence:

I appeal to each of you to consider: if a constituent in your own
constituency was suffering what I am suffering -- illegal encroachment on
their land, 18 years of a Panchayat order going unenforced, trees felled
on their property, health-damaging noise every Sunday -- and could not
get a response from you, what would you want someone to do?

I ask you to please help me reach MLA Delilah Lobo. I ask you to
encourage her to respond to this letter, to acknowledge my complaint,
and to use her position as my elected representative to help me.

I am not asking for a political intervention. I am asking one elected
representative to encourage another to do their duty by a constituent.

To Honourable Members who represent coastal constituencies or who have
had experience with noise and encroachment issues: your specific insight
and solidarity in this matter would be deeply valuable.

{FACTS}
{FOOTER}""",
    },

    # ── 9 ── Corruption / Bribery Question
    {
        "subject": "A Humble and Truthful Question: Why Has a Panchayat Order Gone Unenforced for 18 Years? Is There an Explanation?",
        "body": f"""Respected MLA Delilah Lobo,

I write to you in humility. I write in search of the truth. I do not
write to accuse anyone. I write because I have run out of other options.

The Siolim-Sodiem Village Panchayat issued Revocation Order
Ref V.P.S.S./2008-09/977 on 24 September 2008. Eighteen years have passed.
The order has never been enforced. The establishment continues to operate,
continues to encroach on my land, continues to fell trees, continues to
generate illegal noise.

I ask a simple question, and I ask it publicly, in the presence of all
the officials, elected representatives, and press on this correspondence:

WHY?

Why has a formal Panchayat order -- issued by the Siolim-Sodiem Panchayat
itself, on the basis of a legal complaint -- gone unenforced for 18 years?

Is it administrative failure? Is it negligence? Is it that no one
considered it important enough to act upon?

Or -- and I ask this with the deepest respect for everyone involved, and
without making any accusation -- could there be another explanation?
Could there be a reason why powerful interests have been able to operate
on my land, in clear violation of a Panchayat order, without consequence?

I do not know the answer. I am asking the question.

To the Panchayat Vigilance Officer: I ask you to investigate whether
there is any documented explanation for why this order was not enforced.

To the press: This is a legitimate question of public interest. Why does
an 18-year-old Panchayat order remain on paper while an illegal
commercial establishment operates freely on a private citizen's land?

To MLA Lobo: You inaugurated this establishment. You have not responded
to my communications. The question of why this situation persists is one
that your constituents -- and all of Goa -- deserve an honest answer to.

{FACTS}
{FOOTER}""",
    },

    # ── 10 ── Community Suffering
    {
        "subject": "I Am Not Alone -- Neighbours Are Also Suffering -- The Whole Community of Sodiem Siolim Appeals to You",
        "body": f"""Respected MLA Delilah Lobo,

I want you to understand something: I am not an isolated case. I am not
a single eccentric resident with a personal grudge. I am a homeowner
whose property has been encroached upon and whose peace has been
destroyed -- and I am not alone in this suffering.

The residents of the area around Survey No. 197/7, Gaunsawaddo, Sodiem,
Siolim live with this noise every Sunday. The 68-75 dB(A) levels do not
stop at my boundary wall. They carry across the neighbourhood. Elderly
residents cannot rest. Children cannot concentrate. The weekends that
should be the most peaceful time in a residential village have become
the loudest and most disruptive.

Neighbouring residents, who have asked to remain anonymous for their own
personal reasons, are also documenting the noise and its impact on their
daily lives. They support this campaign. They ask me to speak for them.

A whole community is looking to its elected representative for a response.

To the Siolim-Sodiem Village Panchayat (Sarpanch Deepika D. Deokar and
Secretary Nilesh Parab): The community you serve is asking you to enforce
your own 2008 order. I ask you: what is preventing you from doing so?

To the Siolim Primary Health Centre: The health impact of sustained noise
at 68-75 dB(A) on a residential population -- including elderly and young
children -- is a matter that your office should assess and document.

To the press: The story is not just one man and his land. It is a whole
neighbourhood asking why the law does not apply to a commercial club
operating in a residential village.

To MLA Lobo: These are your constituents. All of them. Please respond.

{FACTS}
{FOOTER}""",
    },

    # ── 11 ── Constitutional Rights
    {
        "subject": "A Citizen's Constitutional Rights Are Being Violated -- Article 21 Right to Life -- MLA Lobo, Please Fulfil Your Duty",
        "body": f"""Respected MLA Delilah Lobo,

As a citizen of India and a voter in the Siolim constituency, I write to
you today to invoke my fundamental constitutional rights.

Article 21 of the Constitution of India guarantees every citizen the
right to life and personal liberty. The Supreme Court of India has
interpreted this to include the right to live in a clean and noise-free
environment, the right to health, and the right to peaceful enjoyment
of one's home and property.

My home is being made unlivable by illegal noise. My land is being
occupied by an illegal establishment. My trees have been destroyed. My
complaints have been on record with the Panchayat since 2008. The
enforcement machinery has not moved.

This is not a personal dispute between neighbours. This is a fundamental
rights violation.

You, MLA Delilah Lobo, have been elected to represent the people of
Siolim in the Goa Legislative Assembly. Your mandate is to protect the
rights of your constituents -- including me. That mandate exists not just
on election day but every day of your term.

I ask you today, formally and publicly, to fulfil your constitutional
and representative duty. Acknowledge my letters. Use your office to
demand that the 2008 Panchayat order be enforced. Ask the GSPCB to
conduct a noise inspection. Ask the Collector to investigate the
encroachment.

To all officials and authorities on this correspondence: I formally place
on record that the encroachment, noise pollution, and tree felling I have
described constitute violations of my constitutional rights, and I
request that your respective offices act within their mandated powers.

To the press: This is a story about whether the law applies equally to
all -- and whether an elected representative fulfils their duty.

{FACTS}
{FOOTER}""",
    },

    # ── 12 ── Final Appeal Before Legal Action
    {
        "subject": "Final Appeal Before Filing with the National Green Tribunal and Bombay High Court -- MLA Lobo -- Please Act Now",
        "body": f"""Respected MLA Delilah Lobo,

This is my twelfth and final letter to you before I proceed to file
formal petitions with the National Green Tribunal (West Zone) and the
Bombay High Court (Goa Bench).

I have written to you with humility. I have shared the facts. I have
asked for your response. I have appealed to your colleagues in the
Assembly, to the press, to the Panchayat, to the Collector, to the
GSPCB, to the Forest Department, to the police, and to the community.

I have given this process every reasonable opportunity to work through
proper channels. I have been patient for eighteen years.

I now draw the attention of all officials, MLAs, and press on this
correspondence to what happens next if there is no response:

1. NATIONAL GREEN TRIBUNAL (West Zone)
   Petition to be filed for illegal tree felling, noise pollution
   exceeding statutory limits, and failure of the GSPCB and Panchayat
   to enforce applicable environmental law.

2. BOMBAY HIGH COURT -- GOA BENCH
   Writ petition under Article 226 for violation of fundamental rights
   under Article 21, non-enforcement of Panchayat Order
   Ref V.P.S.S./2008-09/977, and failure of state authorities to act
   on a documented encroachment and illegal construction.

3. DIRECTOR OF PANCHAYATS -- FORMAL COMPLAINT
   Formal complaint regarding the Siolim-Sodiem Panchayat's 18-year
   failure to enforce its own 2008 Revocation Order.

4. ANTI-CORRUPTION BUREAU
   If no credible administrative explanation is forthcoming for the
   18-year non-enforcement of a formal Panchayat order, I will ask the
   ACB to examine whether any financial inducement has played a role in
   the persistent inaction of officials.

MLA Lobo: I do not want to go to court. I want to resolve this through
dialogue and through the proper functioning of the system. I am asking
you, one last time, to respond to your constituent. To acknowledge my
letters. To use your office to help.

To all authorities on copy: Your offices have been formally notified of
my grievance. Your responses, or lack thereof, are now on public record.

To the press: The next chapter of this story begins the day this letter
is sent. The people of Siolim and of Goa are watching.

{FACTS}
{FOOTER}""",
    },
]

print(f"Preparing to send {len(emails)} emails to Delilah Lobo (mlasil.gvs@gov.in)")
print(f"CC list: {len(CC.split(','))} addresses\n")

sent, failed = [], []
for i, em in enumerate(emails, 1):
    m = EmailMessage()
    m["From"]    = FROM
    m["To"]      = TO_LOBO
    m["Cc"]      = CC
    m["Subject"] = em["subject"]
    m.set_content(em["body"])
    label = f"Email {i:02d}: {em['subject'][:60]}..."
    print(f"[{i:02d}/12] Sending ...", end=" ", flush=True)
    try:
        via = send_with_fallback(m)
        print(f"OK ({via})")
        sent.append(i)
    except Exception as e:
        print(f"FAILED: {e}")
        failed.append((i, str(e)))
    if i < len(emails):
        time.sleep(15)

print(f"\n{'='*60}")
print(f"SENT:   {len(sent)}/12 -- {sent}")
if failed:
    print(f"FAILED: {failed}")
print("="*60)
