if(sync.ext.Registry.extension.type === 'dita') {
  sync.ext.Registry.extension.registerActionsHandler(function(editor, actionsConfig) {

    if (shouldInstallTableActions(actionsConfig)) {
      var actionsManager = editor.getActionsManager();
      addOldStyleTableActions(actionsConfig, actionsManager);
    }

    function addOldStyleTableActions(actionsConfiguration, actionsManager) {
      var split_join_actions = [
        {"id": "table.join.row.cells", "type": "action"},
        {"id": "table.join.cell.above", "type": "action"},
        {"id": "table.join.cell.below", "type": "action"},
        {"type": "sep"},
        {"id": "table.split.left", "type": "action"},
        {"id": "table.split.right", "type": "action"},
        {"id": "table.split.above", "type": "action"},
        {"id": "table.split.below", "type": "action"},
        {"type": "sep"}
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
      [].concat(split_join_actions, row_actions, column_actions).forEach(function(action) {
        sync.actions.TableAction.wrapTableAction(actionsManager, action.id);
      });

      actionsConfiguration.toolbars[0].children.push({
        "type": "list",
        "name": "Join or split table cells.",
        "displayName": tr(msgs.TABLE_JOIN_SPLIT_),
        "icon16": "/images/TableJoinSplit16.png",
        "icon20": "/images/TableJoinSplit24.png",
        "children": split_join_actions
      });

      var contextualItems = actionsConfiguration.contextualItems;
      for (var i = 0; i < contextualItems.length; i++) {
        if (contextualItems[i].name === "Table") {
          var items = contextualItems[i].children;
          Array.prototype.push.apply(items, split_join_actions);

          var row_actions_index = indexOfId(items, row_actions[2].id);
          goog.bind(items.splice, items, row_actions_index, 1).apply(items, row_actions);

          var column_actions_index = indexOfId(items, column_actions[2].id);
          goog.bind(items.splice, items, column_actions_index, 1).apply(items, column_actions);
          break;
        }
      }
    };

    function shouldInstallTableActions(actionsConfiguration) {
      var toolbars = actionsConfiguration.toolbars;
      if (toolbars && toolbars.length > 0 && toolbars[0].name == "DITA") {
        var items = toolbars[0].children;
        return indexOfId(items, 'table.join') != -1;
      }
      return false;
    };

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
  });
}