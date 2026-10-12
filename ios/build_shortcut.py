#!/usr/bin/env python3
"""Build and publicly sign the Insta Preview Share macOS/iOS shortcut."""

from __future__ import annotations

import argparse
import copy
import plistlib
import re
import subprocess
import tempfile
import uuid
from pathlib import Path


IOS_DIR = Path(__file__).resolve().parent
TEMPLATE_PATH = IOS_DIR / "upstream-template.wflow"
DEFAULT_OUTPUT = IOS_DIR / "Insta Preview Share.shortcut"
DEFAULT_DOMAIN = "oginstagram.com"
MATCH_PATTERN = (
    r"(?i:(?<![A-Za-z0-9@./?&=+%#;:-])(?:https?://)?(?:www\.)?"
    r"instagram\.com/(p|reel)/([A-Za-z0-9_-]+)/?(?:[?#][^\s]*)?"
    r"(?=$|\s|[)\]}>]|[.,!?;:]+(?=$|\s|[)\]}>])))"
)
REPLACE_PATTERN = r"(?is)^[\s\S]*?" + MATCH_PATTERN + r"[\s\S]*$"


def _uuid(name: str) -> str:
    return str(uuid.uuid5(uuid.NAMESPACE_URL, f"https://github.com/MTGVim/insta-preview-share/{name}")).upper()


def _text_token(value: dict) -> dict:
    return {
        "Value": {
            "string": "￼",
            "attachmentsByRange": {"{0, 1}": value},
        },
        "WFSerializationType": "WFTextTokenString",
    }


def _input_token() -> dict:
    return _text_token({"Type": "ExtensionInput"})


def _action_output_token(action_uuid: str, output_name: str, *, text_attachment: bool = True) -> dict:
    attachment = {"OutputUUID": action_uuid, "Type": "ActionOutput", "OutputName": output_name}
    if text_attachment:
        return _text_token(attachment)
    return {"Value": attachment, "WFSerializationType": "WFTextTokenAttachment"}


def build_workflow(template: dict, domain: str = DEFAULT_DOMAIN) -> dict:
    """Return an upstream-based workflow with validated Instagram URL handling."""
    labels = domain.split(".")
    if (
        len(domain) > 253
        or len(labels) < 2
        or any(
            not 1 <= len(label) <= 63
            or not label[0].isalnum()
            or not label[-1].isalnum()
            or re.fullmatch(r"[A-Za-z0-9-]+", label) is None
            for label in labels
        )
    ):
        raise ValueError("domain must be a DNS hostname without a scheme or path")

    workflow = copy.deepcopy(template)
    workflow["WFWorkflowInputContentItemClasses"] = list(
        dict.fromkeys([*workflow["WFWorkflowInputContentItemClasses"], "WFStringContentItem"])
    )

    match_id = _uuid("match-instagram-url")
    replace_id = _uuid("replace-instagram-url")
    clipboard_id = _uuid("copy-transformed-url")
    share_id = _uuid("share-transformed-url")
    text_id = _uuid("invalid-url-guidance")
    show_id = _uuid("show-invalid-url-guidance")
    group_id = _uuid("valid-instagram-url-branch")

    match = {
        "WFWorkflowActionIdentifier": "is.workflow.actions.text.match",
        "WFWorkflowActionParameters": {
            "WFMatchTextPattern": MATCH_PATTERN,
            "text": _input_token(),
            "UUID": match_id,
        },
    }
    condition_input = {
        "Type": "Variable",
        "Variable": {
            "Value": {
                "Type": "ActionOutput",
                "OutputName": "일치",
                "OutputUUID": match_id,
                "Aggrandizements": [{"Type": "WFPropertyVariableAggrandizement", "PropertyName": "text"}],
            },
            "WFSerializationType": "WFTextTokenAttachment",
        },
    }
    conditional = {
        "WFWorkflowActionIdentifier": "is.workflow.actions.conditional",
        "WFWorkflowActionParameters": {
            "WFControlFlowMode": 0,
            "WFInput": condition_input,
            "WFCondition": 100,
            "GroupingIdentifier": group_id,
        },
    }
    replace = {
        "WFWorkflowActionIdentifier": "is.workflow.actions.text.replace",
        "WFWorkflowActionParameters": {
            "WFReplaceTextRegularExpression": True,
            "WFReplaceTextFind": REPLACE_PATTERN,
            "WFReplaceTextReplace": f"https://{domain}/$1/$2/",
            "WFInput": _input_token(),
            "CustomOutputName": "Updated Text",
            "UUID": replace_id,
        },
    }
    clipboard = {
        "WFWorkflowActionIdentifier": "is.workflow.actions.setclipboard",
        "WFWorkflowActionParameters": {
            "WFLocalOnly": False,
            "WFInput": _action_output_token(replace_id, "Updated Text", text_attachment=False),
            "UUID": clipboard_id,
            "WFExpirationDate": "",
        },
    }
    share = {
        "WFWorkflowActionIdentifier": "is.workflow.actions.share",
        "WFWorkflowActionParameters": {
            "WFInput": _action_output_token(replace_id, "Updated Text", text_attachment=False),
            "UUID": share_id,
        },
    }
    otherwise = {
        "WFWorkflowActionIdentifier": "is.workflow.actions.conditional",
        "WFWorkflowActionParameters": {"WFControlFlowMode": 1, "GroupingIdentifier": group_id},
    }
    guidance = {
        "WFWorkflowActionIdentifier": "is.workflow.actions.gettext",
        "WFWorkflowActionParameters": {
            "WFTextActionText": "지원하는 Instagram 게시물 또는 릴스 링크를 찾지 못했습니다. Instagram에서 링크를 다시 공유하거나 복사해 주세요.",
            "UUID": text_id,
        },
    }
    show_guidance = {
        "WFWorkflowActionIdentifier": "is.workflow.actions.showresult",
        "WFWorkflowActionParameters": {
            "Text": _action_output_token(text_id, "텍스트"),
            "UUID": show_id,
        },
    }
    end = {
        "WFWorkflowActionIdentifier": "is.workflow.actions.conditional",
        "WFWorkflowActionParameters": {"GroupingIdentifier": group_id, "WFControlFlowMode": 2},
    }

    workflow["WFWorkflowActions"] = [match, conditional, replace, clipboard, share, otherwise, guidance, show_guidance, end]
    return workflow


def build_signed_shortcut(output: Path = DEFAULT_OUTPUT) -> Path:
    template = plistlib.loads(TEMPLATE_PATH.read_bytes())
    workflow = build_workflow(template)
    output = output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="insta-preview-share-") as temp_dir:
        source = Path(temp_dir) / "Insta Preview Share.unsigned.shortcut"
        source.write_bytes(plistlib.dumps(workflow, fmt=plistlib.FMT_BINARY, sort_keys=False))
        subprocess.run(
            ["shortcuts", "sign", "--mode", "anyone", "--input", str(source), "--output", str(output)],
            check=True,
        )
    output.chmod(0o644)
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="signed shortcut output path")
    args = parser.parse_args()
    print(build_signed_shortcut(args.output))


if __name__ == "__main__":
    main()
