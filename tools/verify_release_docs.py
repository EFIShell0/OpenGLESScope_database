from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
b=(ROOT/'BUILD_AUDIT.md').read_text();c=(ROOT/'changelog.md').read_text();r=(ROOT/'rules/PROJECT_RULES.md').read_text()
for token in ['# OpenGLESScope Database 3.0.27 build audit','- Database: 3.0.27','- Current producer: OpenGLESScope 3.0.7 / 3007','Normalizer: 16','app.v3027.js`, `site.v3027.css` and `config.js?v=3027']:
    assert token in b, token
assert c.startswith('# OpenGLESScope Database 3.0.27')
assert '## Release 2.0.2 canonical report and snapshot parity' in r
assert (ROOT/'rules/VULKANSCOPE_DATABASE_1.4.12_PROJECT_RULES_REFERENCE.md').is_file()
assert (ROOT/'rules/vulkanscope_database_1_4_12_rule_applicability.json').is_file()
print('OpenGLESScope Database 3.0.27 release docs: PASS')
