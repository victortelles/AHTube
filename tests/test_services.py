import io
import os
import shutil
import tempfile
import unittest
from unittest.mock import patch, MagicMock
from PIL import Image

from src.services.extractor import (
    resolve_ffmpeg_path,
    fetch_video_metadata,
    extract_media,
    list_downloaded_files,
)
from src.services.image_converter import (
    get_image_info,
    prepare_image_for_format,
    convert_single_image,
    batch_convert,
    create_zip_archive,
    scan_image_directory,
    list_converted_images,
)
from src.services.explorer import open_folder_in_foreground
from src.ui.primitives import get_badge_html

class TestImageConverterService(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        # Create a sample test PNG in memory
        img = Image.new("RGBA", (64, 64), color=(255, 0, 0, 128))
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        self.sample_png_bytes = buf.getvalue()
        
        # Save sample file to disk
        self.sample_png_path = os.path.join(self.temp_dir, "test_sample.png")
        with open(self.sample_png_path, "wb") as f:
            f.write(self.sample_png_bytes)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_get_image_info_bytes(self):
        info = get_image_info(self.sample_png_bytes)
        self.assertIsNotNone(info)
        self.assertEqual(info["format"], "PNG")
        self.assertEqual(info["width"], 64)
        self.assertEqual(info["height"], 64)
        self.assertEqual(info["mode"], "RGBA")
        self.assertGreater(info["size_kb"], 0)

    def test_get_image_info_file_path(self):
        info = get_image_info(self.sample_png_path)
        self.assertIsNotNone(info)
        self.assertEqual(info["format"], "PNG")
        self.assertEqual(info["width"], 64)

    def test_get_image_info_invalid(self):
        info = get_image_info(b"not_an_image_data")
        self.assertIsNone(info)

    def test_prepare_image_for_format_flatten_alpha(self):
        img = Image.new("RGBA", (10, 10), (0, 255, 0, 128))
        prepared = prepare_image_for_format(img, "JPEG")
        self.assertEqual(prepared.mode, "RGB")

    def test_prepare_image_for_format_ico(self):
        img = Image.new("RGBA", (300, 300), (0, 0, 255, 255))
        prepared = prepare_image_for_format(img, "ICO")
        self.assertLessEqual(prepared.width, 256)
        self.assertLessEqual(prepared.height, 256)

    def test_convert_single_image_in_memory(self):
        success, result_bytes = convert_single_image(
            input_source=self.sample_png_bytes,
            target_format="WEBP",
            quality=80
        )
        self.assertTrue(success)
        self.assertIsInstance(result_bytes, bytes)
        self.assertGreater(len(result_bytes), 0)

    def test_convert_single_image_to_file(self):
        dest_path = os.path.join(self.temp_dir, "output.jpg")
        success, result_path = convert_single_image(
            input_source=self.sample_png_bytes,
            target_format="JPEG",
            output_path=dest_path,
            quality=85
        )
        self.assertTrue(success)
        self.assertEqual(result_path, dest_path)
        self.assertTrue(os.path.exists(dest_path))

    def test_convert_single_image_invalid_source(self):
        success, err = convert_single_image(
            input_source=b"corrupted",
            target_format="PNG"
        )
        self.assertFalse(success)
        self.assertIsInstance(err, str)

    def test_batch_convert(self):
        out_dir = os.path.join(self.temp_dir, "batch_out")
        items = [
            {"name": "test1.png", "source": self.sample_png_bytes},
            {"name": "test2.png", "source": self.sample_png_bytes},
        ]
        result = batch_convert(
            items=items,
            target_format="WEBP",
            output_dir=out_dir,
            quality=90
        )
        self.assertEqual(result["total"], 2)
        self.assertEqual(result["successful_count"], 2)
        self.assertEqual(result["failed_count"], 0)
        self.assertEqual(len(result["successful_files"]), 2)

    def test_scan_image_directory(self):
        images = scan_image_directory(self.temp_dir)
        self.assertGreaterEqual(len(images), 1)
        self.assertEqual(images[0]["name"], "test_sample.png")

    def test_list_converted_images(self):
        images = list_converted_images(self.temp_dir)
        self.assertGreaterEqual(len(images), 1)

    def test_create_zip_archive(self):
        zip_bytes = create_zip_archive([self.sample_png_path])
        self.assertIsInstance(zip_bytes, bytes)
        self.assertGreater(len(zip_bytes), 0)

class TestExtractorService(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        # Create dummy media files
        self.dummy_mp3 = os.path.join(self.temp_dir, "song.mp3")
        with open(self.dummy_mp3, "wb") as f:
            f.write(b"ID3" + b"\x00" * 1024)
            
        self.dummy_mp4 = os.path.join(self.temp_dir, "video.mp4")
        with open(self.dummy_mp4, "wb") as f:
            f.write(b"\x00" * 2048)
            
        self.dummy_txt = os.path.join(self.temp_dir, "readme.txt")
        with open(self.dummy_txt, "w", encoding="utf-8") as f:
            f.write("ignore me")

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_resolve_ffmpeg_path(self):
        # Should not raise exception
        result = resolve_ffmpeg_path()
        self.assertTrue(result is None or isinstance(result, str))

    def test_list_downloaded_files(self):
        files = list_downloaded_files(self.temp_dir)
        self.assertEqual(len(files), 2)
        names = [f["name"] for f in files]
        self.assertIn("song.mp3", names)
        self.assertIn("video.mp4", names)
        self.assertNotIn("readme.txt", names)
        
        audio_item = next(f for f in files if f["name"] == "song.mp3")
        self.assertEqual(audio_item["type"], "audio")
        video_item = next(f for f in files if f["name"] == "video.mp4")
        self.assertEqual(video_item["type"], "video")

    def test_list_downloaded_files_empty(self):
        non_existent = os.path.join(self.temp_dir, "empty_dir")
        files = list_downloaded_files(non_existent)
        self.assertEqual(files, [])

    def test_fetch_video_metadata_invalid_url(self):
        meta = fetch_video_metadata("https://www.youtube.com/watch?v=invalid_id_999999999")
        self.assertIsNone(meta)

    def test_extract_media_unsupported_mode(self):
        success, msg = extract_media(
            url="https://www.youtube.com/watch?v=test",
            output_dir=self.temp_dir,
            mode="unsupported_mode"
        )
        self.assertFalse(success)
        self.assertIn("Modo no soportado", msg)

class TestExplorerService(unittest.TestCase):
    @patch("subprocess.Popen")
    def test_open_folder_in_foreground(self, mock_popen):
        with tempfile.TemporaryDirectory() as tmp_dir:
            open_folder_in_foreground(tmp_dir)
            mock_popen.assert_called_once()

class TestUIPrimitives(unittest.TestCase):
    def test_get_badge_html(self):
        badge = get_badge_html("320 kbps", variant="audio")
        self.assertIn("dad-badge", badge)
        self.assertIn("dad-badge-audio", badge)
        self.assertIn("320 kbps", badge)

if __name__ == "__main__":
    unittest.main()
