# clients/

Each client organization gets its own folder here, created by the `/new-client` workflow:

```
clients/
├── ACTIVE                  <- one line: the slug of the client being worked on
├── acme-logistics/
│   ├── profile.md
│   ├── data/
│   └── outputs/
│       ├── decision-log.md
│       └── reports/
└── another-client/
```

Use `/switch-client` to change the active client.

**Everything in this folder except this README is excluded from Git** (see `.gitignore`). Client information is confidential, so do not remove that rule.
