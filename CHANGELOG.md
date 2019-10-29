# Changelog

## 1.4.1
[Full Changelog](https://github.com/richtier/alexa-browser-client/pull/25)

### Implemented enhancements
- Simplified makefile. Use direct `flake8` and `pytest` commands instead of  `make lint` and `make test`.
- Add CHANGELOG.md

### Fixed bugs
- Upgrade alexa-voice-service-client to fix synchronise device state bug
- Added button to demo to prevent chrome blocking audio interaction
- Update tests to facilitate upgrading asgiref
