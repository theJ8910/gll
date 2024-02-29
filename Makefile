# GNU Make workspace makefile autogenerated by Premake

ifndef config
  config=debug_x32
endif

ifndef verbose
  SILENT = @
endif

ifeq ($(config),debug_x32)
  gll_config = debug_x32
endif
ifeq ($(config),debug_x64)
  gll_config = debug_x64
endif
ifeq ($(config),release_x32)
  gll_config = release_x32
endif
ifeq ($(config),release_x64)
  gll_config = release_x64
endif

PROJECTS := gll

.PHONY: all clean help $(PROJECTS) 

all: $(PROJECTS)

gll:
ifneq (,$(gll_config))
	@echo "==== Building gll ($(gll_config)) ===="
	@${MAKE} --no-print-directory -C . -f gll.make config=$(gll_config)
endif

clean:
	@${MAKE} --no-print-directory -C . -f gll.make clean

help:
	@echo "Usage: make [config=name] [target]"
	@echo ""
	@echo "CONFIGURATIONS:"
	@echo "  debug_x32"
	@echo "  debug_x64"
	@echo "  release_x32"
	@echo "  release_x64"
	@echo ""
	@echo "TARGETS:"
	@echo "   all (default)"
	@echo "   clean"
	@echo "   gll"
	@echo ""
	@echo "For more information, see https://github.com/premake/premake-core/wiki"