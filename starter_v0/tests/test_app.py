from pathlib import Path
import shutil

from streamlit.testing.v1 import AppTest

import ui_session


def test_demo_gate_blocks_chat_until_correct_code(tmp_path, monkeypatch):
    root = Path(__file__).resolve().parents[1]
    (tmp_path / "artifacts").mkdir()
    for name in ("system_prompt.md", "tools.yaml"):
        shutil.copyfile(root / "artifacts" / name, tmp_path / "artifacts" / name)
    (tmp_path / ".env").write_text("DEMO_ACCESS_CODE=offline-demo-test-code\n", encoding="utf-8")
    monkeypatch.setattr(ui_session, "ROOT", tmp_path)
    app = AppTest.from_file(str(root / "app.py")).run(timeout=20)
    assert not app.exception and not app.chat_input
    app.text_input[0].input("wrong-code")
    app.button[0].click().run(timeout=20)
    assert len(app.error) == 1 and not app.chat_input
    app.text_input[0].input("offline-demo-test-code")
    app.button[0].click().run(timeout=20)
    assert not app.exception and len(app.chat_input) == 1
