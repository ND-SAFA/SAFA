module.exports = {
  transpileDependencies: ["vuetify", "vuex-module-decorators", "vuex-persist"],
  pluginOptions: {
    electronBuilder: {
      nodeIntegration: true,
    },
  },
  lintOnSave: true,
};
