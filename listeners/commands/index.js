const { reposCommandCallback } = require('./repo-command');

module.exports.register = (app) => {
  app.command('/repos', reposCommandCallback);
};
