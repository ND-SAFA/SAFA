import {
  _GettersTree,
  defineStore,
  DefineStoreOptions,
  StateTree,
} from "pinia";

/**
 * Curries the creation of a store so that it can be used locally in multiple places.
 *
 * @param store - The store configuration to create.
 * @return A function that converts an id into a unique store instance (assuming the id itself is not used elsewhere).
 */
export function createLocalStore<
  Id extends string,
  S extends StateTree = Record<string, unknown>,
  G extends _GettersTree<S> = Record<string, never>,
  A = Record<string, unknown>
>(store: Omit<DefineStoreOptions<Id, S, G, A>, "id">) {
  // eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
  return (id: Id) => defineStore(id, store);
}
