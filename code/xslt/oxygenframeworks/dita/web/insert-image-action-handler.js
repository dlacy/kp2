if(sync.ext.Registry.extension.type === 'dita') {
  sync.ext.Registry.extension.registerActionsHandler(function(editor, actionsConfig) {
    var actionsManager = editor.getActionsManager();

    var originalInsertImageAction = actionsManager.getActionById('insert.image');
    if (originalInsertImageAction) {
      var insertImageAction = new sync.actions.InsertImage(
        originalInsertImageAction,
        "ro.sync.ecss.extensions.dita.topic.InsertImageOperation",
        editor);
      actionsManager.registerAction('insert.image', insertImageAction);
    }
  });
}