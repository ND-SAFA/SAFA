<template>
  <v-container>
    <h1 class="text-h4 my-2">Notation Key</h1>
    <v-container>
      <p>General Safety Tree Notation</p>
      <p>
        Represents a raw artifact retrieved from the project repository, e.g.,
        hazard, requirements, or test case.
      </p>
      <p>
        Represents a package retrieved from the project repository that contains
        source code.
      </p>
      <p>
        Warns that a type of element is completely missing. Can be egregious or
        nuanced.
      </p>
      <p>Delta Tree Notation</p>
      <p>No change across versions.</p>
      <p>Added to current version.</p>
      <p>Existed in baseline version; deleted from current version.</p>
      <p>Existed in baseline version; <b>modified</b> in current version.</p>
    </v-container>
  </v-container>
</template>
