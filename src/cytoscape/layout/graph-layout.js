"use strict";
exports.__esModule = true;
/**
 * Defines a graph layout.
 */
var GraphLayout = /** @class */ (function () {
    function GraphLayout(autoMoveHandlers, cytoEventHandlers, layoutTemplate, preLayoutHooks, postLayoutHooks) {
        this.klaySettings = layoutTemplate;
        this.preLayoutHooks = preLayoutHooks;
        this.postLayoutHooks = postLayoutHooks;
        this.autoMoveHandlers = autoMoveHandlers;
        this.cytoEventHandlers = cytoEventHandlers;
        this.autoMoveHandlers = autoMoveHandlers;
    }
    /**
     * Creates the layout.
     *
     * @param cy - The cy instance.
     */
    GraphLayout.prototype.createLayout = function (cy) {
        this.preLayoutHook(cy);
        cy.layout({
            name: "klay",
            klay: this.klaySettings
        }).run();
        this.postLayoutHook(cy);
    };
    /**
     * Runs pre-layout hooks.
     *
     * @param cy - The cy instance.
     */
    GraphLayout.prototype.preLayoutHook = function (cy) {
        for (var _i = 0, _a = this.preLayoutHooks; _i < _a.length; _i++) {
            var preHook = _a[_i];
            preHook(cy, this);
        }
    };
    /**
     * Runs post-layout hooks.
     *
     * @param cy - The cy instance.
     */
    GraphLayout.prototype.postLayoutHook = function (cy) {
        for (var _i = 0, _a = this.postLayoutHooks; _i < _a.length; _i++) {
            var postHook = _a[_i];
            postHook(cy, this);
        }
    };
    return GraphLayout;
}());
exports["default"] = GraphLayout;
