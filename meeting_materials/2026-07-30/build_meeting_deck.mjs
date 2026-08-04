import fs from "node:fs/promises";
import { Presentation, PresentationFile } from "@oai/artifact-tool";

const OUT_DIR =
  "/Users/alioubarry/Desktop/Livrables_McGill_WellE/Reunion_McGill_2026-07-30";
const OUT_PPTX = `${OUT_DIR}/Presentation_McGill_30_juillet_2026.pptx`;
const BUILD_DIR = "/tmp/mcgill_meeting_20260730/rendered_by_artifact_tool";

const W = 1280;
const H = 720;
const M = 48;
const FONT = "Helvetica Neue";

const C = {
  ink: "#111111",
  white: "#FFFFFF",
  paper: "#F6F7F8",
  panel: "#ECEFF2",
  grid: "#D6DADF",
  muted: "#5E6875",
  blue: "#2474E5",
  cyan: "#68C7E8",
  teal: "#14877E",
  yellow: "#F4C542",
  red: "#C94F4F",
  green: "#2D8A57",
  purple: "#7656B6",
};

const SRC = {
  sow:
    "/Users/alioubarry/PROJECT/mcgill_iot_cattle/SOW Alliou - Complété (avec montants).docx",
  readme:
    "/Users/alioubarry/Desktop/Livrables_McGill_WellE/Objectif1_Pipeline_detection_boiterie/README_livraison_objectif1.txt",
  report:
    "/Users/alioubarry/Desktop/Livrables_McGill_WellE/Objectif1_Pipeline_detection_boiterie/RAPPORTS/Objectif1_rapport_livraison.docx",
  summary:
    "/Users/alioubarry/Desktop/Livrables_McGill_WellE/Objectif1_Pipeline_detection_boiterie/TABLEAUX_CSV/objective1_multi_season_summary.csv",
  reinforced:
    "/Users/alioubarry/Desktop/Livrables_McGill_WellE/Objectif1_Pipeline_detection_boiterie/TABLEAUX_CSV/objective1_reinforced_summary_by_season.csv",
  concordance:
    "/Users/alioubarry/Desktop/Livrables_McGill_WellE/Objectif1_Pipeline_detection_boiterie/TABLEAUX_CSV/concordance_par_experience.csv",
  sls:
    "/Users/alioubarry/Desktop/Livrables_McGill_WellE/Objectif1_Pipeline_detection_boiterie/ANNEXE_pipeline_actuelle_HYPO_instabilite_hybride/TABLEAUX_CSV/pipeline_actuelle_validation_sls_synthese.csv",
  annexTotal:
    "/Users/alioubarry/Desktop/Livrables_McGill_WellE/Objectif1_Pipeline_detection_boiterie/ANNEXE_pipeline_actuelle_HYPO_instabilite_hybride/TABLEAUX_CSV/pipeline_actuelle_synthese_totale.csv",
  note:
    "/Users/alioubarry/Desktop/Livrables_McGill_WellE/Objectif1_Pipeline_detection_boiterie/NOTES_SOW/note_technique_reproductibilite.md",
  validation:
    "/Users/alioubarry/Desktop/Livrables_McGill_WellE/Objectif1_Pipeline_detection_boiterie/NOTES_SOW/rapport_validation_concordance.md",
  inventory:
    "/Users/alioubarry/PROJECT/mcgill_iot_cattle/reports/mcgill_complete_inventory.md",
  config: "/Users/alioubarry/PROJECT/core/config.py",
  io: "/Users/alioubarry/PROJECT/core/io.py",
  features: "/Users/alioubarry/PROJECT/core/features.py",
  model: "/Users/alioubarry/PROJECT/core/model_if.py",
  pipeline: "/Users/alioubarry/PROJECT/core/pipeline.py",
  alerts: "/Users/alioubarry/PROJECT/core/_alerts_engine.py",
  reinforcement:
    "/Users/alioubarry/PROJECT/mcgill_iot_cattle/run_objective1_reinforcement.py",
  annexScript:
    "/Users/alioubarry/PROJECT/mcgill_iot_cattle/make_objective1_current_pipeline_annex.py",
  nbAudit:
    "/Users/alioubarry/PROJECT/mcgill_iot_cattle/notebooks/01_audit_donnees_mcgill.ipynb",
  nbConvert:
    "/Users/alioubarry/PROJECT/mcgill_iot_cattle/notebooks/02_convert_icetag_to_pipeline.ipynb",
  nbPipeline:
    "/Users/alioubarry/PROJECT/mcgill_iot_cattle/notebooks/05_objectif1_pipeline_icetag.ipynb",
  nbConcordance:
    "/Users/alioubarry/PROJECT/mcgill_iot_cattle/notebooks/10_tache1_2_concordance_alertes_comportement.ipynb",
  nbReinforcement:
    "/Users/alioubarry/PROJECT/mcgill_iot_cattle/notebooks/13_objectif1_renforcement_scientifique.ipynb",
};

function addRect(slide, x, y, w, h, fill, options = {}) {
  return slide.shapes.add({
    geometry: options.geometry || "rect",
    name: options.name,
    position: { left: x, top: y, width: w, height: h },
    fill,
    line: {
      style: "solid",
      fill: options.lineFill || fill,
      width: options.lineWidth ?? 0,
    },
    ...(options.radius ? { borderRadius: "rounded-lg" } : {}),
  });
}

function addLine(slide, x, y, w, color = C.ink, width = 2) {
  return slide.shapes.add({
    geometry: "straightConnector1",
    position: { left: x, top: y, width: w, height: 0 },
    fill: "none",
    line: { style: "solid", fill: color, width },
  });
}

function addText(slide, text, x, y, w, h, options = {}) {
  const box = slide.shapes.add({
    geometry: "textbox",
    name: options.name,
    position: { left: x, top: y, width: w, height: h },
    fill: options.fill || "none",
    line: {
      style: "solid",
      fill: options.lineFill || "none",
      width: options.lineWidth ?? 0,
    },
  });
  box.text = text;
  box.text.style = {
    fontSize: options.size || 22,
    typeface: FONT,
    color: options.color || C.ink,
    bold: options.bold || false,
    italic: options.italic || false,
    alignment: options.align || "left",
    verticalAlignment: options.valign || "top",
  };
  return box;
}

function addPill(slide, text, x, y, w, color = C.ink, fill = C.panel) {
  addRect(slide, x, y, w, 34, fill, { geometry: "roundRect", radius: 7 });
  addText(slide, text, x + 10, y + 6, w - 20, 22, {
    size: 15,
    bold: true,
    color,
    align: "center",
  });
}

function addHeader(slide, title, section, number) {
  slide.background.fill = C.white;
  addText(slide, section.toUpperCase(), M, 28, 300, 24, {
    size: 14,
    bold: true,
    color: C.blue,
  });
  addText(slide, title, M, 58, 1120, 68, {
    size: 38,
    bold: true,
    color: C.ink,
  });
  addLine(slide, M, 132, W - M * 2, C.grid, 1);
  addText(slide, String(number).padStart(2, "0"), 1180, 672, 50, 20, {
    size: 13,
    color: C.muted,
    align: "right",
  });
}

function addNotes(slide, paragraphs, sources) {
  const sourceBlock = [
    "",
    "[Sources]",
    ...sources.map((source) => `- ${source}`),
    "[/Sources]",
  ];
  slide.speakerNotes.textFrame.setText([...paragraphs, ...sourceBlock]);
  slide.speakerNotes.setVisible(true);
}

function bullet(slide, text, x, y, w, options = {}) {
  addRect(slide, x, y + 8, 8, 8, options.color || C.blue, {
    geometry: "ellipse",
  });
  addText(slide, text, x + 20, y, w - 20, options.h || 54, {
    size: options.size || 20,
    color: options.textColor || C.ink,
    bold: options.bold || false,
  });
}

