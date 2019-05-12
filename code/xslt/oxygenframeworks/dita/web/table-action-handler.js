if(sync.ext.Registry.extension.type === 'dita') {
  sync.ext.Registry.extension.registerActionsHandler(function(editor, actionsConfig) {
    var actionsManager = editor.getActionsManager();

    var originalInsertTableAction = actionsManager.getActionById('insert.table');
    if (originalInsertTableAction) {
      var insertTableAction = new sync.actions.InsertTable(
        originalInsertTableAction,
        "ro.sync.ecss.extensions.dita.topic.table.InsertTableOperation",
        editor,
        [sync.actions.InsertTable.TableTypes.CALS, sync.actions.InsertTable.TableTypes.DITA_SIMPLE],
        [sync.actions.InsertTable.ColumnWidthTypes.PROPORTIONAL,
          sync.actions.InsertTable.ColumnWidthTypes.DYNAMIC,
          sync.actions.InsertTable.ColumnWidthTypes.FIXED]);

      editor.getActionsManager().registerAction('insert.table', insertTableAction);
    }

    var originalInsertTableWizardAction = actionsManager.getActionById('insert.table.wizard');
    if (originalInsertTableWizardAction) {
      var insertTableAction = new sync.actions.InsertTable(
        originalInsertTableWizardAction,
        "ro.sync.ecss.extensions.dita.topic.table.InsertTableOperation",
        editor,
        [sync.actions.InsertTable.TableTypes.CALS, sync.actions.InsertTable.TableTypes.DITA_SIMPLE],
        [sync.actions.InsertTable.ColumnWidthTypes.PROPORTIONAL,
          sync.actions.InsertTable.ColumnWidthTypes.DYNAMIC,
          sync.actions.InsertTable.ColumnWidthTypes.FIXED]);
      actionsManager.registerAction('insert.table.wizard', insertTableAction);
    }
  });
}