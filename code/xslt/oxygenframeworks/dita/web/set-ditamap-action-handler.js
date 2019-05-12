if(sync.ext.Registry.extension.type === 'dita') {
  sync.ext.Registry.extension.registerActionsHandler(function(editor, actionsConfig) {
    if (editor.ditamapsManagerEnabled) {
      var ACTION_ID = 'DITA/SetDitaMap';
      var editingSupport = editor.getEditingSupport();
      var askForDitamapAction =
        new sync.actions.AskForDitamap(editor, editor.widgets, editingSupport.scheduler,
          editingSupport.getController(), editingSupport.problemReporter);
      editor.getActionsManager().registerAction(ACTION_ID, askForDitamapAction);

      // Add a "set ditamap" button to the DITA toolbar
      for (var i = 0; i < actionsConfig.toolbars.length; i++) {
        var toolbar = actionsConfig.toolbars[i];
        if (toolbar.name === 'DITA') {
          toolbar.children.unshift({
            id: ACTION_ID,
            type: 'action'
          }, {
            type: 'sep'
          });
          break;
        }
      }

    }
  });
}