function statBlock(slide, x, y, w, value, label, color = C.blue) {
  addText(slide, value, x, y, w, 70, {
    size: 50,
    bold: true,
    color,
  });
  addText(slide, label, x, y + 72, w, 58, {
    size: 18,
    color: C.muted,
  });
}

function tableGrid(slide, x, y, widths, rows, options = {}) {
  const rowH = options.rowH || 56;
  let yy = y;
  rows.forEach((row, r) => {
    let xx = x;
    row.forEach((value, c) => {
      const isHeader = r === 0;
      addRect(
        slide,
        xx,
        yy,
        widths[c],
        rowH,
        isHeader ? C.ink : r % 2 ? C.white : C.paper,
        { lineFill: C.grid, lineWidth: 1 },
      );
      addText(slide, String(value), xx + 10, yy + 12, widths[c] - 20, rowH - 18, {
        size: isHeader ? 16 : options.size || 17,
        bold: isHeader,
        color: isHeader ? C.white : C.ink,
        align: c === 0 ? "left" : options.numericCenter ? "center" : "left",
        valign: "middle",
      });
      xx += widths[c];
    });
    yy += rowH;
  });
}

function labelAbove(slide, text, x, y, w, color = C.muted) {
  addText(slide, text.toUpperCase(), x, y, w, 22, {
    size: 13,
    bold: true,
    color,
  });
}

const presentation = Presentation.create({
  slideSize: { width: W, height: H },
});

// 1. Cover
{
  const slide = presentation.slides.add();
  slide.background.fill = C.white;
  addText(slide, "McGILL / WELL-E", M, 38, 420, 36, {
    size: 22,
    bold: true,
    color: C.blue,
  });
  addRect(slide, 1018, 0, 262, 720, C.ink);
  addRect(slide, 1018, 0, 18, 720, C.cyan);
  addText(
    slide,
    "Objectif 1",
    M,
    170,
    850,
    74,
    { size: 58, bold: true },
  );
  addText(
    slide,
    "De données IceTag hétérogènes à des alertes interprétables",
    M,
    244,
    860,
    190,
    { size: 44, bold: true },
  );
  addText(
    slide,
    "Travail réalisé, résultats, livrables et suite proposée",
    M,
    486,
    760,
    60,
    { size: 24, color: C.muted },
  );
  addText(slide, "Réunion du 30 juillet 2026", M, 632, 500, 26, {
    size: 18,
    bold: true,
  });
  addText(slide, "Aliou Barry", 1062, 570, 170, 64, {
    size: 24,
    bold: true,
    color: C.white,
  });
  addNotes(
    slide,
    [
      "OUVERTURE PROPOSÉE (30 secondes)",
      "« L’objectif 1 ne consistait pas simplement à lancer un algorithme. Il fallait transférer une pipeline existante sur quatre corpus IceTag différents, harmoniser les entrées, produire des sorties reproductibles, puis qualifier ce que les alertes signifient réellement. »",
      "Annoncez le fil de la présentation : promesse contractuelle, travail technique, résultats, limites, livrables, prochaine décision.",
      "Message de posture : être précis sur ce qui est réussi et prudent sur ce qui n’est pas encore validé cliniquement.",
    ],
    [SRC.sow, SRC.report],
  );
}

// 2. Executive summary
{
  const slide = presentation.slides.add();
  addHeader(slide, "Le résultat en une minute", "Synthèse exécutive", 2);
  addText(
    slide,
    "Le transfert demandé par le SOW est réalisé et documenté. La sortie est un système de détection de signaux comportementaux à vérifier, pas un diagnostic clinique automatique.",
    M,
    158,
    1140,
    82,
    { size: 25, bold: true },
  );
  addRect(slide, M, 282, 360, 288, C.paper);
  addRect(slide, 460, 282, 360, 288, C.paper);
  addRect(slide, 872, 282, 360, 288, C.paper);
  statBlock(slide, 78, 326, 300, "4 / 4", "saisons IceTag exécutées", C.blue);
  statBlock(slide, 496, 326, 300, "375 031", "intervalles de 15 min produits", C.teal);
  statBlock(slide, 906, 326, 300, "385", "notifications brutes, toutes traçables", C.purple);
  addText(
    slide,
    "Les 385 notifications ont ensuite été requalifiées : 37 prioritaires (A), 195 individuelles à vérifier (B) et 153 probablement collectives (C).",
    78,
    482,
    1090,
    60,
    { size: 20, color: C.muted },
  );
  addPill(slide, "4 livrables SOW présents", M, 612, 250, C.green, "#E8F4ED");
  addPill(slide, "résultat reproductible", 316, 612, 238, C.blue, "#E8F0FC");
  addPill(slide, "validation clinique encore limitée", 584, 612, 316, C.red, "#FCEBEB");
  addNotes(
    slide,
    [
      "Dites d’abord le verdict : le résultat contractuel est positif, car les quatre saisons ont été traitées et les quatre livrables de l’objectif 1 sont présents.",
      "375 031 correspond au nombre total d’intervalles vache × 15 minutes, pas à 375 031 observations indépendantes de boiterie.",
      "385 est le nombre de notifications après regroupement temporel et délai de refroidissement de 12 heures. Ce n’est ni 385 vaches boiteuses ni 385 diagnostics.",
      "La requalification A/B/C est l’amélioration majeure apportée au livrable initial : elle rend la charge d’alertes interprétable en séparant les signaux individuels des événements collectifs.",
      "Formule sûre : « Objectif contractuellement atteint; performance clinique non démontrée faute de vérité-terrain suffisante. »",
    ],
    [SRC.sow, SRC.summary, SRC.reinforced, SRC.readme],
  );
}

// 3. SOW mapping
{
  const slide = presentation.slides.add();
  addHeader(slide, "Ce que le SOW demandait, et où c’est livré", "Engagement", 3);
  tableGrid(
    slide,
    M,
    164,
    [220, 325, 240, 397],
    [
      ["Tâche", "Livrable attendu", "État", "Emplacement"],
      ["1.1", "Données traitées + alertes", "Livré", "DONNEES_TRAITEES_ALERTES/"],
      ["1.1", "Note de reproductibilité", "Livrée", "NOTES_SOW/note_technique...md"],
      ["1.2", "Table de concordance", "Livrée", "TABLEAUX_CSV/table_concordance.csv"],
      ["1.2", "Rapport court de validation", "Livré", "NOTES_SOW/rapport_validation...md"],
    ],
    { rowH: 70, size: 17 },
  );
  addText(
    slide,
    "Montant associé dans le SOW : 3 700 $ pour les semaines 1 à 4.",
    M,
    556,
    720,
    36,
    { size: 21, bold: true },
  );
  addText(
    slide,
    "Le rapport Word et le PowerPoint sont des couches de communication ajoutées aux quatre livrables techniques.",
    M,
    602,
    1080,
    42,
    { size: 18, color: C.muted },
  );
  addNotes(
    slide,
    [
      "Cette diapositive est la réponse directe à « avez-vous livré ce qui était prévu ? »",
      "Parcourez les quatre lignes sans entrer encore dans la méthode.",
      "Précisez que le rapport Word et la présentation ne remplacent pas les fichiers techniques : ils les expliquent.",
      "Sur la rémunération : le montant du SOW couvre un transfert scientifique reproductible et une validation exploratoire, pas seulement la génération d’un document.",
      "Ne présentez pas l’annexe HYPO comme un livrable obligatoire du SOW; c’est une analyse complémentaire qui montre la continuité scientifique.",
    ],
    [SRC.sow, SRC.readme],
  );
}

