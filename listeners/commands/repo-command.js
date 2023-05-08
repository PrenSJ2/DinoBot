const axios = require('axios');

const reposCommandCallback = async ({ ack, respond }) => {
  try {
    await ack();

    // Your code
    const repositories = [
      {
        name: 'TC-api-docs',
        link: 'https://github.com/tutorcruncher/tc-api-docs',
        caretaker: 'Seb',
      },
      {
        name: 'Socket-frontend',
        link: 'https://github.com/tutorcruncher/socket-frontend',
        caretaker: 'Seb',
      },
      {
        name: 'Socket-server',
        link: 'https://github.com/tutorcruncher/socket-server',
        caretaker: 'Seb',
      },
      {
        name: 'uk-postcode-api',
        link: 'https://github.com/tutorcruncher/uk-postcode-api',
        caretaker: 'Seb',
      },
      {
        name: 'TC-imports',
        link: 'https://github.com/tutorcruncher/tc-imports',
        caretaker: 'Dan',
      },
      {
        name: 'TCIntercom',
        link: 'https://github.com/tutorcruncher/TCIntercom',
        caretaker: 'Dan',
      },
      {
        name: 'Static-maps',
        link: 'https://github.com/tutorcruncher/static-maps',
        caretaker: 'Dan',
      },
      {
        name: 'TC-virus-checker',
        link: 'https://github.com/tutorcruncher/tc-virus-checker',
        caretaker: 'Dan',
      },
      {
        name: 'hermes',
        link: 'https://github.com/tutorcruncher/hermes',
        caretaker: 'Henty',
      },
      {
        name: 'Morpheus',
        link: 'https://github.com/tutorcruncher/morpheus',
        caretaker: 'Henty',
      },
    ];

    let formattedMessage = '';

    for (const repo of repositories) {
      const repo_name = repo.name;
      const repo_link = repo.link;
      const repo_caretaker = repo.caretaker;

      // Fetch open pull requests from GitHub API
      const pull_requests_url = `https://api.github.com/repos/tutorcruncher/${repo_name}/pulls?state=open`;
      const headers = { Authorization: `Bearer ${process.env.GITHUB_TOKEN}` };
      let pull_requests_count = 0;
      try {
        const pull_requests_response = await axios.get(pull_requests_url, { headers });
        pull_requests_count = pull_requests_response.data.length;
      } catch (error) {
        console.error(error);
      }

      // Fetch last release information
      const releases_url = `https://api.github.com/repos/tutorcruncher/${repo_name}/releases`;
      let last_release_date = 'No releases found';
      try {
        const releases_response = await axios.get(releases_url, { headers });
        const releases = releases_response.data;
        if (releases.length > 0) {
          const last_release = releases[0];
          last_release_date = last_release.published_at.slice(0, 10);
        }
      } catch (error) {
        console.error(error);
      }


      // Format the message for the current repository
      const table = [
        {
          field: 'Link',
          value: repo_link,
        },
        {
          field: 'Open Pull Requests',
          value: pull_requests_count.toString(),
        },
        {
          field: 'Last Release Date',
          value: last_release_date,
        },
        {
          field: 'Caretaker',
          value: repo_caretaker,
        },
      ];

      const formattedTable = table.map(({ field, value }) => `*${field}:* ${value}`).join('\n');

      formattedMessage += `*Repository: ${repo_name}*\n`
        + `${formattedTable}\n\n`;
    }

    await respond({
      text: formattedMessage,
      response_type: 'in_channel',
    });
  } catch (error) {
    console.error(error);
  }
};

module.exports = { reposCommandCallback };
