import { RawLocation } from "vue-router/types/router";
import { NavigationGuardNext, Route } from "vue-router";
import Vue from "vue";

export type NextPayload = RawLocation | false | void | ((vm: Vue) => void);
export type RouterCheck = (
  to: Route,
  from: Route,
  next: NavigationGuardNext
) => void;