// 4. Data landscape
{
  const slide = presentation.slides.add();
  addHeader(slide, "Les données réellement mobilisées", "Périmètre des données", 4);
  addText(
    slide,
    "Un inventaire large a servi à retrouver et qualifier les sources. L’analyse de l’objectif 1 porte ensuite sur quatre corpus IceTag ciblés.",
    M,
    152,
    1140,
    58,
    { size: 22 },
  );
  tableGrid(
    slide,
    M,
    236,
    [248, 155, 225, 275, 279],
    [
      ["Saison", "Profils", "Intervalles", "Période", "Couverture moyenne"],
      ["Winter 2019", "17", "136 929", "janv. – avr. 2019", "94,4 %"],
      ["Summer 2019", "18", "139 111", "juin – sept. 2019", "98,3 %"],
      ["Fall 2019", "30", "93 860", "nov. – déc. 2019", "99,3 %"],
      ["Fall 2021", "10 traités / 8 complets", "5 131", "30 nov. – 6 déc.", "100,0 %"],
    ],
    { rowH: 61, size: 17 },
  );
  addText(slide, "2 414 fichiers inventoriés", M, 584, 330, 34, {
    size: 22,
    bold: true,
    color: C.blue,
  });
  addText(
    slide,
    "≠ 2 414 fichiers injectés dans la pipeline. L’inventaire sert à identifier les bons corpus et leurs métadonnées.",
    350,
    584,
    830,
    48,
    { size: 18, color: C.muted },
  );
  addNotes(
    slide,
    [
      "Expliquez la différence entre inventaire documentaire et données analytiques.",
      "L’inventaire recensait 2 256 fichiers IceTag, 151 fichiers HOBO, 5 jeux de scans comportementaux, un agrégat comportemental et une documentation. Il a évité de mélanger des expériences, versions et formats.",
      "Les quatre lignes du tableau sont les données effectivement passées dans l’objectif 1.",
      "Fall 2021 : 10 profils ont été conservés dans la trace technique, mais seulement 8 sont considérés comme complets/utilisables pour l’interprétation. Cette transparence évite de masquer les profils partiels.",
      "Les couvertures moyennes élevées indiquent une bonne densité globale, mais quelques bins à faible couverture existent; les règles de qualité les filtrent.",
    ],
    [SRC.inventory, SRC.summary, SRC.report],
  );
}

// 5. Harmonization
{
  const slide = presentation.slides.add();
  addHeader(slide, "Pourquoi une adaptation était indispensable", "Ingénierie des données", 5);
  const items = [
    ["Formats", "noms de colonnes et unités variables"],
    ["Temps", "timestamps hétérogènes, colonne T absente au départ"],
    ["Identité", "Cow_ID, couleurs et correspondances selon l’expérience"],
    ["Qualité", "couverture, doublons, valeurs négatives et profils partiels"],
  ];
  items.forEach((item, i) => {
    const y = 166 + i * 112;
    addText(slide, String(i + 1).padStart(2, "0"), M, y, 70, 44, {
      size: 30,
      bold: true,
      color: i % 2 ? C.teal : C.blue,
    });
    addText(slide, item[0], 132, y, 210, 40, {
      size: 24,
      bold: true,
    });
    addText(slide, item[1], 350, y, 510, 58, {
      size: 21,
      color: C.muted,
    });
    addLine(slide, 132, y + 74, 730, C.grid, 1);
  });
  addRect(slide, 900, 160, 280, 420, C.paper);
  labelAbove(slide, "Schéma canonique", 928, 190, 220, C.blue);
  ["Cow", "T", "Steps", "Motion Index", "Lying / Standing", "Transitions"].forEach(
    (value, i) => {
      addPill(slide, value, 928, 228 + i * 52, 224, C.ink, C.white);
    },
  );
  addText(
    slide,
    "Résultat : la même pipeline peut lire les quatre saisons sans modifier sa logique.",
    132,
    612,
    980,
    40,
    { size: 21, bold: true },
  );
  addNotes(
    slide,
    [
      "C’est ici qu’il faut rendre visible le travail qui ne se voit pas dans le nombre final d’alertes.",
      "L’erreur initiale « None of ['T'] are in the columns » montrait que les fichiers McGill n’étaient pas directement compatibles avec la pipeline. La conversion crée une colonne temporelle canonique T et harmonise Cow.",
      "Le module io.py normalise les colonnes et les types; il trie les observations, convertit les durées et traite les valeurs impossibles.",
      "La logique métier et les seuils restent ensuite identiques entre saisons. C’est important pour la comparaison : l’adaptation porte sur les entrées, pas sur un réglage opportuniste par saison.",
      "Réponse courte à « pourquoi autant de fichiers/scripts ? » : chaque couche a une responsabilité distincte et vérifiable.",
    ],
    [SRC.io, SRC.nbConvert, SRC.nbAudit, SRC.note],
  );
}

// 6. Pipeline flow
{
  const slide = presentation.slides.add();
  addHeader(slide, "La chaîne d’analyse appliquée aux quatre saisons", "Méthode", 6);
  const steps = [
    ["1", "Harmoniser", "Cow, T, mesures"],
    ["2", "Agrèger", "bins de 15 min"],
    ["3", "Construire", "features robustes"],
    ["4", "Détecter", "Isolation Forest"],
    ["5", "Confirmer", "règles + persistance"],
    ["6", "Qualifier", "A / B / C"],
  ];
  const boxW = 176;
  const gap = 22;
  steps.forEach((step, i) => {
    const x = M + i * (boxW + gap);
    addRect(slide, x, 232, boxW, 220, i === 5 ? C.ink : C.paper, {
      lineFill: i === 5 ? C.ink : C.grid,
      lineWidth: 1,
    });
    addText(slide, step[0], x + 18, 252, 54, 44, {
      size: 28,
      bold: true,
      color: i === 5 ? C.cyan : C.blue,
    });
    addText(slide, step[1], x + 18, 318, boxW - 36, 54, {
      size: 19,
      bold: true,
      color: i === 5 ? C.white : C.ink,
    });
    addText(slide, step[2], x + 18, 380, boxW - 36, 52, {
      size: 17,
      color: i === 5 ? "#CED4DC" : C.muted,
    });
    if (i < steps.length - 1) {
      addRect(slide, x + boxW + 4, 330, 14, 14, C.blue, {
        geometry: "chevron",
      });
    }
  });
  addText(
    slide,
    "Le modèle propose des anomalies; les règles temporelles et comportementales déterminent les épisodes; le contexte troupeau détermine la priorité.",
    M,
    514,
    1160,
    70,
    { size: 22, bold: true },
  );
  addText(
    slide,
    "La sortie finale reste une alerte à vérifier, jamais une confirmation clinique automatique.",
    M,
    604,
    1160,
    38,
    { size: 20, color: C.red, bold: true },
  );
  addNotes(
    slide,
    [
      "Décrivez la logique dans cet ordre; ne commencez pas par Isolation Forest.",
      "Les données sont agrégées sur 15 minutes. Les features incluent notamment des scores robustes, des différences temporelles, des moyennes mobiles et des variables cycliques d’heure.",
      "Isolation Forest est entraîné par vache : il cherche des états atypiques par rapport au fonctionnement habituel de la même vache.",
      "Les règles retiennent un épisode dans une fenêtre glissante de 7 heures lorsque le taux d’anomalies atteint au moins 24 %, que les signaux comportementaux sont cohérents et que la couverture est suffisante.",
      "Une notification est déclenchée au début de l’épisode; le délai de 12 heures évite les répétitions rapprochées.",
      "Le renforcement troupeau ne remplace pas la pipeline : il intervient après la notification et requalifie les 385 sorties selon le contexte collectif et le caractère spécifique à la vache.",
    ],
    [SRC.features, SRC.model, SRC.pipeline, SRC.alerts, SRC.reinforcement],
  );
}

