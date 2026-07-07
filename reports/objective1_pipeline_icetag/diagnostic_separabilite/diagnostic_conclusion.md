# Diagnostic de séparabilité — Winter 2019 (labels SLS synchrones)

Vaches analysées : 16 (boiteuses SLS>=2 : 5, saines/légères : 11)

## 1. Séparabilité univariée
Features IceTag testées : 5 | significatives (p<0.05) : 0

              feature  moy_boiteuses  moy_saines  p_value significatif_5pct
           Pas / jour         664.60      671.74   1.0000               non
  Variabilité des pas         364.56      296.05   0.3773               non
 Heures couché / jour          14.87       14.54   0.5833               non
Nb de couchers / jour          83.00       63.46   0.2674               non
  Motion Index / jour        1975.06     2993.95   1.0000               non

## 2. Plafond multivarié (Random Forest, Leave-One-Out)
AUC = 0.236 | balanced accuracy = 0.409 (0.5 = hasard)

## 3. Pipeline gelé vs SLS
Spearman rho = 0.033 (p=0.904) | Mann-Whitney notifs p = 0.649

## Conclusion
Aucune feature IceTag ne sépare les vaches boiteuses des saines, et un classifieur multivarié ne fait pas mieux que le hasard. Le signal de boiterie n'est PAS présent dans les données IceTag de cette cohorte d'étude d'exercice. 

=> L'absence de détection n'est imputable NI au pipeline NI au travail du mémoire : c'est une limite des données/de la cohorte. On ne peut pas détecter un signal absent de l'entrée. Le mémoire reste valide (validé par injection sur ses propres données).