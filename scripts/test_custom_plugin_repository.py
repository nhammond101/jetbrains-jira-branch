from __future__ import annotations

import tempfile
import textwrap
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

from scripts.custom_plugin_repository import publish_custom_repository


class CustomPluginRepositoryTest(unittest.TestCase):
    def test_publish_custom_repository_writes_zip_and_update_plugins_xml(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo = Path(temp_dir)
            plugin_xml = repo / "src/main/resources/META-INF/plugin.xml"
            plugin_xml.parent.mkdir(parents=True, exist_ok=True)
            plugin_xml.write_text(
                textwrap.dedent(
                    """\
                    <idea-plugin>
                        <id>com.example.test</id>
                        <name>Example Plugin</name>
                        <vendor>example</vendor>
                        <description>
                            Multiline
                            description text
                        </description>
                        <idea-version since-build="241" until-build="251.*"/>
                    </idea-plugin>
                    """
                ),
                encoding="utf-8",
            )

            zip_path = repo / "build/distributions/example-plugin-1.2.3.zip"
            zip_path.parent.mkdir(parents=True, exist_ok=True)
            zip_path.write_bytes(b"zip-bytes")

            output_dir = repo / "build/jetbrains"
            publish_custom_repository(
                plugin_xml_path=plugin_xml,
                zip_path=zip_path,
                output_dir=output_dir,
                version="1.2.3",
                download_base_url="https://owner.github.io/repo/jetbrains",
            )

            copied_zip = output_dir / zip_path.name
            self.assertTrue(copied_zip.exists())
            self.assertEqual(zip_path.read_bytes(), copied_zip.read_bytes())

            update_plugins = output_dir / "updatePlugins.xml"
            self.assertTrue(update_plugins.exists())

            root = ET.fromstring(update_plugins.read_text(encoding="utf-8"))
            plugin = root.find("plugin")
            self.assertIsNotNone(plugin)
            assert plugin is not None
            self.assertEqual("com.example.test", plugin.get("id"))
            self.assertEqual("1.2.3", plugin.get("version"))
            self.assertEqual(
                "https://owner.github.io/repo/jetbrains/example-plugin-1.2.3.zip",
                plugin.get("url"),
            )
            self.assertEqual("Example Plugin", plugin.findtext("name"))
            self.assertEqual("example", plugin.findtext("vendor"))
            self.assertEqual("Multiline description text", plugin.findtext("description"))
            idea_version = plugin.find("idea-version")
            self.assertIsNotNone(idea_version)
            assert idea_version is not None
            self.assertEqual("241", idea_version.get("since-build"))
            self.assertEqual("251.*", idea_version.get("until-build"))


if __name__ == "__main__":
    unittest.main()
