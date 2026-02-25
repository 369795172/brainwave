# dev ↔ master 分支差异分析

---

# 合并执行计划（Merge Execution Plan）

## 目标

合并 dev 与 master，得到统一代码库，并按以下规则取舍功能。

## 保留项

| 类别 | 项目 | 说明 |
|------|------|------|
| **GA 迁移** | 移除 Beta header、`type: "realtime"`、`response.output_text.delta` | openai_realtime_client.py、realtime_server.py |
| **gpt-realtime-1.5** | 模型选项 | realtime.html 下拉：mini + 1.5，删掉 gpt-realtime |
| **create_realtime_session 修复** | 移除 sessions API 不接受的 `type` | 随 WebRTC 删除，该 endpoint 不再保留 |
| **IndexedDB Replay** | 录音重放、Replay 按钮 | main.js、realtime.html、realtime_server |
| **模型选择（仅 realtime）** | realtime.html 下拉保留 | 仅 WebSocket 版，不含 WebRTC |
| **config.py** | 集中配置 | 保留，但移除 X.AI 相关配置 |
| **master PR #4,5,7,10,11,12,13** | 蓝牙、音频时序、IndexedDB、prompt、websockets | 全部保留 |
| **修复** | 音频资源清理、WebSocket cleanup、IndexedDB sessions 错误 | 保留 |
| **Message Handler** | `response.output_text.delta`（OpenAI GA） | 保留；x.ai 专用 handler 删除 |

## 删除项

| 类别 | 项目 | 涉及文件/位置 |
|------|------|---------------|
| **X.AI 支持** | 整个移除 | xai_realtime_client.py（删文件）、config.py（XAI_*）、realtime_server.py（provider/xai 逻辑）、realtime.html（xai-grok 选项）、main.js（xai 分支） |
| **WebRTC** | 整个移除 | static/webrtc.html、static/webrtc.js、/webrtc 路由、/api/v1/realtime/session 端点 |
| **Gemini 转录** | 整个移除 | gemini_client.py（删）、static/transcribe.html、static/transcribe.js、/transcribe 路由、/api/v1/transcribe_gemini 端点 |
| **X.AI 相关修复** | modalities 参数、x.ai message handlers | realtime_server.py 中 XAI 分支、`response.output_audio_transcript.delta` 等 x.ai 专用 handler |
| **已删 md** | 保持删除 | doc/merge.md、xai_integration_plan.md、xai_vs_openai_comparison.md（若存在则删） |

## Message Type Handler 取舍

| Handler | 归属 | 操作 |
|---------|------|------|
| `response.text.delta` | OpenAI | 保留 |
| `response.output_text.delta` | OpenAI GA | 保留 |
| `response.output_audio_transcript.delta` | x.ai 用此代替 text.delta | **删除**（移除 x.ai 后不需要） |
| `input_audio_buffer.speech_stopped` | 可能两边都有 | 保留（通用） |
| `input_audio_buffer.committed` | 可能两边都有 | 保留 |
| `conversation.item.added` | GA | 保留 |
| `response.output_audio.delta/done` | 音频输出，我们 text-only | 可保留（无害）或删 |

## 执行步骤（分阶段，先计划不执行）

### Phase 1：合并
1. `git checkout dev`
2. `git merge master`，解决冲突
3. 测试合并后能否正常启动

### Phase 2：删除 X.AI
1. 删除 `xai_realtime_client.py`
2. 从 `realtime_server.py` 移除：`XAIRealtimeAudioTextClient` 导入、provider 选择、xai 分支
3. 从 `config.py` 移除：`XAI_API_KEY`、`XAI_REALTIME_*`、`REALTIME_PROVIDER`
4. 从 `realtime.html` 移除 xai-grok 选项
5. 从 `main.js` 移除 xai 相关分支（provider、model 判断）
6. 移除 handler：`response.output_audio_transcript.delta`（x.ai 专用）

### Phase 3：删除 WebRTC
1. 删除 `static/webrtc.html`、`static/webrtc.js`
2. 从 `realtime_server.py` 移除：`/webrtc` 路由、`/api/v1/realtime/session`、`/api/v1/realtime/default_prompt`、`CreateRealtimeSessionRequest` 等 WebRTC 相关

### Phase 4：删除 Gemini 转录
1. 删除 `gemini_client.py`（仅用于文件上传转录，与 llm_processor 的 GeminiProcessor 无关）
2. 删除 `static/transcribe.html`、`static/transcribe.js`
3. 从 `realtime_server.py` 移除：`/transcribe` 路由、`/api/v1/transcribe_gemini` 端点、`GeminiTranscriptionSSEData`
4. 从 `prompts.py` 移除 `gemini-transcription`（仅 transcribe_gemini 使用）
5. **注意**：`llm_processor.py` 的 GeminiProcessor（Readability/Correctness/AskAI）保留

### Phase 5：模型选项与 config 清理
1. `realtime.html`：保留 mini、1.5，删除 xai-grok，将 gpt-realtime 改为 gpt-realtime-1.5
2. `config.py`：保留 `OPENAI_REALTIME_MODEL`、`OPENAI_REALTIME_MODALITIES`；删除 XAI 相关、`OPENAI_REALTIME_SESSION_TTL_SEC`（仅 WebRTC 用）

### Phase 6：删除 md 文件
1. 删除 `doc/merge.md`（若存在）
2. 删除 `xai_integration_plan.md`、`xai_vs_openai_comparison.md`（若存在）

