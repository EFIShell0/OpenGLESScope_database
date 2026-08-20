from pathlib import Path
import json
root=Path(__file__).resolve().parents[1]
data=root/"data"/"index.json"
obj=json.loads(data.read_text(encoding="utf-8"))
if obj.get("schemaVersion")!=2 or not isinstance(obj.get("reports"),list): raise SystemExit("Invalid static index")
obj["reports"].sort(key=lambda x:(str(x.get("submitted_at",x.get("submittedAt",""))),str(x.get("id",""))),reverse=True)
data.write_text(json.dumps(obj,separators=(",",":"),ensure_ascii=False)+"\n",encoding="utf-8")
print(f"Indexed {len(obj['reports'])} reports")
