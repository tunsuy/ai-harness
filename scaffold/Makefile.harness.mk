# ai-harness Make targets — include from project Makefile:
#   include Makefile.harness.mk

.PHONY: check-harness check-ship kb-gen context-pack handoff wip-save pr-merge skills-ui

check-harness:
	scripts/check-harness.sh

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
