module.exports = {
  transpileDependencies: ["vuetify", "vuex-module-decorators"],
  pluginOptions: {
    electronBuilder: {
      nodeIntegration: true,
    },
  },
  lintOnSave: true,
};
