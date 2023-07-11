const userHuddleChanged = async ({ event, say }) => {
  try {
    // Send a message to the user who has been sent a huddle
    await say({
      channel: event.user, // This is the ID of the user who has been sent a huddle
      text: "You have been sent a huddle.",
    });
  } catch (error) {
    console.log(error);
  }
};
