"use strict";
var __extends = (this && this.__extends) || (function () {
    var extendStatics = function (d, b) {
        extendStatics = Object.setPrototypeOf ||
            ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
            function (d, b) { for (var p in b) if (Object.prototype.hasOwnProperty.call(b, p)) d[p] = b[p]; };
        return extendStatics(d, b);
    };
    return function (d, b) {
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
exports.__esModule = true;
var vuex_module_decorators_1 = require("vuex-module-decorators");
var JobModule = /** @class */ (function (_super) {
    __extends(JobModule, _super);
    /**
     * This module tracks the jobs submitted by the user.
     */
    function JobModule() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        /**
         * The list of user jobs.
         */
        _this.jobs = [];
        /**
         * The index of the selected job.
         */
        _this.selectedJob = -1;
        return _this;
    }
    /**
     * Adds job to list of jobs if new job, otherwise updates previous one.
     */
    JobModule.prototype.addOrUpdateJob = function (job) {
        var newJobs = this.jobs.filter(function (j) { return j.id !== job.id; }).concat([job]);
        this.SET_JOBS(newJobs);
    };
    /**
     * Selects the given job if exists in jobs.
     */
    JobModule.prototype.selectJob = function (job) {
        var _this = this;
        this.jobs.forEach(function (j, i) {
            if (j.id === job.id) {
                _this.SET_SELECT_JOB_INDEX(i);
            }
        });
    };
    /**
     * Removes job matching id of given job.
     */
    JobModule.prototype.deleteJob = function (job) {
        var _this = this;
        this.SET_SELECT_JOB_INDEX(-1);
        setTimeout(function () {
            _this.SET_JOBS(_this.jobs.filter(function (j) { return j.id != job.id; }));
        }, 500);
    };
    /**
     * Sets the current user's jobs.
     */
    JobModule.prototype.SET_JOBS = function (jobs) {
        this.jobs = jobs;
    };
    /**
     * Sets the currently selected job index, otherwise -1.
     */
    JobModule.prototype.SET_SELECT_JOB_INDEX = function (index) {
        this.selectedJob = index;
    };
    Object.defineProperty(JobModule.prototype, "getJob", {
        /**
         * @returns The job with given id.
         */
        get: function () {
            var _this = this;
            return function (jobId) {
                return _this.jobs.filter(function (j) { return j.id === jobId; })[0];
            };
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(JobModule.prototype, "currentJobs", {
        /**
         * @returns All current jobs.
         */
        get: function () {
            return this.jobs;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(JobModule.prototype, "selectedJobIndex", {
        /**
         * @returns The index of the selected job.
         */
        get: function () {
            return this.selectedJob;
        },
        enumerable: false,
        configurable: true
    });
    __decorate([
        vuex_module_decorators_1.Action
    ], JobModule.prototype, "addOrUpdateJob");
    __decorate([
        vuex_module_decorators_1.Action
    ], JobModule.prototype, "selectJob");
    __decorate([
        vuex_module_decorators_1.Action
    ], JobModule.prototype, "deleteJob");
    __decorate([
        vuex_module_decorators_1.Mutation
    ], JobModule.prototype, "SET_JOBS");
    __decorate([
        vuex_module_decorators_1.Mutation
    ], JobModule.prototype, "SET_SELECT_JOB_INDEX");
    JobModule = __decorate([
        vuex_module_decorators_1.Module({ namespaced: true, name: "job" })
        /**
         * This module tracks the jobs submitted by the user.
         */
    ], JobModule);
    return JobModule;
}(vuex_module_decorators_1.VuexModule));
exports["default"] = JobModule;
