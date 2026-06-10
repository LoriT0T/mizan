"""Concern: structural schema conformance.

Owns the single job of checking a parsed JSON instance against a JSON-Schema
(draft-07 subset: type, required, properties, additionalProperties:false, enum,
pattern, minLength, maxLength, minItems, items, nested objects/arrays).

Dependency-free (stdlib only). Reaches into no sibling unit. Entry point:
`validate(instance, schema) -> list[str]` returning human-readable error paths
(empty list == valid).
"""
import re

_TYPES = {
    "object": dict, "array": list, "string": str,
    "boolean": bool, "integer": int, "number": (int, float),
}


def _type_ok(value, t):
    if t == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if t == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if t == "boolean":
        return isinstance(value, bool)
    return isinstance(value, _TYPES[t])


def validate(instance, schema, path="$"):
    errors = []
    t = schema.get("type")
    if t and not _type_ok(instance, t):
        errors.append(f"{path}: expected type {t}, got {type(instance).__name__}")
        return errors  # type wrong → deeper checks meaningless

    if "enum" in schema and instance not in schema["enum"]:
        errors.append(f"{path}: value {instance!r} not in enum {schema['enum']}")

    if isinstance(instance, str):
        if "minLength" in schema and len(instance) < schema["minLength"]:
            errors.append(f"{path}: shorter than minLength {schema['minLength']}")
        if "maxLength" in schema and len(instance) > schema["maxLength"]:
            errors.append(f"{path}: longer than maxLength {schema['maxLength']} (len={len(instance)})")
        if "pattern" in schema and not re.search(schema["pattern"], instance):
            errors.append(f"{path}: {instance!r} does not match pattern {schema['pattern']}")

    if isinstance(instance, dict):
        for req in schema.get("required", []):
            if req not in instance:
                errors.append(f"{path}: missing required property '{req}'")
        props = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            for key in instance:
                if key not in props:
                    errors.append(f"{path}: additional property '{key}' not allowed")
        for key, subschema in props.items():
            if key in instance:
                errors.extend(validate(instance[key], subschema, f"{path}.{key}"))

    if isinstance(instance, list):
        if "minItems" in schema and len(instance) < schema["minItems"]:
            errors.append(f"{path}: fewer than minItems {schema['minItems']}")
        if "items" in schema:
            for i, item in enumerate(instance):
                errors.extend(validate(item, schema["items"], f"{path}[{i}]"))

    return errors
