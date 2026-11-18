from pathlib import Path
import json
import re

root = Path(__file__).resolve().parents[1]
package = root
guide = (package / '03-通用安装交付文档.md').read_text(encoding='utf-8')
code = re.search(r'```python\n(.*?)\n```', guide, re.S).group(1)
namespace = {}
exec(compile(code, 'installation-guide-reference.py', 'exec'), namespace)
new_state, reduce_event = namespace['new_state'], namespace['reduce_event']
checks = []

def record(name, condition):
    checks.append({'name': name, 'passed': bool(condition)})
    if not condition:
        raise AssertionError(name)

def event(text, order=0, **changes):
    result = dict(host_namespace='test-host', session_id='session-a',
                  event_id=f'event-{order}', order=order, origin='human_direct',
                  accepted=True, text=text)
    result.update(changes)
    return result

def initial():
    return new_state('test-host', 'session-a')

record('新会话默认 OFF', initial()['mode'] == 'OFF')
cases = [
    ('独占首行开启', '【急急如律令】', 'ON'),
    ('首行开启并附带任务', '【急急如律令】\n做任务', 'ON'),
    ('CRLF 换行', '【急急如律令】\r\n做任务', 'ON'),
    ('CR 换行', '【急急如律令】\r做任务', 'ON'),
    ('前置空格不触发', ' 【急急如律令】', 'OFF'),
    ('后置空格不触发', '【急急如律令】 ', 'OFF'),
    ('前置空行不触发', '\n【急急如律令】', 'OFF'),
    ('第二行口令不触发', '说明\n【急急如律令】', 'OFF'),
    ('同行任务不触发', '【急急如律令】请做任务', 'OFF'),
    ('引用不触发', '> 【急急如律令】', 'OFF'),
    ('代码块不触发', '```\n【急急如律令】\n```', 'OFF'),
    ('零宽字符不触发', '\u200b【急急如律令】', 'OFF'),
    ('BOM 字符不触发', '\ufeff【急急如律令】', 'OFF'),
    ('空输入不触发', '', 'OFF'),
    ('近似括号不触发', '[急急如律令]', 'OFF'),
]
for label, text, expected in cases:
    record(label, reduce_event(initial(), event(text))['mode'] == expected)

on = reduce_event(initial(), event('【急急如律令】'))
record('原状态不被原地修改', initial()['revision'] == 0 and on['revision'] == 1)
again = reduce_event(on, event('【急急如律令】', 1))
record('重复开启状态与版本幂等', again['mode'] == 'ON' and again['revision'] == 1)
ordinary = reduce_event(again, event('继续任务', 2))
record('普通消息维持 ON', ordinary['mode'] == 'ON')
record('正文退出口令不触发', reduce_event(ordinary, event('说明\n【return 0】', 3))['mode'] == 'ON')
off = reduce_event(ordinary, event('【return 0】\n继续任务', 4))
record('退出并附带任务', off['mode'] == 'OFF' and off['revision'] == 2)
record('重复退出幂等', reduce_event(off, event('【return 0】', 5))['revision'] == 2)
record('旧 ON 事件不能覆盖新 OFF', reduce_event(off, event('【急急如律令】', 0)) == off)
record('同一事件重放无效', reduce_event(on, event('【急急如律令】')) == on)
record('未接受消息无效', reduce_event(on, event('【return 0】', 1, accepted=False)) == on)
for origin in ('other', 'unknown', 'tool', 'subagent', 'scheduled', 'cross_session'):
    record(f'{origin} 来源不得开启', reduce_event(initial(), event('【急急如律令】', origin=origin))['mode'] == 'OFF')
    record(f'{origin} 来源不得退出', reduce_event(on, event('【return 0】', 1, origin=origin))['mode'] == 'ON')
for key, value in [('session_id', 'session-b'), ('host_namespace', 'another-host')]:
    try:
        reduce_event(on, event('【return 0】', 1, **{key: value}))
    except ValueError:
        record(f'{key} 隔离', True)
    else:
        record(f'{key} 隔离', False)
record('JSON 往返保留状态', json.loads(json.dumps(on)) == on)
record('新分叉状态独立', new_state('test-host', 'fork-b')['mode'] == 'OFF' and on['mode'] == 'ON')
for changes in ({'order': True}, {'order': -1}, {'event_id': ''}, {'text': None}):
    try:
        candidate = event('【急急如律令】')
        candidate.update(changes)
        reduce_event(initial(), candidate)
    except ValueError:
        record('无效输入被拒绝 ' + repr(changes), True)
    else:
        record('无效输入被拒绝 ' + repr(changes), False)

result = {'scope': '从交付安装文档提取的纯状态函数；不是宿主或模型端到端测试',
          'passed': sum(c['passed'] for c in checks), 'total': len(checks), 'checks': checks}
print("Session protocol:", result["passed"], "/", result["total"])
import sys
sys.path.insert(0, str(root / "adapters"))
from codex_speed import speed_override
catalog = [{"id": "priority", "name": "Fast"}]
for urgent in (False, True):
    for fresh in (False, True):
        for tier in (None, "default", "priority", "ultrafast", "unknown"):
            for available in ([], catalog):
                got = speed_override(urgent=urgent, new_turn=fresh, inherited_tier=tier, service_tiers=available)
                expected = {"serviceTierForTurn":"priority"} if urgent and fresh and tier=="default" and available else {}
                assert got == expected
for lang in ("", ".zh-CN"):
    assert (root / ("INSTALL"+lang+".md")).is_file()
    assert "urgent-execution/SKILL.md" in (root / ("README"+lang+".md")).read_text(encoding="utf8")
assert (root / "urgent-execution/SKILL.md").read_text(encoding="utf8").startswith("---\nname: urgent-execution\ndescription: ")
print("Speed matrix: 40/40; documentation paths and metadata OK")
assert speed_override(urgent=True, new_turn=True, inherited_tier="default",
                      service_tiers=catalog, manual_choice=True) == {}
