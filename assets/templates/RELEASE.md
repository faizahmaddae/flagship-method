# RELEASE — building and proving a {{PROJECT_NAME}} release

<!-- if:release -->
The procedure for making the artefacts a store would take, and proving they are right, on
{{PLATFORMS}}.

**Nothing here sends anything to a store.** An upload of any kind, a test track included, happens
only when {{OWNER}} explicitly asks for that specific upload. Submission for review or release to
the public comes only after their own device test of the exact build and their explicit approval.
This document ends at verified artefacts and the facts the owner needs to decide.

<!-- flagship-method template (optional doc). Content and checklists:
flagship-method references/release-and-store.md. Tool versions, store specs and platform behaviour
are volatile: keep them in dated blocks and re-verify. Never put a secret, keystore password or
production id in this file; name the gitignored file that holds it. At kickoff, fill what is
decided; every slot only a later phase can fill gets one line instead of a guess: "Written in Phase
<n.m>; decided so far: <…>" (references/project-kit.md §12). -->

## 0. What must exist first (the owner's; PROGRESS "END-OF-PROJECT LIST")

| Input | Where | Without it |
|---|---|---|
| [TODO: e.g. production app and service ids] | [TODO: gitignored env file; `cp <file>.example <file>`] | [TODO: the build carries sample ids, and the verifier refuses it] |
| [TODO: the signing key] | [TODO: gitignored; the owner's] | [TODO: the release falls back to a debug key, and the verifier refuses it] |
| [TODO: the backend config] | [TODO: where] | [TODO: what the verifier does] |

## 1. Baseline (the tree must be green)

```bash
[TODO: every selftest, analysis, the full test suite, and the verifier's and the run gate's own selftests]
```

## 2. Regenerate the platform folders and set the version

```bash
[TODO: setup script]        # writes the real ids from the env files; twice is byte-identical
# version: <name>+<build>   (the owner's numbers: never invented, never reused)
```

## 3. [TODO: platform A]

1. Build with the release flags: [TODO: command].
2. The static verifier: [TODO: command] must print "Ready to upload". It checks ids, signatures,
   merged permissions, entitlements, configs and stamps.
3. The run gate on the exact artefact that uploads: [TODO: command]. Fresh install, version read back
   from the device, cold start, the first screen's main control present within 30 s, N units used,
   a health check after each stage.
4. The review notes: [TODO: where they live; the verifier prints them]. If users can create
   accounts, the notes say where in-app account deletion is.

## 4. [TODO: platform B]

[TODO: the same steps. Where no tool can start a release build, compare the privacy report from the
signed archive with the label, and say so in §5.]

## 5. What a passing run does NOT prove

<!-- Write the blind spots of every gate here; the owner's device test covers exactly this list.
Examples of the kind: a release build that no tool here could start; purchases run without a store
account (the billing connection merely did not crash); a gate that stops before the first ad
appears; a preview check that verifies the file's format, not what it shows. -->

- [TODO: each blind spot, and the device check that covers it]

## 6. Reference numbers

> **Dated facts (as of [TODO: date], commit [TODO: hash] — re-measure on change):** [TODO: artefact
> sizes, one-device download size, cold start (first install and warm), the privacy manifests found
> in the bundle.]

## 7. Side effects of a release build

<!-- What talks to real services (symbol or mapping uploads, crash reports, analytics), and how each
is gated: on the real signing key or an archive build, never on a debug-signed test build. Give a
command that proves the gate (a dry run that shows no upload task). -->

- [TODO: each side effect, its gate, and the command that proves the gate]

## 8. The store folder (`docs/{{SLUG}}/store/`, written in Phase 5)

<!-- Shapes and checks: flagship-method references/release-and-store.md §5 and §7. Every reason
stated in these files is checked against the code. -->

| Path | Holds | Checked by |
|---|---|---|
| `store/text/<store>/` | every store-visible text, one file each, exactly as pasted | [TODO: the copy checker: lengths, registry equals the files on disk] |
| `store/LISTING.md` | the claim table (every claim mapped to code) and the length table | [TODO: the copy checker] |
| `store/RATINGS.md` | each questionnaire answer with the code that justifies it; the computed rating | [TODO: re-checked at every release, dated] |
| `store/PRIVACY_ANSWERS.md` | the privacy label and data-safety answers per data type, from every SDK's disclosure and the privacy decisions | [TODO: compared with the manifests in the built artefact] |

Screenshots are generated from the real app by [TODO: command], twice byte-identical; the preview
video is re-recorded whenever the visuals change; the fallback set (icon and first screenshot) is
kept beside them.
<!-- /if:release -->
