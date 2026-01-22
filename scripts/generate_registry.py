#!/usr/bin/env python3
"""
Generate the Lucide icons registry from the Lucide repository.

Usage:
    python scripts/generate_registry.py /path/to/lucide/icons

This script parses all SVG and JSON files from the Lucide icons directory
and generates separate registry notebooks for icons, categories, and tags.
"""

import argparse
import json
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Tuple


def parse_svg_elements(svg_path: Path) -> List[Dict[str, Any]]:
    """Parse SVG file and extract child elements."""
    tree = ET.parse(svg_path)
    root = tree.getroot()

    elements = []

    # Process each child element of the SVG root
    for child in root:
        # Remove namespace prefix from tag
        tag = child.tag.replace('{http://www.w3.org/2000/svg}', '')

        if tag == 'path':
            elements.append({
                'type': 'PathElement',
                'attrs': {'d': child.get('d')}
            })
        elif tag == 'circle':
            elements.append({
                'type': 'CircleElement',
                'attrs': {
                    'cx': child.get('cx'),
                    'cy': child.get('cy'),
                    'r': child.get('r')
                }
            })
        elif tag == 'rect':
            attrs = {
                'x': child.get('x'),
                'y': child.get('y'),
                'width': child.get('width'),
                'height': child.get('height')
            }
            if child.get('rx'):
                attrs['rx'] = child.get('rx')
            elements.append({
                'type': 'RectElement',
                'attrs': attrs
            })
        elif tag == 'line':
            elements.append({
                'type': 'LineElement',
                'attrs': {
                    'x1': child.get('x1'),
                    'y1': child.get('y1'),
                    'x2': child.get('x2'),
                    'y2': child.get('y2')
                }
            })
        elif tag == 'ellipse':
            elements.append({
                'type': 'EllipseElement',
                'attrs': {
                    'cx': child.get('cx'),
                    'cy': child.get('cy'),
                    'rx': child.get('rx'),
                    'ry': child.get('ry')
                }
            })
        elif tag == 'polyline':
            elements.append({
                'type': 'PolylineElement',
                'attrs': {'points': child.get('points')}
            })
        elif tag == 'polygon':
            elements.append({
                'type': 'PolygonElement',
                'attrs': {'points': child.get('points')}
            })
        else:
            print(f"Warning: Unknown SVG element type '{tag}' in {svg_path.name}")

    return elements


def parse_json_metadata(json_path: Path) -> Tuple[List[str], List[str]]:
    """Parse JSON metadata file and extract categories and tags."""
    data = json.loads(json_path.read_text())
    categories = data.get('categories', [])
    tags = data.get('tags', [])
    return categories, tags


def format_element(element: Dict[str, Any]) -> str:
    """Format an element dict as Python code."""
    elem_type = element['type']
    attrs = element['attrs']

    # Format attributes
    attr_parts = []
    for key, value in attrs.items():
        if value is None:
            continue
        # Escape quotes in string values
        escaped_value = value.replace('\\', '\\\\').replace('"', '\\"')
        attr_parts.append(f'{key}="{escaped_value}"')

    return f"{elem_type}({', '.join(attr_parts)})"


def format_icon_data(elements: List[Dict[str, Any]], categories: List[str], tags: List[str]) -> str:
    """Format IconData as Python code."""
    # Format elements list
    if len(elements) == 1:
        elements_str = f"[{format_element(elements[0])}]"
    else:
        elem_strs = [format_element(e) for e in elements]
        elements_str = "[\n            " + ",\n            ".join(elem_strs) + "\n        ]"

    # Format categories and tags
    categories_str = repr(categories)
    tags_str = repr(tags)

    return f"IconData(elements={elements_str}, categories={categories_str}, tags={tags_str})"


