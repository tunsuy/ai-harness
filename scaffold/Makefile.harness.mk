# ai-harness Make targets — include from project Makefile:
#   include Makefile.harness.mk

.PHONY: check-harness kb-gen context-pack handoff wip-save

check-harness:
	scripts/check-harness.sh

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
