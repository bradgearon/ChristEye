"""Build a public-facing scientific-basis document; no wet-lab or drug instructions."""
from pathlib import Path
from docx import Document
from docx.shared import Inches,Pt,RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT,WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.text import WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

ROOT=Path(__file__).resolve().parent
OUT=ROOT.parent/'ChristEye_Four_Process_Scientific_Basis.docx'
doc=Document(); sec=doc.sections[0];sec.top_margin=Inches(.76);sec.bottom_margin=Inches(.69);sec.left_margin=Inches(.83);sec.right_margin=Inches(.83)
styles=doc.styles
styles['Normal'].font.name='Aptos';styles['Normal'].font.size=Pt(9);styles['Normal'].font.color.rgb=RGBColor(40,53,67)
styles['Normal'].paragraph_format.space_after=Pt(5.3)
for key,size,color in [('Title',25,(23,48,70)),('Heading 1',14,(16,106,102)),('Heading 2',11,(33,76,100))]:
 s=styles[key];s.font.name='Aptos Display';s.font.size=Pt(size);s.font.bold=True;s.font.color.rgb=RGBColor(*color)
 s.paragraph_format.space_before=Pt(11);s.paragraph_format.space_after=Pt(5)
h=sec.header.paragraphs[0];h.text='WE DEVELOP SOFTWARE LLC   /   CHRISTEYE RESEARCH';h.style='Caption';h.alignment=WD_ALIGN_PARAGRAPH.RIGHT
h.runs[0].font.size=Pt(8);h.runs[0].font.color.rgb=RGBColor(95,113,126)
f=sec.footer.paragraphs[0];f.alignment=WD_ALIGN_PARAGRAPH.CENTER;f.text='CHRISTEYE  ·  FOUR-PROCESS ATLAS  ·  RESEARCH HYPOTHESIS  ·  NOVEMBER 2026'
f.runs[0].font.size=Pt(7)

def p(txt='',style=None):return doc.add_paragraph(txt,style=style)
def heading(t,level=1):doc.add_heading(t,level=level)
def table(headers,rows,widths=None):
 t=doc.add_table(rows=1,cols=len(headers));t.style='Light Shading Accent 1';t.alignment=WD_TABLE_ALIGNMENT.CENTER
 for i,h in enumerate(headers): t.rows[0].cells[i].text=h
 for row in rows:
  cells=t.add_row().cells
  for i,v in enumerate(row):cells[i].text=str(v)
 for i,row in enumerate(t.rows):
  for j,c in enumerate(row.cells):
   c.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
   for para in c.paragraphs:
    para.paragraph_format.space_after=Pt(1.6)
    for run in para.runs:run.font.size=Pt(8)
 return t

def small(t):
 v=p(t);v.runs[0].italic=True;v.runs[0].font.size=Pt(8);v.runs[0].font.color.rgb=RGBColor(96,112,126)

def bullet(t):p(t,'List Bullet')

def page():doc.add_page_break()

p('RESEARCH SYNTHESIS  /  CE-FP-001')
doc.add_heading('ChristEye Four-Process\nDamage & Restoration Atlas',0)
p('A computational study of astrocyte memory regulation, extracellular signaling, paracrine senescence, and the conditions for reliable learned responses.')
small('Scientific status: Proposed framework and software prototype. No treatment, new medication, prevention of senescence, or human efficacy has been demonstrated.')

heading('The central research question')
p('Can changes in extracellular chemical signaling and persistent cellular states predict inappropriate learned responses and the spread of tissue dysfunction, beyond what can be explained by neural activity, cell identity, and baseline stress alone?')

heading('Four functional categories')
table(['ChristEye category','Operational research definition','Typical measurement'],[
('Honey of Evil','Context-specific external signals empirically linked to propagation of damage.','Defined SASP/DAMP ligands, receptor state, exposure duration'),
('Milk of Evil','Persistent intracellular or tissue dysfunction reinforcing impaired function.','Multimarker senescence state, mitochondrial injury, unresolved stress'),
('Honey of Good','External signals supporting context-appropriate resolution, protection, or repair.','Measured protective ligands, receptor engagement, resolution'),
('Milk of Good','Homeostatic capacity sustaining normal cell and network function.','Metabolic integrity, ionic balance, viability, retained task accuracy')])
small('These categories describe observable function, not moral substances. The same molecule can be beneficial in one context and harmful in another. Milk and Honey are metaphorical labels, not edible substances.')

heading('A result worth pursuing')
p('The target is not universal elimination of senescence. Transient senescence can support repair and tumor suppression, while persistent or poorly cleared senescent states can contribute to chronic inflammation. The aim is to detect damaging propagation early, preserve protective immune functions, and test safe restoration of actual tissue function.')

