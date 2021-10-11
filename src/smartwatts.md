# SmartWatts

SmartWatts is a software-defined power meter based on the PowerAPI toolkit.
SmartWatts is a configurable software that can estimate the power consumption of
software in real-time.
SmartWatts need to receive several metrics provided by
[hwpc-sensor](https://github.com/powerapi-ng/hwpc-sensor) :

- The Running Average Power Limit (RAPL)
- TSC
- APERF
- MPERF
- CPU_CLK_THREAD_UNHALTED:REF_P
- CPU_CLK_THREAD_UNHALTED:THREAD_P
- LLC_MISSES
- INSTRUCTIONS_RETIRED

The reasons of those metrics are described in [SmartWatts: Self-Calibrating
Software-Defined Power Meter for Containers](https://hal.inria.fr/hal-02470128)