// 7. Frozen parameters
{
  const slide = presentation.slides.add();
  addHeader(slide, "Des paramètres gelés pour une comparaison honnête", "Reproductibilité", 7);
  const params = [
    ["15 min", "intervalle"],
    ["6 %", "contamination IF"],
    ["7 h", "persistance"],
    ["12 h", "délai entre notifications"],
    ["25 %", "couverture minimale"],
    ["42", "graine aléatoire"],
  ];
  params.forEach((p, i) => {
    const col = i % 3;
    const row = Math.floor(i / 3);
    const x = M + col * 400;
    const y = 170 + row * 190;
    addLine(slide, x, y, 330, i < 3 ? C.blue : C.teal, 5);
    addText(slide, p[0], x, y + 24, 330, 58, {
      size: 38,
      bold: true,
    });
    addText(slide, p[1], x, y + 92, 330, 48, {
      size: 18,
      color: C.muted,
    });
  });
  addRect(slide, M, 554, 1184, 78, C.ink);
  addText(
    slide,
    "Pourquoi : empêcher qu’un ajustement différent par saison fabrique artificiellement de “bons” résultats.",
    M + 24,
    575,
    1110,
    40,
    { size: 21, color: C.white, bold: true },
  );
  addNotes(
    slide,
    [
      "Les paramètres sont centraux pour la défendabilité : ils sont définis une fois dans config.py et réutilisés.",
      "La contamination à 6 % est la proportion attendue de points atypiques dans le modèle, pas la proportion attendue de vaches boiteuses.",
      "La persistance de 7 heures et le délai de 12 heures évitent qu’un même épisode génère une notification à chaque intervalle.",
      "Le seuil de couverture protège contre les conclusions basées sur des intervalles presque vides.",
      "Réponse à « avez-vous optimisé sur les scores SLS ? » : non. Les seuils du livrable principal ont été gelés; les SLS servent à une analyse de concordance séparée.",
    ],
    [SRC.config, SRC.alerts, SRC.note],
  );
}

// 8. Outputs
{
  const slide = presentation.slides.add();
  addHeader(slide, "Trois niveaux de sortie par saison", "Traçabilité", 8);
  const columns = [
    {
      x: M,
      color: C.blue,
      title: "predictions.csv",
      label: "Niveau intervalle",
      body: "Une ligne par vache et par bin de 15 min : features, scores, drapeaux et qualité.",
    },
    {
      x: 445,
      color: C.teal,
      title: "alerts_only.csv",
      label: "Niveau notification",
      body: "Seulement les débuts d’épisodes retenus après règles, persistance et cooldown.",
    },
    {
      x: 842,
      color: C.purple,
      title: "summary.csv",
      label: "Niveau synthèse",
      body: "Résultats par vache : nombre de bins, anomalies, épisodes et notifications.",
    },
  ];
  columns.forEach((col) => {
    addRect(slide, col.x, 180, 350, 360, C.paper);
    addRect(slide, col.x, 180, 350, 12, col.color);
    labelAbove(slide, col.label, col.x + 24, 224, 300, col.color);
    addText(slide, col.title, col.x + 24, 270, 300, 58, {
      size: 25,
      bold: true,
    });
    addText(slide, col.body, col.x + 24, 346, 300, 132, {
      size: 20,
      color: C.muted,
    });
  });
  addText(
    slide,
    "Puis : objective1_reinforced_alerts.csv ajoute le contexte troupeau et la priorité A/B/C sans effacer les résultats initiaux.",
    M,
    582,
    1160,
    56,
    { size: 21, bold: true },
  );
  addNotes(
    slide,
    [
      "Cette diapositive répond à « à quoi servent tous les CSV ? »",
      "predictions.csv est la trace la plus détaillée et la plus volumineuse; elle permet de reproduire un graphique ou d’auditer une décision à un instant donné.",
      "alerts_only.csv est le fichier opérationnel à examiner pour les événements.",
      "summary.csv sert au contrôle rapide par vache et à la synthèse saisonnière.",
      "Le fichier renforcé conserve la notification initiale et ajoute des colonnes de contexte. Cette séparation évite de réécrire l’historique du pipeline.",
      "Les dates anciennes visibles dans Finder correspondent à la génération initiale du 29 mai. Elles ont été conservées pour la traçabilité; les sorties renforcées sont plus récentes.",
    ],
    [SRC.readme, SRC.summary, SRC.reinforced],
  );
}

// 9. Alerts by season
{
  const slide = presentation.slides.add();
  addHeader(slide, "385 notifications brutes sur quatre saisons", "Résultats", 9);
  const data = [
    ["Winter 2019", 149, 14, 46, 89],
    ["Summer 2019", 127, 16, 94, 17],
    ["Fall 2019", 105, 7, 51, 47],
    ["Fall 2021", 4, 0, 4, 0],
  ];
  const max = 160;
  const chartX = 250;
  const chartW = 900;
  const barH = 66;
  data.forEach((d, i) => {
    const y = 174 + i * 112;
    addText(slide, d[0], M, y + 18, 180, 34, {
      size: 19,
      bold: true,
    });
    let x = chartX;
    const parts = [
      [d[2], C.blue, "A"],
      [d[3], C.cyan, "B"],
      [d[4], "#AEB5C0", "C"],
    ];
    parts.forEach((p) => {
      const w = (p[0] / max) * chartW;
      if (w > 0) {
        addRect(slide, x, y, w, barH, p[1]);
        if (w > 38) {
          addText(slide, String(p[0]), x, y + 18, w, 30, {
            size: 18,
            bold: true,
            align: "center",
            color: p[2] === "C" ? C.ink : C.white,
          });
        }
        x += w;
      }
    });
    addText(slide, String(d[1]), x + 12, y + 17, 80, 30, {
      size: 21,
      bold: true,
    });
  });
  addPill(slide, "A prioritaire", 250, 625, 160, C.white, C.blue);
  addPill(slide, "B à vérifier", 430, 625, 170, C.ink, C.cyan);
  addPill(slide, "C collectif probable", 620, 625, 220, C.ink, "#AEB5C0");
  addText(slide, "Longueur des barres = total par saison", 880, 632, 300, 24, {
    size: 15,
    color: C.muted,
    align: "right",
  });
  addNotes(
    slide,
    [
      "Lisez les totaux de droite : 149 + 127 + 105 + 4 = 385.",
      "Les segments montrent la qualification finale. Winter 2019 a beaucoup d’alertes collectives, ce qui explique pourquoi le nombre brut semblait trop élevé.",
      "Fall 2021 a seulement quatre notifications parce que la fenêtre est très courte, environ six jours. Ce résultat n’est pas comparable aux saisons de plusieurs mois.",
      "Les taux normalisés étaient de 10,45, 8,76, 10,74 et 7,48 notifications par 100 vache-jours respectivement. Ils servent mieux que les totaux pour comparer des durées différentes.",
      "Formule sûre : « Le volume brut n’est pas interprété seul; il est normalisé par exposition et requalifié par contexte. »",
    ],
    [SRC.summary, SRC.reinforced],
  );
}

