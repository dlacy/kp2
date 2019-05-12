if(sync.ext.Registry.extension.type === 'dita') {
  sync.ext.Registry.extension.registerActionsHandler(function(editor, actionsConfig) {
    var actionsManager = editor.getActionsManager();
    // Wrap the Insert Web Link action.
    var insertWebLinkId = 'insert.url.reference';
    var originalInsertWebLinkAction = actionsManager.getActionById(insertWebLinkId);
    if(originalInsertWebLinkAction) {
      var insertWebLinkAction = new sync.actions.InsertWebLink(
        originalInsertWebLinkAction,
        'ro.sync.ecss.extensions.dita.link.InsertXrefOperation',
        editor,
        'reference_value',
        {
          format: 'html',
          scope: 'external',
          'href type': 'web page'
        });
      actionsManager.registerAction(insertWebLinkId, insertWebLinkAction);
      var changeToWebLinkAction = new sync.actions.InsertWebLink(
        originalInsertWebLinkAction,
        'ro.sync.ecss.extensions.dita.link.InsertXrefOperation',
        editor,
        'reference_value',
        {
          format: 'html',
          scope: 'external',
          'href type': 'web page',
          replace_reference: 'true'
        });
      actionsManager.registerAction('change.url.reference', changeToWebLinkAction);
    }
  });
}