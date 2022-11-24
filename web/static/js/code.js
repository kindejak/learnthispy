

const output = document.getElementById("output");
  
const editor = CodeMirror.fromTextArea(document.getElementById("code"), {
    mode: {
        name: "python",
        version: 3,
        singleLineStringErrors: false
    },
    extraKeys: {"Ctrl-Space": "autocomplete"},
    lineNumbers: true,
    indentUnit: 4,
    matchBrackets: true,
    hint: CodeMirror.pythonHint,
    gutters: ["CodeMirror-lint-markers"],
}); 


var ExcludedIntelliSenseTriggerKeys =
{
    "8": "backspace",
    "9": "tab",
    "13": "enter",
    "16": "shift",
    "17": "ctrl",
    "18": "alt",
    "19": "pause",
    "20": "capslock",
    "27": "escape",
    "33": "pageup",
    "34": "pagedown",
    "35": "end",
    "36": "home",
    "37": "left",
    "38": "up",
    "39": "right",
    "40": "down",
    "45": "insert",
    "46": "delete",
    "91": "left window key",
    "92": "right window key",
    "93": "select",
    "107": "add",
    "109": "subtract",
    "110": "decimal point",
    "111": "divide",
    "112": "f1",
    "113": "f2",
    "114": "f3",
    "115": "f4",
    "116": "f5",
    "117": "f6",
    "118": "f7",
    "119": "f8",
    "120": "f9",
    "121": "f10",
    "122": "f11",
    "123": "f12",
    "144": "numlock",
    "145": "scrolllock",
    "186": "semicolon",
    "187": "equalsign",
    "188": "comma",
    "189": "dash",
    "190": "period",
    "191": "slash",
    "192": "graveaccent",
    "220": "backslash",
    "222": "quote"
}

editor.on("keyup", function(cm, event)
{

    if (!cm.state.completionActive &&
        !ExcludedIntelliSenseTriggerKeys[(event.keyCode || event.which).toString()])
    {
        CodeMirror.commands.autocomplete(cm, null, { completeSingle: false });
    }
});

// liter when enter was pressed
editor.on("keyup", function(cm, event) {
    if (event.keyCode == 13) {
        pythonValidator(editor.getValue());
    }
});

  
editor.setOption("theme", "idea");



function pythonValidator(code) {
    console.log("Validating Python code");
    //var code = editor.getValue();
    // send code to server via json post using fetch
    
    fetch('/lint/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            code: code
        })
    }).then(response => response.json())
    .then(data => {
        var errors_warnings = [];
        var parsed_data = Object.values(JSON.parse(data))
        console.log(data);
                for (var i in parsed_data) {
                    console.log(parsed_data[i]);
                    var severity = 'warning';
                    if (parsed_data[i]["type"] === 'error' || parsed_data[i]["type"] === 'fatal') {
                        severity = 'error';
                    }

                    errors_warnings.push({
                        message: parsed_data[i]["message"],
                        message_id: parsed_data[i]["message-id"],
                        severity: severity,
                        line: parsed_data[i]["line"]-1,
                            });
                } 
                annotateEditor(errors_warnings);
                dumpLinterOutputToDiv(errors_warnings);
            }    
    )
}

function annotateEditor(errors_warnings) {
    editor.clearGutter("CodeMirror-lint-markers");
    for(i in errors_warnings) {
        console.log(errors_warnings);
        if (errors_warnings[i]["severity"] == 'error') {
            editor.doc.setGutterMarker(errors_warnings[i]["line"], "CodeMirror-lint-markers", makeError(errors_warnings[i]["message_id"], errors_warnings[i]["message"]));
        } else if (errors_warnings[i]["severity"] == 'warning') {
            editor.doc.setGutterMarker(errors_warnings[i]["line"], "CodeMirror-lint-markers", makeWarning(errors_warnings[i]["message_id"], errors_warnings[i]["message"]));
    }
    }
}

function dumpLinterOutputToDiv(data) {
    lint_output = document.getElementById("lint_output");
    lint = "";
    for (var i in data) {
        lint = lint + "<p class='lint " + data[i]["severity"] + "'><b>line " + data[i]["line"] + "</b>, lintcode: " + data[i]["message_id"] + " ->" + data[i]["message"] + "</p>";
    } 
    console.log(lint);
    lint_output.innerHTML = lint;
}

function escapeHtml(unsafe)
{
    return unsafe
         .replace(/&/g, "&amp;")
         .replace(/</g, "&lt;")
         .replace(/>/g, "&gt;")
         .replace(/"/g, "&quot;")
         .replace(/'/g, "&#039;");
 }

function makeWarning(name, description) {
    var marker = document.createElement("div");
    marker.innerHTML = "<i title='" + name + ": " + escapeHtml(description) + "' class='em em-warning' aria-role='presentation' aria-label='WARNING SIGN'></i>";
    return marker;
  }

function makeError(name, description) {
    var marker = document.createElement("div");
    marker.innerHTML = "<i title='" + name + ": " + escapeHtml(description) + "' class='em em-no_entry' aria-role='presentation' aria-label='NO ENTRY'></i>";
    marker.setAttribute(name, description);
    return marker;
  }
