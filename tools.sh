#!/bin/bash
# OMO 工具封装 - 让 OpenClaw 可以通过 shell 调用

OMO_DIR="/home/mi/.openclaw/workspace/omo-system"
OMO_PY="$OMO_DIR/omo.py"
OMO_MCP="$OMO_DIR/omo_mcp.py"

case "$1" in
  list-agents)
    python3 "$OMO_PY" list-agents
    ;;
  list-categories)
    python3 "$OMO_PY" list-categories
    ;;
  route)
    shift
    python3 "$OMO_PY" route "$@"
    ;;
  intent)
    shift
    python3 "$OMO_PY" intent "$@"
    ;;
  status)
    python3 "$OMO_PY" status
    ;;
  prompt)
    shift
    python3 "$OMO_PY" prompt "$@"
    ;;
  mcp)
    shift
    echo "$@" | python3 "$OMO_MCP"
    ;;
  *)
    echo "Usage: $0 {list-agents|list-categories|route|intent|status|prompt|mcp}"
    exit 1
    ;;
esac