def generate_icons_notebook(
    icons_data: Dict[str, Dict[str, Any]],
    output_path: Path
) -> None:
    """Generate the icons.ipynb notebook."""

    # Generate ICONS dictionary code
    icons_entries = []
    for name in sorted(icons_data.keys()):
        data = icons_data[name]
        icon_code = format_icon_data(data['elements'], data['categories'], data['tags'])
        icons_entries.append(f'    "{name}": {icon_code}')

    icons_code = "ICONS: Dict[str, IconData] = {\n" + ",\n".join(icons_entries) + "\n}"

    notebook = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "# registry.icons\n",
                    "\n",
                    "> Auto-generated registry of Lucide icon data.\n",
                    ">\n",
                    "> **Note:** This module is auto-generated by `scripts/generate_registry.py`. Do not edit manually."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": ["#| default_exp registry.icons"]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "#| export\n",
                    "from typing import Dict\n",
                    "\n",
                    "from cjm_fasthtml_lucide_icons.core import (\n",
                    "    IconData,\n",
                    "    PathElement,\n",
                    "    CircleElement,\n",
                    "    RectElement,\n",
                    "    LineElement,\n",
                    "    EllipseElement,\n",
                    "    PolylineElement,\n",
                    "    PolygonElement,\n",
                    ")"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## Icon Registry\n",
                    "\n",
                    "Maps icon names to their `IconData` containing SVG elements and metadata."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "#| export\n",
                    f"# AUTO-GENERATED: Do not edit manually\n",
                    f"# Generated from Lucide icons repository ({len(icons_data)} icons)\n",
                    f"# Run `python scripts/generate_registry.py` to regenerate\n",
                    "\n",
                    icons_code
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": ["#| hide\n", "import nbdev; nbdev.nbdev_export()"]
            }
        ],
        "metadata": {
            "kernelspec": {
                "display_name": "python3",
                "language": "python",
                "name": "python3"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }

    output_path.write_text(json.dumps(notebook, indent=1))
    print(f"Generated {output_path}")


def generate_categories_notebook(
    categories_index: Dict[str, List[str]],
    output_path: Path
) -> None:
    """Generate the categories.ipynb notebook."""

    # Generate CATEGORIES dictionary code
    categories_entries = []
    for cat in sorted(categories_index.keys()):
        icon_list = sorted(categories_index[cat])
        categories_entries.append(f'    "{cat}": {repr(icon_list)}')

    categories_code = "CATEGORIES: Dict[str, List[str]] = {\n" + ",\n".join(categories_entries) + "\n}"

    notebook = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "# registry.categories\n",
                    "\n",
                    "> Auto-generated category index for Lucide icons.\n",
                    ">\n",
                    "> **Note:** This module is auto-generated by `scripts/generate_registry.py`. Do not edit manually."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": ["#| default_exp registry.categories"]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "#| export\n",
                    "from typing import Dict, List"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## Category Index\n",
                    "\n",
                    "Maps category names to lists of icon names in that category."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "#| export\n",
                    f"# AUTO-GENERATED: Do not edit manually ({len(categories_index)} categories)\n",
                    f"# Run `python scripts/generate_registry.py` to regenerate\n",
                    "\n",
                    categories_code
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": ["#| hide\n", "import nbdev; nbdev.nbdev_export()"]
            }
        ],
        "metadata": {
            "kernelnel": {
                "display_name": "python3",
                "language": "python",
                "name": "python3"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }

    output_path.write_text(json.dumps(notebook, indent=1))
    print(f"Generated {output_path}")


def generate_tags_notebook(
    tags_index: Dict[str, List[str]],
    output_path: Path
) -> None:
    """Generate the tags.ipynb notebook."""

    # Generate TAGS dictionary code
    tags_entries = []
    for tag in sorted(tags_index.keys()):
        icon_list = sorted(tags_index[tag])
        tags_entries.append(f'    "{tag}": {repr(icon_list)}')

    tags_code = "TAGS: Dict[str, List[str]] = {\n" + ",\n".join(tags_entries) + "\n}"

    notebook = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "# registry.tags\n",
                    "\n",
                    "> Auto-generated tag index for Lucide icons.\n",
                    ">\n",
                    "> **Note:** This module is auto-generated by `scripts/generate_registry.py`. Do not edit manually."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": ["#| default_exp registry.tags"]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "#| export\n",
                    "from typing import Dict, List"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## Tag Index\n",
                    "\n",
                    "Maps tags to lists of icon names with that tag."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "#| export\n",
                    f"# AUTO-GENERATED: Do not edit manually ({len(tags_index)} tags)\n",
                    f"# Run `python scripts/generate_registry.py` to regenerate\n",
                    "\n",
                    tags_code
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": ["#| hide\n", "import nbdev; nbdev.nbdev_export()"]
            }
        ],
        "metadata": {
            "kernelspec": {
                "display_name": "python3",
                "language": "python",
                "name": "python3"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }

    output_path.write_text(json.dumps(notebook, indent=1))
    print(f"Generated {output_path}")


def generate_registry_notebooks(
    icons_dir: Path,
    output_dir: Path
) -> None:
    """Generate the registry notebooks from Lucide icons."""

    # Collect all icons
    icons_data = {}
    categories_index = defaultdict(list)
    tags_index = defaultdict(list)

    # Find all SVG files
    svg_files = sorted(icons_dir.glob('*.svg'))
    print(f"Found {len(svg_files)} SVG files")

    for svg_path in svg_files:
        icon_name = svg_path.stem
        json_path = svg_path.with_suffix('.json')

        # Parse SVG elements
        elements = parse_svg_elements(svg_path)
        if not elements:
            print(f"Warning: No elements found in {svg_path.name}")
            continue

        # Parse metadata
        categories, tags = [], []
        if json_path.exists():
            categories, tags = parse_json_metadata(json_path)

        # Store icon data
        icons_data[icon_name] = {
            'elements': elements,
            'categories': categories,
            'tags': tags
        }

        # Build indices
        for cat in categories:
            categories_index[cat].append(icon_name)
        for tag in tags:
            tags_index[tag].append(icon_name)

    print(f"Processed {len(icons_data)} icons")
    print(f"Found {len(categories_index)} categories")
    print(f"Found {len(tags_index)} tags")

    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate separate notebooks
    generate_icons_notebook(icons_data, output_dir / "icons.ipynb")
    generate_categories_notebook(categories_index, output_dir / "categories.ipynb")
    generate_tags_notebook(tags_index, output_dir / "tags.ipynb")


def main():
    parser = argparse.ArgumentParser(
        description="Generate Lucide icons registry from Lucide repository"
    )
    parser.add_argument(
        "icons_dir",
        type=Path,
        help="Path to the Lucide icons directory (e.g., /path/to/lucide/icons)"
    )
    parser.add_argument(
        "-o", "--output",
        type=Path,
        default=None,
        help="Output directory for registry notebooks (default: nbs/registry relative to script)"
    )

    args = parser.parse_args()

    # Validate icons directory
    if not args.icons_dir.exists():
        print(f"Error: Icons directory does not exist: {args.icons_dir}")
        return 1

    # Determine output directory
    if args.output:
        output_dir = args.output
    else:
        # Default to nbs/registry relative to the project root
        script_dir = Path(__file__).parent
        output_dir = script_dir.parent / "nbs" / "registry"

    # Generate registry notebooks
    generate_registry_notebooks(args.icons_dir, output_dir)

    return 0


if __name__ == "__main__":
    exit(main())
