"""``file=`` kwargs: load table/yaml content straight from disk."""

from cmx.backends.components import Article
from cmx.backends.markdown import CommonMark


def test_table_from_csv(tmp_path):
    p = tmp_path / "t.csv"
    p.write_text("a,b\n1,2\n3,4\n")
    doc = Article()
    assert doc.table(file=str(p))._md == (
        "|   a |   b |\n"
        "|-----|-----|\n"
        "|   1 |   2 |\n"
        "|   3 |   4 |\n"
    )


def test_table_from_tsv(tmp_path):
    p = tmp_path / "t.tsv"
    p.write_text("a\tb\n1\t2\n")
    doc = Article()
    assert doc.table(file=str(p)).data.columns.tolist() == ["a", "b"]


def test_table_from_yaml(tmp_path):
    p = tmp_path / "rows.yaml"
    p.write_text("- {a: 1, b: 2}\n- {a: 3, b: 4}\n")
    doc = Article()
    assert doc.table(file=str(p)).data.shape == (2, 2)


def test_yaml_from_file_is_verbatim(tmp_path):
    p = tmp_path / "cfg.yaml"
    p.write_text("# my config\nlr: 0.1\nepochs: 10\n")
    doc = CommonMark(filename=str(tmp_path / "out.md"))
    # Comments are preserved -- the file content is shown as-is.
    assert doc.yaml(file=str(p))._md == "```yaml\n# my config\nlr: 0.1\nepochs: 10\n```\n"
