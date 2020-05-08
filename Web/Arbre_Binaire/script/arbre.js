function lancerscript(nom, optionsligne){
    console.log(nom + " : Script lancé");
    path = "../ScriptPython/".concat(nom);
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

