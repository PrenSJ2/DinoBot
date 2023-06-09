const { App, LogLevel } = require("@slack/bolt");
const { registerListeners } = require("./listeners");

const { FileInstallationStore } = require('@slack/oauth');
const app = new App({
  appToken: process.env.SLACK_APP_TOKEN,
  signingSecret: process.env.SLACK_SIGNING_SECRET,
  clientId: process.env.SLACK_CLIENT_ID,
  clientSecret: process.env.SLACK_CLIENT_SECRET,
  stateSecret: 'my-state-secret',
  scopes: ['commands', 'users:read'],
  installationStore: new FileInstallationStore(),
  // socketMode: true,
});

/** Register Listeners */
registerListeners(app);

(async () => {
  // Start your app
  console.log("PORT", process.env.PORT);
  await app.start(process.env.PORT || 3000);
  console.log('⚡️ DinoBot app is running!');
})();
