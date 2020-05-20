chart_config = { chart : {container: '#tree', scrollbar: 'native', 
connectors: { type: 'step' },
 node: { HTMLclass: 'nodeExample1' },
 animation: { nodeAnimation: "easeOutBounce", nodeSpeed: 700,connectorsAnimation: "bounce", connectorsSpeed: 700 }},
nodeStructure : {text: { name: 'Ton personnage est-il réel ?', desc :'1537 personnages' }, collapsed : true, children : [
{text: { name: '1078 personnage(s)',perso1 : 'Michel Blanc (acteur français)',perso2 : 'Roselyne Bachelot',perso3 : 'Brigitte Macron', desc : 'Ton personnage est-il français ?'},HTMLclass :'light-green',collapsed : true, children : [{text : {name : 'Fin'}, collapsed: true}]
}, 
 {text: { name: '771 personnage(s)',perso1 : 'Toki (frère de Ken le survivant)',perso2 : 'Ford Prefect (perso du Guide du voyageur galactique)',perso3 : 'Ant-man (super héros Marvel)', desc : 'Ton personnage est-il un personnage de jeu vidéo ?'},HTMLclass :'light-red',collapsed : true, children : [{text : {name : 'Fin'}, collapsed: true}]
 } 
] }};