# BioTools

## Program Dependencies

- BBtools >= 37.23

### Package currently under development.
Installation: 
- Clone this repository.
- Move into this directory.
- `pip3 install -e .`

### Functionality
##### bbtools
For all bbtools, additional options can be specified with argument='parameter' passed in after mandatory arguments.

`bbtools.bbmap(reference, forward_reads, out_file)` Mandatory args: reference file (should be fasta 
formatted), forward reads (reverse reads will be found automatically if R1/R2 naming convention is used), output file (sam or bam).
If reverse reads do not follow naming convention, specify with reverse_in='path/to/reads'.

`bbtools.bbduk_trim(forward_in, forward_out)` Does quality trimming of reads.
As with bbmap, if R1/R2 naming convention is used, reverse input/output don't need to be specified.
If convenction isn't followed, specify with reverse_in='path' and reverse_out='path'

`bbtools.bbduk_bait(reference, forward_in, forward_out)` Baits reads in input that match reference, writes to output.
As with bbmap, if R1/R2 naming convention is used, reverse input/output don't need to be specified.
If convenction isn't followed, specify with reverse_in='path' and reverse_out='path'

`bbtools.bbduk_filter(reference, forward_in, forward_out)` Filters reads in input that match reference, writes clean reads to output.
As with bbmap, if R1/R2 naming convention is used, reverse input/output don't need to be specified.
If convenction isn't followed, specify with reverse_in='path' and reverse_out='path'

`bbtools.dedupe(input, output)` Runs dedupe on input, writes to output.

`bbtools.seal(reference, forward_in, rpkm)` Runs seal to generate rpkm stats on reference.
