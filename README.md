# Proje_PIR 

Ce projet PIR vise à découvrir la problématique de la couverture optimale d’un
environnement donné avec une flotte de robots coopératifs.
# Problème 
Le problème de couverture, ou problème de déploiement optimal, vise à trouver l'emplacement
optimal d'un réseau de capteurs de telle sorte que certains critères définissant le niveau de
couverture de l'équipe dans une région d'intérêt soient optimisés. Ces critères peuvent par exemple
refléter la dispersion globale des capteurs dans l'environnement ou quantifier leur proximité avec les
différentes parties de l'environnement. Le problème de la couverture optimale est un problème
largement étudié dans la littérature en raison de ses nombreuses applications allant de la
surveillance d'une zone donnée par des robots mobiles au placement optimal de ressources, telles
que des antennes, pour optimiser un réseau de communication. Cependant, les défis qui se posent
dans des scénarios non triviaux, font de ce problème un domaine de recherche encore très actif.
![image](https://user-images.githubusercontent.com/101548708/236159856-138bf699-3493-46e0-805d-927c57db03cd.png)

Dans ce sujet, on étudiera différentes stratégies pour obtenir des solutions de couverture avec des
robots mobiles en considérant différents scénarios, tels que : des poids non-uniformes définis dans
l'environnement, différentes définitions de distances et des capacités de communication limitées
dans le réseau. Les environnements étudiés seront principalement en 2D sauf pour le point 4 où
nous considérerons aussi la couverture d’une surface en 3D. Les solutions obtenues seront
également implémentées et testées en simulation (code à développer en Python).
# Travaux
Dans ce projet, le travail s’organisera en plusieurs sous objectifs répartis entre les
étudiants :

1) Définition et implémentation d’une stratégie de couverture multi-robots basée sur des partitions
de Voronoi et étude de différentes définitions de distances en s’inspirant des références [1] et [6].
2) Étude de scenarios avec des fonctions de densité d’information non-uniforme et variant dans le
temps. On pourra s’inspirer du travail présenté dans [2].
3) Étude d’une stratégie distribuée de couverture avec un système multi-robots en considérant des
contraints de communication. On pourra s’inspirer de la solution présentée dans [3].
4) Extension des stratégies de couverture basée sur des partitions de Voronoi pour des surfaces 3D,
en s’inspirant de [4]. Étude du cas particulier d’une sphère.
5) Définition et implémentation d’une stratégie de couverture multi-robots pour des environnements
avec des obstacles basée sur des champs de potentiel. On pourra s’inspirer de la référence [5].
