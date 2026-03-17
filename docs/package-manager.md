# Package Manager (mkpkg)

`mkpkg` installs and removes `.mkpkg` packages and tracks them in a local database.

## Package Format
```
package.mkpkg
├── metadata.json
├── files/
└── install.sh (optional)
```

## Database
- Default database: `/var/lib/mkpkg`
- Cache: `/var/cache/mkpkg`
- Repo config: `/etc/mkpkg/repos.conf`

## Commands
- `mkpkg install <pkg|path.mkpkg>`
- `mkpkg remove <pkg>`
- `mkpkg update`
- `mkpkg search <term>`
- `mkpkg list`

## Target Root Install
To install into a mounted target root (e.g. during installation):
```
mkpkg --root /mnt install <pkg>
```

## Repo Configuration
`/etc/mkpkg/repos.conf` should list local repo paths, one per line:
```
/repo/core
/repo/extra
/repo/community
```

## Troubleshooting
- Missing package: verify `.mkpkg` exists in repo paths.
- Corrupt package: rebuild with `mkbuild` and re-publish.
- Files missing: reinstall the package.
