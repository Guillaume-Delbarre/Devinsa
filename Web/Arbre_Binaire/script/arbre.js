
let {PythonShell} = require('python-shell');

function lancerscript(optionsligne){

    console.log(" finalTree.py : Script lancé");

    path = "../ScriptPython/finalTree.py";

    let options = {args: optionsligne};

    PythonShell.run(path, options, function (err) {

            if (err) {

                console.log(err)

                console.log(nom + " : Echec de l'execution");

            }else{

                //console.log(nom + ' fini');

            }

    });

}

function getValue(){
    var arg = parseInt(document.getElementById("tag1").value,10);
    if (isNaN(arg)){
        alert("Valeur saisie incorrecte");
        return;
    }
    else if(arg<1) {
        alert("Veuillez saisir une valeur supérieur à 0");
        return;
    }

}