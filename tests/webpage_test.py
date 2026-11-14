import importlib
from types import SimpleNamespace

from click.testing import CliRunner

from lmtoolbox.webpage import extract_text


def test_extract_text_excludes_inert_templates_and_hidden_content():
    html = """<p>Visible <b>text</b></p>
    <template><p hidden>Secret</p><script>window.secret()</script>
      <img alt="Template image"><template>Nested template</template>
    </template><img alt="Visible image"><script>other_secret()</script>"""

    assert extract_text(html) == "Visible text Visible image"


def test_extract_text_preserves_normal_content_around_template_like_text():
    html = """<p>Before &amp; after</p><!-- <template>ignored</template> -->
    <script>const example = "<template>ignored</template>";</script>
    <p>Visible <b>text</b></p><img alt="Visible image">"""

    assert extract_text(html) == "Before & after  Visible textVisible image"


def test_summarize_filters_webpage_before_sending_prompt(monkeypatch, tmp_path):
    monkeypatch.setenv("HOME", str(tmp_path))
    cli = importlib.import_module("lmtoolbox.cli")
    monkeypatch.setattr(
        cli.requests,
        "get",
        lambda *args, **kwargs: SimpleNamespace(
            text="<p>Visible</p><template><script>secret()</script></template>"
        ),
    )
    prompts = []
    monkeypatch.setattr(cli, "process_command", lambda *args: prompts.append(args[4]))

    result = CliRunner().invoke(cli.summarize, ["https://example.com"])

    assert result.exit_code == 0, result.output
    assert prompts == ["Visible"]
