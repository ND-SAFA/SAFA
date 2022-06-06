"use strict";
exports.__esModule = true;
exports.jobModule = exports.typeOptionsModule = exports.subtreeModule = exports.commitModule = exports.viewportModule = exports.deltaModule = exports.artifactSelectionModule = exports.traceModule = exports.artifactModule = exports.documentModule = exports.projectModule = exports.errorModule = exports.sessionModule = exports.logModule = exports.appModule = void 0;
var vue_1 = require("vue");
var vuex_1 = require("vuex");
var vuex_module_decorators_1 = require("vuex-module-decorators");
var vuex_persist_1 = require("@/plugins/vuex-persist");
var modules_1 = require("./modules");
vue_1["default"].use(vuex_1["default"]);
vue_1["default"].config.devtools = true;
var store = new vuex_1["default"].Store({
    mutations: {},
    actions: {},
    modules: {
        session: modules_1.SessionModule,
        app: modules_1.AppModule,
        project: modules_1.ProjectModule,
        document: modules_1.DocumentModule,
        artifact: modules_1.ArtifactModule,
        trace: modules_1.TraceModule,
        delta: modules_1.DeltaModule,
        warning: modules_1.ErrorModule,
        typeOptions: modules_1.TypeOptionsModule,
        artifactSelection: modules_1.ArtifactSelectionModule,
        viewport: modules_1.ViewportModule,
        commit: modules_1.CommitModule,
        subtree: modules_1.SubtreeModule,
        snackbar: modules_1.SnackbarModule,
        job: modules_1.JobModule
    },
    plugins: [vuex_persist_1.vuexLocal.plugin]
});
exports.appModule = vuex_module_decorators_1.getModule(modules_1.AppModule, store);
exports.logModule = vuex_module_decorators_1.getModule(modules_1.SnackbarModule, store);
exports.sessionModule = vuex_module_decorators_1.getModule(modules_1.SessionModule, store);
exports.errorModule = vuex_module_decorators_1.getModule(modules_1.ErrorModule, store);
exports.projectModule = vuex_module_decorators_1.getModule(modules_1.ProjectModule, store);
exports.documentModule = vuex_module_decorators_1.getModule(modules_1.DocumentModule, store);
exports.artifactModule = vuex_module_decorators_1.getModule(modules_1.ArtifactModule, store);
exports.traceModule = vuex_module_decorators_1.getModule(modules_1.TraceModule, store);
exports.artifactSelectionModule = vuex_module_decorators_1.getModule(modules_1.ArtifactSelectionModule, store);
exports.deltaModule = vuex_module_decorators_1.getModule(modules_1.DeltaModule, store);
exports.viewportModule = vuex_module_decorators_1.getModule(modules_1.ViewportModule, store);
exports.commitModule = vuex_module_decorators_1.getModule(modules_1.CommitModule, store);
exports.subtreeModule = vuex_module_decorators_1.getModule(modules_1.SubtreeModule, store);
exports.typeOptionsModule = vuex_module_decorators_1.getModule(modules_1.TypeOptionsModule, store);
exports.jobModule = vuex_module_decorators_1.getModule(modules_1.JobModule, store);
exports["default"] = store;
