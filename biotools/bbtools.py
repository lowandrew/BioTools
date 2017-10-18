import os
import subprocess
from biotools import accessoryfunctions


def kwargs_to_string(kwargs):
    """
    Given a set of kwargs, turns them into a string which can then be passed to a command.
    :param kwargs: kwargs from a function call.
    :return: outstr: A string, which is '' if no kwargs were given, and the kwargs in string format otherwise.
    """
    outstr = ''
    for arg in kwargs:
        outstr += ' {}={}'.format(arg, kwargs[arg])
    return outstr


def bbmap(reference, forward_in, out_bam, reverse_in='NA', **kwargs):
    """
    Wrapper for bbmap. Assumes that bbmap executable is in your $PATH.
    :param reference: Reference fasta. Won't be written to disk by default. If you want it to be, add nodisk='t' as an arg.
    :param forward_in: Input reads. Should be in fastq format.
    :param out_bam: Output file. Should end in .sam or .bam
    :param reverse_in: If your reverse reads are present and normal conventions (R1 for forward, R2 for reverse) are
     followed, the reverse reads will be followed automatically. If you want to specify reverse reads, you may do so.
    :param kwargs: Other arguments to give to bbmap in parameter=argument format. See bbmap documentation for full list.
    :return: out and err: stdout string and stderr string from running bbmap.
    """
    options = kwargs_to_string(kwargs)
    if os.path.isfile(forward_in.replace('R1', 'R2')) and reverse_in == 'NA':
        reverse_in = forward_in.replace('R1', 'R2')
        cmd = 'bbmap.sh ref={} in={} in2={} out={} nodisk{}'.format(reference, forward_in, reverse_in, out_bam, options)
    elif reverse_in == 'NA':
        cmd = 'bbmap.sh ref={} in={} out={} nodisk{}'.format(reference, forward_in, out_bam, options)
    else:
        cmd = 'bbmap.sh ref={} in={} in2={} out={} nodisk{}'.format(reference, forward_in, reverse_in, out_bam, options)
    out, err = accessoryfunctions.run_subprocess(cmd)
    return out, err


def bbduk_trim(forward_in, forward_out, reverse_in='NA', reverse_out='NA', **kwargs):
    """
    Wrapper for using bbduk to quality trim reads. Contains arguments used in OLC Assembly Pipeline, but these can
    be overwritten by using keyword parameters.
    :param forward_in: Forward reads you want to quality trim.
    :param forward_out: Output forward reads.
    :param reverse_in: Reverse input reads. Don't need to be specified if R1/R2 naming convention is used.
    :param reverse_out: Reverse output reads. Don't need to be specified if R1/R2 convention is used.
    :param kwargs: Other arguments to give to bbduk in parameter=argument format. See bbduk documentation for full list.
    :return: out and err: stdout string and stderr string from running bbduk.
    """
    options = kwargs_to_string(kwargs)
    cmd = 'which bbduk.sh'
    try:
        bbduk_dir = subprocess.check_output(cmd.split()).decode('utf-8')
        bbduk_dir = os.path.split(bbduk_dir)[:-1]
        bbduk_dir = bbduk_dir[0]
    except subprocess.CalledProcessError:
        print('ERROR: Could not find bbduk. Plase check that the bbtools package is installed and on your $PATH.\n\n')
        raise FileNotFoundError
    if os.path.isfile(forward_in.replace('R1', 'R2')) and reverse_in == 'NA':
        reverse_in = forward_in.replace('R1', 'R2')
        if reverse_out == 'NA':
            if 'R1' in forward_out:
                reverse_out = forward_out.replace('R1', 'R2')
            else:
                raise ValueError('If you do not specify reverse_out, forward_out must contain R1.\n\n')
        cmd = 'bbduk.sh in1={} in2={} out1={} out2={} qtrim=w trimq=20 k=25 minlength=50 forcetrimleft=15' \
              ' ref={}/resources/adapters.fa overwrite hdist=1 tpe tbo{}'.format(forward_in, reverse_in,
                                                                                 forward_out, reverse_out,
                                                                                 bbduk_dir, options)
    elif reverse_in == 'NA':
        cmd = 'bbduk.sh in={} out={} qtrim=w trimq=20 k=25 minlength=50 forcetrimleft=15' \
              ' ref={}/resources/adapters.fa overwrite hdist=1 tpe tbo{}'.format(forward_in, forward_out,
                                                                                 bbduk_dir, options)
    else:
        if reverse_out == 'NA':
            raise ValueError('Reverse output reads must be specified.')
        cmd = 'bbduk.sh in1={} in2={} out1={} out2={} qtrim=w trimq=20 k=25 minlength=50 forcetrimleft=15' \
              ' ref={}/resources/adapters.fa overwrite hdist=1 tpe tbo{}'.format(forward_in, reverse_in,
                                                                                 forward_out, reverse_out,
                                                                                 bbduk_dir, options)
    out, err = accessoryfunctions.run_subprocess(cmd)
    return out, err


