import uuid

import pike.ntstatus
import pike.smb2
import pytest


def validate_filename_support(char):
    spclchar = char.encode("utf-16", "surrogatepass").decode(
        "utf-16", "surrogatepass"
    )
    filename = f"test_io_{spclchar}_{uuid.uuid4()}.txt"
    return filename


@pytest.mark.parametrize(
    "char, description",
    [
        ("\ud83d\ude4f", "valid surrogate pairs"),
        ("\U0001F600", "32-bit character"),
        ("\uD83D", "high surrogate"),
        ("\uDC00", "low surrogate"),
        ("\u4F60\u597D", "BMP characters"),
    ],
)
def test_surrogate_filename_behavior(pike_TreeConnect, char, description):
    filename = validate_filename_support(char)
    try:
        with pike_TreeConnect() as tc:
            with tc.chan.create(
                tc.tree,
                filename,
                access=pike.smb2.GENERIC_READ
                | pike.smb2.GENERIC_WRITE
                | pike.smb2.DELETE,
            ).result() as fh:
                buf = "test123"
                tc.chan.write(fh, 0, buf)
                read_data = tc.chan.read(fh, len(buf), 0).tobytes().decode()
                assert (
                    read_data == buf
                ), f"Data mismatch: expected {buf}, got {read_data}"
    except Exception as e:
        pytest.fail(f"Unexpected error for filename '{filename}' with description '{description}': {e}")
