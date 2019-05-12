if(sync.ext.Registry.extension.type === 'dita') {
  sync.ext.Registry.extension.registerActionsHandler(function(editor, actionsConfig) {
    var actionsManager = editor.getActionsManager();
    var convertSimpleTableToCalsTableId = 'convert.simple.table.to.cals.table';
    var convertSimpleTableToCalsTableAction = actionsManager.getActionById(convertSimpleTableToCalsTableId);
    if(convertSimpleTableToCalsTableAction) {
      // The action's enabled status should be context aware
      convertSimpleTableToCalsTableAction.isEnabled = function() {
        var isEnabled = false;
        var classValue = ' ' + (editor.getSelectionManager().getSelection().getNodeAtSelection().getAttribute('class')  || '') + ' ';
        if (classValue.indexOf(' topic/strow ') !== -1 ||
          classValue.indexOf(' topic/sthead ') !== -1 ||
          classValue.indexOf(' topic/stentry ') !== -1 ||
          classValue.indexOf(' topic/simpletable ') !== -1) {

          // We are inside a simple table
          isEnabled = true;
        }
        return isEnabled;
      };
    }
  });
}
