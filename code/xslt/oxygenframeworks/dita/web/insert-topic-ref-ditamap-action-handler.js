if(sync.ext.Registry.extension.type === 'ditamap') {
  sync.ext.Registry.extension.registerActionsHandler(function(editor, actionsConfig) {
    var actionsManager = editor.getActionsManager();
    var originalInsertTopicRef = actionsManager.getActionById('insert.topicref');
    if (originalInsertTopicRef) {
      var insertTopicRef = new sync.actions.InsertTopicRef(originalInsertTopicRef, editor);
      if (insertTopicRef.isEnabled()) {
        actionsManager.registerAction('insert.topicref', insertTopicRef);
      }
    }
  });
}