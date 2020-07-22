# sim_telarray_configuration
sim_telarray configuration for FACT

## Install

* sim_telarray (in simtel directory)
```bash
./clean_all .
cp sim_telarray/cfg/common/atmprof{9,8}.dat
EXTRA_DEFINES="-DMAXIMUM_SLICES=300" ./build_all cta epos
```

* download fact tools
```
make -f downloads.mk
```

## Run

```bash
snakemake --use-conda --cores <N>
```