def bbduk_bait(reference, forward_in, forward_out, reverse_in='NA', reverse_out='NA', **kwargs):
    """
    Uses bbduk to bait out reads that have kmers matching to a reference.
    :param reference: Reference you want to pull reads out for. Should be in fasta format.
    :param forward_in: Forward reads you want to quality trim.
    :param forward_out: Output forward reads.
    :param reverse_in: Reverse input reads. Don't need to be specified if R1/R2 naming convention is used.
    :param reverse_out: Reverse output reads. Don't need to be specified if R1/R2 convention is used.
    :param kwargs: Other arguments to give to bbduk in parameter=argument format. See bbduk documentation for full list.
    :return: out and err: stdout string and stderr string from running bbduk.
    """
    options = kwargs_to_string(kwargs)
    if os.path.isfile(forward_in.replace('R1', 'R2')) and reverse_in == 'NA':
        reverse_in = forward_in.replace('R1', 'R2')
        if reverse_out == 'NA':
            if 'R1' in forward_out:
                reverse_out = forward_out.replace('R1', 'R2')
            else:
                raise ValueError('If you do not specify reverse_out, forward_out must contain R1.\n\n')
        cmd = 'bbduk.sh in={} in2={} outm={} outm2={} ref={}{}'.format(forward_in, reverse_in,
                                                                       forward_out, reverse_out,
                                                                       reference, options)
    elif reverse_in == 'NA':
        cmd = 'bbduk.sh in={} outm={} ref={}{}'.format(forward_in, forward_out, reference, options)
    else:
        if reverse_out == 'NA':
            raise ValueError('Reverse output reads must be specified.')
        cmd = 'bbduk.sh in={} in2={} outm={} outm2={} ref={}{}'.format(forward_in, reverse_in,
                                                                       forward_out, reverse_out,
                                                                       reference, options)
    out, err = accessoryfunctions.run_subprocess(cmd)
    return out, err


def bbduk_filter(reference, forward_in, forward_out, reverse_in='NA', reverse_out='NA', **kwargs):
    """
    Uses bbduk to filter out reads that have kmers matching to a reference.
    :param reference: Reference you want to pull reads out for. Should be in fasta format.
    :param forward_in: Forward reads you want to quality trim.
    :param forward_out: Output forward reads.
    :param reverse_in: Reverse input reads. Don't need to be specified if R1/R2 naming convention is used.
    :param reverse_out: Reverse output reads. Don't need to be specified if R1/R2 convention is used.
    :param kwargs: Other arguments to give to bbduk in parameter=argument format. See bbduk documentation for full list.
    :return: out and err: stdout string and stderr string from running bbduk.
    """
    options = kwargs_to_string(kwargs)
    if os.path.isfile(forward_in.replace('R1', 'R2')) and reverse_in == 'NA':
        reverse_in = forward_in.replace('R1', 'R2')
        if reverse_out == 'NA':
            if 'R1' in forward_out:
                reverse_out = forward_out.replace('R1', 'R2')
            else:
                raise ValueError('If you do not specify reverse_out, forward_out must contain R1.\n\n')
        cmd = 'bbduk.sh in={} in2={} out={} out2={} ref={}{}'.format(forward_in, reverse_in,
                                                                     forward_out, reverse_out,
                                                                     reference, options)
    elif reverse_in == 'NA':
        cmd = 'bbduk.sh in={} out={} ref={}{}'.format(forward_in, forward_out, reference, options)
    else:
        if reverse_out == 'NA':
            raise ValueError('Reverse output reads must be specified.')
        cmd = 'bbduk.sh in={} in2={} out={} out2={} ref={}{}'.format(forward_in, reverse_in,
                                                                     forward_out, reverse_out,
                                                                     reference, options)
    out, err = accessoryfunctions.run_subprocess(cmd)
    return out, err


def dedupe(input, output, **kwargs):
    """
    Runs dedupe from the bbtools package.
    :param input: Input file.
    :param output: Output file.
    :param kwargs: Arguments to give to dedupe in parameter=argument format. See dedupe documentation for full list.
    :return: out and err: stdout string and stderr string from running dedupe.
    """
    options = kwargs_to_string(kwargs)
    cmd = 'dedupe.sh in={} out={}{}'.format(input, output, options)
    out, err = accessoryfunctions.run_subprocess(cmd)
    return out, err


def seal(reference, forward_in, output_file, reverse_in='NA', **kwargs):
    """
    Runs seal from the bbtools package.
    :param reference: Reference file, in fasta format.
    :param forward_in: Forward reads, fastq format.
    :param output_file: Output file to put rpkm statistics into.
    :param reverse_in: Reverse reads. Not necessary to specify if in same folder and follow R1/R2 convention.
    :param kwargs: Arguments to give to seal in parameter=argument format. See seal documentation for full list.
    :return: out and err: stdout string and stderr string from running dedupe.
    """
    options = kwargs_to_string(kwargs)
    if os.path.isfile(forward_in.replace('R1', 'R2')) and reverse_in == 'NA':
        reverse_in = forward_in.replace('R1', 'R2')
        cmd = 'seal.sh ref={} in={} in2={} rpkm={} nodisk{}'.format(ref, forward_in, reverse_in, output_file, options)
    elif reverse_in == 'NA':
        cmd = 'seal.sh ref={} in={} rpkm={} nodisk{}'.format(ref, forward_in, output_file, options)
    else:
        cmd = 'seal.sh ref={} in={} in2={} rpkm={} nodisk{}'.format(ref, forward_in, reverse_in, output_file, options)
    out, err = accessoryfunctions.run_subprocess(cmd)
    return out, err
