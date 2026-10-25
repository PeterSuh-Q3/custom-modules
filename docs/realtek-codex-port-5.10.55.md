# Realtek Codex port for Synology Linux 5.10.55

## Scope

The port candidate branches apply the Realtek source from the `mshell-modules` 5.10.55 tree to these ten Synology platform/DSM targets:

- EPYC7002: DSM 7.3 and 7.4
- Gemini Lake: DSM 7.3 and 7.4
- R1000: DSM 7.3 and 7.4
- V1000: DSM 7.3 and 7.4
- EPYC7003: DSM 7.4
- Ice Lake: DSM 7.4

The ten source branches had identical Realtek source blobs and build Makefiles before this port. The port therefore uses common driver code and stamps `pilot_target` with the exact platform/DSM/kernel tuple in each candidate branch.

## Applied source

- PCIe drivers: `r8125`, `r8126`, `r8127`, and `r8168`, including the existing `_txrx` / `_tx` variants, source metadata, and the bounded `r8168_tx` recovery logic.
- USB: Realtek `r8152` v2.22.1 source and its 5.10.55 compatibility header.
- `distributor=PeterSuh-Q3` and build revision metadata are embedded in the modules. This is module identification metadata, not cryptographic signing.

The port preserves the Synology source-tree Makefiles, Kconfig symbols, module names, aliases and packaging paths. It does not modify `r8169`, kernel-wide configuration, EEE defaults, or WOL defaults. The `r8168_tx` recovery remains limited to TX-timeout requests, capped at three requests per ten-minute window; it does not promise recovery from a carrier-only loss or change WOL behavior.

`r8153_ecm` is excluded: none of the ten target Kconfig trees declares `CONFIG_USB_RTL8153_ECM`. Adding a second USB driver and a new Kconfig/build path would change binding behavior and needs a separate review.

## Candidate branches

Each platform source candidate is named `codex/realtek-<platform>-<DSM>-5.10.55`. `codex/realtek-build-workflow` updates the all-platform workflow to check out that source branch before compiling. The original platform refs remain unchanged.

## Validation status

Source-tree validation confirms all ten candidates are based on their matching Synology branch, retain pre-existing file modes and build Makefiles, contain the platform-specific metadata, and include the same driver implementation. Whitespace checks pass. The full ten-target kernel/module builds and live module load tests have not yet run; compilation against each Synology configuration, `modpost`, package inspection (`modinfo`, aliases, dependencies, vermagic), and staged DSM runtime tests remain required before promotion.
