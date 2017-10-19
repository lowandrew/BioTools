# BioTools

## Program Dependencies

Testing done with: 
- BBTools 37.23
- jellyfish 2.2.6
- mash 1.1.1

Other versions of these programs should work, but no guarantees.

### Package currently under development.
Installation: 
- Clone this repository.
- Move into this directory.
- `pip3 install -e .`

### Functionality
##### bbtools
For all bbtools, additional options can be specified with argument='parameter' passed in after mandatory arguments.

`bbtools.bbmap(reference, forward_in, out_bam)` 

Mandatory args: reference file (should be fasta 
formatted), forward reads (reverse reads will be found automatically if R1/R2 naming convention is used), output file (sam or bam).
If reverse reads do not follow naming convention, specify with reverse_in='path/to/reads'.

`bbtools.bbduk_trim(forward_in, forward_out)` 

Does quality trimming of reads.
As with bbmap, if R1/R2 naming convention is used, reverse input/output don't need to be specified.
If convenction isn't followed, specify with reverse_in='path' and reverse_out='path'

`bbtools.bbduk_bait(reference, forward_in, forward_out)` 

Baits reads in input that match reference, writes to output.
As with bbmap, if R1/R2 naming convention is used, reverse input/output don't need to be specified.
If convenction isn't followed, specify with reverse_in='path' and reverse_out='path'

`bbtools.bbduk_filter(reference, forward_in, forward_out)` 

Filters reads in input that match reference, writes clean reads to output.
As with bbmap, if R1/R2 naming convention is used, reverse input/output don't need to be specified.
If convenction isn't followed, specify with reverse_in='path' and reverse_out='path'

`bbtools.dedupe(input, output)` 

Runs dedupe on input, writes to output.

`bbtools.seal(reference, forward_in, rpkm)` 

Runs seal to generate rpkm stats on reference.

##### jellyfish
All jellyfish programs take additional options using options='string of options', where
string of options is exactly the same as what you would enter on the command line.

`jellyfish.count(forward_in, kmer_size=31, count_file='mer_counts.jf', hash_size='100M')`
 
 Runs jellyfish count, with a default kmer size of 31 and output file mer_counts.jf, finding canonical kmers.
Can be run on reads or assemblies. If using paired-end reads and following the R1/R2 naming 
 convention, reverse reads do not need to be specified. If not following convention, specify reverse reads
 with reverse_in='path/to/reverse/reads'. Handles gzipped or plain-text files (bz2 support coming soon!)

`jellyfish.dump(mer_file, outfile=counts.fasta)` 

Dumps the output file from jellyfish count (mer_file) into a human-readable
format, default file outfile.fasta.

##### mash

For mash, additional options are specified as argument='parameter'. If the argument is a switch with no parameter, 
pass in argument=''.

`mash.sketch(file_to_sketch_1, file_to_sketch_2, output_sketch='sketch.msh', threads=1)`

Runs mash sketch. Anything passed as a positional argument will be sketched and output to the file
specified by output_sketch. Any number of positional arguments can be called, and patterns (such as *.fastq) are also
acceptable.

`mash.dist(file_1, file_2, output_file='distances.tab', threads=1)`

Runs mash dist on positional arguments (as with `mash.sketch`, any number can be passed in and patterns work).
Outputs results to a tab-delimited file which can be interpreted by `mash.read_mash_output`

`mash.read_mash_output(result_file)`

Reads a mash output file created by mash dist. Returns a list where each entry in the list represents one row from 
the result file. Each item in the list has the following attributes: query, reference, distance, pvalue, and matching_hash.
Distance and pvalue are floats, all others are returned as strings. For example, to get the distance between the query 
and reference in a result_list for the result at index 2, use result_list[2].distance

##### fasta

Operations on fasta files.

`fasta.clean_names(in_fasta, out_fasta='NA', method='split', delimiter='NA', truncate_value=10)`

Cleans up titles on fasta files in case they're too long, making programs not like them.
Only mandatory argument is in_fasta. On default settings, will split titles on whitespace, modifying the input file.
Can specify output file using out_fasta.
Can be changed to other delimiters by changing the delimiter argument. Other option is to truncate to a number
of characters, default 10. To switch to this, use the argument method='truncate'. Any other parameter for the method
argument will result in a ValueError.