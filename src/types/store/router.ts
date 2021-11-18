import { RawLocation } from "vue-router/types/router";
import { NavigationGuardNext, Route } from "vue-router";

export type NextPayload = RawLocation | false | void | ((vm: Vue) => any);
export type RouterCheck = (
  to: Route,
  from: Route,
  next: NavigationGuardNext
) => void;