// 10. Reclassification
{
  const slide = presentation.slides.add();
  addHeader(slide, "A, B et C hiérarchisent la revue, pas la boiterie", "Renforcement scientifique", 10);
  addText(
    slide,
    "IF + règles produit d’abord 385 notifications. Le contexte troupeau les classe ensuite sans modifier ce total.",
    M,
    154,
    1120,
    62,
    { size: 23, bold: true },
  );
  const total = 385;
  const parts = [
    { n: 37, label: "A — prioritaire", color: C.blue },
    { n: 195, label: "B — à vérifier", color: C.cyan },
    { n: 153, label: "C — collectif probable", color: "#AEB5C0" },
  ];
  let x = M;
  parts.forEach((p) => {
    const w = (p.n / total) * (W - M * 2);
    addRect(slide, x, 274, w, 112, p.color);
    if (w > 80) {
      addText(slide, String(p.n), x, 298, w, 42, {
        size: 28,
        bold: true,
        align: "center",
        color: p.color === "#AEB5C0" ? C.ink : C.white,
      });
      addText(slide, `${Math.round((p.n / total) * 100)} %`, x, 344, w, 28, {
        size: 16,
        align: "center",
        color: p.color === "#AEB5C0" ? C.ink : C.white,
      });
    }
    x += w;
  });
  parts.forEach((p, i) => {
    const xx = M + i * 395;
    addRect(slide, xx, 446, 18, 18, p.color);
    addText(slide, p.label, xx + 30, 440, 320, 32, {
      size: 19,
      bold: true,
    });
    const descriptions = [
      "Non collective + profil distinct du troupeau + score interne ≥ 45.",
      "Non collective + appui troupeau moins net ou score plus modéré.",
      "≥ 30 % des vaches sur ± 1 jour, ou ≥ 50 % sur ± 3 jours.",
    ];
    const actions = [
      "Revoir en premier",
      "Vérifier la vache",
      "Rechercher une cause commune",
    ];
    addText(slide, descriptions[i], xx, 488, 340, 76, {
      size: 16,
      color: C.muted,
    });
    addText(slide, actions[i], xx, 568, 340, 30, {
      size: 17,
      bold: true,
      color: i === 0 ? C.blue : i === 1 ? C.teal : C.purple,
    });
  });
  addText(
    slide,
    "A/B/C ne sont ni des stades cliniques ni des sorties HYPO. D est prévu pour une qualité insuffisante : 0 cas.",
    M,
    622,
    1100,
    34,
    { size: 18, bold: true, color: C.red },
  );
  addNotes(
    slide,
    [
      "Commencez par préciser les deux étapes : la baseline IF + règles produit 385 notifications; la couche troupeau les classe ensuite sans en ajouter ni en supprimer.",
      "Le contexte troupeau est valide si la couverture atteint au moins 75 % pour au moins 50 % du troupeau, avec un minimum de cinq vaches au même timestamp.",
      "A : notification non collective, déviation spécifique de la vache par rapport à la médiane contemporaine du troupeau et score lame_confidence ≥ 45. A signifie priorité de revue, pas certitude clinique.",
      "B : notification non collective, mais appui troupeau moins net ou score plus modéré. Elle reste à vérifier individuellement.",
      "C : notification située dans un événement touchant au moins 30 % des vaches dans ± 1 jour ou au moins 50 % dans ± 3 jours. Elle oriente vers une cause commune possible : gestion, exercice, météo, manipulation ou problème technique.",
      "La règle de classement est ordonnée : une qualité insuffisante donnerait D; un événement collectif donne C; sinon un signal spécifique avec score ≥ 45 donne A; les autres notifications valides donnent B.",
      "Aucune notification n’a été classée D dans la sortie finale.",
      "Le score lame_confidence combine empiriquement cohérence des familles de signaux, taux d’anomalies, Motion Index et extrémité du score IF. Il sert au classement relatif et ne doit pas être lu comme une probabilité clinique.",
      "A/B/C appartient au renforcement de la baseline contractuelle IF. L’approche HYPO + instabilité + hybride reste une analyse complémentaire séparée en annexe.",
    ],
    [SRC.reinforced, SRC.reinforcement, SRC.alerts, SRC.report],
  );
}

// 11. Collective events
{
  const slide = presentation.slides.add();
  addHeader(slide, "Les événements collectifs expliquent une grande part du bruit", "Contexte troupeau", 11);
  const collective = [
    ["Winter 2019", 59.7],
    ["Fall 2019", 44.8],
    ["Summer 2019", 13.4],
    ["Fall 2021", 0.0],
  ];
  collective.forEach((d, i) => {
    const y = 178 + i * 105;
    addText(slide, d[0], M, y + 11, 190, 34, { size: 19, bold: true });
    addRect(slide, 254, y, 830, 50, C.panel);
    const width = (d[1] / 65) * 830;
    if (width > 0) addRect(slide, 254, y, width, 50, i === 0 ? C.purple : C.teal);
    addText(slide, `${d[1].toFixed(1).replace(".", ",")} %`, 1100, y + 10, 100, 30, {
      size: 20,
      bold: true,
      align: "right",
    });
  });
  addRect(slide, M, 592, 1160, 54, "#FFF6D8");
  addText(
    slide,
    "Conclusion : le filtre collectif réduit le risque d’interpréter un événement de troupeau comme une boiterie individuelle.",
    M + 20,
    608,
    1110,
    28,
    { size: 19, bold: true },
  );
  addNotes(
    slide,
    [
      "Winter 2019 : 89 des 149 notifications ont été marquées collectives, soit 59,7 %. Fall 2019 : 47 sur 105, soit 44,8 %.",
      "Cette lecture est plus crédible que de présenter toutes les alertes comme des suspicions individuelles.",
      "Le filtre collectif ne prouve pas la cause de l’événement. Il signale seulement que plusieurs vaches ont changé simultanément.",
      "Réponse à « les alertes sont-elles trop nombreuses ? » : le nombre brut était trop peu informatif; la requalification montre qu’environ 40 % sont probablement contextuelles, et seulement 37 sont prioritaires.",
      "Si on vous demande le taux global : 153 / 385 = 39,7 % d’événements collectifs probables.",
    ],
    [SRC.reinforced, SRC.report],
  );
}

// 12. Behavioral concordance
{
  const slide = presentation.slides.add();
  addHeader(slide, "Concordance temporelle avec les scans comportementaux", "Tâche 1.2", 12);
  const d = [
    ["Fall 2019", 44.4, "12 / 27"],
    ["Winter 2019", 26.8, "11 / 41"],
    ["Summer 2019", 24.1, "14 / 58"],
    ["Fall 2021", 0.4, "1 / 270"],
  ];
  d.forEach((row, i) => {
    const y = 180 + i * 92;
    addText(slide, row[0], M, y + 9, 180, 30, { size: 19, bold: true });
    addRect(slide, 240, y, 680, 46, C.panel);
    addRect(slide, 240, y, (row[1] / 50) * 680, 46, i === 0 ? C.blue : C.teal);
    addText(slide, `${row[1].toFixed(1).replace(".", ",")} %`, 940, y + 7, 110, 30, {
      size: 20,
      bold: true,
      align: "right",
    });
    addText(slide, row[2], 1080, y + 8, 110, 28, {
      size: 17,
      color: C.muted,
      align: "right",
    });
  });
  addText(
    slide,
    "Interprétation correcte : chevauchement descriptif ±1 jour. Ces scans ne sont pas des diagnostics cliniques et les expériences ne sont pas directement comparables.",
    M,
    574,
    1130,
    70,
    { size: 20, bold: true, color: C.red },
  );
  addNotes(
    slide,
    [
      "Expliquez exactement ce qui est mesuré : proportion de scans ayant au moins une alerte dans une fenêtre de plus ou moins un jour.",
      "Ce résultat répond au livrable de concordance, mais il ne donne ni sensibilité ni spécificité.",
      "Les comportements observés sont des contextes complémentaires. Ils ne sont pas une vérité-terrain clinique de boiterie.",
      "Fall 2021 doit être interprété à part : 270 lignes de scans sur une fenêtre IceTag très courte et un mapping d’identité différent. Le taux de 0,4 % reflète surtout le faible recouvrement temporel.",
      "Ne dites pas que 44,4 % est une précision de 44,4 %. C’est un taux de coexistence temporelle.",
    ],
    [SRC.concordance, SRC.validation, SRC.sow],
  );
}

