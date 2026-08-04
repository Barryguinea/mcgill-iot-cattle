import fs from "node:fs/promises";
import { Presentation, PresentationFile } from "@oai/artifact-tool";

const OUT_DIR =
  "/Users/alioubarry/Desktop/Livrables_McGill_WellE/Reunion_McGill_2026-07-30";
const OUT_PPTX = `${OUT_DIR}/Presentation_partage_ecran_McGill_30_juillet_2026.pptx`;
const BUILD_DIR = "/tmp/mcgill_meeting_20260730/screen_share_artifact_previews";

const W = 1280;
const H = 720;
const M = 52;
const FONT = "Helvetica Neue";

const C = {
  ink: "#111111",
  white: "#FFFFFF",
  paper: "#F5F6F7",
  panel: "#E9EDF1",
  grid: "#D5DAE0",
  muted: "#5E6875",
  blue: "#2474E5",
  cyan: "#65C4E5",
  teal: "#14877E",
  purple: "#7656B6",
  green: "#2D8A57",
  red: "#B94A4A",
  yellow: "#F5D269",
  gray: "#ADB5C0",
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
  annex:
    "/Users/alioubarry/Desktop/Livrables_McGill_WellE/Objectif1_Pipeline_detection_boiterie/ANNEXE_pipeline_actuelle_HYPO_instabilite_hybride/TABLEAUX_CSV/pipeline_actuelle_synthese_totale.csv",
  inventory:
    "/Users/alioubarry/PROJECT/mcgill_iot_cattle/reports/mcgill_complete_inventory.md",
  config: "/Users/alioubarry/PROJECT/core/config.py",
  pipeline: "/Users/alioubarry/PROJECT/core/pipeline.py",
  alerts: "/Users/alioubarry/PROJECT/core/_alerts_engine.py",
  reinforcement:
    "/Users/alioubarry/PROJECT/mcgill_iot_cattle/run_objective1_reinforcement.py",
  obj2Report:
    "/Users/alioubarry/Desktop/Livrables_McGill_WellE/Objectif2_Environnement_x_comportement/RAPPORTS/Objectif2_rapport_livraison.docx",
  obj2Model:
    "/Users/alioubarry/Desktop/Livrables_McGill_WellE/Objectif2_Environnement_x_comportement/TABLEAUX_CSV/objective2_mixed_model_summary.csv",
  obj2Desc:
    "/Users/alioubarry/Desktop/Livrables_McGill_WellE/Objectif2_Environnement_x_comportement/TABLEAUX_CSV/objective2_descriptifs.csv",
};

function rect(slide, x, y, w, h, fill, lineFill = fill, lineWidth = 0) {
  return slide.shapes.add({
    geometry: "rect",
    position: { left: x, top: y, width: w, height: h },
    fill,
    line: { style: "solid", fill: lineFill, width: lineWidth },
  });
}

