const { appHomeOpenedCallback } = require('./app-home-opened');
const { userHuddleChanged } = require('./user-huddle-changed');

module.exports.register = (app) => {
  app.event('app_home_opened', appHomeOpenedCallback);
  app.event('user_huddle_changed', userHuddleChanged);
};
