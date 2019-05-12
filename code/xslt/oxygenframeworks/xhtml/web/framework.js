goog.provide('sync.xhtml.XhtmlExtension');


/**
 * Constructor for the xhtml Extension.
 *
 * @constructor
 */
sync.xhtml.XhtmlExtension = function(){
  sync.ext.Extension.call(this);
};
goog.inherits(sync.xhtml.XhtmlExtension, sync.ext.Extension);

/**
 * Editor created callback.
 *
 * @param {sync.Editor} editor The currently created editor.
 */
sync.xhtml.XhtmlExtension.prototype.editorCreated = function(editor) {
  goog.events.listen(editor, sync.api.Editor.EventTypes.ACTIONS_LOADED, function(e) {
    var actionsManager = editor.getActionsManager();
    var originalInsertImageAction = actionsManager.getActionById('insert.image');
    if (originalInsertImageAction) {
      var insertImageAction = new sync.actions.InsertImage(
        originalInsertImageAction,
        "ro.sync.ecss.extensions.xhtml.InsertImgOperation",
        editor);
      actionsManager.registerAction('insert.image', insertImageAction);
    }

    // Wrap the Insert Web Link action.
    var insertWebLinkActionId = 'a.href';
    var originalInsertWebLinkAction = actionsManager.getActionById(insertWebLinkActionId);
    if(originalInsertWebLinkAction) {
      var insertWebLinkAction = new sync.actions.InsertWebLink(
        originalInsertWebLinkAction,
        'ro.sync.ecss.extensions.commons.operations.SurroundWithFragmentOperation',
        editor,
        'fragment-url');
      // override the get params method to inject the fragment with the input value.
      insertWebLinkAction.getParams = function() {
        var params = sync.actions.InsertWebLink.prototype.getParams.call(this);
        return {
          fragment: '<a href="' + params['fragment-url'] + '" xmlns="http://www.w3.org/1999/xhtml">' + 
            params['fragment-url'] + 
          '</a>'
        }
      };
      actionsManager.registerAction(insertWebLinkActionId, insertWebLinkAction);
    }

    var originalInsertTableAction = actionsManager.getActionById('insert.table');
    if (originalInsertTableAction) {
      var insertTableAction = new sync.actions.InsertTable(
        originalInsertTableAction,
        "ro.sync.ecss.extensions.commons.table.operations.xhtml.InsertTableOperation",
        editor,
        [sync.actions.InsertTable.TableTypes.HTML],
        [sync.actions.InsertTable.ColumnWidthTypes.PROPORTIONAL,
          sync.actions.InsertTable.ColumnWidthTypes.DYNAMIC,
          sync.actions.InsertTable.ColumnWidthTypes.FIXED], 'Caption');
      actionsManager.registerAction('insert.table', insertTableAction);
    }

    addOldStyleTableActions(e.actionsConfiguration, "XHTML", editor);
  }, true);
};

/**
 * Adds old-style (selection-based actions to the current configuration.
 *
 * @param {object} actionsConfiguration The actions configuration.
 * @param {string} toolbarName name of the toolbar defined in the framework.
 * @param {sync.api.Editor} editor The actions manager.
 */
function addOldStyleTableActions(actionsConfiguration, toolbarName, editor) {
  if (isFrameworkActions(actionsConfiguration, toolbarName)) {
    var join_action = [
      {"id": "table.join", "type": "action"}
    ];
    var split_action = [
      {"id": "table.split", "type": "action"}
    ];
    var row_actions = [
      {"id": "insert.table.row.above", "type": "action"},
      {"id": "insert.table.row.below", "type": "action"},
      {"id": "delete.table.row", "type": "action"}
    ];
    var column_actions = [
      {"id": "insert.table.column.before", "type": "action"},
      {"id": "insert.table.column.after", "type": "action"},
      {"id": "delete.table.column", "type": "action"}
    ];

    // Make table-related actions context-aware.
    [].concat(join_action, split_action, row_actions, column_actions).forEach(function(action) {
      sync.actions.TableAction.wrapTableAction(editor, action.id);
    });

    // Wrap the table split action
    var splitActionId = 'table.split';
    var originalSplitAction = editor.getActionsManager().getActionById(splitActionId);
    if (originalSplitAction) {
      var splitTableAction = new sync.actions.SplitTableCell(
        originalSplitAction,
        editor);
      editor.getActionsManager().registerAction(splitActionId, splitTableAction);
    }

    var contextualItems = actionsConfiguration.contextualItems;
    for (var i = 0; i < contextualItems.length; i++) {
      if (contextualItems[i].name === tr(msgs.TABLE_)) {
        var items = contextualItems[i].children;

        var row_actions_index = indexOfId(items, row_actions[2].id);
        goog.bind(items.splice, items, row_actions_index, 1).apply(items, row_actions);

        var column_actions_index = indexOfId(items, column_actions[2].id);
        goog.bind(items.splice, items, column_actions_index, 1).apply(items, column_actions);
        break;
      }
    }
  }
}

/**
 * @param {Array<{id:string}>} items The array of items.
 * @param {string} id The ID that we search for.
 * @return {number} The index of the element with the given ID.
 */
function indexOfId(items, id) {
  for (var i = 0; i < items.length; i++) {
    if (items[i].id === id) {
      return i;
    }
  }
  return -1;
}

/**
 * @param {object} actionsConfiguration The actions configuration.
 * @param {string} toolbarName name of the toolbar defined in the framework.
 *
 * @return {boolean} true if the actions loaded come from the framework.
 */
function isFrameworkActions(actionsConfiguration, toolbarName) {
  var toolbars = actionsConfiguration.toolbars;
  return toolbars && toolbars.length > 0 && toolbars[0].name == toolbarName;
}

// Publish the extension.
sync.ext.Registry.extension = new sync.xhtml.XhtmlExtension();