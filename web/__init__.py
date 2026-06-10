"""Mizan local web frontend.

ARCHITECTURAL WALL (enforced + tested): this package contains ZERO rule logic,
ZERO registry reads, and ZERO checker code. It imports the orchestrator AS A
LIBRARY (run_text / generate_for_text / scope_info / calibration_status) and
renders results. The engine is fully runnable and testable with this package
absent (proven by the wall test). Local demonstration only — never deployed.
"""