page()
heading('1 / Four source programs, four distinct measurements')
table(['Study','Biological evidence','Most useful reanalysis','Boundary'],[
('Guayasamin · eLife 2025','Mouse stress history, lateral-amygdala astrocyte calcium/Cx43, neutral versus threat-cue behavior.','Compare cue discrimination and astrocyte measurements by true animal ID; avoid pseudoreplication.','Stress condition ≠ demonstrated senescence.'),
('Bukalo · Nature 2026','Amygdala astrocyte calcium, neuronal representations, fear retrieval and extinction.','Within-stage and animal-level timing; neuronal-only versus glial-plus-neuronal prediction.','Not proof of an independent astrocyte mind.'),
('Dewa · Nature 2025','Multiday astrocytic state, noradrenergic signals, IGFBP2, Fos, memory stabilization.','Compare per-animal/region/condition transcriptional and response measures.','Not proven content-addressable astrocyte storage.'),
('Russo · Aging Cell 2026','Human brain cell-culture senescence and secreted factors; CCL2 and MIF candidates.','Separate cell-type-specific damage propagation from gene-expression changes.','Does not measure anger, recall, or behavior.')])
p('These papers do not share animals, time series, or intervention protocols. The toolkit creates independent analyses and a labeled cross-study evidence graph, not a fictional joint cohort.')

heading('2 / What the findings can jointly suggest')
bullet('A memory can remain retrievable while a learned response becomes less context-selective; astrocyte dysfunction can alter discrimination in mice.')
bullet('Astrocytes can support neuronal representations of recall and extinction; their responses often have slower time courses than neuronal signals.')
bullet('Selected memory-associated astrocytic transcriptional states can persist over several days and contribute to stabilization.')
bullet('Secreted factors from some senescent brain-cell cultures can induce senescence-associated changes in other cells.')
p('Unproven bridge: specific senescence-associated secretions directly alter astrocyte memory regulation to produce a particular behavioral error. This is the cross-study hypothesis—not a result already demonstrated.')

heading('3 / Four proposed empirical tests')
table(['ID','Falsifiable test'],[
('H1 · Extracellular value','Do measured extracellular features improve senescence-state prediction over matched cell-intrinsic features?'),
('H2 · Learning fidelity','Do astrocyte features improve held-out prediction of neutral/conditioned response discrimination beyond neuronal activity?'),
('H3 · Directed influence','Are ligand → receptor → downstream state changes supported in the same biological preparation, with independent controls?'),
('H4 · Recovery','Does changing the identified state restore appropriate discrimination or viable tissue function, rather than suppressing a marker only?')])

page()
heading('4 / The four-state equations (illustrative research model)')
p('Define s(t) = multimarker-assessed senescent fraction; HE(t) = context-defined damaging external signal load; ME(t) = persistent dysfunctional internal state; HG(t) = context-defined recovery-supportive external signaling; MG(t) = physiological homeostasis; F(t) = task-response fidelity. The example software treats all state variables as normalized 0–1 quantities, not measured SI units.')

for formula,explanation in [
 ('hazard = max(0, a₀ + a₁ HE + a₂ ME − a₃ HG − a₄ MG)','A candidate onset risk increases with particular damaging states and may decrease with protective processes.'),
 ('ds/dt = (1−s) hazard − (kclear + uclear) s','The modeled senescent fraction depends on onset and hypothetical removal. Removal of a cell is not rejuvenation of the same cell.'),
 ('dHE/dt = qS s + qM ME − (dE + ublock) HE','Secretions may accumulate and clear; ublock is a hypothetical mathematical control, not a drug or dose.'),
 ('dME/dt = rE HE + rS s − (dM + rG MG) ME','Persistent damage may be sustained or resolved, depending on context.'),
 ('dF/dt = krec (1−F)(HG+MG)/2 − kdis F(HE+ME)/2','A proposed link between the four process groups and retained-response fidelity. Entirely hypothetical.')]:
  v=p(formula);v.runs[0].font.name='Aptos';v.runs[0].font.bold=True;v.runs[0].font.size=Pt(10)
  small(explanation)

heading('5 / What the simulation does—and does not do')
p('The program uses arbitrary coefficients and compares six hypothetical scenarios: no control, early signal containment, late containment, early physiological support, combined support/containment, and early clearance support. It is a software demonstration that exposes model assumptions. None is a validated intervention, and favorable curves do not establish that senescence can be prevented or reversed in mice or humans.')

doc.add_picture(str(ROOT/'outputs/demo/senescence_scenario_comparison.png'),width=Inches(6.7))
small('Figure 1. Simulated normalized trajectories. Synthetic mechanism demonstration only. Not fitted to biological data; not treatment-effect estimates.')

