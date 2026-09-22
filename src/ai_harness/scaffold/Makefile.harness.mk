# ai-harness Make targets — include from project Makefile:
#   include Makefile.harness.mk

.PHONY: check-harness check-ship kb-gen context-pack handoff wip-save pr-merge skills-ui design-lint

check-harness:
	scripts/check-harness.sh

# Layer-1 设计门禁：硬编码值必须命中 docs/design/DESIGN.md token 表（front matter 自动解析）。
# 扫描范围：DESIGN_LINT_TARGETS（缺省读 DESIGN.md lint.targets）；原型送闸前另跑
# node scripts/design-lint.js docs/features/<id>/prototype/vN
DESIGN_LINT_TARGETS ?=
design-lint:
	node scripts/design-lint.js $(DESIGN_LINT_TARGETS)

check-ship:
	python3 scripts/kb_sync.py check-ship

kb-gen:
	python3 scripts/kb_sync.py gen

context-pack:
	@test -n "$(TASK)" || (echo "Usage: make context-pack TASK=resume DOMAIN=example"; exit 2)
	python3 scripts/kb_sync.py pack $(TASK) $(if $(DOMAIN),--domain $(DOMAIN),)

handoff:
	scripts/handoff.sh

wip-save:
	@test -n "$(MSG)" || (echo "Usage: make wip-save MSG=\"short progress\""; exit 2)
	MSG="$(MSG)" scripts/wip-save.sh

pr-merge:
	@test -n "$(PR)" || (echo "Usage: make pr-merge PR=<n>"; exit 2)
	bash scripts/pr-merge.sh $(PR)

skills-ui:
	bash scripts/install-ui-skills.sh