// 13. SLS
{
  const slide = presentation.slides.add();
  addHeader(slide, "Les scores SLS : un signal prometteur, mais un petit échantillon", "Validation exploratoire", 13);
  addRect(slide, M, 170, 530, 360, C.paper);
  labelAbove(slide, "Pipeline contractuelle IF + règles", 80, 204, 430, C.blue);
  addText(slide, "Pas de concordance observée", 80, 252, 430, 52, {
    size: 28,
    bold: true,
  });
  addText(slide, "16 vaches\n5 avec SLS ≥ 2\np = 0,649\nρ = 0,033", 80, 326, 360, 170, {
    size: 23,
    color: C.muted,
  });
  addRect(slide, 650, 170, 530, 360, C.ink);
  labelAbove(slide, "Annexe HYPO + instabilité + hybride", 686, 204, 450, C.cyan);
  addText(slide, "Séparation exploratoire", 686, 252, 430, 52, {
    size: 28,
    bold: true,
    color: C.white,
  });
  addText(slide, "14 vaches évaluables\n3 avec SLS ≥ 2\nAUC = 0,924\np = 0,031", 686, 326, 360, 170, {
    size: 23,
    color: "#D9DEE5",
  });
  addRect(slide, M, 566, 1132, 74, "#FFF6D8");
  addText(
    slide,
    "Conclusion défendable : résultat encourageant pour l’hybride, trop fragile pour annoncer une performance diagnostique.",
    M + 22,
    586,
    1084,
    38,
    { size: 20, bold: true },
  );
  addNotes(
    slide,
    [
      "Cette comparaison doit être présentée avec beaucoup de discipline.",
      "La pipeline IF du SOW n’a pas montré d’association avec les SLS dans la cohorte disponible.",
      "L’annexe applique l’approche scientifique actuelle HYPO + instabilité + hybride aux mêmes corpus. Sur la fenêtre pré-SLS, le mode hiérarchique obtient une AUC de 0,924 et p = 0,031.",
      "Mais il n’y a que 14 vaches évaluables et seulement 3 cas SLS ≥ 2. Une AUC élevée peut être instable dans un échantillon aussi petit.",
      "Les cohortes et définitions de notification diffèrent entre les deux analyses. On ne doit donc pas annoncer une amélioration clinique quantifiée de 0,033 à 0,924.",
      "Réponse sûre : « l’annexe identifie une direction prometteuse à valider prospectivement; elle ne transforme pas l’objectif 1 en outil diagnostique validé. »",
    ],
    [SRC.sls, SRC.annexTotal, SRC.report],
  );
}

// 14. Verdict
{
  const slide = presentation.slides.add();
  addHeader(slide, "Ce qui est réussi, et ce qui reste à démontrer", "Verdict scientifique", 14);
  addRect(slide, M, 170, 555, 416, "#EAF4EF");
  addRect(slide, 625, 170, 555, 416, "#FCEDED");
  labelAbove(slide, "Réussi", 84, 206, 420, C.green);
  [
    "Transfert sur quatre saisons",
    "Pipeline reproductible et paramètres gelés",
    "Sorties détaillées, alertes et synthèses",
    "Concordance comportementale documentée",
    "Priorisation A/B/C par contexte troupeau",
  ].forEach((t, i) => bullet(slide, t, 84, 250 + i * 58, 470, { color: C.green, size: 19 }));
  labelAbove(slide, "Non démontré à ce stade", 661, 206, 440, C.red);
  [
    "Diagnostic clinique automatique",
    "Sensibilité et spécificité fiables",
    "Seuils optimaux généralisables",
    "Cause exacte des événements collectifs",
    "Supériorité clinique confirmée de l’hybride",
  ].forEach((t, i) => bullet(slide, t, 661, 250 + i * 58, 470, { color: C.red, size: 19 }));
  addText(
    slide,
    "Le travail est positif parce qu’il transforme des données hétérogènes en une analyse vérifiable et précise honnêtement la portée du résultat.",
    M,
    620,
    1130,
    38,
    { size: 20, bold: true },
  );
  addNotes(
    slide,
    [
      "Ne laissez pas « absence de validation clinique » être interprétée comme « échec du projet ».",
      "Le SOW demandait une application et une évaluation. Une évaluation scientifique peut conclure qu’un signal est exploitable comme alerte mais insuffisant comme diagnostic.",
      "Le résultat positif est la chaîne complète, reproductible et auditée, plus la qualification des limites.",
      "La principale limite vient du manque de labels cliniques synchronisés et suffisamment nombreux, pas d’une absence de traitement.",
      "Phrase clé : « Nous avons réduit l’incertitude : nous savons ce que la pipeline produit, dans quelles conditions, et ce qu’il faut mesurer ensuite pour la valider. »",
    ],
    [SRC.sow, SRC.report, SRC.validation, SRC.sls],
  );
}

// 15. Folder map
{
  const slide = presentation.slides.add();
  addHeader(slide, "Comment lire le dossier de livraison", "Architecture des livrables", 15);
  addText(slide, "README_livraison_objectif1.txt", M, 160, 450, 42, {
    size: 24,
    bold: true,
    color: C.blue,
  });
  addText(slide, "Point d’entrée : contenu, correspondance SOW et limites.", M, 202, 620, 42, {
    size: 18,
    color: C.muted,
  });
  const folders = [
    ["RAPPORTS/", "Rapport Word + présentation", C.blue],
    ["DONNEES_TRAITEES_ALERTES/", "Sorties détaillées et alertes", C.teal],
    ["TABLEAUX_CSV/", "Synthèses et concordance", C.purple],
    ["NOTES_SOW/", "Reproductibilité et validation", C.green],
    ["ANNEXE_pipeline_actuelle_…/", "HYPO + instabilité + hybride", C.red],
  ];
  folders.forEach((f, i) => {
    const y = 274 + i * 70;
    addRect(slide, M, y, 24, 24, f[2]);
    addText(slide, f[0], 88, y - 3, 420, 34, {
      size: 21,
      bold: true,
    });
    addText(slide, f[1], 540, y - 2, 600, 34, {
      size: 19,
      color: C.muted,
    });
  });
  addRect(slide, 866, 154, 314, 82, C.ink);
  addText(slide, "Ordre conseillé", 888, 171, 270, 26, {
    size: 15,
    bold: true,
    color: C.cyan,
  });
  addText(slide, "README → Rapport → CSV", 888, 199, 270, 26, {
    size: 18,
    bold: true,
    color: C.white,
  });
  addNotes(
    slide,
    [
      "Cette carte est destinée au destinataire du dossier.",
      "README : commencer ici.",
      "RAPPORTS : version lisible pour la décision; le fichier Word est la référence narrative.",
      "DONNEES_TRAITEES_ALERTES : preuves de l’exécution, par saison et par vache.",
      "TABLEAUX_CSV : chiffres de synthèse utilisés dans les rapports.",
      "NOTES_SOW : description reproductible et rapport de concordance exigés par le contrat.",
      "ANNEXE : approche HYPO + instabilité + hybride, fournie séparément pour ne pas confondre la baseline contractuelle et l’évolution scientifique.",
    ],
    [SRC.readme],
  );
}

// 16. Scripts and notebooks
{
  const slide = presentation.slides.add();
  addHeader(slide, "Les notebooks et scripts, chacun avec un rôle précis", "Reproductibilité technique", 16);
  tableGrid(
    slide,
    M,
    156,
    [320, 390, 472],
    [
      ["Fichier", "Rôle", "Pourquoi il existe"],
      ["01_audit_donnees_mcgill.ipynb", "Inventaire et qualité", "Comprendre formats, périodes et lacunes"],
      ["02_convert_icetag_to_pipeline.ipynb", "Conversion canonique", "Produire Cow, T et mesures compatibles"],
      ["05_objectif1_pipeline_icetag.ipynb", "Exécution principale", "Lancer la pipeline sur les 4 saisons"],
      ["10_tache1_2_concordance…ipynb", "Alignement scans-alertes", "Répondre à la tâche 1.2"],
      ["13_objectif1_renforcement…ipynb", "Contexte troupeau", "Classer A/B/C et contrôler le collectif"],
      ["run_objective1_reinforcement.py", "Traitement automatisé", "Rejouer la qualification sans édition manuelle"],
    ],
    { rowH: 65, size: 16 },
  );
  addText(
    slide,
    "L’annexe HYPO est construite par un script de lecture séparé; aucun fichier du dépôt du mémoire n’est modifié.",
    M,
    616,
    1130,
    38,
    { size: 18, bold: true, color: C.red },
  );
  addNotes(
    slide,
    [
      "Présentez ces fichiers comme une chaîne de preuves, pas comme une collection de notebooks.",
      "01 répond à « quelles données avons-nous ? »; 02 à « comment les rendre compatibles ? »; 05 à « comment reproduire les alertes ? »; 10 à « comment vérifier la concordance ? »; 13 à « comment réduire les alertes collectives ? ».",
      "Les modules core/ contiennent la logique réutilisable; les notebooks racontent et exécutent l’expérience McGill.",
      "Le script de renforcement permet de rejouer le post-traitement de manière déterministe, ce qui évite les manipulations manuelles.",
      "L’annexe lit les sorties de l’approche actuelle et les repaquette pour McGill; elle n’écrit pas dans le dépôt du mémoire.",
    ],
    [SRC.nbAudit, SRC.nbConvert, SRC.nbPipeline, SRC.nbConcordance, SRC.nbReinforcement, SRC.reinforcement, SRC.annexScript],
  );
}

