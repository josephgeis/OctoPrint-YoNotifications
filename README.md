# OctoPrint-YoNotifications

Send OctoPrint Notifications using Yo.

## Setup

Install via the bundled [Plugin Manager](https://github.com/foosel/OctoPrint/wiki/Plugin:-Plugin-Manager)
or manually using this URL:

    https://github.com/juniorrubyist/OctoPrint-YoNotifications/archive/master.zip

## Configuration

**TODO:**

```yaml
yonotifier:
  apiKey: xxxxxxx
  [Event]:
    enabled: true
    message: An event happened. {{ parameter }}
  username: MYUSERNAME
```

<<<<<<< HEAD
- `apiKey` - Your API Key found on [Yo Dashboard](https://dashboard.justyo.co/).
- `[Event]` - Replace with event name found in [OctoPrint Docs](http://docs.octoprint.org/en/master/events/index.html#available-events).
- `enabled` - Whether to use this event or not (`true` or `false`).
- `username` - Your Yo username.
=======
`apiKey` - Your API Key found on [Yo Dashboard](https://dashboard.justyo.co/).
`[Event]` - Replace with event name found in [OctoPrint Docs](http://docs.octoprint.org/en/master/events/index.html#available-events).
`enabled` - Whether to use this event or not (`true` or `false`).
`username` - Your Yo username.
>>>>>>> 2a6e6ca8124b00eadb042390c7420ab181a93d32