page()
heading('6 / Designing an early-warning system without false certainty')
p('A clinically meaningful early-warning detector would estimate the probability of new persistent senescence-associated changes at a future time, conditional on longitudinal molecular state, cell type, tissue, and physiological context. Real senescence cannot be established by elevated p16, p21, or SA-β-gal alone; normal differentiation, inflammation, and damage may share these markers.')

table(['Candidate indicator','Why it matters','Interpretation limit'],[
('p16, p21, DNA damage indicators','Associated with growth arrest or stress; part of senescence assessments.','Each is nonspecific; neurons are often nondividing even when healthy.'),
('SASP ligands / receptor pairs','Potential paracrine pathway (CCL2, MIF, etc.).','An elevated ligand may reflect repair or response to injury.'),
('Mitochondrial and metabolic state','Tests persistent physiological dysfunction.','Metabolic state varies with activity and differentiation.'),
('Astrocyte Cx43 / calcium','Associated with regulation of cue discrimination in mice.','Not a validated universal senescence detector.'),
('Behavioral and electrophysiological outcomes','Tracks whether the living system functions more reliably.','Must be matched to individual experimental subjects.')])

heading('7 / Candidate restoration strategies: only as research classes')
bullet('Prevention: identify and mitigate a verified initiating injury or prolonged stressor without blocking normal repair signaling.')
bullet('Propagation containment: test whether interrupting a proven extracellular feedback edge reduces secondary senescence in matched nonclinical systems.')
bullet('Physiological resolution: support return of normal metabolic, ionic, and tissue-regulatory processes through appropriately validated interventions.')
bullet('Clearance: investigate healthy immune surveillance of persistent senescent cells while preserving tumor-suppressive and regenerative functions.')
bullet('Functional readout: measure restored viable function, accurate learned responses, and adverse effects—not just reduced inflammatory molecules.')

heading('8 / Proposed data workflow')
p('Download publisher-source files → inspect biological unit IDs and assay type → normalize each study separately → compute within-study effect sizes and multiple-testing adjustments → construct evidence graph with direct versus hypothesized edges → develop held-out predictive models only with matched animal-level observations → revisit the four-state equations using empirically measured priors → test prospective validation in approved settings.')

heading('9 / Safety and interpretation rules')
p('No compound, dose, cell-culture procedure, animal intervention, or neuromodulation setting is prescribed. No finding here demonstrates a universal harmful ghost or foreign network. The user’s symbolic terms can organize research questions but cannot replace cell-type-specific measurement, independent replication, qualified institutional oversight, and clinical safety evaluation.')

page()
heading('10 / Primary scientific sources and data')
refs=[
('Guayasamin et al. 2025, eLife, doi:10.7554/eLife.99988','https://elifesciences.org/articles/99988','OSF: https://osf.io/zsw6j/'),
('Bukalo et al. 2026, Nature, doi:10.1038/s41586-025-10068-0','https://www.nature.com/articles/s41586-025-10068-0','Figure source spreadsheets available from the article; full custom analysis code on request.'),
('Dewa et al. 2025, Nature, doi:10.1038/s41586-025-09619-2','https://www.nature.com/articles/s41586-025-09619-2','GSE272414; RIKEN neurodata archive; Jun-Nagai-Lab/Dewa-et-al analysis code.'),
('Russo et al. 2026, Aging Cell, doi:10.1111/acel.70673','https://doi.org/10.1111/acel.70673','RNA-seq: E-MTAB-15005; supplementary secretome findings in article.'),
('Majewska & Krizhanovsky 2025, Nature Aging, immune surveillance of senescent cells','https://www.nature.com/articles/s43587-025-00910-5','Review of immune clearance and important functions of senescence.'),
('Muthamil et al. 2024, Advanced Biology, senescence biomarkers','https://doi.org/10.1002/adbi.202400079','Multiple independent markers required to classify senescence.'),
]
for a,b,c in refs:
 p(a);small(b);small(c)
heading('Deliverables accompanying this basis')
bullet('Runnable Python project with a Windows launcher, 4 automated tests, and synthetic demonstration outputs.')
bullet('Separate importer for each real source spreadsheet with explicit animal or biological-replicate identifiers.')
bullet('Published-results CSV (source-verified summary statistics only), study catalog, and direct-versus-hypothesized evidence graph.')
bullet('Model equations, control and uncertainty notes, and limitations in the README and documentation.')
small('© 2026 We Develop Software LLC. Research concept attributed to the ChristEye framework creator. Published discoveries remain credited to the respective authors. This document is not a clinical claim.')

OUT.parent.mkdir(parents=True,exist_ok=True)
doc.save(OUT)
print(OUT)