// 17. Value
{
  const slide = presentation.slides.add();
  addHeader(slide, "Ce que rémunère réellement l’objectif 1", "Valeur du travail", 17);
  const phases = [
    ["1", "Cartographier", "identifier les bonnes sources parmi des milliers de fichiers"],
    ["2", "Harmoniser", "rendre quatre expériences compatibles sans altérer la logique"],
    ["3", "Exécuter", "produire 375 031 bins et des sorties auditables"],
    ["4", "Évaluer", "concordance, couverture, collectif, SLS et limites"],
    ["5", "Livrer", "documentation, CSV, rapport Word et présentation"],
  ];
  phases.forEach((p, i) => {
    const x = M + i * 232;
    addText(slide, p[0], x, 176, 50, 38, {
      size: 25,
      bold: true,
      color: C.blue,
    });
    if (i < phases.length - 1) addLine(slide, x + 46, 194, 175, C.grid, 2);
    addText(slide, p[1], x, 244, 200, 42, {
      size: 22,
      bold: true,
    });
    addText(slide, p[2], x, 304, 200, 132, {
      size: 17,
      color: C.muted,
    });
  });
  addRect(slide, M, 492, 1160, 116, C.ink);
  addText(slide, "3 700 $", 76, 520, 230, 56, {
    size: 40,
    bold: true,
    color: C.cyan,
  });
  addText(
    slide,
    "Le montant est justifié par une chaîne complète de recherche appliquée, reproductible et livrée, pas par le nombre d’alertes ni par une promesse de diagnostic.",
    330,
    516,
    820,
    66,
    { size: 21, bold: true, color: C.white },
  );
  addNotes(
    slide,
    [
      "Ne soyez pas défensif. Montrez la correspondance entre la charge et les preuves livrées.",
      "La partie la plus coûteuse est la compréhension et l’alignement de données hétérogènes, puis le contrôle scientifique des résultats.",
      "Le fait d’avoir identifié une limite clinique n’annule pas le travail; c’est le résultat attendu d’une évaluation honnête.",
      "Réponse à « pourquoi 3 700 $ ? » : « Le SOW rémunère quatre semaines de transfert, adaptation, exécution, validation exploratoire et documentation. Les quatre livrables sont présents et chaque chiffre peut être retracé jusqu’aux sorties par intervalle. »",
      "Évitez de justifier le montant par le volume de code ou le nombre de pages.",
    ],
    [SRC.sow, SRC.readme, SRC.note, SRC.validation],
  );
}

// 18. Next steps
{
  const slide = presentation.slides.add();
  addHeader(slide, "La suite : passer de l’alerte au test clinique", "Prochaine décision", 18);
  const steps = [
    {
      n: "01",
      title: "Verrouiller les labels",
      body: "Obtenir des scores locomoteurs datés, plusieurs niveaux de gravité et assez de cas positifs.",
      color: C.blue,
    },
    {
      n: "02",
      title: "Valider prospectivement",
      body: "Geler la pipeline hybride, définir les fenêtres et mesurer sensibilité, spécificité et délai.",
      color: C.teal,
    },
    {
      n: "03",
      title: "Tester l’opérationnel",
      body: "Revue des A d’abord, puis B; documenter les causes des C et le temps de suivi.",
      color: C.purple,
    },
  ];
  steps.forEach((s, i) => {
    const x = M + i * 396;
    addText(slide, s.n, x, 174, 100, 42, {
      size: 26,
      bold: true,
      color: s.color,
    });
    addLine(slide, x, 226, 330, s.color, 5);
    addText(slide, s.title, x, 258, 330, 64, {
      size: 25,
      bold: true,
    });
    addText(slide, s.body, x, 342, 330, 160, {
      size: 20,
      color: C.muted,
    });
  });
  addRect(slide, M, 560, 1160, 78, "#E9F0FB");
  addText(
    slide,
    "Décision demandée à McGill : confirmer le livrable 1 et choisir la cohorte clinique qui servira à la validation suivante.",
    M + 22,
    581,
    1110,
    38,
    { size: 21, bold: true, color: C.blue },
  );
  addNotes(
    slide,
    [
      "La suite logique n’est pas de multiplier les modèles. C’est d’améliorer la vérité-terrain.",
      "Étape 1 : réunir des scores locomoteurs ou SLS datés et synchronisés avec les capteurs, idéalement répétés par vache.",
      "Étape 2 : choisir avant l’analyse la version de pipeline, les fenêtres et les métriques. Cela évite l’optimisation après coup.",
      "Étape 3 : mesurer aussi l’utilité opérationnelle : combien d’alertes à revoir, combien de causes collectives, combien de jours avant le score clinique.",
      "Question à poser en réunion : « Quelle cohorte McGill peut fournir le meilleur recouvrement entre IceTag et scores locomoteurs indépendants ? »",
    ],
    [SRC.report, SRC.sls, SRC.validation],
  );
}

// 19. Close
{
  const slide = presentation.slides.add();
  slide.background.fill = C.ink;
  addText(slide, "CONCLUSION", M, 46, 300, 28, {
    size: 15,
    bold: true,
    color: C.cyan,
  });
  addText(
    slide,
    "Un objectif livré,\nun résultat qualifié,\nune validation à poursuivre.",
    M,
    156,
    900,
    300,
    { size: 54, bold: true, color: C.white },
  );
  addText(
    slide,
    "La valeur du travail est de rendre les données et les alertes traçables, comparables et scientifiquement interprétables.",
    M,
    520,
    890,
    96,
    { size: 25, color: "#D1D7DE" },
  );
  addRect(slide, 1015, 0, 18, 720, C.cyan);
  addText(slide, "Questions", 1060, 586, 170, 40, {
    size: 26,
    bold: true,
    color: C.white,
    align: "right",
  });
  addNotes(
    slide,
    [
      "CONCLUSION PROPOSÉE (20 secondes)",
      "« L’objectif 1 est terminé au sens du SOW : les quatre saisons sont traitées, les sorties sont reproductibles et les quatre livrables sont présents. L’analyse montre que la pipeline est utile comme système d’alerte comportementale, surtout après qualification du contexte troupeau. La prochaine étape scientifique est une validation prospective avec davantage de labels cliniques synchronisés. »",
      "Après cette phrase, arrêtez-vous et invitez les questions.",
    ],
    [SRC.sow, SRC.readme, SRC.report],
  );
}