function text(slide, value, x, y, w, h, options = {}) {
  const box = slide.shapes.add({
    geometry: "textbox",
    position: { left: x, top: y, width: w, height: h },
    fill: "none",
    line: { style: "solid", fill: "none", width: 0 },
  });
  box.text = value;
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

function line(slide, x, y, w, color = C.grid, width = 1) {
  return slide.shapes.add({
    geometry: "straightConnector1",
    position: { left: x, top: y, width: w, height: 0 },
    fill: "none",
    line: { style: "solid", fill: color, width },
  });
}

function header(slide, title, section, number) {
  slide.background.fill = C.white;
  text(slide, section.toUpperCase(), M, 26, 460, 24, {
    size: 14,
    bold: true,
    color: C.blue,
  });
  text(slide, title, M, 58, 1150, 70, {
    size: 38,
    bold: true,
  });
  line(slide, M, 134, W - M * 2, C.grid, 1);
  text(slide, String(number).padStart(2, "0"), 1184, 672, 42, 18, {
    size: 13,
    color: C.muted,
    align: "right",
  });
}

function notes(slide, paragraphs, sources) {
  slide.speakerNotes.textFrame.setText([
    ...paragraphs,
    "",
    "[Sources]",
    ...sources.map((source) => `- ${source}`),
    "[/Sources]",
  ]);
  slide.speakerNotes.setVisible(true);
}

function bullet(slide, value, x, y, w, options = {}) {
  rect(slide, x, y + 8, 9, 9, options.color || C.blue);
  text(slide, value, x + 22, y, w - 22, options.h || 54, {
    size: options.size || 20,
    color: options.textColor || C.ink,
    bold: options.bold || false,
  });
}

function metric(slide, x, y, w, value, label, color) {
  text(slide, value, x, y, w, 66, { size: 46, bold: true, color });
  text(slide, label, x, y + 70, w, 54, { size: 18, color: C.muted });
}

function table(slide, x, y, widths, rows, rowH = 60, bodySize = 17) {
  rows.forEach((row, r) => {
    let xx = x;
    row.forEach((value, c) => {
      rect(
        slide,
        xx,
        y + r * rowH,
        widths[c],
        rowH,
        r === 0 ? C.ink : r % 2 ? C.white : C.paper,
        C.grid,
        1,
      );
      text(
        slide,
        String(value),
        xx + 10,
        y + r * rowH + 11,
        widths[c] - 20,
        rowH - 16,
        {
          size: r === 0 ? 16 : bodySize,
          bold: r === 0,
          color: r === 0 ? C.white : C.ink,
          valign: "middle",
        },
      );
      xx += widths[c];
    });
  });
}

const deck = Presentation.create({ slideSize: { width: W, height: H } });

// 1 — Cover
{
  const slide = deck.slides.add();
  slide.background.fill = C.white;
  rect(slide, 1005, 0, 275, 720, C.ink);
  rect(slide, 1005, 0, 18, 720, C.cyan);
  text(slide, "McGILL / WELL-E", M, 40, 450, 32, {
    size: 21,
    bold: true,
    color: C.blue,
  });
  text(slide, "Bilan des travaux", M, 180, 800, 72, {
    size: 54,
    bold: true,
  });
  text(slide, "Objectif 1", M, 260, 800, 86, {
    size: 66,
    bold: true,
    color: C.blue,
  });
  text(
    slide,
    "Application et évaluation de la pipeline de détection sur les données IceTag",
    M,
    370,
    820,
    110,
    { size: 31, bold: true },
  );
  text(slide, "Réunion du 30 juillet 2026", M, 630, 500, 30, {
    size: 18,
    bold: true,
  });
  text(slide, "Aliou Barry", 1050, 570, 180, 48, {
    size: 24,
    bold: true,
    color: C.white,
    align: "right",
  });
  notes(
    slide,
    [
      "MESSAGE PRINCIPAL — L’objectif 1 a été exécuté sur les quatre corpus prévus, documenté et transformé en un paquet de livraison traçable. La présentation distingue clairement ce qui est démontré techniquement de ce qui reste à valider cliniquement.",
      "OUVERTURE PROPOSÉE — Merci pour cette rencontre. Je vais vous présenter le travail réalisé sur l’objectif 1 : les données utilisées, la chaîne appliquée, les notifications obtenues, leur concordance avec les informations disponibles, puis les livrables et la suite recommandée.",
      "Le fil conducteur est volontairement simple : partir du mandat du SOW, montrer les traitements réellement effectués, expliquer les résultats sans les surinterpréter et terminer par les décisions attendues de McGill/WELL-E.",
      "Le terme « notification » sera privilégié pendant la présentation. Une notification signale un épisode comportemental inhabituel à examiner; elle ne constitue pas, à elle seule, un diagnostic de boiterie.",
      "Le travail comporte deux niveaux distincts : la baseline Isolation Forest demandée au SOW, puis l’approche actuelle HYPO + instabilité + hybride présentée séparément en annexe scientifique.",
      "TRANSITION — Je commence par rappeler exactement ce que le mandat demandait, afin que les résultats et les livrables puissent être évalués par rapport au bon périmètre.",
      "QUESTION POSSIBLE — « Quel est le verdict global? » Réponse courte : objectif contractuel atteint et résultats reproductibles; validation clinique encore exploratoire faute d’un nombre suffisant de scores locomoteurs synchronisés.",
    ],
    [SRC.sow, SRC.report],
  );
}

// 2 — Mandate
{
  const slide = deck.slides.add();
  header(slide, "Le mandat de l’objectif 1", "Contexte", 2);
  text(
    slide,
    "Appliquer et évaluer une pipeline existante de détection sur quatre nouveaux corpus IceTag.",
    M,
    164,
    1120,
    72,
    { size: 28, bold: true },
  );
  const items = [
    ["1.1", "Adapter les entrées", "Rendre les quatre expériences compatibles avec la pipeline."],
    ["1.1", "Exécuter la pipeline", "Produire scores, épisodes et alertes avec les paramètres existants."],
    ["1.2", "Évaluer la concordance", "Aligner les alertes avec les scans et les informations disponibles."],
    ["1.2", "Documenter", "Fournir données traitées, tableaux et notes de reproductibilité."],
  ];
  items.forEach((item, i) => {
    const y = 274 + i * 82;
    text(slide, item[0], M, y, 70, 34, {
      size: 19,
      bold: true,
      color: i < 2 ? C.blue : C.teal,
    });
    text(slide, item[1], 136, y, 280, 34, { size: 21, bold: true });
    text(slide, item[2], 438, y, 720, 46, { size: 19, color: C.muted });
    line(slide, 136, y + 55, 1020, C.grid, 1);
  });
  notes(
    slide,
    [
      "MESSAGE PRINCIPAL — Le mandat ne demandait pas d’inventer un nouveau détecteur clinique. Il demandait d’adapter et d’exécuter une pipeline existante sur quatre corpus IceTag, puis d’en évaluer la concordance et d’en documenter la reproductibilité.",
      "La tâche 1.1 couvre deux opérations : harmoniser les entrées hétérogènes, puis produire pour chaque saison les scores par intervalle, les épisodes retenus et les notifications finales.",
      "La tâche 1.2 couvre l’évaluation : aligner temporellement les notifications avec les scans disponibles, produire une table de concordance et rédiger une note de validation précisant la portée et les limites.",
      "Les quatre composantes de livraison attendues sont présentes : données traitées avec alertes, note technique de reproductibilité, table de concordance et rapport court de validation.",
      "L’adaptation a porté sur les formats, les colonnes, les identifiants de vache, les timestamps et les unités. La logique de la baseline et ses paramètres ont été gardés communs entre les saisons pour que les sorties restent comparables.",
      "L’approche HYPO + instabilité + hybride ne remplace pas rétroactivement le mandat. Elle est conservée dans une annexe séparée afin de montrer l’évolution scientifique sans confondre la baseline contractuelle et le développement plus récent.",
      "TRANSITION — Après avoir fixé ce périmètre, la diapositive suivante résume le volume réellement traité et le résultat contractuel.",
      "QUESTION POSSIBLE — « Avez-vous changé le modèle pour obtenir de meilleurs résultats? » Réponse : non pour la baseline du SOW; les mêmes paramètres gelés ont été utilisés sur les quatre saisons. La nouvelle approche est évaluée séparément.",
    ],
    [SRC.sow, SRC.readme],
  );
}

// 3 — Overview
{
  const slide = deck.slides.add();
  header(slide, "Le travail réalisé en synthèse", "Bilan", 3);
  text(
    slide,
    "Les quatre saisons ont été traitées et les sorties sont disponibles à trois niveaux : intervalle, notification et synthèse.",
    M,
    160,
    1120,
    64,
    { size: 24, bold: true },
  );
  rect(slide, M, 276, 352, 250, C.paper);
  rect(slide, 464, 276, 352, 250, C.paper);
  rect(slide, 868, 276, 352, 250, C.paper);
  metric(slide, 84, 324, 290, "4 / 4", "saisons IceTag traitées", C.blue);
  metric(slide, 500, 324, 290, "375 031", "intervalles de 15 minutes", C.teal);
  metric(slide, 904, 324, 290, "385", "notifications de la baseline", C.purple);
  rect(slide, M, 574, 1168, 68, C.ink);
  text(
    slide,
    "Les quatre livrables prévus au SOW sont présents et reliés aux résultats.",
    M + 24,
    593,
    1120,
    34,
    { size: 21, bold: true, color: C.white },
  );
  notes(
    slide,
    [
      "MESSAGE PRINCIPAL — Le verdict contractuel est positif : quatre saisons sur quatre ont été traitées et les quatre composantes prévues au SOW sont disponibles.",
      "Les 375 031 observations représentent des unités « vache × intervalle de 15 minutes ». Une même vache contribue donc de nombreux intervalles au cours de sa période de suivi.",
      "La pipeline a produit 385 notifications finales. Ce nombre correspond au début de 385 épisodes retenus après les règles de persistance, de cohérence, de couverture et le délai de répétition.",
      "Il ne faut pas interpréter 385 comme 385 vaches boiteuses, ni comme 385 diagnostics. Une vache peut recevoir plusieurs notifications et chacune demande une revue du contexte.",
      "Les sorties existent à trois niveaux complémentaires : les prédictions détaillées pour chaque intervalle, les notifications au début des épisodes retenus et les synthèses agrégées par vache ou par saison.",
      "Le paquet permet donc à la fois une lecture rapide des résultats et un audit complet jusqu’aux intervalles qui ont conduit à chaque événement.",
      "TRANSITION — Ces volumes regroupent cependant quatre expériences de durées et de structures différentes; il faut maintenant les replacer dans leur contexte.",
      "QUESTION POSSIBLE — « 385 alertes, est-ce beaucoup? » Réponse : le total brut seul ne suffit pas. Il faut tenir compte de la durée, du nombre de vaches et surtout distinguer les signaux individuels des épisodes collectifs.",
    ],
    [SRC.summary, SRC.readme, SRC.report],
  );
}

// 4 — Data
{
  const slide = deck.slides.add();
  header(slide, "Quatre corpus, quatre contextes expérimentaux", "Données", 4);
  table(
    slide,
    M,
    176,
    [240, 185, 220, 285, 238],
    [
      ["Saison", "Profils", "Intervalles", "Période", "Couverture"],
      ["Winter 2019", "17", "136 929", "janv. – avr. 2019", "94,4 %"],
      ["Summer 2019", "18", "139 111", "juin – sept. 2019", "98,3 %"],
      ["Fall 2019", "30", "93 860", "nov. – déc. 2019", "99,3 %"],
      ["Fall 2021", "10 traités / 8 complets", "5 131", "30 nov. – 6 déc.", "100,0 %"],
    ],
    72,
    17,
  );
  text(
    slide,
    "L’inventaire complet a permis d’identifier les bonnes sources; l’analyse porte ensuite sur les quatre corpus définis dans le SOW.",
    M,
    574,
    1120,
    54,
    { size: 20, color: C.muted },
  );
  notes(
    slide,
    [
      "MESSAGE PRINCIPAL — Les quatre corpus n’ont ni la même durée, ni le même nombre de profils, ni exactement le même contexte expérimental. Les résultats bruts doivent donc être lus avec ces différences en tête.",
      "Avant l’analyse, un inventaire de 2 414 fichiers a été réalisé pour identifier les bonnes sources, relier les expériences aux périodes attendues et écarter les duplications ou fichiers non pertinents.",
      "Winter 2019 comprend 17 profils et 136 929 intervalles; Summer 2019, 18 profils et 139 111 intervalles; Fall 2019, 30 profils et 93 860 intervalles.",
      "Fall 2021 est un cas particulier : dix profils ont été tracés dans les sources, mais huit sont complets pour l’interprétation. La période exploitable ne couvre qu’environ une semaine, du 30 novembre au 6 décembre.",
      "La couverture est une mesure de complétude temporelle : nombre d’échantillons bruts présents dans un intervalle divisé par le nombre attendu. Elle ne mesure ni la qualité clinique ni le pourcentage de vaches saines.",
      "Un intervalle dont la couverture est inférieure à 25 % ne peut pas générer de notification. Une absence de donnée brute ne doit jamais être interprétée comme une absence de mouvement.",
      "La couverture moyenne élevée indique que les intervalles conservés sont généralement bien renseignés. Le 100 % de Fall 2021 ne compense toutefois pas la brièveté de cette expérience.",
      "TRANSITION — La diversité de ces corpus explique pourquoi une part importante du travail a porté sur l’harmonisation et les contrôles de qualité.",
      "QUESTION POSSIBLE — « Peut-on comparer directement les quatre totaux? » Réponse : seulement avec prudence; les durées et les effectifs diffèrent, et Fall 2021 est nettement plus court.",
    ],
    [SRC.inventory, SRC.summary, SRC.report],
  );
}

// 5 — Work performed
{
  const slide = deck.slides.add();
  header(slide, "Cinq étapes pour rendre l’analyse reproductible", "Travail réalisé", 5);
  const phases = [
    ["01", "Inventorier", "Formats, périodes, identités et qualité"],
    ["02", "Harmoniser", "Schéma commun Cow, T et mesures"],
    ["03", "Exécuter", "Même logique sur les quatre saisons"],
    ["04", "Évaluer", "Scans, SLS, couverture et contexte troupeau"],
    ["05", "Livrer", "CSV, notes, rapport et annexes"],
  ];
  phases.forEach((p, i) => {
    const x = M + i * 234;
    text(slide, p[0], x, 184, 80, 36, {
      size: 24,
      bold: true,
      color: i % 2 ? C.teal : C.blue,
    });
    line(slide, x, 236, 194, i % 2 ? C.teal : C.blue, 5);
    text(slide, p[1], x, 276, 200, 50, { size: 23, bold: true });
    text(slide, p[2], x, 348, 200, 120, { size: 18, color: C.muted });
  });
  rect(slide, M, 526, 1168, 92, C.paper);
  text(
    slide,
    "Résultat : une même chaîne peut lire les quatre saisons sans réécrire la logique pour chaque expérience.",
    M + 24,
    553,
    1116,
    42,
    { size: 22, bold: true, color: C.teal },
  );
  notes(
    slide,
    [
      "MESSAGE PRINCIPAL — La valeur technique du travail réside autant dans la préparation reproductible des données que dans l’exécution du modèle.",
      "L’inventaire a d’abord établi quelles sources correspondaient à chaque saison, quelles variables étaient disponibles et quels profils étaient complets ou partiels.",
      "L’harmonisation a ensuite créé un schéma commun autour de l’identifiant de vache « Cow », du timestamp « T » et des mesures comportementales nécessaires à la pipeline.",
      "Cette étape corrige les variations de noms de colonnes, de formats de date, d’unités, de Cow_ID, de couleurs d’identification et de structure entre les fichiers.",
      "Des contrôles ont vérifié l’ordre chronologique, les doublons, les périodes couvertes, la présence des colonnes requises et la proportion de données réellement disponible dans chaque intervalle.",
      "La même chaîne a ensuite été exécutée sur les quatre saisons avec des paramètres communs. Cette décision évite d’ajuster opportunément les seuils à une saison particulière.",
      "Enfin, chaque niveau de sortie a été conservé : intervalles, notifications, résumés, tableaux de concordance et notes de reproductibilité. Les chiffres présentés peuvent ainsi être retracés jusqu’aux données traitées.",
      "TRANSITION — La diapositive suivante montre comment ces données harmonisées deviennent une notification, puis une priorité A, B ou C.",
      "QUESTION POSSIBLE — « Pourquoi cette étape a-t-elle pris du temps? » Réponse : sans harmonisation fiable, une erreur de timestamp, d’identifiant ou d’unité peut produire une alerte artificielle ou empêcher l’exécution complète.",
    ],
    [SRC.inventory, SRC.pipeline, SRC.report],
  );
}

// 6 — Pipeline
{
  const slide = deck.slides.add();
  header(slide, "La chaîne analytique appliquée", "Méthode", 6);
  const steps = [
    ["Données", "IceTag brut"],
    ["15 min", "Agrégation"],
    ["Features", "Profils robustes"],
    ["IF", "Anomalies par vache"],
    ["Règles", "Persistance + cohérence"],
    ["A / B / C", "Contexte troupeau"],
  ];
  steps.forEach((s, i) => {
    const x = M + i * 196;
    rect(slide, x, 226, 170, 214, i === 5 ? C.ink : C.paper, C.grid, 1);
    text(slide, String(i + 1), x + 18, 248, 48, 34, {
      size: 24,
      bold: true,
      color: i === 5 ? C.cyan : C.blue,
    });
    text(slide, s[0], x + 18, 312, 134, 44, {
      size: 21,
      bold: true,
      color: i === 5 ? C.white : C.ink,
    });
    text(slide, s[1], x + 18, 370, 134, 54, {
      size: 17,
      color: i === 5 ? "#D2D8DF" : C.muted,
    });
    if (i < 5) {
      slide.shapes.add({
        geometry: "chevron",
        position: { left: x + 176, top: 320, width: 14, height: 18 },
        fill: C.blue,
        line: { style: "solid", fill: C.blue, width: 0 },
      });
    }
  });
  text(
    slide,
    "Paramètres communs : 15 min | IF 6 % | persistance 7 h | cooldown 12 h | couverture ≥ 25 %.",
    M,
    516,
    1130,
    54,
    { size: 20, bold: true },
  );
  text(
    slide,
    "Étape 1 : IF + règles produit une notification. Étape 2 : A/B/C en fixe la priorité.",
    M,
    596,
    1130,
    36,
    { size: 20, color: C.red, bold: true },
  );
  notes(
    slide,
    [
      "MESSAGE PRINCIPAL — Une notification n’est pas produite par Isolation Forest seul. Elle résulte d’une chaîne en six étapes qui combine profil individuel, persistance temporelle, cohérence comportementale, qualité des données et contexte troupeau.",
      "Premièrement, les mesures brutes sont agrégées en intervalles de 15 minutes. La couverture de chaque intervalle est calculée en parallèle pour distinguer un vrai signal d’un manque de données.",
      "Deuxièmement, des variables robustes décrivent l’écart à la ligne de base de la même vache, les variations temporelles, les différences par rapport aux moyennes mobiles et les cycles horaires.",
      "Troisièmement, Isolation Forest est entraîné par vache, avec une portion initiale de 60 % utilisée comme ligne de base et une contamination fixée à 6 %. Il identifie des états atypiques, pas une boiterie clinique.",
      "Quatrièmement, les règles métier exigent une persistance : dans une fenêtre glissante de sept heures, au moins 24 % des intervalles doivent être anormaux, avec une cohérence comportementale suffisante.",
      "Cinquièmement, un intervalle doit avoir au moins 25 % de couverture pour participer à une notification. Une notification est inscrite au début de l’épisode retenu et un cooldown de douze heures évite les répétitions rapprochées.",
      "Sixièmement, le contexte du troupeau contemporain est ajouté pour classer la notification A, B ou C. Cette étape ne crée pas trois modèles et ne change pas le total de 385 notifications.",
      "Les paramètres ont été gelés et gardés identiques entre saisons. Cela renforce la reproductibilité, même si cela ne garantit pas que ces seuils soient cliniquement optimaux dans tous les troupeaux.",
      "TRANSITION — Nous pouvons maintenant lire les nombres par saison, en gardant à l’esprit qu’il s’agit de débuts d’épisodes comportementaux retenus.",
      "QUESTION POSSIBLE — « Pourquoi Isolation Forest? » Réponse : il permet de construire un profil individuel sans exiger de labels cliniques abondants. Sa limite est précisément qu’il détecte l’atypique, pas directement la boiterie.",
    ],
    [SRC.config, SRC.pipeline, SRC.alerts, SRC.report],
  );
}

// 7 — Results by season
{
  const slide = deck.slides.add();
  header(slide, "Notifications par saison et niveau de priorité", "Résultats", 7);
  const data = [
    ["Winter 2019", 149, 14, 46, 89],
    ["Summer 2019", 127, 16, 94, 17],
    ["Fall 2019", 105, 7, 51, 47],
    ["Fall 2021", 4, 0, 4, 0],
  ];
  const max = 160;
  const x0 = 250;
  const chartW = 900;
  data.forEach((d, i) => {
    const y = 178 + i * 104;
    text(slide, d[0], M, y + 16, 180, 30, { size: 19, bold: true });
    let x = x0;
    [
      [d[2], C.blue, C.white],
      [d[3], C.cyan, C.ink],
      [d[4], C.gray, C.ink],
    ].forEach((p) => {
      const w = (p[0] / max) * chartW;
      if (w > 0) {
        rect(slide, x, y, w, 60, p[1]);
        if (w > 34) {
          text(slide, String(p[0]), x, y + 17, w, 28, {
            size: 17,
            bold: true,
            color: p[2],
            align: "center",
          });
        }
        x += w;
      }
    });
    text(slide, String(d[1]), x + 12, y + 16, 70, 30, {
      size: 20,
      bold: true,
    });
  });
  const legend = [
    ["A — prioritaire", C.blue],
    ["B — individuelle à vérifier", C.cyan],
    ["C — événement collectif probable", C.gray],
  ];
  legend.forEach((l, i) => {
    const x = x0 + i * 280;
    rect(slide, x, 618, 18, 18, l[1]);
    text(slide, l[0], x + 28, 614, 250, 26, { size: 16, bold: true });
  });
  notes(
    slide,
    [
      "MESSAGE PRINCIPAL — La baseline a produit 385 notifications : 149 en Winter 2019, 127 en Summer 2019, 105 en Fall 2019 et 4 en Fall 2021.",
      "Chaque barre additionne les catégories A, B et C de la même saison. Les couleurs sont donc des priorités de revue attribuées après la détection, et non les sorties de trois algorithmes différents.",
      "Winter 2019 contient 14 notifications A, 46 B et 89 C. Summer 2019 en contient 16 A, 94 B et 17 C. Fall 2019 en contient 7 A, 51 B et 47 C. Fall 2021 contient 4 B.",
      "Le total de Fall 2021 est faible principalement parce que la fenêtre analysée ne couvre qu’environ une semaine. Il ne faut pas conclure que cette saison est intrinsèquement moins à risque.",
      "Rapportés au temps d’observation disponible, les ordres de grandeur sont plus proches que les totaux bruts : environ 10,45, 8,76, 10,74 et 7,48 notifications par 100 vache-jours respectivement.",
      "Le nombre de notifications reste un indicateur de charge de revue, pas un taux de boiterie. Une même vache peut générer plusieurs épisodes au cours de son suivi.",
      "La forte composante C de Winter 2019 et Fall 2019 indique qu’une partie importante des signaux survient simultanément chez plusieurs vaches; elle doit être examinée avant toute interprétation individuelle.",
      "TRANSITION — La prochaine diapositive explique précisément comment les 385 notifications ont été réparties en A, B et C.",
      "QUESTION POSSIBLE — « Pourquoi n’y a-t-il aucune catégorie A en Fall 2021? » Réponse : aucune des quatre notifications n’a réuni simultanément le caractère non collectif, le contraste troupeau et le score interne requis; la courte période limite aussi l’interprétation.",
    ],
    [SRC.summary, SRC.reinforced],
  );
}

// 8 — Reclassification
{
  const slide = deck.slides.add();
  header(slide, "A, B et C hiérarchisent la revue, pas la boiterie", "Renforcement", 8);
  text(
    slide,
    "Les 385 notifications IF + règles sont conservées. Le contexte troupeau est ajouté ensuite pour fixer leur priorité.",
    M,
    164,
    1120,
    62,
    { size: 24, bold: true },
  );
  const parts = [
    [37, "A", C.blue, C.white],
    [195, "B", C.cyan, C.ink],
    [153, "C", C.gray, C.ink],
  ];
  let x = M;
  parts.forEach((p) => {
    const w = (p[0] / 385) * (W - M * 2);
    rect(slide, x, 270, w, 96, p[2]);
    text(slide, String(p[0]), x, 286, w, 36, {
      size: 27,
      bold: true,
      color: p[3],
      align: "center",
    });
    text(slide, `${Math.round((p[0] / 385) * 100)} %`, x, 326, w, 24, {
      size: 16,
      color: p[3],
      align: "center",
    });
    x += w;
  });
  const definitions = [
    [
      "A — 37",
      "Non collective + profil distinct du troupeau + score interne ≥ 45",
      "Revoir en premier",
      C.blue,
    ],
    [
      "B — 195",
      "Non collective + appui troupeau moins net ou score modéré",
      "Vérifier la vache",
      C.teal,
    ],
    [
      "C — 153",
      "≥ 30 % des vaches sur ± 1 jour, ou ≥ 50 % sur ± 3 jours",
      "Rechercher une cause commune",
      C.purple,
    ],
  ];
  definitions.forEach((d, i) => {
    const xx = M + i * 394;
    line(slide, xx, 430, 330, d[3], 5);
    text(slide, d[0], xx, 452, 330, 34, { size: 22, bold: true });
    text(slide, d[1], xx, 498, 330, 68, { size: 17, color: C.muted });
    text(slide, d[2], xx, 574, 330, 32, { size: 18, bold: true, color: d[3] });
  });
  text(
    slide,
    "Ce ne sont ni des stades cliniques ni des sorties HYPO. Une catégorie D est prévue pour les données insuffisantes : 0 cas.",
    M,
    630,
    1150,
    30,
    { size: 17, bold: true, color: C.red },
  );
  notes(
    slide,
    [
      "MESSAGE PRINCIPAL — A, B et C sont des niveaux de priorité opérationnelle. Ils ne représentent ni trois degrés de boiterie ni trois diagnostics.",
      "Deux étapes doivent être distinguées : IF + règles produit d’abord 385 notifications; le renforcement troupeau les requalifie ensuite sans en ajouter ni en supprimer.",
      "Le contexte troupeau n’est déclaré exploitable que si les données couvrent au moins 75 % de l’intervalle pour au moins 50 % du troupeau, avec un minimum de cinq vaches observées au même moment.",
      "La catégorie C est attribuée en premier lorsqu’un épisode est probablement collectif : au moins 30 % des vaches sont alertées dans une fenêtre de ± 1 jour, ou au moins 50 % dans une fenêtre de ± 3 jours.",
      "Parmi les notifications non collectives, A exige un signal propre à la vache par rapport à la médiane contemporaine du troupeau et un score interne lame_confidence d’au moins 45. Ce sont les 37 dossiers à revoir en premier.",
      "B regroupe les 195 notifications non collectives dont le contraste avec le troupeau est moins net ou dont le score interne est plus modéré. Elles restent pertinentes, mais avec une priorité inférieure.",
      "C regroupe 153 notifications pour lesquelles le premier réflexe doit être la recherche d’une cause commune : changement de gestion, exercice, météo, déplacement du troupeau, alimentation ou problème partagé de capteurs.",
      "Une catégorie D est prévue lorsque la couverture ou le contexte sont insuffisants; aucune notification finale n’a été classée D dans les sorties livrées.",
      "Le score lame_confidence est un indice empirique construit pour le classement relatif. Il combine plusieurs familles de signaux, mais il ne doit pas être lu comme une probabilité clinique de boiterie.",
      "A/B/C appartient au renforcement de la baseline IF. Les sorties HYPO + instabilité + hybride sont séparées en annexe et n’utilisent pas ce même vocabulaire de priorité.",
      "TRANSITION — Cette hiérarchisation révèle notamment qu’une part importante des notifications de certaines saisons est collective.",
      "QUESTION POSSIBLE — « Une catégorie A signifie-t-elle que la vache est boiteuse? » Réponse : non. A signifie seulement « signal individuel prioritaire à vérifier »; une observation clinique reste nécessaire.",
    ],
    [SRC.reinforced, SRC.reinforcement, SRC.alerts, SRC.report],
  );
}

// 9 — Collective context
{
  const slide = deck.slides.add();
  header(slide, "Une part importante des signaux est collective", "Contexte troupeau", 9);
  const rows = [
    ["Winter 2019", 59.7, "89 / 149"],
    ["Fall 2019", 44.8, "47 / 105"],
    ["Summer 2019", 13.4, "17 / 127"],
    ["Fall 2021", 0.0, "0 / 4"],
  ];
  rows.forEach((r, i) => {
    const y = 178 + i * 102;
    text(slide, r[0], M, y + 10, 180, 30, { size: 19, bold: true });
    rect(slide, 250, y, 780, 48, C.panel);
    if (r[1] > 0) rect(slide, 250, y, (r[1] / 65) * 780, 48, i === 0 ? C.purple : C.teal);
    text(slide, `${r[1].toFixed(1).replace(".", ",")} %`, 1050, y + 8, 100, 30, {
      size: 20,
      bold: true,
      align: "right",
    });
    text(slide, r[2], 1160, y + 9, 70, 28, {
      size: 15,
      color: C.muted,
      align: "right",
    });
  });
  rect(slide, M, 584, 1168, 64, "#FFF5D6");
  text(
    slide,
    "Cette lecture réduit le risque d’interpréter un changement collectif comme un problème individuel.",
    M + 22,
    602,
    1118,
    34,
    { size: 20, bold: true },
  );
  notes(
    slide,
    [
      "MESSAGE PRINCIPAL — Le contexte troupeau empêche de confondre trop rapidement un épisode collectif avec une anomalie propre à une vache.",
      "En Winter 2019, 89 des 149 notifications, soit 59,7 %, sont classées C. En Fall 2019, la proportion est de 47 sur 105, soit 44,8 %.",
      "Summer 2019 présente une composante collective plus faible : 17 notifications sur 127, soit 13,4 %. Fall 2021 n’en compte aucune parmi ses quatre notifications.",
      "Un regroupement collectif important apparaît notamment au début de février 2019 en Winter. Il serait utile de le confronter aux journaux de gestion, à la météo et au protocole expérimental.",
      "Le classement C ne prouve pas la cause de l’événement et ne signifie pas automatiquement « faux positif ». Il indique que le signal est partagé et que l’explication individuelle est moins prioritaire.",
      "Les causes possibles comprennent un changement de routine, une activité imposée, un stress environnemental, un déplacement, un changement d’alimentation ou un artefact de mesure commun.",
      "Cette lecture améliore l’utilité du système : au lieu de demander une inspection séparée de nombreuses vaches au même moment, elle oriente d’abord vers une vérification du contexte du troupeau.",
      "TRANSITION — Après cette lecture interne des notifications, nous les comparons aux scans comportementaux disponibles dans les expériences.",
      "QUESTION POSSIBLE — « Est-ce que le système produit trop d’alertes? » Réponse : le nombre brut est élevé dans certaines périodes, mais le classement collectif montre qu’une partie peut être traitée comme un seul événement de contexte plutôt que comme plusieurs cas cliniques indépendants.",
    ],
    [SRC.reinforced, SRC.report],
  );
}

// 10 — Behavioral scans
{
  const slide = deck.slides.add();
  header(slide, "Concordance temporelle avec les scans comportementaux", "Évaluation", 10);
  const rows = [
    ["Fall 2019", 44.4, "12 / 27"],
    ["Winter 2019", 26.8, "11 / 41"],
    ["Summer 2019", 24.1, "14 / 58"],
    ["Fall 2021", 0.4, "1 / 270"],
  ];
  rows.forEach((r, i) => {
    const y = 180 + i * 95;
    text(slide, r[0], M, y + 9, 180, 30, { size: 19, bold: true });
    rect(slide, 250, y, 720, 46, C.panel);
    if (r[1] > 0) rect(slide, 250, y, (r[1] / 50) * 720, 46, i === 0 ? C.blue : C.teal);
    text(slide, `${r[1].toFixed(1).replace(".", ",")} %`, 995, y + 7, 100, 30, {
      size: 20,
      bold: true,
      align: "right",
    });
    text(slide, r[2], 1120, y + 8, 90, 28, {
      size: 16,
      color: C.muted,
      align: "right",
    });
  });
  text(
    slide,
    "Mesure présentée : proportion de scans avec au moins une alerte dans une fenêtre de ±1 jour.",
    M,
    576,
    1120,
    38,
    { size: 20, bold: true },
  );
  text(
    slide,
    "Ces taux décrivent un chevauchement temporel; ils ne représentent pas une précision diagnostique.",
    M,
    620,
    1120,
    34,
    { size: 18, color: C.red },
  );
  notes(
    slide,
    [
      "MESSAGE PRINCIPAL — La concordance présentée ici mesure un chevauchement temporel entre les scans comportementaux et les notifications; elle ne mesure pas la précision diagnostique.",
      "La règle est la suivante : pour chaque scan, on recherche au moins une notification de la même vache dans une fenêtre de ± 1 jour autour de la date du scan.",
      "Fall 2019 présente 12 scans avec notification sur 27, soit 44,4 %. Winter 2019 en présente 11 sur 41, soit 26,8 %, et Summer 2019, 14 sur 58, soit 24,1 %.",
      "Fall 2021 présente 1 scan avec notification sur 270, soit 0,4 %. Cette expérience combine un grand nombre de scans et une fenêtre IceTag très courte; son taux n’est donc pas directement comparable aux autres saisons.",
      "Dans certains anciens fichiers, la colonne porte le nom « taux_concurrence_% ». Le terme correct à employer à l’oral est « taux de concordance temporelle » ou « taux de cooccurrence ».",
      "Les scans décrivent des comportements ou des observations ponctuelles. Ils ne constituent pas une vérité-terrain clinique de boiterie et ne permettent pas de calculer une sensibilité, une spécificité ou une exactitude.",
      "Le résultat positif est que les données et les alertes ont pu être alignées de façon traçable dans les quatre expériences. La limite est que le sens clinique d’un chevauchement reste ambigu.",
      "Les comparaisons comportementales groupées n’ont pas fourni une validation clinique robuste à l’intérieur de chaque expérience; elles doivent rester descriptives.",
      "TRANSITION — Les scores SLS de Winter 2019 apportent une information plus proche de la locomotion et permettent une validation exploratoire plus pertinente.",
      "QUESTION POSSIBLE — « 44,4 % veut-il dire que le modèle est précis à 44,4 %? » Réponse : non. Cela signifie seulement que 12 des 27 scans de Fall 2019 ont une notification temporellement proche pour la même vache.",
    ],
    [SRC.concordance, SRC.report],
  );
}

// 11 — SLS and current approach
{
  const slide = deck.slides.add();
  header(slide, "Les scores SLS distinguent les deux approches", "Validation exploratoire", 11);
  text(
    slide,
    "Winter 2019 — score SLS du 12 mars; pour l’approche actuelle, signaux mesurés strictement durant les 7 jours précédents.",
    M,
    154,
    1160,
    34,
    { size: 18, color: C.muted },
  );
  rect(slide, M, 198, 540, 354, C.paper);
  rect(slide, 640, 198, 580, 354, C.ink);
  text(slide, "BASELINE DU SOW", 84, 228, 430, 24, {
    size: 14,
    bold: true,
    color: C.blue,
  });
  text(slide, "IF + règles", 84, 268, 430, 44, { size: 28, bold: true });
  text(slide, "16 vaches évaluables\n5 avec SLS ≥ 2\np = 0,649\nρ = 0,033", 84, 338, 380, 142, {
    size: 22,
    color: C.muted,
  });
  text(slide, "Aucune association observée", 84, 492, 440, 34, {
    size: 20,
    bold: true,
    color: C.red,
  });
  text(slide, "APPROCHE ACTUELLE — ANNEXE", 678, 228, 470, 24, {
    size: 14,
    bold: true,
    color: C.cyan,
  });
  text(slide, "HYPO + instabilité + hybride", 678, 268, 470, 58, {
    size: 27,
    bold: true,
    color: C.white,
  });
  text(
    slide,
    "14 évaluables; 3 avec SLS ≥ 2\n6,67 vs 4,45 notifications\nAUC = 0,924  |  p = 0,031\nρ = 0,504  |  p = 0,066",
    678,
    334,
    470,
    152,
    {
    size: 20,
    color: "#D7DDE4",
    },
  );
  text(slide, "Alignement exploratoire positif", 678, 492, 470, 34, {
    size: 20,
    bold: true,
    color: C.cyan,
  });
  rect(slide, M, 584, 1168, 70, "#FFF5D6");
  text(
    slide,
    "Résultat prometteur, mais non diagnostique : seulement 3 cas positifs, SLS maximal = 2 et traitement Exercise confondu.",
    M + 22,
    603,
    1118,
    36,
    { size: 20, bold: true },
  );
  notes(
    slide,
    [
      "MESSAGE PRINCIPAL — Les scores SLS disponibles ne soutiennent pas la baseline IF, mais ils montrent un alignement exploratoire encourageant avec l’approche actuelle HYPO + instabilité + hybride. Ce signal est prometteur, pas encore une validation diagnostique.",
      "Pour la baseline demandée au SOW, 16 vaches sont évaluables, dont 5 avec un SLS ≥ 2. La comparaison des notifications entre groupes donne un test de Mann-Whitney p = 0,649 et la corrélation continue donne rho = 0,033.",
      "Ces valeurs indiquent qu’aucune association SLS n’est observée pour la baseline IF dans cette cohorte. On ne doit donc pas présenter les notifications IF comme des cas de boiterie confirmés.",
      "Pour l’approche actuelle, l’unité statistique est la vache et la fenêtre principale couvre les sept jours strictement antérieurs au score SLS du 12 mars 2019. Les événements du jour du score ne sont pas utilisés pour éviter une ambiguïté temporelle.",
      "La variante primaire hiérarchique a été prédéfinie sans consulter les SLS. Les scores SLS n’ont servi ni à entraîner la détection ni à fixer les seuils; ils sont utilisés uniquement comme comparaison externe exploratoire.",
      "Sur 14 vaches évaluables, les trois vaches avec SLS ≥ 2 ont reçu en moyenne 6,67 notifications hybrides, contre 4,45 pour les onze vaches avec SLS < 2.",
      "La séparation des deux groupes est exploratoirement positive : AUC = 0,924 et test de Mann-Whitney p = 0,031. La corrélation avec le score SLS continu est également positive, rho = 0,504, mais n’atteint pas le seuil conventionnel de significativité, p = 0,066.",
      "Une AUC élevée dans un si petit échantillon peut être instable. Elle décrit la séparation observée dans cette cohorte précise et ne constitue pas une estimation fiable de performance généralisable.",
      "La cohorte ne contient que trois cas positifs et leur sévérité est légère : le SLS maximal est 2 et aucun cas SLS ≥ 3 n’est disponible. Les intervalles de confiance et les performances diagnostiques seraient donc très incertains.",
      "Le traitement Exercise est confondu avec le statut SLS : les trois vaches SLS ≥ 2 appartiennent au groupe Exercise. Une partie de la séparation peut refléter le protocole expérimental plutôt qu’un effet propre de la locomotion.",
      "Les cohortes, les fenêtres et les définitions de notification ne sont pas identiques entre la baseline et l’approche actuelle. Cette diapositive compare leur alignement exploratoire aux SLS, mais ne constitue pas un essai clinique comparatif définitif.",
      "FORMULATION À UTILISER — La baseline IF n’est pas alignée aux SLS dans les données disponibles. L’approche hybride montre un signal positif et cohérent avec les SLS, qui doit être confirmé sur davantage de cas, notamment des SLS ≥ 3, avec un protocole prospectif.",
      "TRANSITION — Cette séparation entre baseline contractuelle et évolution scientifique se retrouve explicitement dans l’organisation du dossier livré.",
      "QUESTION POSSIBLE — « Peut-on annoncer 92,4 % de précision? » Réponse : non. L’AUC de 0,924 mesure une séparation exploratoire sur seulement 14 vaches et 3 cas positifs; ce n’est ni une précision, ni une sensibilité, ni une performance clinique validée.",
    ],
    [SRC.sls, SRC.annex, SRC.report],
  );
}

// 12 — Deliverables
{
  const slide = deck.slides.add();
  header(slide, "Les livrables disponibles", "Dossier de livraison", 12);
  table(
    slide,
    M,
    166,
    [355, 425, 388],
    [
      ["Dossier", "Contenu", "Utilisation"],
      ["RAPPORTS/", "Rapport Word et présentations", "Lecture et communication"],
      ["DONNEES_TRAITEES_ALERTES/", "Prédictions, alertes et résumés", "Audit détaillé"],
      ["TABLEAUX_CSV/", "Synthèses, priorités et concordance", "Vérification des chiffres"],
      ["NOTES_SOW/", "Reproductibilité et validation", "Preuves contractuelles"],
      ["ANNEXE_pipeline_actuelle_…/", "HYPO + instabilité + hybride", "Évolution scientifique"],
    ],
    70,
    17,
  );
  text(
    slide,
    "Point d’entrée recommandé : README_livraison_objectif1.txt",
    M,
    610,
    1120,
    34,
    { size: 20, bold: true, color: C.blue },
  );
  notes(
    slide,
    [
      "MESSAGE PRINCIPAL — Le dossier de livraison est organisé pour permettre deux usages : une lecture rapide par le rapport Word et un audit technique complet par les CSV et les notes.",
      "Le point d’entrée recommandé est README_livraison_objectif1.txt. Il indique l’ordre de lecture, le rôle de chaque dossier et la correspondance exacte entre les fichiers et les tâches 1.1 et 1.2 du SOW.",
      "RAPPORTS contient le rapport Word de livraison et les présentations utiles à la communication. Le rapport résume la méthode, les résultats et les limites sans exiger de lire les fichiers techniques.",
      "DONNEES_TRAITEES_ALERTES contient les sorties détaillées. Les fichiers predictions.csv représentent tous les intervalles vache × 15 minutes; alerts_only.csv contient uniquement le début des épisodes retenus; summary.csv résume les résultats par vache.",
      "TABLEAUX_CSV contient les tableaux de synthèse par saison, par vache, par niveau A/B/C et les tables de concordance. C’est le dossier à ouvrir lorsqu’un chiffre présenté doit être vérifié rapidement.",
      "NOTES_SOW contient la note de reproductibilité et le rapport de validation de la concordance. Ces documents expliquent comment relancer ou contrôler l’analyse et quelles précautions d’interprétation appliquer.",
      "ANNEXE_pipeline_actuelle_HYPO_instabilite_hybride est volontairement séparée. Elle documente l’évolution scientifique actuelle sans modifier la baseline qui répond au contrat.",
      "Pour une remise à McGill/WELL-E, il suffit de transmettre le dossier Objectif1_Pipeline_detection_boiterie complet. Les anciens brouillons et rapports intermédiaires ne sont pas nécessaires.",
      "TRANSITION — Avec les données, les résultats et les livrables explicités, nous pouvons formuler précisément ce qui est établi et ce qui reste à confirmer.",
      "QUESTION POSSIBLE — « Quel fichier faut-il ouvrir en premier? » Réponse : le README, puis le rapport Word. Les CSV servent ensuite à vérifier un résultat précis ou à refaire une analyse.",
    ],
    [SRC.readme, SRC.report],
  );
}

// 13 — Verdict
{
  const slide = deck.slides.add();
  header(slide, "Ce que les résultats permettent de conclure", "Portée scientifique", 13);
  rect(slide, M, 176, 550, 398, "#E9F4EE");
  rect(slide, 630, 176, 590, 398, "#FBEDED");
  text(slide, "ÉTABLI PAR LE TRAVAIL", 84, 210, 470, 26, {
    size: 14,
    bold: true,
    color: C.green,
  });
  [
    "Transfert réussi sur quatre saisons",
    "Paramètres communs et sorties reproductibles",
    "Alertes priorisées par contexte troupeau",
    "Concordance comportementale documentée",
    "Livrables complets et traçables",
  ].forEach((v, i) => bullet(slide, v, 84, 258 + i * 55, 470, { color: C.green, size: 19 }));
  text(slide, "À CONFIRMER PAR UNE ÉTUDE CLINIQUE", 668, 210, 500, 26, {
    size: 14,
    bold: true,
    color: C.red,
  });
  [
    "Sensibilité et spécificité",
    "Seuils généralisables",
    "Délai entre signal et boiterie clinique",
    "Charge d’alertes acceptable sur le terrain",
    "Supériorité clinique de l’approche hybride",
  ].forEach((v, i) => bullet(slide, v, 668, 258 + i * 55, 500, { color: C.red, size: 19 }));
  text(
    slide,
    "Conclusion : une chaîne d’alerte comportementale exploitable pour la recherche et la revue ciblée.",
    M,
    612,
    1130,
    34,
    { size: 20, bold: true, color: C.teal },
  );
  notes(
    slide,
    [
      "MESSAGE PRINCIPAL — L’objectif 1 est un succès technique et contractuel, avec une portée scientifique utile, mais il ne constitue pas encore une validation clinique de détection de la boiterie.",
      "Ce qui est établi : les quatre corpus ont été convertis et exécutés; les paramètres sont communs; les sorties sont reproductibles; les notifications sont traçables jusqu’aux intervalles sources.",
      "Le renforcement troupeau améliore l’usage opérationnel en séparant les signaux individuels prioritaires des épisodes collectifs probables. Il réduit ainsi le risque de traiter plusieurs vaches comme des cas indépendants lorsqu’un événement est partagé.",
      "La concordance avec les scans comportementaux est documentée, mais elle décrit seulement une proximité temporelle. Elle ne fournit pas une mesure de performance clinique.",
      "La baseline IF n’a pas montré d’alignement aux SLS disponibles. L’approche actuelle hybride montre un signal exploratoire positif, mais la cohorte est trop petite et trop confondue pour conclure à une supériorité clinique.",
      "Ce qui n’est pas encore établi : sensibilité, spécificité, seuils généralisables, délai avant apparition clinique, charge d’alertes acceptable et performance dans un autre troupeau.",
      "La formulation correcte est donc « chaîne d’alerte comportementale exploitable pour la recherche et la revue ciblée », et non « outil diagnostique validé de boiterie ».",
      "Cette conclusion est positive parce qu’elle répond au SOW, rend les analyses reproductibles et identifie clairement le meilleur chemin vers une validation clinique crédible.",
      "TRANSITION — La prochaine étape n’est pas d’ajouter immédiatement un autre modèle; elle consiste à améliorer la qualité et la quantité de vérité-terrain.",
      "QUESTION POSSIBLE — « L’objectif est-il atteint? » Réponse : oui au sens du SOW et de la faisabilité technique. La validation clinique complète constitue l’étape suivante, pas un résultat déjà revendiqué.",
    ],
    [SRC.sow, SRC.report, SRC.sls],
  );
}

// 14 — Objective 2, next deliverable
{
  const slide = deck.slides.add();
  header(
    slide,
    "Environnement et comportement : le prochain livrable",
    "Objectif 2",
    14,
  );
  text(slide, "CE QUI EST DÉJÀ FAIT", M, 176, 560, 26, {
    size: 14,
    bold: true,
    color: C.teal,
  });
  [
    "IceTag, sondes HOBO et scans synchronisés sur Summer 2019",
    "87 501 intervalles de 15 min, 17 vaches, 62 jours",
    "Indice THI calculé et aligné au même pas de temps",
    "Analyses de sensibilité à plusieurs niveaux d’agrégation",
  ].forEach((v, i) => bullet(slide, v, M, 218 + i * 62, 560, { color: C.teal, size: 19 }));
  metric(slide, M, 470, 180, "87 501", "intervalles synchronisés", C.teal);
  metric(slide, M + 200, 470, 150, "17", "vaches", C.blue);
  metric(slide, M + 370, 470, 150, "62", "jours", C.purple);

  text(slide, "RÉSULTAT PRINCIPAL", 660, 176, 560, 26, {
    size: 14,
    bold: true,
    color: C.blue,
  });
  table(
    slide,
    660,
    212,
    [330, 110, 120],
    [
      ["Association THI et activité", "Effet", "p"],
      ["Avant contrôle du jour", "+0,221", "< 0,001"],
      ["Après contrôle du jour", "+0,061", "0,36"],
    ],
    58,
    17,
  );
  rect(slide, 660, 400, 560, 116, "#FBEDED");
  text(
    slide,
    "L’association positive disparaît une fois le jour contrôlé : elle existe entre les journées, sans effet thermique propre démontré. Le stress sévère (THI ≥ 80) ne concerne que 1,1 % des intervalles.",
    684,
    418,
    512,
    82,
    { size: 17, color: C.red },
  );
  rect(slide, M, 556, 1168, 88, "#E8F0FB");
  text(
    slide,
    "Livrable 2 prêt à être remis : rapport, jeu de données intégré, tableaux, figures et code de reproduction.",
    M + 24,
    582,
    1116,
    40,
    { size: 21, bold: true, color: C.blue },
  );
  notes(
    slide,
    [
      "MESSAGE PRINCIPAL — L’objectif 2 est terminé et constitue le prochain livrable. Je le présente ici brièvement pour annoncer la suite, sans entrer dans le détail aujourd’hui.",
      "Le travail de synchronisation est fait : les mesures IceTag, les sondes HOBO extérieures et les scans comportementaux sont alignés sur Summer 2019, au pas de quinze minutes.",
      "Périmètre : 87 501 intervalles vache-quinze minutes, 17 vaches et 62 jours. L’écart avec les 139 111 intervalles de l’objectif 1 est attendu, car les sondes environnementales ne couvrent la période qu’à partir du 1er juillet 2019.",
      "Résultat central, à présenter avec prudence : l’association entre le THI et l’activité est positive et forte avant contrôle du jour, avec +0,221 pas par unité de THI. Après contrôle explicite du jour, l’effet tombe à +0,061 avec un p de 0,36, donc non concluant.",
      "Interprétation correcte : l’association existe entre les journées, mais elle est confondue avec le protocole d’accès à l’exercice et la progression saisonnière. Je ne revendique donc aucun effet thermique causal indépendant.",
      "Le stress thermique sévère, THI supérieur ou égal à 80, ne concerne que 1,1 % des intervalles dans ce corpus québécois. C’est une limite structurelle des données, pas de l’analyse.",
      "Le volet comportement reste exploratoire : les scans ne couvrent que huit jours, ce qui est insuffisant pour intégrer le comportement comme covariable robuste.",
      "TRANSITION — Je propose de vous transmettre ce livrable et d’en discuter lors d’un prochain point, puis de revenir aux décisions attendues sur l’objectif 1.",
      "QUESTION POSSIBLE — « Le THI influence-t-il le comportement? » Réponse : dans ces données, l’association est visible entre les journées, mais elle n’est plus concluante une fois le jour contrôlé. Conclure à un effet thermique demanderait un protocole séparant la chaleur des autres différences entre journées.",
    ],
    [SRC.obj2Report, SRC.obj2Model, SRC.obj2Desc],
  );
}

// 15 — Next steps
{
  const slide = deck.slides.add();
  header(slide, "Proposition pour la prochaine étape", "Suite du projet", 15);
  const steps = [
    ["01", "Sélectionner la cohorte", "Meilleur recouvrement entre IceTag et scores locomoteurs datés", C.blue],
    ["02", "Geler le protocole", "Version, seuils, fenêtre d’alerte et métriques définis avant l’analyse", C.teal],
    ["03", "Valider prospectivement", "Sensibilité, spécificité, délai et intervalles de confiance", C.purple],
    ["04", "Évaluer l’usage", "Charge de revue A/B/C et causes des événements collectifs", C.green],
  ];
  steps.forEach((s, i) => {
    const x = M + i * 292;
    text(slide, s[0], x, 184, 70, 38, { size: 25, bold: true, color: s[3] });
    line(slide, x, 236, 244, s[3], 5);
    text(slide, s[1], x, 274, 244, 58, { size: 22, bold: true });
    text(slide, s[2], x, 350, 244, 146, { size: 18, color: C.muted });
  });
  rect(slide, M, 546, 1168, 94, "#E8F0FB");
  text(
    slide,
    "Décisions proposées : confirmer la livraison de l’objectif 1 et identifier la cohorte clinique de validation.",
    M + 24,
    574,
    1116,
    42,
    { size: 21, bold: true, color: C.blue },
  );
  notes(
    slide,
    [
      "MESSAGE PRINCIPAL — La priorité suivante est une validation clinique mieux dessinée, fondée sur des scores locomoteurs datés et suffisamment nombreux, plutôt que l’ajout immédiat d’un nouveau modèle.",
      "Étape 1 : sélectionner une cohorte présentant un recouvrement clair entre les données IceTag et des scores locomoteurs répétés. Il faut davantage de vaches SLS ≥ 2 et, idéalement, plusieurs cas SLS ≥ 3.",
      "Étape 2 : geler avant l’analyse la version du pipeline, les seuils, la durée de la fenêtre antérieure au score et les métriques. Cette préspécification limite le risque d’adapter la méthode aux résultats observés.",
      "Étape 3 : conduire une validation prospective ou, à défaut, une validation rétrospective strictement préspécifiée. Les résultats attendus sont la sensibilité, la spécificité, les valeurs prédictives, le délai d’alerte et leurs intervalles de confiance.",
      "Étape 4 : mesurer l’usage opérationnel. Il faut déterminer combien de revues A et B sont réalistes par jour, quelles catégories produisent les cas pertinents et quelles causes expliquent les regroupements C.",
      "La première décision demandée à McGill/WELL-E est de confirmer que le paquet de l’objectif 1 répond aux quatre livrables du SOW.",
      "La deuxième décision est d’identifier la meilleure cohorte clinique disponible et de clarifier le protocole SLS : définition exacte du score, dates, évaluateur, répétitions et traitements expérimentaux.",
      "Une information de gestion sur l’épisode collectif du début de février 2019 serait également utile pour distinguer un événement réel de troupeau d’un éventuel artefact.",
      "TRANSITION — Je termine par trois messages simples, puis j’ouvre la discussion sur ces deux décisions.",
      "QUESTION POSSIBLE — « Que vous faut-il concrètement de notre part? » Réponse : une confirmation de livraison, la documentation exacte des SLS et l’accès à une cohorte comportant plus de scores locomoteurs synchronisés et de cas positifs.",
    ],
    [SRC.report, SRC.sls],
  );
}

// 16 — Closing
{
  const slide = deck.slides.add();
  slide.background.fill = C.ink;
  rect(slide, 1004, 0, 18, 720, C.cyan);
  text(slide, "McGILL / WELL-E", M, 42, 400, 28, {
    size: 16,
    bold: true,
    color: C.cyan,
  });
  text(
    slide,
    "Objectif 1 :\ntraité, documenté\net prêt pour la validation suivante.",
    M,
    170,
    880,
    280,
    { size: 52, bold: true, color: C.white },
  );
  text(
    slide,
    "Merci. Questions et discussion.",
    M,
    562,
    720,
    48,
    { size: 26, color: "#D2D8DF" },
  );
  text(slide, "30 juillet 2026", 1048, 616, 180, 30, {
    size: 18,
    bold: true,
    color: C.white,
    align: "right",
  });
  notes(
    slide,
    [
      "MESSAGE PRINCIPAL — L’objectif 1 est traité au sens du SOW, les résultats sont reproductibles et les limites sont documentées de manière transparente.",
      "CONCLUSION ORALE PROPOSÉE — En résumé, les quatre saisons ont été harmonisées et analysées avec une chaîne commune. Les 385 notifications ont été rendues plus actionnables par le classement A, B et C, et tous les résultats sont traçables dans le dossier livré.",
      "Deuxième message : la baseline IF répond au mandat technique, mais elle ne montre pas d’alignement aux SLS disponibles. Il serait donc incorrect de la présenter comme un détecteur clinique validé.",
      "Troisième message : l’approche actuelle HYPO + instabilité + hybride montre un alignement exploratoire encourageant avec les SLS, mais seulement sur 14 vaches et 3 cas positifs, avec un confondant lié au groupe Exercise.",
      "La demande de clôture est double : confirmer la réception et la conformité du livrable de l’objectif 1, puis convenir de la cohorte et du protocole qui permettront la validation clinique suivante.",
      "OUVERTURE DES QUESTIONS — Je peux revenir sur la construction des notifications, les catégories A/B/C, la couverture, les tables de concordance, les résultats SLS ou l’organisation des fichiers.",
      "RÉPONSE COURTE SI LE VERDICT EST DEMANDÉ — Succès technique et contractuel; signal scientifique prometteur pour l’approche actuelle; preuve clinique encore insuffisante.",
    ],
    [SRC.sow, SRC.readme, SRC.report],
  );
}

await fs.mkdir(OUT_DIR, { recursive: true });
await fs.mkdir(BUILD_DIR, { recursive: true });

for (const [index, slide] of deck.slides.items.entries()) {
  const stem = `slide-${String(index + 1).padStart(2, "0")}`;
  const png = await deck.export({ slide, format: "png", scale: 1 });
  await fs.writeFile(`${BUILD_DIR}/${stem}.png`, new Uint8Array(await png.arrayBuffer()));
  const layout = await slide.export({ format: "layout" });
  await fs.writeFile(`${BUILD_DIR}/${stem}.layout.json`, await layout.text());
}

const montage = await deck.export({ format: "webp", montage: true, scale: 1 });
await fs.writeFile(
  `${BUILD_DIR}/deck-montage.webp`,
  new Uint8Array(await montage.arrayBuffer()),
);

const file = await PresentationFile.exportPptx(deck);
await file.save(OUT_PPTX);
console.log(`Created ${OUT_PPTX}`);