### Phase 7：测试
- [x] WebSocket 录音（`/`）
- [x] 模型选择（mini / 1.5）
- [x] IndexedDB Replay
- [x] Readability / Correctness 按钮

---

## 执行完成记录（2025-02-25）

合并与清理已全部完成：

- **Phase 1–4**：dev 合并 master，删除 X.AI、WebRTC、Gemini 转录
- **Phase 5–6**：模型选项（mini + 1.5）、config 清理、删除 md 文件
- **Phase 7**：功能测试通过

当前 master 仅保留：OpenAI WebSocket realtime、Readability、Correctness、IndexedDB Replay、模型选择、config.py。

---

## 合并冲突预判

| 文件 | 可能冲突 |
|------|----------|
| realtime_server.py | master 有蓝牙/音频修复，dev 有 WebRTC/x.ai/Gemini；合并时两边的改动都要进，Phase 2–4 再删 |
| static/main.js | master 与 dev 的 model/provider 逻辑可能不同，需手动合并 |
| requirements.txt | 合并版本要求；保留 google-genai（Readability/Correctness 用 GeminiProcessor）|

---

## 当前状态（2025-02-25）

| 分支 | 最新 commit | 相对对方 |
|------|-------------|----------|
| **master** | 2cb3fdf Feature/xai support (#15) | 落后 dev 30 commits，领先 dev 15 commits |
| **dev** | dc14e7b realtime: remove type param from create_realtime_session | 领先 master 30 commits，落后 master 15 commits |

**共同祖先**: `f7ab078`（约在 Integrate with Gemini Flash 2.5 之前）

---

## dev 有而 master 没有的（30 commits）

### 功能类
- **GA 迁移**: 移除 Beta header，`type: "realtime"`，`response.output_text.delta`
- **gpt-realtime-1.5**: 模型选项替换 gpt-realtime
- **create_realtime_session 修复**: 移除 sessions API 不接受的 `type` 参数
- **x.ai 支持**: xai_realtime_client、provider 选择、grok 模型
- **WebRTC**: webrtc.html/js、`/api/v1/realtime/session`
- **Gemini 转录**: gemini_client.py、transcribe.html/js、`/api/v1/transcribe_gemini`
- **IndexedDB Replay**: 录音重放、Replay 按钮
- **模型选择**: realtime.html 下拉、main.js/webrtc.js 传 model
- **config.py**: 集中配置

### 修复类
- 音频资源清理、WebSocket 关闭时 cleanup
- XAI modalities 参数、message type handlers
- IndexedDB sessions object store 错误

### 已删除（dev 上）
- doc/merge.md
- xai_integration_plan.md
- xai_vs_openai_comparison.md

---

## master 有而 dev 没有的（15 commits）

来自 GitHub PR 的合并：
- **#15** Feature/xai support
- **#13** Fix IndexedDB 'sessions' object store error
- **#12** Add IndexedDB Replay Feature
- **#11** Local Storage and OpenAI Real-time improvements
- **#10** fix bluetooth microphone bug
- **#7** Use enhanced realtime prompt（前缀、gpt-realtime 默认）
- **#5** Fix audio upload timing issue
- **#4** websockets version requirement

---

## 文件差异（dev vs master）

| 文件 | dev 状态 |
|------|----------|
| gemini_client.py | 新增（master 无） |
| openai_realtime_client.py | 已改（GA、type: realtime） |
| realtime_server.py | 已改（WebRTC、x.ai、Gemini、修复） |
| requirements.txt | 已改 |
| static/realtime.html | 已改（模型选择） |
| static/transcribe.html | 新增 |
| static/transcribe.js | 新增 |
| static/webrtc.html | 新增 |
| static/webrtc.js | 新增 |
| tests/test_openai_realtime_client.py | 已改 |

---

## prompts.py 与 config.py

- **prompts.py**: master 与 dev **无差异**（`git diff` 为空）
- **config.py**: 两分支均有，内容一致

你之前提到「有一些 prompt 有隐私」——当前两分支的 prompts 内容相同。若需要区分公开/私有，可考虑：
- 用 `.env` 或环境变量注入敏感 prompt
- 或维护 `prompts.private.py`（gitignore）并在代码中按环境加载

---

## 同步策略建议

### 方案 A：dev 合并 master（把上游 PR 合进 dev）
```bash
git checkout dev
git merge master
# 解决冲突（若有）
```
- 优点：dev 获得 #4 #5 #7 #10 #11 #12 #13 #15 的修复和功能
- 注意：部分功能（如 IndexedDB、x.ai）dev 已有自己的实现，可能重复或冲突

### 方案 B：master 合并 dev（把 dev 推回上游）
```bash
git checkout master
git merge dev
# 解决冲突
git push origin master
```
- 前提：确认要公开的内容（含 prompts）符合隐私要求
- 优点：GitHub 上的 master 与本地 dev 对齐

### 方案 C：分步同步
1. 先在 dev 上 `git merge master`，解决冲突并测试
2. 再决定是否把 dev 合并回 master 并 push

---

## 潜在冲突点

1. **realtime_server.py**: master 有蓝牙麦克风、音频时序等修复，dev 有 WebRTC、x.ai、Gemini 等，需合并两边的改动
2. **IndexedDB / Replay**: master 的 #12 #13 与 dev 的实现可能重叠，需去重或统一
3. **x.ai**: master 的 #15 与 dev 的 x.ai 实现可能重复，需对比并保留一份
4. **prompts / 默认模型**: master 有 PR #7 的 prompt 和 gpt-realtime 默认，dev 已改为 gpt-realtime-1.5，需统一策略