// 20. Appendix - 385 alerts
{
  const slide = presentation.slides.add();
  addHeader(slide, "Q : 385 alertes, n’est-ce pas trop ?", "Annexe — Questions difficiles", 20);
  addText(slide, "Réponse courte", M, 164, 300, 34, {
    size: 18,
    bold: true,
    color: C.blue,
  });
  addText(
    slide,
    "385 est un total multi-saison avant priorisation, pas 385 diagnostics.",
    M,
    210,
    1080,
    58,
    { size: 30, bold: true },
  );
  const answers = [
    ["Exposition", "9,86 notifications / 100 vache-jours au total"],
    ["Priorité", "37 seulement sont classées A"],
    ["Contexte", "153 sont probablement collectives"],
    ["Action", "la file de revue devient A → B → investigation des C"],
  ];
  answers.forEach((a, i) => {
    const y = 320 + i * 70;
    addText(slide, a[0], M, y, 180, 34, { size: 19, bold: true });
    addText(slide, a[1], 240, y, 900, 42, { size: 19, color: C.muted });
  });
  addNotes(
    slide,
    [
      "Réponse complète : « Le chiffre brut n’a pas de sens sans durée, nombre de vaches et contexte. Le taux global est d’environ 9,86 notifications par 100 vache-jours. Après qualification, 37 sont prioritaires et 153 semblent collectives. »",
      "Ajoutez que le seuil opérationnel devra être calibré avec des utilisateurs et des labels cliniques, car une bonne sensibilité scientifique peut produire une charge excessive sur le terrain.",
    ],
    [SRC.summary, SRC.reinforced, SRC.annexTotal],
  );
}

// 21. Appendix - IF versus hybrid
{
  const slide = presentation.slides.add();
  addHeader(slide, "Q : pourquoi livrer IF si l’approche actuelle est HYPO ?", "Annexe — Questions difficiles", 21);
  tableGrid(
    slide,
    M,
    176,
    [250, 410, 522],
    [
      ["Élément", "IF + règles", "HYPO + instabilité + hybride"],
      ["Rôle", "Baseline explicitement demandée par le SOW", "Évolution scientifique actuelle"],
      ["Sortie", "385 notifications", "1 179 notifications hybrides"],
      ["Force", "Comparabilité et traçabilité contractuelle", "Signal SLS exploratoire prometteur"],
      ["Limite", "Pas d’association SLS observée", "Plus sensible, plus d’alertes, petit n SLS"],
      ["Statut", "Livrable principal", "Annexe de recherche"],
    ],
    { rowH: 70, size: 17 },
  );
  addText(
    slide,
    "Les deux répondent à des questions différentes; leurs comptes ne doivent pas être fusionnés.",
    M,
    618,
    1110,
    34,
    { size: 20, bold: true, color: C.red },
  );
  addNotes(
    slide,
    [
      "Réponse courte : « Parce que le SOW nomme explicitement Isolation Forest + règles. J’ai livré cette baseline comme demandé, puis ajouté l’approche actuelle dans une annexe clairement séparée. »",
      "La nouvelle approche produit beaucoup plus de notifications : 1 179 contre 385. Cela montre une sensibilité analytique plus élevée, mais aussi un besoin plus fort de calibration opérationnelle.",
      "Ne dites pas que l’une est définitivement meilleure. Dites que l’hybride est la direction actuelle et qu’elle doit être confirmée sur une cohorte clinique plus robuste.",
    ],
    [SRC.sow, SRC.annexTotal, SRC.sls, SRC.readme],
  );
}

// 22. Appendix - Fall 2021
{
  const slide = presentation.slides.add();
  addHeader(slide, "Q : Fall 2021 compte 10 vaches ou 8 ?", "Annexe — Questions difficiles", 22);
  statBlock(slide, M, 190, 300, "10", "profils présents dans la trace technique", C.blue);
  addText(slide, "→", 392, 220, 100, 60, {
    size: 46,
    bold: true,
    color: C.grid,
    align: "center",
  });
  statBlock(slide, 520, 190, 300, "8", "profils complets pour l’interprétation", C.teal);
  addText(slide, "→", 852, 220, 100, 60, {
    size: 46,
    bold: true,
    color: C.grid,
    align: "center",
  });
  statBlock(slide, 980, 190, 220, "4", "notifications", C.purple);
  addRect(slide, M, 404, 1130, 156, C.paper);
  addText(
    slide,
    "La différence n’est pas une incohérence : deux profils partiels sont conservés pour la traçabilité mais ne soutiennent pas l’interprétation scientifique.",
    80,
    448,
    1060,
    70,
    { size: 23, bold: true },
  );
  addText(
    slide,
    "La fenêtre de six jours explique aussi le faible nombre d’alertes et rend les comparaisons saisonnières fragiles.",
    M,
    604,
    1120,
    42,
    { size: 19, color: C.muted },
  );
  addNotes(
    slide,
    [
      "Réponse courte : « Dix profils ont été traités; huit seulement sont complets. Les deux profils partiels restent dans la trace pour ne pas masquer les données reçues. »",
      "La transparence sur les exclusions est une force du livrable.",
      "Fall 2021 ne doit pas être utilisée pour conclure sur un taux saisonnier parce que l’exposition est très courte.",
    ],
    [SRC.summary, SRC.report, SRC.readme],
  );
}

// 23. Appendix - metrics
{
  const slide = presentation.slides.add();
  addHeader(slide, "Q : pourquoi pas de sensibilité ou spécificité ?", "Annexe — Questions difficiles", 23);
  addText(
    slide,
    "Ces métriques exigent une vérité-terrain clinique datée pour chaque cas positif et négatif.",
    M,
    170,
    1120,
    64,
    { size: 30, bold: true },
  );
  const needs = [
    ["Labels indépendants", "score locomoteur/SLS, date et examinateur"],
    ["Cas suffisants", "plus que 3 à 5 vaches positives"],
    ["Fenêtre pré-spécifiée", "délai acceptable entre alerte et examen"],
    ["Cohorte complète", "positifs et négatifs suivis de la même façon"],
  ];
  needs.forEach((n, i) => {
    const x = M + (i % 2) * 585;
    const y = 294 + Math.floor(i / 2) * 150;
    addText(slide, String(i + 1).padStart(2, "0"), x, y, 70, 40, {
      size: 26,
      bold: true,
      color: i < 2 ? C.blue : C.teal,
    });
    addText(slide, n[0], x + 72, y, 430, 34, { size: 21, bold: true });
    addText(slide, n[1], x + 72, y + 44, 430, 56, {
      size: 18,
      color: C.muted,
    });
  });
  addText(
    slide,
    "Sans cela, publier un chiffre de “performance” serait plus convaincant en apparence, mais moins correct scientifiquement.",
    M,
    606,
    1120,
    42,
    { size: 20, bold: true, color: C.red },
  );
  addNotes(
    slide,
    [
      "Réponse courte : « Nous n’avons pas assez de labels cliniques synchronisés pour construire une matrice de confusion fiable. »",
      "La concordance comportementale n’est pas une vérité-terrain de boiterie.",
      "L’AUC exploratoire de l’hybride est utile pour planifier l’étude suivante, mais ne remplace pas une validation prospective.",
      "Proposez la suite concrète : geler la version hybride, définir la fenêtre d’alerte et organiser des scores locomoteurs répétés par un évaluateur indépendant.",
    ],
    [SRC.validation, SRC.sls, SRC.report],
  );
}

await fs.mkdir(OUT_DIR, { recursive: true });
await fs.mkdir(BUILD_DIR, { recursive: true });

for (const [index, slide] of presentation.slides.items.entries()) {
  const stem = `slide-${String(index + 1).padStart(2, "0")}`;
  const png = await presentation.export({ slide, format: "png", scale: 1 });
  await fs.writeFile(`${BUILD_DIR}/${stem}.png`, new Uint8Array(await png.arrayBuffer()));
  const layout = await slide.export({ format: "layout" });
  await fs.writeFile(`${BUILD_DIR}/${stem}.layout.json`, await layout.text());
}

const montage = await presentation.export({
  format: "webp",
  montage: true,
  scale: 1,
});
await fs.writeFile(
  `${BUILD_DIR}/deck-montage.webp`,
  new Uint8Array(await montage.arrayBuffer()),
);

const pptx = await PresentationFile.exportPptx(presentation);
await pptx.save(OUT_PPTX);

console.log(`Created ${OUT_PPTX}`);
console.log(`Rendered artifact-tool previews in ${BUILD_DIR}`);
