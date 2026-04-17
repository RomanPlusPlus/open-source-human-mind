These versions are especially useful as fallbacks (e.g. use a smaller version if the monthly cost budget is approaching the limit).
Also useful for high-volume data processing, and for affordable public deployments.

# nano_sideload.txt 

Is about 220x smaller than the full thing. At 46 KB, small enough for a practical local deployment.

The file consists of:
- a slightly modified system_message.txt
- structured_self_facts.txt, massively compressed 

In spite of the extremely small size, still clearly preserves a lot of my personality.

# micro_sideload.txt

Is about 10x smaller than the full thing. At 997 KB, small enough to fit into 1 mT contexts.

Consists of:
- a slightly modified nano_sideload.txt
- the rest of the full_dataset, massively compressed by nano_sideload.txt