#!/usr/bin/env python3
"""Export Synology libata callbacks used by the modular sata_sil24 driver."""

from pathlib import Path


source = Path("drivers/ata/libata-scsi.c")
data = source.read_text()
for signature, symbol in (
    ("void syno_libata_device_list_set(", "syno_libata_device_list_set"),
    ("int syno_libata_disk_power_loss_when_reboot(", "syno_libata_disk_power_loss_when_reboot"),
):
    if data.count(signature) != 1:
        raise SystemExit(f"Expected one definition of {symbol}")
    start = data.index(signature)
    opening = data.index("{", start)
    depth = 0
    for pos in range(opening, len(data)):
        if data[pos] == "{":
            depth += 1
        elif data[pos] == "}":
            depth -= 1
            if depth == 0:
                break
    else:
        raise SystemExit(f"Could not find end of {symbol}")
    export = f"\nEXPORT_SYMBOL_GPL({symbol});"
    if export not in data:
        data = data[: pos + 1] + export + data[pos + 1 :]

source.write_text(data)
