"""Run: python3 -m unittest discover -s tests -v"""
import importlib.util
from pathlib import Path
import struct
import tempfile
import unittest

script = Path(__file__).resolve().parents[1] / "scripts" / "check_artwork.py"
spec = importlib.util.spec_from_file_location("check_artwork", script)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class ArtworkInspectionTests(unittest.TestCase):
    def test_png_dimensions(self):
        png = b"\x89PNG\r\n\x1a\n" + b"\x00\x00\x00\rIHDR" + struct.pack(">II", 1200, 1200) + b"\x08\x02\x00\x00\x00"
        self.assertEqual(module.identify_image(png), ("PNG", 1200, 1200))

    def test_gif_dimensions(self):
        gif = b"GIF89a" + struct.pack("<HH", 500, 500) + b"\x00\x00\x00"
        self.assertEqual(module.identify_image(gif), ("GIF", 500, 500))

    def test_jpeg_dimensions(self):
        jpg = b"\xff\xd8\xff\xc0\x00\x11\x08" + struct.pack(">HH", 400, 600) + b"\x03" + b"\x00" * 9
        self.assertEqual(module.identify_image(jpg), ("JPEG", 600, 400))

    def test_reject_unknown(self):
        with self.assertRaisesRegex(ValueError, "unrecognized"):
            module.identify_image(b"not an image")

    def test_reject_truncated(self):
        for broken in (b"\x89PNG\r\n\x1a\n", b"GIF89a", b"\xff\xd8\xff\xc0"):
            with self.subTest(broken=broken), self.assertRaises(ValueError):
                module.identify_image(broken)

    def test_inspect_file(self):
        gif = b"GIF89a" + struct.pack("<HH", 320, 240) + b"\x00\x00\x00"
        with tempfile.TemporaryDirectory() as tmp:
            file = Path(tmp) / "sample.gif"
            file.write_bytes(gif)
            props = module.inspect(file)
            self.assertEqual(props["size_bytes"], len(gif))
            self.assertEqual(props["format"], "GIF")
            self.assertEqual(props["width"], 320)


if __name__ == "__main__":
    unittest.main()
