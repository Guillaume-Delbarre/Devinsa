chart_config = { chart : {container: '#tree', scrollbar: 'native', 
connectors: { type: 'step' },
 node: { HTMLclass: 'nodeExample1' },
 animation: { nodeAnimation: "easeOutBounce", nodeSpeed: 700,connectorsAnimation: "bounce", connectorsSpeed: 700 }},
nodeStructure : {text: { name: 'Ton personnage est-il réel ?' }, collapsed : true, children : [

{
text: { name: '1167 personnage(s)',perso1 : 'Cyril Dumoulin ',perso2 : 'Cartman ',perso3 : 'Le petit Grégory ', desc : 'Ton personnage est-il français ?'},HTMLclass :'light-green',collapsed : true, children : [
{text : {name : 'Fin'}, collapsed: true}]
}, 
 {
text: { name: '1424 personnage(s)',perso1 : 'Le petit Grégory ',perso2 : 'Cartman ',perso3 : 'Cyril Dumoulin ', desc : 'Ton personnage est-il un personnage de jeu vidéo ?'},HTMLclass :'light-red',collapsed : true, children : [
{text : {name : 'Fin'}, collapsed: true}]
 } 
] } 
 };