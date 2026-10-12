# Scene asset registry

Only asset metadata records belong in this directory; do not commit large source media or model files here by default. Keep those on the approved data lake and retain a relative path, source locator, checksum, transformations, rights decision, attribution, reviewer, and verification date in the asset record.

Schema: `../schemas/asset-v0.schema.json`.

An asset is selectable by the historical-state resolver only when:
- its record ID matches the state reference;
- its SHA-256 contains exactly 64 hexadecimal characters;
- `verification_status=VERIFIED`, with reviewer and date;
- `rights_status=CLEARED`, an explicit `license_id`, and attribution text;
- its source registry record has status `REVIEWED` or `RIGHTS_CLEARED`, and explicitly states both `redistribution_allowed=Yes` and `commercial_use=Yes`.

This is a conservative project policy, not a legal conclusion. Only set `CLEARED` after reviewing the actual item-specific licence/permission and intended uses. A public URL or a file that downloads successfully is not rights clearance.

No production scene asset is registered yet.
