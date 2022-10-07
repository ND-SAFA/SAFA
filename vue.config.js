// eslint-disable-next-line @typescript-eslint/no-var-requires
const fs = require("fs");

module.exports = {
  transpileDependencies: ["vuetify"],
  pluginOptions: {
    electronBuilder: {
      nodeIntegration: true,
    },
  },
  lintOnSave: true,
  devServer: fs.existsSync("./certs/localhost.safa.ai.pem")
    ? {
        https: {
          key: fs.readFileSync("./certs/localhost.safa.ai-key.pem"),
          cert: fs.readFileSync("./certs/localhost.safa.ai.pem"),
        },
        host: "localhost.safa.ai",
        port: 8080,
      }
    : {},
};
