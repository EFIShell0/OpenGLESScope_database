from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
b=(ROOT/'BUILD_AUDIT.md').read_text(encoding='utf-8');c=(ROOT/'changelog.md').read_text(encoding='utf-8');r=(ROOT/'rules/PROJECT_RULES.md').read_text(encoding='utf-8')
for token in ['# OpenGLESScope Database 3.0.31 build audit','- Database: 3.0.31','- Current producer: OpenGLESScope 3.0.7 / 3007','Normalizer: 16','app.v3031.js`, `site.v3031.css` and `config.js?v=3031']:
    assert token in b, token
assert c.startswith('# OpenGLESScope Database 3.0.31')
assert '## Release 2.0.2 canonical report and snapshot parity' in r
assert (ROOT/'rules/VULKANSCOPE_DATABASE_1.4.12_PROJECT_RULES_REFERENCE.md').is_file()
assert (ROOT/'rules/vulkanscope_database_1_4_12_rule_applicability.json').is_file()
print('OpenGLESScope Database 3.0.31 release docs: PASS')
