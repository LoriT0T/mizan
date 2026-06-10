"""Isolated test for schema_validator. Runs alone — imports only the unit + stdlib."""
import unittest
import schema_validator as sv


class TestSchemaValidator(unittest.TestCase):
    def test_valid_object_passes(self):
        schema = {
            "type": "object", "required": ["id"], "additionalProperties": False,
            "properties": {"id": {"type": "string", "pattern": "^R[0-9]+$"}},
        }
        self.assertEqual(sv.validate({"id": "R1"}, schema), [])

    def test_missing_required(self):
        schema = {"type": "object", "required": ["id"], "properties": {}}
        errs = sv.validate({}, schema)
        self.assertTrue(any("missing required property 'id'" in e for e in errs))

    def test_enum_violation(self):
        schema = {"type": "string", "enum": ["established", "contested"]}
        self.assertTrue(sv.validate("maybe", schema))

    def test_additional_property_rejected(self):
        schema = {"type": "object", "additionalProperties": False, "properties": {"a": {"type": "string"}}}
        errs = sv.validate({"a": "x", "b": "y"}, schema)
        self.assertTrue(any("additional property 'b'" in e for e in errs))

    def test_maxlength(self):
        schema = {"type": "string", "maxLength": 3}
        self.assertTrue(sv.validate("abcd", schema))
        self.assertEqual(sv.validate("abc", schema), [])

    def test_min_items_and_items(self):
        schema = {"type": "array", "minItems": 1, "items": {"type": "string"}}
        self.assertTrue(sv.validate([], schema))
        self.assertTrue(sv.validate([1], schema))   # wrong item type
        self.assertEqual(sv.validate(["ok"], schema), [])

    def test_pattern_arabic_passthrough(self):
        # Arabic content in a free-text field must not trip the validator.
        schema = {"type": "string", "minLength": 1}
        self.assertEqual(sv.validate("المرابحة", schema), [])

    def test_wrong_type_short_circuits(self):
        schema = {"type": "object", "required": ["id"], "properties": {}}
        errs = sv.validate("not-an-object", schema)
        self.assertTrue(any("expected type object" in e for e in errs))


if __name__ == "__main__":
    unittest.main()
