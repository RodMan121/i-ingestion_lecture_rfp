<map version="freeplane 1.9.0">
<node TEXT="Migration CMN : Nutanix / OVHcloud">
    
    <node TEXT="Phase 1 : Planification &amp; Cadrage (Mois 1)" POSITION="right">
      <node TEXT="1.1 Lancement &amp; Gouvernance">
        <node TEXT="Réunion Kick-off &amp; Comitologie (Co_TECH, Co_PIL)"/>
        <node TEXT="Outils ITSM (ServiceNow, Jira)"/>
      </node>
      <node TEXT="1.2 Audit Technique &amp; Right-Sizing">
        <node TEXT="Découverte (Nutanix Collector : CPU, RAM, IOPS)"/>
        <node TEXT="Décisions d&apos;architecture &amp; Optimisation (Anti-gaspillage)"/>
      </node>
      <node TEXT="1.3 Cartographie des Dépendances">
        <node TEXT="Identification flux inter-applicatifs"/>
        <node TEXT="Constitution des Move Groups (vagues)"/>
      </node>
      <node TEXT="1.4 Anticipation &amp; Livrables">
        <node TEXT="Stratégie de réversibilité (Exit Strategy)"/>
        <node TEXT="Livrables : Plan de Transition, DAT, PAQ, PAS"/>
      </node>
    </node>

    <node TEXT="Phase 2 : Landing Zone (Mois 2)" POSITION="right">
      <node TEXT="2.1 Infrastructure Matérielle (IaaS)">
        <node TEXT="Bare Metal OVHcloud (Tier 3 / ISO 27001)"/>
        <node TEXT="Déploiement AHV &amp; AOS (Data Locality)"/>
      </node>
      <node TEXT="2.2 Réseau &amp; Résilience">
        <node TEXT="vRack OVHcloud (Interconnexion L2)"/>
        <node TEXT="Routage OSPF &amp; VLANs (Iso-IP)"/>
      </node>
      <node TEXT="2.3 Cybersécurité">
        <node TEXT="Micro-segmentation (Nutanix Flow)"/>
        <node TEXT="Périmètre : WAF, Anti-DDoS, Bastion"/>
        <node TEXT="Nutanix Data Lens (Analyse comportementale NAS)"/>
      </node>
      <node TEXT="2.4 Validation (Jalon)">
        <node TEXT="Tests HA &amp; PRA/PCA virtuels"/>
        <node TEXT="Go/No-Go Migration"/>
      </node>
    </node>

    <node TEXT="Phase 3 : Migration Factory (Mois 3 à 5)" POSITION="left">
      <node TEXT="3.1 Phase Pilote">
        <node TEXT="Migration à blanc (VMs non-critiques)"/>
        <node TEXT="Validation transferts &amp; VM tools"/>
      </node>
      <node TEXT="3.2 Vagues de Migration (Seeding)">
        <node TEXT="Exécution via Move Groups"/>
        <node TEXT="Copie asynchrone CBT (Nutanix Move)"/>
      </node>
      <node TEXT="3.3 Bascule (Cutover)">
        <node TEXT="Plage de maintenance (Delta final)"/>
        <node TEXT="Arrêt source &gt; Démarrage cible"/>
      </node>
      <node TEXT="3.4 Recette &amp; Rollback (Jalon)">
        <node TEXT="Tests UAT par le CMN"/>
        <node TEXT="Application Rollback si échec"/>
        <node TEXT="100% des charges migrées"/>
      </node>
    </node>

    <node TEXT="Phase 4 : Hypercare &amp; Run (Mois 6+)" POSITION="left">
      <node TEXT="4.1 Hypercare">
        <node TEXT="Support N2/N3 renforcé post-bascule"/>
        <node TEXT="Stabilisation environnements"/>
      </node>
      <node TEXT="4.2 MCO (Maintien Condition Opérationnelle)">
        <node TEXT="Routines d&apos;infogérance"/>
        <node TEXT="Nutanix LCM (Mises à jour sans coupure)"/>
      </node>
      <node TEXT="4.3 SOC &amp; Sauvegardes">
        <node TEXT="SIEM (Rétention 12 mois)"/>
        <node TEXT="Sauvegardes immuables (S3 Object Lock)"/>
      </node>
      <node TEXT="4.4 FinOps &amp; Clôture (Jalon)">
        <node TEXT="Machine Learning Prism X-Fit (Optimisation)"/>
        <node TEXT="Clôture Unité d&apos;Œuvre Initialisation"/>
        <node TEXT="Passage en Run total (VSR validée)"/>
      </node>
    </node>

  </node>
</map>
