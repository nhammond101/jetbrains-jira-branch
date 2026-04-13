from __future__ import annotations

import argparse
import shutil
import textwrap
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class PluginMetadata:
    plugin_id: str
    name: str
    vendor: str
    description: str
    since_build: str | None
    until_build: str | None


def _normalized_text(value: str | None) -> str:
    if value is None:
        return ""
    # Keep descriptions readable while stripping XML indentation noise.
    return " ".join(value.split())


def read_plugin_metadata(plugin_xml_path: Path) -> PluginMetadata:
    root = ET.parse(plugin_xml_path).getroot()

    plugin_id = _normalized_text(root.findtext("id"))
    if not plugin_id:
        raise ValueError(f"Missing plugin id in {plugin_xml_path}")

    name = _normalized_text(root.findtext("name"))
    vendor = _normalized_text(root.findtext("vendor"))
    description = _normalized_text(root.findtext("description"))

    idea_version = root.find("idea-version")
    since_build = idea_version.get("since-build") if idea_version is not None else None
    until_build = idea_version.get("until-build") if idea_version is not None else None

    return PluginMetadata(
        plugin_id=plugin_id,
        name=name,
        vendor=vendor,
        description=description,
        since_build=since_build,
        until_build=until_build,
    )


def build_update_plugins_xml(metadata: PluginMetadata, version: str, plugin_url: str) -> str:
    plugins = ET.Element("plugins")
    plugin = ET.SubElement(
        plugins,
        "plugin",
        {
            "id": metadata.plugin_id,
            "url": plugin_url,
            "version": version,
        },
    )

    if metadata.name:
        ET.SubElement(plugin, "name").text = metadata.name
    if metadata.vendor:
        ET.SubElement(plugin, "vendor").text = metadata.vendor
    if metadata.description:
        ET.SubElement(plugin, "description").text = metadata.description

    idea_version_attributes: dict[str, str] = {}
    if metadata.since_build:
        idea_version_attributes["since-build"] = metadata.since_build
    if metadata.until_build:
        idea_version_attributes["until-build"] = metadata.until_build
    if idea_version_attributes:
        ET.SubElement(plugin, "idea-version", idea_version_attributes)

    ET.indent(plugins, space="    ")
    xml_body = ET.tostring(plugins, encoding="unicode")
    return '<?xml version="1.0" encoding="UTF-8"?>\n' + xml_body + "\n"


def publish_custom_repository(
    *,
    plugin_xml_path: Path,
    zip_path: Path,
    output_dir: Path,
    version: str,
    download_base_url: str,
) -> None:
    if not zip_path.exists():
        raise FileNotFoundError(f"Plugin zip was not found: {zip_path}")

    metadata = read_plugin_metadata(plugin_xml_path)

    output_dir.mkdir(parents=True, exist_ok=True)
    target_zip_path = output_dir / zip_path.name
    shutil.copy2(zip_path, target_zip_path)

    plugin_url = f"{download_base_url.rstrip('/')}/{zip_path.name}"
    update_plugins_xml = build_update_plugins_xml(metadata, version=version, plugin_url=plugin_url)
    (output_dir / "updatePlugins.xml").write_text(update_plugins_xml, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create a JetBrains custom plugin repository directory with updatePlugins.xml.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent(
            """\
            Example:
              python3 scripts/custom_plugin_repository.py \\
                --version 1.2.3 \\
                --zip-path build/distributions/jira-branch-opener-1.2.3.zip \\
                --download-base-url https://owner.github.io/repo/jetbrains \\
                --output-dir build/jetbrains
            """
        ),
    )
    parser.add_argument("--repo-root", default=".", help="Path to the repository root.")
    parser.add_argument("--version", required=True, help="Plugin version for updatePlugins.xml.")
    parser.add_argument("--zip-path", required=True, help="Path to the built plugin zip archive.")
    parser.add_argument(
        "--plugin-xml-path",
        default="src/main/resources/META-INF/plugin.xml",
        help="Path to plugin.xml used as metadata source.",
    )
    parser.add_argument("--output-dir", required=True, help="Directory to write updatePlugins.xml and the plugin zip.")
    parser.add_argument(
        "--download-base-url",
        required=True,
        help="Public base URL where files in output-dir are served.",
    )

    args = parser.parse_args()
    repo_root = Path(args.repo_root).resolve()

    publish_custom_repository(
        plugin_xml_path=(repo_root / args.plugin_xml_path).resolve(),
        zip_path=(repo_root / args.zip_path).resolve(),
        output_dir=(repo_root / args.output_dir).resolve(),
        version=args.version,
        download_base_url=args.download_base_url,
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
