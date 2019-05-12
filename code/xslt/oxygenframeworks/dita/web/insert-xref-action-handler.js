if(sync.ext.Registry.extension.type === 'dita') {
  sync.ext.Registry.extension.registerActionsHandler(function(editor, actionsConfig) {
    var actionsManager = editor.getActionsManager();
    var originalInsertXref = actionsManager.getActionById('insert.cross.reference');
    if (originalInsertXref) {
      var insertXref = new sync.actions.InsertXref(originalInsertXref, editor);
      actionsManager.registerAction('insert.cross.reference', insertXref);
      var changeXref = new sync.actions.InsertXref(originalInsertXref, editor, {replace_reference: 'true'});
      actionsManager.registerAction('change.cross.reference', changeXref);
    }
  });
}