goog.provide('sync.dita.DitaExtension');

/**
 * Constructor for the DITA Extension.
 *
 * @constructor
 */
sync.dita.DitaExtension = function() {
  sync.ext.Extension.call(this);

  this.type = sync.ext.Registry.extensionURL.indexOf("ditamap") != -1 ? 'ditamap' : 'dita';

  this.actionsHandlers = [];
};
goog.inherits(sync.dita.DitaExtension, sync.ext.Extension);


sync.dita.DitaExtension.prototype.registerActionsHandler = function(handler) {
  this.actionsHandlers.push(handler);
};


/**
 * Editor created callback.
 *
 * @param {sync.Editor} editor The currently created editor.
 */
sync.dita.DitaExtension.prototype.editorCreated = function(editor) {
  // Listening on capture so we can add actions to the toolbar before
  // plugins have a chance to remove actions.
  goog.events.listen(editor, sync.api.Editor.EventTypes.ACTIONS_LOADED, goog.bind(function(e) {
    var i;
    for(i = 0; i < this.actionsHandlers.length; i++) {
      this.actionsHandlers[i](editor, e.actionsConfiguration);
    }
  }, this), true);

  if(this.type === 'ditamap') {
    // Override the open link action to provide the current ditamap as a param.
    goog.events.listen(editor, sync.api.Editor.EventTypes.LINK_OPENED, function(e) {
      if (! e.external) {
        var urlParams = sync.util.getApiParams();
        if (! urlParams.ditamap) {
          e.params['ditamap'] = editor.options.url;
        } else {
          // If the ditamap is already specified, it means that the current map is a
          // sub-map and the links must be opened in the context of the parent map.
        }
      }
    }, true);
  }
};

