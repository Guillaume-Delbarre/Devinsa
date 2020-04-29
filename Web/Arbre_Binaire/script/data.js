chart_config = { chart : {container: '#tree', scrollbar: 'native', 
connectors: { type: 'step' },
 node: { HTMLclass: 'nodeExample1' },
 animation: { nodeAnimation: "easeOutBounce", nodeSpeed: 700,connectorsAnimation: "bounce", connectorsSpeed: 700 }},
nodeStructure : {text: { name: 'Ton personnage est-il réel ?' }, collapsed : true, children : [

{
text: { name: '113 personnage(s)',perso1 : 'Jill (Va-11 Hall-a)',perso2 : 'Tracer (Overwatch)',perso3 : 'Altair', desc : 'Ton personnage est-il français ?'},HTMLclass :'light-green',collapsed : true, children : [
{text : {name : 'Fin'}, collapsed: true}]
}, 
 {
text: { name: '370 personnage(s)',perso1 : 'Tryphon Tournesol',perso2 : 'Tyler Durden (perso du film fight club)[',perso3 : 'Ford Prefect (perso du Guide du voyageur galactique)', desc : 'Ton personnage est-il un personnage de jeu vidéo ?'},HTMLclass :'light-red',collapsed : true, children : [
{text : {name : 'Fin'}, collapsed: true}]
 } 
] } 
 };