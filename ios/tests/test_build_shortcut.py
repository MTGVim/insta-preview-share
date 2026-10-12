import plistlib
import re
import unittest
from pathlib import Path

from ios import build_shortcut


IOS = Path(__file__).parent


class ShortcutBehaviorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        template = plistlib.loads((IOS.parent / "upstream-template.wflow").read_bytes())
        cls.workflow = build_shortcut.build_workflow(template)
        cls.actions = cls.workflow["WFWorkflowActions"]
        cls.by_id = {action["WFWorkflowActionIdentifier"]: action for action in cls.actions}
        cls.match_pattern = cls.by_id["is.workflow.actions.text.match"]["WFWorkflowActionParameters"]["WFMatchTextPattern"]
        cls.replaces = [
            action["WFWorkflowActionParameters"]
            for action in cls.actions
            if action["WFWorkflowActionIdentifier"] == "is.workflow.actions.text.replace"
        ]
        cls.replace = cls.replaces[0]

    def transform(self, value):
        match = re.search(self.match_pattern, value, re.IGNORECASE)
        if not match:
            return value
        replacement = re.sub(r"\$(\d+)", r"\\g<\1>", self.replace["WFReplaceTextReplace"])
        value = re.sub(self.replace["WFReplaceTextFind"], replacement, value, count=1, flags=re.IGNORECASE)
        return value

    def test_supported_instagram_urls_preserve_media_type_and_shortcode(self):
        cases = {
            "https://www.instagram.com/p/C8a_0b-9/?igsh=abc": "https://oginstagram.com/p/C8a_0b-9/",
            "https://instagram.com/reel/Reel_42?exln=xyz&psln=abc&utm_source=copy": "https://oginstagram.com/reel/Reel_42/",
            "http://www.instagram.com/p/AbC123": "https://oginstagram.com/p/AbC123/",
            "instagram.com/reel/Ab-C_9/": "https://oginstagram.com/reel/Ab-C_9/",
            "https://instagram.com/reel/abc123/@handle": "https://oginstagram.com/reel/abc123/",
        }
        for source, expected in cases.items():
            with self.subTest(source=source):
                self.assertEqual(self.transform(source), expected)

    def test_lookalike_hosts_and_unsupported_paths_are_not_transformed(self):
        invalid = [
            "https://instagram.com.evil.example/p/abc123",
            "https://oginstagram.com.evil.example/p/abc123",
            "https://eviloginstagram.com/p/abc123",
            "https://evilinstagram.com/p/abc123",
            "https://evil.instagram.com/p/abc123",
            "https://instagram.com:8443/p/abc123",
            "https://user@instagram.com/p/abc123",
            "https://instagram.com/stories/name/123",
            "https://instagram.com/p/abc123/extra",
            "https://instagram.com/p/abc%2Fextra",
            "https://instagram.com/p/abc123.evil",
            "ftp://instagram.com/p/abc123",
            "https://example.com/p/abc123",
            "https://example.com/?next=https://instagram.com/p/abc123",
            "https://example.com/?next=instagram.com/p/abc123",
        ]
        for source in invalid:
            with self.subTest(source=source):
                self.assertEqual(self.transform(source), source)

    def test_text_wrappers_and_instagram_share_metadata_are_removed(self):
        cases = {
            "Link: https://instagram.com/p/abc123.": "https://oginstagram.com/p/abc123/",
            "https://instagram.com/reel/abc123/\n@handle님의 이 Instagram 게시물 보기":
                "https://oginstagram.com/reel/abc123/",
            "https://instagram.com/reel/DeLBjsTTOEy/@yeon_._doo님의 이 Instagram 게시물 보기":
                "https://oginstagram.com/reel/DeLBjsTTOEy/",
            "https://oginstagram.com/reel/DbIl324B6jX/@edmrhythm.ply님의 이 Instagram 게시물 보기":
                "https://oginstagram.com/reel/DbIl324B6jX/",
            "https://instagram.com/reel/abc123/@handle/trailing text to discard":
                "https://oginstagram.com/reel/abc123/",
        }
        for source, expected in cases.items():
            with self.subTest(source=source):
                self.assertEqual(self.transform(source), expected)

    def test_alternate_domain_changes_only_the_generated_destination(self):
        template = plistlib.loads((IOS.parent / "upstream-template.wflow").read_bytes())
        workflow = build_shortcut.build_workflow(template, domain="share.example")
        action = next(
            action for action in workflow["WFWorkflowActions"]
            if action["WFWorkflowActionIdentifier"] == "is.workflow.actions.text.replace"
        )
        self.assertEqual(
            action["WFWorkflowActionParameters"]["WFReplaceTextReplace"],
            "https://share.example/$1/$2/",
        )

    def test_invalid_domain_labels_are_rejected(self):
        template = plistlib.loads((IOS.parent / "upstream-template.wflow").read_bytes())
        with self.assertRaises(ValueError):
            build_shortcut.build_workflow(template, domain="bad..example")

    def test_workflow_keeps_clipboard_fallback_and_shares_only_the_valid_branch(self):
        classes = self.workflow["WFWorkflowInputContentItemClasses"]
        self.assertIn("WFStringContentItem", classes)
        self.assertEqual(self.workflow["WFWorkflowNoInputBehavior"]["Name"], "WFWorkflowNoInputBehaviorGetClipboard")

        identifiers = [action["WFWorkflowActionIdentifier"] for action in self.actions]
        self.assertIn("is.workflow.actions.setclipboard", identifiers)
        self.assertIn("is.workflow.actions.notification", identifiers)
        self.assertIn("is.workflow.actions.share", identifiers)
        self.assertIn("is.workflow.actions.showresult", identifiers)
        self.assertLess(identifiers.index("is.workflow.actions.text.match"), identifiers.index("is.workflow.actions.conditional"))

        match_parameters = self.by_id["is.workflow.actions.text.match"]["WFWorkflowActionParameters"]
        match_pattern = match_parameters["WFMatchTextPattern"]
        self.assertEqual(match_parameters["text"]["Value"]["attachmentsByRange"]["{0, 1}"], {"Type": "ExtensionInput"})
        self.assertEqual(self.replace["WFInput"], match_parameters["text"])
        self.assertEqual(self.replace["WFReplaceTextFind"], build_shortcut.REPLACE_PATTERN)
        self.assertIn(match_pattern, self.replace["WFReplaceTextFind"])
        self.assertTrue(self.replace["WFReplaceTextRegularExpression"])
        self.assertEqual(self.replace["WFReplaceTextReplace"], "https://oginstagram.com/$1/$2/")
        condition_action = next(
            action for action in self.actions
            if action["WFWorkflowActionIdentifier"] == "is.workflow.actions.conditional"
            and action["WFWorkflowActionParameters"]["WFControlFlowMode"] == 0
        )
        self.assertNotIn("WFConditions", condition_action["WFWorkflowActionParameters"])
        self.assertEqual(condition_action["WFWorkflowActionParameters"]["WFCondition"], 100)
        condition = condition_action["WFWorkflowActionParameters"]["WFInput"]["Variable"]["Value"]
        self.assertEqual(condition["OutputUUID"], match_parameters["UUID"])
        replacement_output = {
            "Value": {
                "OutputUUID": self.replace["UUID"],
                "Type": "ActionOutput",
                "OutputName": self.replace["CustomOutputName"],
            },
            "WFSerializationType": "WFTextTokenAttachment",
        }
        for identifier in ("is.workflow.actions.setclipboard", "is.workflow.actions.share"):
            self.assertEqual(self.by_id[identifier]["WFWorkflowActionParameters"]["WFInput"], replacement_output)

        conditional = [
            action["WFWorkflowActionParameters"]["WFControlFlowMode"]
            for action in self.actions
            if action["WFWorkflowActionIdentifier"] == "is.workflow.actions.conditional"
        ]
        self.assertEqual(conditional, [0, 1, 2])

        start = identifiers.index("is.workflow.actions.conditional")
        otherwise = identifiers.index("is.workflow.actions.conditional", start + 1)
        end = identifiers.index("is.workflow.actions.conditional", otherwise + 1)
        true_branch = identifiers[start + 1 : otherwise]
        false_branch = identifiers[otherwise + 1 : end]
        self.assertIn("is.workflow.actions.text.replace", true_branch)
        self.assertEqual(true_branch.count("is.workflow.actions.text.replace"), 1)
        self.assertIn("is.workflow.actions.setclipboard", true_branch)
        self.assertIn("is.workflow.actions.notification", true_branch)
        self.assertIn("is.workflow.actions.share", true_branch)
        self.assertLess(true_branch.index("is.workflow.actions.text.replace"), true_branch.index("is.workflow.actions.setclipboard"))
        self.assertLess(identifiers.index("is.workflow.actions.setclipboard"), identifiers.index("is.workflow.actions.notification"))
        self.assertLess(identifiers.index("is.workflow.actions.notification"), identifiers.index("is.workflow.actions.share"))
        self.assertIn("is.workflow.actions.gettext", false_branch)
        self.assertIn("is.workflow.actions.showresult", false_branch)
        self.assertNotIn("is.workflow.actions.share", false_branch)


if __name__ == "__main__":
    unittest.main()
