OUTPUT_PATH='build'
FACT_TOOLS_VERSION='v1.1.3'
FACT_TOOLS=$(OUTPUT_PATH)/fact-tools-$(FACT_TOOLS_VERSION).jar

all: $(FACT_TOOLS) $(addprefix $(OUTPUT_PATH)/, \
	testMcDrsFile.drs.fits.gz \
	delays_zero.csv \
	)

$(OUTPUT_PATH):
	mkdir -p $@

$(FACT_TOOLS): | $(OUTPUT_PATH)
	wget --timestamping \
		https://github.com/fact-project/fact-tools/releases/download/$(FACT_TOOLS_VERSION)/fact-tools-$(FACT_TOOLS_VERSION).jar \
		-O $@

$(OUTPUT_PATH)/testMcDrsFile.drs.fits.gz: | $(OUTPUT_PATH)
	wget --timestamping \
		https://github.com/fact-project/fact-tools/raw/master/src/main/resources/testMcDrsFile.drs.fits.gz \
		-O $@

$(OUTPUT_PATH)/delays_zero.csv: | $(OUTPUT_PATH)
	wget --timestamping \
		https://raw.githubusercontent.com/fact-project/fact-tools/master/src/main/resources/default/delays_zero.csv \
		-O $@
