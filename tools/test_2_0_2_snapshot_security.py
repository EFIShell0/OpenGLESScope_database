from pathlib import Path
import re
root=Path(__file__).resolve().parents[1]
workflow=(root/'tools/pages.workflow.yml').read_text()
worker=(root/'worker/src/index.js').read_text()
migration=(root/'worker/migrations/0004_payload_chunks.sql').read_text()
def gate(source=workflow,code=worker):
    if source.count('group: pages-publication')!=2: raise AssertionError('release/snapshot must serialize publication independently')
    for token in ['release-publish:', 'snapshot-refresh:', 'cancel-in-progress: false', 'queue: max', 'ref: main', 'verify_published_snapshot.py', 'build_live_index.py', '--expect-report-id "$REPORT_ID"', 'REPORT_ID: ${{ inputs.report_id }}', 'python tools/quality_gate.py', 'python tools/audit_database.py --artifact-tree _site']:
        if token not in source:raise AssertionError('snapshot publication guard missing: '+token)
    for token in ['D1_INLINE_PAYLOAD_BYTES=1450000', 'MAX_CANONICAL_BYTES=4*1024*1024', 'splitPayloadChunks', 'loadStoredPayload', 'await sha(storedPayload)!==row.id', 'ctx?.waitUntil', 'AbortSignal.timeout(6500)', 'attempt<3', "response.status!==429&&response.status<500", 'env.DB.batch(statements)', 'if(Number(insertResult?.meta?.changes||0)>0']:
        if token not in code:raise AssertionError('canonical storage or dispatch guard missing: '+token)
    if 'payload_json' not in (root/'worker/migrations/0001_init.sql').read_text():raise AssertionError('inline legacy schema lost')
    if 'PRIMARY KEY (report_id, chunk_index)' not in migration:raise AssertionError('chunk ordering uniqueness not enforced')
    if 'SNAPSHOT_GITHUB_TOKEN' in (root/'worker/wrangler.jsonc').read_text():raise AssertionError('snapshot credential in public config')
    if 'payload_json' in (root/'tools/build_live_index.py').read_text():raise AssertionError('raw report leaked to public index')
    return True
assert gate()
for label,changed in [('missing snapshot serializer',workflow.replace('group: pages-publication','group: uncoordinated-release',1)),('missing published verification',workflow.replace('verify_published_snapshot.py','not_verified.py')),('missing report trigger',workflow.replace('--expect-report-id "$REPORT_ID"','--no-trigger-check'))]:
    try:gate(changed,worker)
    except AssertionError:pass
    else:raise AssertionError(label+' mutation passed')
for label,changed in [('no integrity',worker.replace('await sha(storedPayload)!==row.id','false')),('no atomic batching',worker.replace('env.DB.batch(statements)','env.DB.batch([])')),('no retry bounds',worker.replace('attempt<3','attempt<99'))]:
    try:gate(workflow,changed)
    except AssertionError:pass
    else:raise AssertionError(label+' mutation passed')
print('OpenGLESScope Database 3.0.18 snapshot/storage positive-negative security gates: PASS')
